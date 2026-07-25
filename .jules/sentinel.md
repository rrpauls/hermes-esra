## 2026-07-22 - [Insecure Default File Permissions for Agent Logs]
**Vulnerability:** Agent logs and history files were being created with default system permissions (often world-readable), which could expose sensitive data like API keys, secrets, or internal context stored in the logs.
**Learning:** System-generated logs often contain highly sensitive data implicitly. Failing to explicitly secure file creation leads to passive data leakage, bypassing application-level security boundaries.
**Prevention:** Always enforce strict POSIX file permissions (`0o600` for files, `0o700` for directories) when writing logs or caches programmatically.

## 2026-07-22 - [Config and Prompt File Exposure during Hot-Reloading]
**Vulnerability:** Programmatic updates to agent configurations, system prompts, reasoning traces, and versioned skill files can be exposed to unauthorized local users if created with standard world-readable permissions.
**Learning:** Config files and prompts often govern the security posture and operational boundaries of an agent. Exposing them can allow local privilege escalation or prompt injection attacks.
**Prevention:** Enforce strict `0o600` POSIX file permissions programmatically using `os.open` with specific O_CREAT flags when updating prompts, configurations, or reasoning trace files during evolution cycles.

## 2026-07-22 - [Insecure Default File Permissions for Reports and Snapshots]
**Vulnerability:** Reports and metric snapshot files were being created with default system permissions, which could expose sensitive evaluation context, metrics, and generated reports to unauthorized local users.
**Learning:** Even internal tooling and report generation must enforce strict POSIX permissions to prevent passive context leakage.
**Prevention:** Always enforce strict `0o600` POSIX file permissions programmatically using `os.open` with specific O_CREAT flags, and use `0o700` when creating directories, for any file that might contain sensitive data or agent context.

## 2026-07-22 - [Time-of-Check to Time-of-Use (TOCTOU) Directory Hijacking in Skill Promotions]
**Vulnerability:** In `tools/skill_validator.py`, a secure backup directory was created using `tempfile.mkdtemp()`. However, it was immediately deleted using `shutil.rmtree()` to allow `shutil.copytree()` to write to the same path. A local attacker could create a directory at that predictable path during the race window, causing `copytree` to fail. The exception handler would then incorrectly assume a legitimate backup existed and copy the attacker's injected files into the production skills directory, leading to privilege escalation or arbitrary skill execution.
**Learning:** Never delete a securely created temporary file or directory (`mkdtemp` / `mkstemp`) just to recreate it with another function. Doing so breaks the atomic creation guarantees and introduces a TOCTOU race condition.
**Prevention:** Use `shutil.copytree(..., dirs_exist_ok=True)` to copy contents into the already-created, secure temporary directory, preserving the strict permissions and atomicity of `mkdtemp()`.

## 2026-07-25 - [Path Traversal in Experiment Loading and Skill Reloading]
**Vulnerability:** In `tools/experiment_runner.py`'s `load_experiment` function and `tools/hermes_integration.py`'s `hot_reload_skill` function, string arguments like `experiment_id` and `skill_name` were concatenated into file paths without sanitization. This allowed attackers to use path traversal strings (e.g., `../../sensitive_file`) to read arbitrary files outside the intended directories.
**Learning:** Any user-provided or dynamic string that is used to build a file path using `Path` or `os.path.join` must be strictly sanitized to prevent path traversal, otherwise an attacker can manipulate the path structure.
**Prevention:** Verify that the provided identifier doesn't contain directory traversal characters. A common approach in Python's `pathlib` is to ensure that `Path(identifier).name == identifier`, or explicitly use a regex to only allow alphanumeric characters and safe separators (e.g., hyphens or underscores).
