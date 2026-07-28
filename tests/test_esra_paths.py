"""Tests for Hermes/ESRA path resolution."""
import os
from pathlib import Path

import pytest

from tools import esra_paths


def test_esra_home_is_repo_root_when_running_from_source():
    # tools/esra_paths.py → parent.parent is the package/repo root
    root = esra_paths.esra_home()
    assert (root / "tools" / "esra_paths.py").is_file()
    assert (root / "tools" / "evolution_hook.py").is_file()


def test_tool_path_and_invocation():
    path = esra_paths.tool_path("evolution_hook.py")
    assert path.name == "evolution_hook.py"
    assert path.is_file()
    cmd = esra_paths.tool_invocation("evolution_hook.py")
    assert cmd.startswith("python ")
    assert "evolution_hook.py" in cmd
    assert Path(cmd.split(" ", 1)[1]).is_file()


def test_tool_path_strips_traversal():
    path = esra_paths.tool_path("../../etc/passwd")
    assert path.name == "passwd"
    assert path.parent == esra_paths.tools_dir()


def test_esra_home_env_override(tmp_path, monkeypatch):
    custom = tmp_path / "custom-esra"
    (custom / "tools").mkdir(parents=True)
    monkeypatch.setenv("ESRA_HOME", str(custom))
    # Re-import not required; functions read env each call
    assert esra_paths.esra_home() == custom.resolve()
    assert esra_paths.tools_dir() == (custom / "tools").resolve()


def test_hermes_home_env_override(tmp_path, monkeypatch):
    custom = tmp_path / "hermes-profile"
    custom.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(custom))
    assert esra_paths.hermes_home() == custom.resolve()
    assert esra_paths.skills_dir() == custom.resolve() / "skills" / "esra"


def test_list_tools_includes_core_modules():
    names = esra_paths.list_tools()
    assert "evolution_hook.py" in names
    assert "esra_paths.py" in names
    assert "skill_validator.py" in names


def test_ensure_tools_on_syspath():
    import sys

    root = esra_paths.ensure_tools_on_syspath()
    assert str(root) in sys.path
    assert (root / "tools").is_dir()
