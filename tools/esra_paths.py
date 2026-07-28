#!/usr/bin/env python3
"""
esra_paths.py

Resolve Hermes / ESRA install locations so tools and docs share one source of truth.

Layout (after ./install.sh):
  $HERMES_HOME/                 # default: ~/.hermes
  ├── AGENTS.md
  ├── skills/esra/              # meta-skills (Hermes skill discovery)
  │   └── esra-runtime/         # documents tool locations for the agent
  └── esra/                     # ESRA package root (not a Hermes skill)
      ├── manifest.json
      └── tools/                # Python CLIs (this package)

Why tools are NOT only under skills/:
  Hermes discovers *skills* (SKILL.md) under ~/.hermes/skills/. Python helper
  CLIs are shared runtime code with cross-imports — they belong in a stable
  package root under Hermes home. The esra-runtime skill teaches Hermes where
  that package lives; tools themselves stay importable as a unit.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def hermes_home() -> Path:
    """Hermes profile root ($HERMES_HOME or ~/.hermes)."""
    raw = os.environ.get("HERMES_HOME") or str(Path.home() / ".hermes")
    return Path(raw).expanduser().resolve()


def esra_home() -> Path:
    """
    ESRA package root.

    Priority:
      1. $ESRA_HOME
      2. Directory containing this file's parent (…/esra/tools/esra_paths.py → …/esra
         or repo-root/tools/esra_paths.py → repo-root when developing from source)
    """
    env = os.environ.get("ESRA_HOME")
    if env:
        return Path(env).expanduser().resolve()
    # tools/esra_paths.py → package/repo root is always parent of tools/
    return Path(__file__).resolve().parent.parent


def tools_dir() -> Path:
    """Directory holding ESRA Python tools."""
    return esra_home() / "tools"


def skills_dir() -> Path:
    """Installed ESRA meta-skills directory (Hermes discovery path)."""
    return hermes_home() / "skills" / "esra"


def manifest_path() -> Path:
    return esra_home() / "manifest.json"


def load_manifest() -> Optional[Dict[str, Any]]:
    path = manifest_path()
    if not path.is_file():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def is_installed_layout() -> bool:
    """True when tools live under $HERMES_HOME/esra/tools (post-install)."""
    try:
        tools = tools_dir().resolve()
        expected = (hermes_home() / "esra" / "tools").resolve()
        return tools == expected and (tools / "evolution_hook.py").is_file()
    except OSError:
        return False


def tool_path(name: str) -> Path:
    """Absolute path to a tool script (e.g. evolution_hook.py)."""
    base = Path(name).name  # prevent path traversal
    return tools_dir() / base


def tool_invocation(name: str) -> str:
    """
    Shell-oriented command string for docs and CLI empty-states.

    Uses the resolved absolute path so Hermes does not depend on cwd or a
    leftover git clone after install.
    """
    return f"python {tool_path(name)}"


def list_tools() -> List[str]:
    """List *.py tool modules (excluding __init__ and private helpers if any)."""
    d = tools_dir()
    if not d.is_dir():
        return []
    names = []
    for p in sorted(d.glob("*.py")):
        if p.name.startswith("_"):
            continue
        names.append(p.name)
    return names


def ensure_tools_on_syspath() -> Path:
    """
    Ensure the package root is on sys.path so `import tools.X` works when a
    script is executed by absolute path (e.g. python ~/.hermes/esra/tools/foo.py).
    """
    import sys

    root = str(esra_home())
    if root not in sys.path:
        sys.path.insert(0, root)
    return esra_home()
