#!/usr/bin/env python3
"""Export Hermes ESRA history and cycle logs as ESRA 1.2 cycle-event JSONL."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

IMPLEMENTATION = "hermes-esra"
SCHEMA_VERSION = "1.0.0"
PROTOCOL_VERSION = "1.2"


def normalize_timestamp(value: Any, fallback: float) -> str:
    if isinstance(value, str) and value:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.astimezone()
            return parsed.isoformat(timespec="seconds")
        except ValueError:
            pass
    return datetime.fromtimestamp(fallback, timezone.utc).isoformat(timespec="seconds")


def stable_id(record: dict[str, Any], source: str) -> str:
    existing = record.get("id")
    if existing:
        return str(existing)
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(f"{IMPLEMENTATION}|{source}|{canonical}".encode()).hexdigest()
    return digest[:32]


def history_event(record: dict[str, Any], source: str, fallback: float) -> dict[str, Any]:
    recommended = bool(record.get("trigger_decision", record.get("triggered", False)))
    evidence = [
        "trigger recommendation recorded" if recommended else "no trigger recommendation recorded",
        f"source:{source}",
    ]
    payload: dict[str, Any] = {
        "source_kind": "trigger-recommendation",
        "recommended": recommended,
    }
    if record.get("forced"):
        payload["forced"] = True
    return {
        "schema_version": SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "id": stable_id(record, source),
        "timestamp": normalize_timestamp(record.get("timestamp"), fallback),
        "implementation": IMPLEMENTATION,
        "event_type": "trigger",
        "outcome": "not-run",
        "evidence": evidence,
        "payload": payload,
    }


def cycle_event(record: dict[str, Any], source: str, fallback: float) -> dict[str, Any]:
    outputs = record.get("outputs") if isinstance(record.get("outputs"), dict) else {}
    decisions = record.get("orchestrator_decisions") if isinstance(record.get("orchestrator_decisions"), dict) else {}
    resources = record.get("duration_and_resources") if isinstance(record.get("duration_and_resources"), dict) else {}
    evidence: list[str] = []
    for key in ("improvements_applied", "new_skills_created", "anomalies", "crisis_interventions"):
        values = outputs.get(key, [])
        if isinstance(values, list):
            evidence.extend(f"{key}:{value}" for value in values if str(value).strip())
    evidence.append(f"source:{source}")
    payload: dict[str, Any] = {"source_kind": "cycle-log"}
    for key in ("skills_activated", "meta_loop_stage"):
        value = decisions.get(key)
        if value not in (None, "", []):
            payload[key] = value
    for key in ("new_skills_created", "improvements_applied", "value_changes"):
        value = outputs.get(key)
        if value not in (None, "", []):
            payload[key] = value
    if outputs.get("anomalies"):
        payload["anomaly_count"] = len(outputs["anomalies"])
    if resources.get("duration_seconds") is not None:
        payload["duration_seconds"] = resources["duration_seconds"]
    event: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "id": stable_id(record, source),
        "timestamp": normalize_timestamp(record.get("timestamp"), fallback),
        "implementation": IMPLEMENTATION,
        "event_type": "integration",
        "evidence": evidence,
        "payload": payload,
    }
    if isinstance(outputs.get("success"), bool):
        event["outcome"] = "success" if outputs["success"] else "failure"
    return event


def export_events(hermes_home: Path) -> list[dict[str, Any]]:
    if hermes_home.exists() and hermes_home.is_symlink():
        raise ValueError(f"refusing symlinked Hermes home: {hermes_home}")
    events: list[dict[str, Any]] = []
    history_path = hermes_home / "evolution_history.json"
    if history_path.exists():
        if history_path.is_symlink():
            raise ValueError(f"refusing symlinked source log: {history_path}")
        history = json.loads(history_path.read_text(encoding="utf-8"))
        if isinstance(history, list):
            for index, record in enumerate(history, start=1):
                if isinstance(record, dict):
                    source = f"evolution_history.json:{index}"
                    events.append(history_event(record, source, history_path.stat().st_mtime))
    log_dir = hermes_home / "evolution-logs"
    if log_dir.exists() and log_dir.is_symlink():
        raise ValueError(f"refusing symlinked source directory: {log_dir}")
    if log_dir.is_dir():
        for path in sorted(log_dir.glob("esra_cycle_*.json")):
            if path.is_symlink():
                raise ValueError(f"refusing symlinked source log: {path}")
            record = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(record, dict):
                events.append(cycle_event(record, path.name, path.stat().st_mtime))
    return events


def write_jsonl(events: Iterable[dict[str, Any]], output: str) -> None:
    encoded = "".join(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n" for event in events)
    if output == "-":
        sys.stdout.write(encoded)
        return
    path = Path(output).expanduser()
    if path.exists() and path.is_symlink():
        raise ValueError(f"refusing symlinked output: {path}")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(encoded)
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", help="Hermes home containing ESRA logs")
    parser.add_argument("--output", default="-", help="JSONL path, or - for stdout")
    args = parser.parse_args(argv)
    home = Path(args.data_dir).expanduser() if args.data_dir else Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")).expanduser()
    try:
        write_jsonl(export_events(home), args.output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
