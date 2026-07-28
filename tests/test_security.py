"""Security regression tests for path traversal, imports, and branch naming."""
import os
import pytest
import tempfile
from pathlib import Path

from tools.esra_paths import (
    is_safe_path_component,
    is_safe_experiment_id,
    require_safe_path_component,
    assert_no_symlinks_in_tree,
    secure_mkdir,
)
from tools.hermes_integration import SkillInjector
from tools.experiment_runner import ExperimentRunner
from tools.human_oversight import HumanOversight


def test_safe_path_component_rejects_traversal():
    assert is_safe_path_component("ooda-framework")
    assert is_safe_path_component("test-skill-v3")
    assert not is_safe_path_component("..")
    assert not is_safe_path_component(".")
    assert not is_safe_path_component("")
    assert not is_safe_path_component("../etc")
    assert not is_safe_path_component("foo/bar")
    assert not is_safe_path_component("foo\\bar")
    # short names like "os" pass the *component* allowlist but must never be
    # passed to importlib (see test_skill_injector_does_not_import_arbitrary_modules)
    assert is_safe_path_component("os")
    with pytest.raises(ValueError):
        require_safe_path_component("../../passwd")


def test_safe_experiment_id():
    assert is_safe_experiment_id("EXP-001")
    assert is_safe_experiment_id("EXP-42")
    assert not is_safe_experiment_id("EXP-001.json")
    assert not is_safe_experiment_id("../EXP-001")
    assert not is_safe_experiment_id("exp-001")
    assert not is_safe_experiment_id("EXP-")


def test_skill_injector_rejects_path_traversal():
    with tempfile.TemporaryDirectory() as tmpdir:
        injector = SkillInjector(skills_dir=Path(tmpdir))
        assert injector.hot_reload_skill("../etc") is False
        assert injector.hot_reload_skill("..") is False
        with pytest.raises(ValueError):
            injector.version_skill("../evil", "content", version=1)
        with pytest.raises(ValueError):
            injector.version_skill("ok", "content", version=0)
        with pytest.raises(ValueError):
            injector.version_skill("ok", "content", version=-1)


def test_skill_injector_does_not_import_arbitrary_modules():
    """Regression: hot_reload must not importlib.import_module('os') etc."""
    with tempfile.TemporaryDirectory() as tmpdir:
        injector = SkillInjector(skills_dir=Path(tmpdir))
        # "os" is a safe path component but must not load the stdlib package
        assert injector.hot_reload_skill("os") is False
        assert injector.hot_reload_skill("sys") is False
        assert injector.hot_reload_skill("http.client") is False


def test_experiment_runner_rejects_path_traversal_ids():
    with tempfile.TemporaryDirectory() as tmpdir:
        runner = ExperimentRunner(base_dir=Path(tmpdir))
        assert runner.load_experiment("../etc/passwd") is None
        assert runner.load_experiment("EXP-001/../../x") is None
        assert runner.load_experiment("not-an-id") is None


def test_branch_name_sanitizes_and_rejects_injection():
    assert HumanOversight.format_pr_branch_name("Self Observer", 1) == "evolve/self-observer-v1"
    # Path separators are stripped/neutralized — must not remain in the branch
    branch = HumanOversight.format_pr_branch_name("../../evil", 1)
    assert ".." not in branch
    assert "/" not in branch.replace("evolve/", "", 1)
    assert branch == "evolve/evil-v1"
    with pytest.raises(ValueError):
        HumanOversight.format_pr_branch_name("ok", version=0)
    with pytest.raises(ValueError):
        HumanOversight.format_pr_branch_name("!!!", 1)


def test_assert_no_symlinks_in_tree():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "ok.txt").write_text("hi", encoding="utf-8")
        assert_no_symlinks_in_tree(root)
        link = root / "badlink"
        try:
            link.symlink_to("/etc/passwd")
        except OSError:
            pytest.skip("symlinks not supported")
        with pytest.raises(ValueError, match="symlink"):
            assert_no_symlinks_in_tree(root)


def test_secure_mkdir_reapplies_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        d = Path(tmpdir) / "nested"
        d.mkdir(mode=0o777)
        # World-writable until we re-secure
        secure_mkdir(d, 0o700)
        mode = d.stat().st_mode & 0o777
        assert mode == 0o700
