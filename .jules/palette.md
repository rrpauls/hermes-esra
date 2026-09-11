# Palette's Journal

This journal documents critical UX and accessibility learnings from working with the ESRA implementation.

## 2026-07-19 - [TTY-Aware ANSI Escape Codes and Empty State Actionability in CLI Dashboards]
**Learning:** CLI terminal tools often suffer from poor visual feedback and can break when piped or logged if ANSI escape codes are hardcoded. Additionally, an uninformative empty state with 0 metrics leaves users confused about how to initiate the system.
**Action:** Ensure CLI tools detect interactive terminals (`sys.stdout.isatty()`) and respect standard environment indicators (like `NO_COLOR`). When metrics are empty, replace standard headers or provide a highly visible call-to-action (CTA) detailing the exact commands to run.

## 2026-07-20 - [Contextual History and Visual Scannability in Terminal UIs]
**Learning:** Aggregated metrics in CLI dashboards are useful, but lack temporal context. Adding a "Recent History" section with micro-formatting (e.g., stripping noisy subsecond parts from ISO timestamps, displaying explicit success/failure emojis, and translating floats to readable durations like `1.0s`) vastly reduces cognitive load during repetitive runs.
**Action:** Always complement high-level aggregated numbers with a localized, structured view of the last N state transitions to give the user immediate feedback on recent trends.

## 2026-07-27 - [Actionable Error States in CLI Tools]
**Learning:** Returning unhelpful error messages (e.g., "Experiment not found") in CLI tools leads to dead-ends. When a user provides an invalid ID or malformed configuration, they are left guessing how to resolve it. Without clear next steps, users abandon flows.
**Action:** Always complement error states with a highly visible `💡 Tip:` offering an actionable command to resolve the issue (e.g., suggesting a command to list available IDs).
## 2026-07-28 - Actionable Error Tooltips
**Learning:** CLI error messages are dead-ends without guidance. Simple failure messages leave users confused about what to fix next, resulting in bad Developer Experience (DX).
**Action:** When printing error states in CLI tools (like validation failures), complement the error with a highly visible `💡 Tip:` that offers specific, actionable guidance on how to fix the issue.
## 2026-08-02 - Comprehensive Actionable Error Tips in CLI
**Learning:** Even if some CLI commands provide tips, inconsistent application across the codebase leaves users confused when they encounter edge case errors like malformed JSON input or missing environment variables.
**Action:** When printing error states in CLI tools like `tools/experiment_runner.py` and `tools/skill_validator.py`, ensure all `sys.stderr` error messages are followed by a highly visible `💡 Tip:` offering specific guidance on resolving that particular issue.
