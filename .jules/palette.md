# Palette's Journal

This journal documents critical UX and accessibility learnings from working with the ESRA implementation.


## 2026-07-19 - [TTY-Aware ANSI Escape Codes and Empty State Actionability in CLI Dashboards]
**Learning:** CLI terminal tools often suffer from poor visual feedback and can break when piped or logged if ANSI escape codes are hardcoded. Additionally, an uninformative empty state with 0 metrics leaves users confused about how to initiate the system.
**Action:** Ensure CLI tools detect interactive terminals (`sys.stdout.isatty()`) and respect standard environment indicators (like `NO_COLOR`). When metrics are empty, replace standard headers or provide a highly visible call-to-action (CTA) detailing the exact commands to run.

## 2026-07-19 - [Contextual History and Visual Scannability in Terminal UIs]
**Learning:** Aggregated metrics in CLI dashboards are useful, but lack temporal context. Adding a "Recent History" section with micro-formatting (e.g., stripping noisy subsecond parts from ISO timestamps, displaying explicit success/failure emojis, and translating floats to readable durations like `1.0s`) vastly reduces cognitive load during repetitive runs.
**Action:** Always complement high-level aggregated numbers with a localized, structured view of the last N state transitions to give the user immediate feedback on recent trends.
