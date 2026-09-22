# AGENTS.md — ESRA Integration for Hermes

> **Goal:** Make Hermes improvement work systematic, value-aligned, observable,
> and evidence-driven through the Evolutionary Self-Recursive Architecture
> (ESRA) meta-layer.

**Official architecture name:** ESRA — Evolutionary Self-Recursive Architecture  
**Specification repository:** https://github.com/rrpauls/esra  
**This repository:** Concrete Hermes implementation of ESRA

---

## Core Rule

After a major architecture or skill change, repeated failure, or an explicit
full-cycle request, evaluate whether to run **one bounded**
`hermes-evolution-orchestrator` review. Routine successful work should not
trigger a full cycle.

A recommendation from `evolution_hook.py` does not execute a cycle. The
caller must explicitly activate the orchestrator.

---

## Install layout (where things live)

After `./install.sh`, Hermes home looks like:

```text
$HERMES_HOME/                         # default: ~/.hermes
├── AGENTS.md                         # this file
├── skills/esra/                      # meta-skills (Hermes skill discovery)
│   ├── esra-runtime/                 # documents tool paths for the agent
│   ├── hermes-evolution-orchestrator/
│   └── …
└── esra/                             # ESRA runtime package (not a skill)
    ├── manifest.json                 # machine-readable paths and protocol version
    ├── conformance.json              # evidence-backed capability declaration
    └── tools/                        # Python CLIs — use these paths
```

| Kind | Path | Discovered by Hermes as |
|------|------|-------------------------|
| Meta-skills | `~/.hermes/skills/esra/` | Skills / slash commands |
| Runtime tools | `~/.hermes/esra/tools/` | Via `esra-runtime` skill + this file |
| Manifest | `~/.hermes/esra/manifest.json` | Read when paths are unclear |
| Conformance | `~/.hermes/esra/conformance.json` | Check supported protocol and capability maturity |

Override roots with `$HERMES_HOME` and/or `$ESRA_HOME` if set.

**Always run tools by installed absolute path** (do not depend on a git clone or cwd):

```bash
python ~/.hermes/esra/tools/evolution_hook.py
python ~/.hermes/esra/tools/evolution_hook.py --force-cycle
python ~/.hermes/esra/tools/skill_validator.py --verbose --skills-dir ~/.hermes/skills/esra
python ~/.hermes/esra/tools/evolution_dashboard.py
```

If unsure, activate the **`esra-runtime`** skill or open `~/.hermes/esra/manifest.json`.

---

## How to Run the Orchestrator

### Recommended Triggers

```text
After this task, run hermes-evolution-orchestrator

orchestrate evolution

run full ESRA cycle

improve the self-development cycle

perform evolutionary audit of this task
```

### Smart Triggering via `evolution_hook.py`

The helper at `~/.hermes/esra/tools/evolution_hook.py` analyzes supplied task
context and local evolution history and recommends whether the caller should
launch the orchestrator.

Callers that preserve lifecycle state must pass `origin`, `root_task_id`, and
`cycle_depth`. `origin=esra`, any `cycle_depth > 0`, or a second recommendation
for the same `root_task_id` is rejected before all trigger heuristics, including
forced or explicit requests. Post-task results are fail-closed: only explicit
`success: true` is success, and declared artifact paths must exist, be non-empty,
and have a valid image envelope when applicable.

**Capabilities:**
- Considers task complexity, new skill creation, and result confidence
- Includes rate limiting
- Analyzes historical patterns
- Produces a recommendation and prompt; it is not a native Hermes event hook

**Usage:**
```bash
python ~/.hermes/esra/tools/evolution_hook.py
python ~/.hermes/esra/tools/evolution_hook.py --force-cycle
```

---

## Decision Structuring

For any uncertainty or important decision, run `ooda-framework` (optionally with related meta-skills such as `self-observer`, `value-clarifier`, or `loop-auditor`).

---

## Periodic Audit

Every **5–10 recorded significant cycles**, or after an anomaly, explicitly
run the audit. If cycle history is unavailable, report cadence as unknown:

```text
Run loop-auditor to audit the current evolutionary cycle
```

---

## Installed ESRA Components

### Meta-skills

All skills live in: `~/.hermes/skills/esra/`

| Skill | Purpose |
|-------|---------|
| `esra-runtime` | **Where tools live** — installed paths and how to run them |
| `hermes-evolution-orchestrator` | Central conductor of the ESRA loop |
| `ooda-framework` | Structures work using Observe → Orient → Decide → Act |
| `self-observer` | Honest monitoring of internal state and patterns |
| `self-improver` | Systematic improvement of skills and processes |
| `value-clarifier` | Value alignment checks (mandatory before experiments) |
| `experimenter` | Design and run safe improvement experiments |
| `mental-model-updater` | Integrate results into long-term models |
| `antifragility-builder` | Grow stronger from stress and uncertainty |
| `loop-auditor` | Meta-audit of the entire evolutionary process |
| `optimizer-philosopher` | Deep trade-off and meaning analysis |
| `system-dynamics-thinker` | Feedback loops, stocks & flows, leverage points |
| `crisis-manager` | High-stakes decision making under uncertainty |
| `hermes-codebase-engineer` | Programming and integration work inside Hermes |
| `github-actions-integrator` | CI/CD workflow creation and GitHub Actions automation |

### Supporting tools (`~/.hermes/esra/tools/`)

| Tool | Purpose |
|------|---------|
| `evolution_hook.py` | Smart detector + history analysis for triggering the orchestrator |
| `esra_logger.py` | Structured JSON logging for ESRA cycles |
| `evolution_dashboard.py` | CLI visualization of evolution metrics |
| `baseline_metrics.py` | KPI tracking and historical snapshots |
| `skill_validator.py` | Skill frontmatter, DAG, and promotion validation |
| `experiment_runner.py` | Safe experiment lifecycle (canary, staged, A/B) |
| `hermes_integration.py` | Native Hermes hooks, skill injection, feedback loop |
| `human_oversight.py` | GitHub issues/PRs and evolutionary audit trail helpers |
| `esra_paths.py` | Shared path resolution for tools and install layout |

---

## Installation

From the root of this repository:

```bash
chmod +x install.sh
./install.sh
```

This installs:

1. Meta-skills → `~/.hermes/skills/esra/` (including `esra-runtime`)
2. Tools package → `~/.hermes/esra/tools/`
3. Manifest → `~/.hermes/esra/manifest.json`
4. Conformance declaration → `~/.hermes/esra/conformance.json`
5. This file → `~/.hermes/AGENTS.md`

Respects `$HERMES_HOME` / `$ESRA_HOME` when set.

---

## Philosophy

- Hermes provides a powerful **engine** for self-improvement.
- ESRA provides the **steering, brakes, navigation, and audit system**.
- `hermes-evolution-orchestrator` is the mechanism that connects them.
- Skills are discovered by Hermes; tools are a **package under Hermes home**, advertised by `esra-runtime`.

The goal is not merely to add skills, but to make the evolution process itself **recursive and self-improving**.

---

## Relationship to the ESRA Specification

This repository implements ESRA for Hermes.  
The pure conceptual and technical description of the architecture (principles, 8 levels, Loop Execution Protocol) lives in the separate repository:

→ https://github.com/rrpauls/esra

---

**Version:** 1.3
**Date:** 28 July 2026  
**Compatible with:** Hermes Agent + ESRA (Evolutionary Self-Recursive Architecture)
