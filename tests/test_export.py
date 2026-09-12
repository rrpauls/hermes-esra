import json
import tempfile
from pathlib import Path

from tools.esra_export import export_events, write_jsonl


def test_export_maps_history_and_cycle_logs_without_sensitive_fields():
    with tempfile.TemporaryDirectory() as temporary:
        home = Path(temporary)
        (home / "evolution_history.json").write_text(
            json.dumps([
                {
                    "timestamp": "2026-09-12T18:00:00+00:00",
                    "trigger_decision": True,
                    "triggered": True,
                    "task_context": {"prompt": "private prompt", "session": "raw-session"},
                    "orchestrator_prompt": "hidden orchestration prompt",
                }
            ]),
            encoding="utf-8",
        )
        logs = home / "evolution-logs"
        logs.mkdir()
        (logs / "esra_cycle_fixture.json").write_text(
            json.dumps({
                "timestamp": "2026-09-12T18:01:00+00:00",
                "input_state": {"prompt": "private cycle input"},
                "orchestrator_decisions": {"skills_activated": ["ooda-framework"], "meta_loop_stage": "ACT"},
                "outputs": {"success": True, "improvements_applied": ["adapter added"], "anomalies": []},
                "duration_and_resources": {"duration_seconds": 1.5, "command_output": "secret output"},
            }),
            encoding="utf-8",
        )

        exported = export_events(home)
        assert len(exported) == 2
        assert exported[0]["event_type"] == "trigger"
        assert exported[0]["outcome"] == "not-run"
        assert exported[1]["event_type"] == "integration"
        assert exported[1]["outcome"] == "success"
        raw = json.dumps(exported)
        assert "private prompt" not in raw
        assert "raw-session" not in raw
        assert "hidden orchestration prompt" not in raw
        assert "secret output" not in raw


def test_export_is_deterministic_and_writes_private_jsonl():
    with tempfile.TemporaryDirectory() as temporary:
        home = Path(temporary)
        (home / "evolution_history.json").write_text(
            '[{"timestamp":"2026-09-12T18:00:00Z","triggered":false}]',
            encoding="utf-8",
        )
        first = export_events(home)
        second = export_events(home)
        assert first == second
        output = home / "portable.jsonl"
        write_jsonl(first, str(output))
        assert output.stat().st_mode & 0o777 == 0o600
        assert json.loads(output.read_text()) == first[0]
