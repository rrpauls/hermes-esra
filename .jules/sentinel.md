## 2026-07-22 - [Insecure Default File Permissions for Agent Logs]
**Vulnerability:** Agent logs and history files were being created with default system permissions (often world-readable), which could expose sensitive data like API keys, secrets, or internal context stored in the logs.
**Learning:** System-generated logs often contain highly sensitive data implicitly. Failing to explicitly secure file creation leads to passive data leakage, bypassing application-level security boundaries.
**Prevention:** Always enforce strict POSIX file permissions (`0o600` for files, `0o700` for directories) when writing logs or caches programmatically.
