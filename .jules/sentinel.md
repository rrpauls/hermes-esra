## 2026-07-22 - [Insecure Default File Permissions for Agent Logs]
**Vulnerability:** Agent logs and history files were being created with default system permissions (often world-readable), which could expose sensitive data like API keys, secrets, or internal context stored in the logs.
**Learning:** System-generated logs often contain highly sensitive data implicitly. Failing to explicitly secure file creation leads to passive data leakage, bypassing application-level security boundaries.
**Prevention:** Always enforce strict POSIX file permissions (`0o600` for files, `0o700` for directories) when writing logs or caches programmatically.

## 2026-07-22 - [Config and Prompt File Exposure during Hot-Reloading]
**Vulnerability:** Programmatic updates to agent configurations, system prompts, reasoning traces, and versioned skill files can be exposed to unauthorized local users if created with standard world-readable permissions.
**Learning:** Config files and prompts often govern the security posture and operational boundaries of an agent. Exposing them can allow local privilege escalation or prompt injection attacks.
**Prevention:** Enforce strict `0o600` POSIX file permissions programmatically using `os.open` with specific O_CREAT flags when updating prompts, configurations, or reasoning trace files during evolution cycles.

## 2026-07-23 - [Insecure Default File Permissions for Reports and Snapshots]
**Vulnerability:** Reports and metric snapshot files were being created with default system permissions, which could expose sensitive evaluation context, metrics, and generated reports to unauthorized local users.
**Learning:** Even internal tooling and report generation must enforce strict POSIX permissions to prevent passive context leakage.
**Prevention:** Always enforce strict `0o600` POSIX file permissions programmatically using `os.open` with specific O_CREAT flags, and use `0o700` when creating directories, for any file that might contain sensitive data or agent context.

## 2026-07-24 - [Time-of-Check to Time-of-Use (TOCTOU) Directory Hijacking in Skill Promotions]
**Vulnerability:** In `tools/skill_validator.py`, a secure backup directory was created using `tempfile.mkdtemp()`. However, it was immediately deleted using `shutil.rmtree()` to allow `shutil.copytree()` to write to the same path. A local attacker could create a directory at that predictable path during the race window, causing `copytree` to fail. The exception handler would then incorrectly assume a legitimate backup existed and copy the attacker's injected files into the production skills directory, leading to privilege escalation or arbitrary skill execution.
**Learning:** Never delete a securely created temporary file or directory (`mkdtemp` / `mkstemp`) just to recreate it with another function. Doing so breaks the atomic creation guarantees and introduces a TOCTOU race condition.
**Prevention:** Use `shutil.copytree(..., dirs_exist_ok=True)` to copy contents into the already-created, secure temporary directory, preserving the strict permissions and atomicity of `mkdtemp()`.

## 2026-07-25 - [Path Traversal in Experiment Loading and Skill Reloading]
**Vulnerability:** In `tools/experiment_runner.py`'s `load_experiment` function and `tools/hermes_integration.py`'s `hot_reload_skill` function, string arguments like `experiment_id` and `skill_name` were concatenated into file paths without sanitization. This allowed attackers to use path traversal strings (e.g., `../../sensitive_file`) to read arbitrary files outside the intended directories.
**Learning:** Any user-provided or dynamic string that is used to build a file path using `Path` or `os.path.join` must be strictly sanitized to prevent path traversal, otherwise an attacker can manipulate the path structure.
**Prevention:** Verify that the provided identifier doesn't contain directory traversal characters. A common approach in Python's `pathlib` is to ensure that `Path(identifier).name == identifier`, or explicitly use a regex to only allow alphanumeric characters and safe separators (e.g., hyphens or underscores).

## 2026-07-26 - [Insecure Predictable Temporary Directory and TOCTOU in Staging Cleanup]
**Vulnerability:** The `--staging-dir` in `tools/skill_validator.py` defaulted to a hardcoded predictable path (`/tmp/esra_skills_staging`). In a shared environment, an attacker could create this directory or a symlink at this path, potentially leading to unauthorized file access or corruption. Furthermore, the staging cleanup logic called `shutil.rmtree(staging_dir)` followed by `staging_dir.mkdir(...)`, which destroys the original secure directory and re-introduces a Time-of-Check to Time-of-Use (TOCTOU) window before recreating it.
**Learning:** Hardcoded predictable paths in shared directories (like `/tmp`) are highly vulnerable to symlink and TOCTOU attacks. In addition, when clearing a securely created directory (like one from `tempfile.mkdtemp`), deleting the entire directory and recreating it breaks its atomic creation guarantee.
**Prevention:** Avoid hardcoding predictable paths in shared directories; always dynamically generate secure temporary directories using `tempfile.mkdtemp`. When securely emptying an existing directory, iterate through and delete its contents individually rather than destroying and recreating the parent directory.

## 2026-07-27 - [Path Traversal in Skill Versioning]
**Vulnerability:** In `tools/hermes_integration.py`, the `version_skill` function in `SkillInjector` lacked input validation for the `skill_name` argument. If `skill_name` was crafted to include path traversal characters (e.g., `../malicious-skill`), it could allow an attacker to write versioned files outside of the designated `skills_dir`, potentially overwriting arbitrary files with `0o600` permissions.
**Learning:** Any input acting as a filename component within dynamic path construction must be validated. If a function is meant to write to a specific directory structure, the provided component must not contain path delimiters.
**Prevention:** Strictly sanitize string arguments meant to be directory or file names by validating that `Path(variable).name == variable` to ensure no path traversal sequences (like `..` or `/`) are present before using them in file operations.

## 2026-07-28 - [Arbitrary File Permission Modification via os.chmod Symlink Following]
**Vulnerability:** Calls to `os.chmod()` on existing directories (often acting as a fallback if `mkdir()` fails to set permissions) follow symlinks by default in Python. If an attacker pre-creates the expected directory (like `~/.hermes/evolution-logs`) as a symlink pointing to a sensitive target (e.g., `/etc/`), the script will inadvertently modify the permissions of the target file/directory.
**Learning:** `os.chmod()` follows symlinks by default. Furthermore, the `follow_symlinks=False` argument is not universally supported across all platforms (e.g., it raises `NotImplementedError` on Linux).
**Prevention:** To securely ensure a directory has the correct permissions when you cannot guarantee its atomic creation, you must explicitly check `if not path.is_symlink():` before calling `os.chmod()`.
