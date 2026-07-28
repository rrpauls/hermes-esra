# hermes-esra

<p align="center"><img src="assets/logo.png" alt="hermes-esra logo" width="240"/></p>

**Hermes implementation of ESRA — Evolutionary Self-Recursive Architecture**

This repository contains the production-grade implementation of ESRA as a set of meta-skills, an orchestrator, and supporting tools for the Hermes agent.

> The pure conceptual and technical description of the architecture lives in a separate repository:  
> **https://github.com/rrpauls/esra** — Evolutionary Self-Recursive Architecture (specification only).

---

## Purpose

Hermes already has a strong native self-improvement mechanism.  
This repository adds a **meta-layer** that makes evolution:

- Structured and conscious (via the ESRA loop)
- Automatic and intelligent (via `hermes-evolution-orchestrator` + `evolution_hook.py`)
- Auditable and improvable (via `loop-auditor`)
- Antifragile and long-term

---

## Main Components

| Component | Purpose | Location |
|-----------|---------|----------|
| `hermes-evolution-orchestrator` | Central conductor of evolution. Connects Hermes native loop with meta-skills | `skills/` |
| `evolution_hook.py` | Smart task detector + history/pattern analysis. Decides when to run the orchestrator | `tools/` |
| `loop-auditor` | Meta-audit of the entire evolutionary process | `skills/` |
| `esra_logger.py` / `evolution_dashboard.py` / `baseline_metrics.py` | Cycle logging, metrics UI, KPI snapshots | `tools/` |
| `skill_validator.py` / `experiment_runner.py` | Skill validation/promotion and experiment lifecycle | `tools/` |
| `hermes_integration.py` / `human_oversight.py` | Native Hermes hooks and human audit trail | `tools/` |
| `install.sh` | One-command installation of all skills + AGENTS.md | Root |
| `AGENTS.md` | Ready-to-use instructions and triggers for Hermes | Root |

### Included meta-skills (14)

`hermes-evolution-orchestrator`, `self-observer`, `self-improver`, `value-clarifier`, `experimenter`, `mental-model-updater`, `antifragility-builder`, `optimizer-philosopher`, `system-dynamics-thi[...]`

---

## Quick Start

```bash
git clone https://github.com/rrpauls/hermes-esra.git
cd hermes-esra

chmod +x install.sh
./install.sh
```

After installation:
- All meta-skills appear in `~/.hermes/skills/esra/`
- `~/.hermes/AGENTS.md` contains usage instructions

---

## How the system works

```
Hermes Native Learning Loop
        ↓ (after complex task / skill creation)
evolution_hook.py (analyzes context + history)
        ↓ (decides whether to run)
hermes-evolution-orchestrator
        ↓
Self-Observer → Self-Improver → Value-Clarifier → Experimenter → ...
        ↓ (periodically)
loop-auditor (meta-audit of the cycle)
```

---

## Relationship to ESRA

- **[esra](https://github.com/rrpauls/esra)**  = pure description of the architecture (what it is, principles, 8 levels, Loop Execution Protocol)
- **hermes-esra** (this repo) = concrete implementation for Hermes

This separation keeps the conceptual core clean and allows other implementations (standalone Python engine, other agents, etc.) in the future.

---

**Status:** Active (July 2026)  
**Version:** 1.2  
This repository implements ESRA for Hermes.
