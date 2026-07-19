# AGENTS.md — ESRA Integration for Hermes

> **Goal:** Make Hermes self-development systematic, value-aligned, observable, and compounding by connecting its native learning loop with the Evolutionary Self-Recursive Architecture (ESRA) meta-layer.

**Official architecture name:** ESRA — Evolutionary Self-Recursive Architecture  
**Specification repository:** https://github.com/rrpauls/esra  
**This repository:** Concrete Hermes implementation of ESRA

---

## Core Rule

**After any complex task**, skill creation, or significant improvement — **always run** `hermes-evolution-orchestrator`  
(or explicitly say: `orchestrate evolution` / `run full ESRA cycle`).

This turns ad-hoc improvements into a deliberate, auditable, and self-improving evolutionary process.

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

### Smart Triggering via `evolution-hook.py`

The helper tool `tools/evolution-hook.py` analyzes task context and evolution history to decide when to launch the orchestrator.

**Capabilities:**
- Considers task complexity, new skill creation, and result confidence
- Includes rate limiting
- Analyzes historical patterns
- Can serve as a reference for future native Hermes integration

**Usage:**
```bash
python tools/evolution-hook.py
```

---

## Periodic Audit

Every **5–10 significant cycles** or after major changes, explicitly run:

```text
Run loop-auditor to audit the current evolutionary cycle
```

---

## Installed ESRA Meta-Skills

All skills live in: `~/.hermes/skills/evolutionary-self-dev/`

| Skill | Purpose |
|-------|---------|
| `hermes-evolution-orchestrator` | Central conductor of the ESRA loop |
| `evolution-hook.py` (tools/) | Smart detector + history analysis for triggering |
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

---

## Installation

From the root of this repository:

```bash
chmod +x install-evolutionary-skills.sh
./install-evolutionary-skills.sh
```

This copies all skills to `~/.hermes/skills/evolutionary-self-dev/` and places `AGENTS.md` into `~/.hermes/`.

---

## Philosophy

- Hermes provides a powerful **engine** for self-improvement.
- ESRA provides the **steering, brakes, navigation, and audit system**.
- `hermes-evolution-orchestrator` is the mechanism that connects them.

The goal is not merely to add skills, but to make the evolution process itself **recursive and self-improving**.

---

## Relationship to the ESRA Specification

This repository implements ESRA for Hermes.  
The pure conceptual and technical description of the architecture (principles, 8 levels, Loop Execution Protocol) lives in the separate repository:

→ https://github.com/rrpauls/esra

---

**Version:** 1.2  
**Date:** 19 July 2026  
**Compatible with:** Hermes Agent + ESRA (Evolutionary Self-Recursive Architecture)
