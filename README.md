# hermes-esra

<p align="center">
  <img src="assets/logo.png" alt="hermes-esra logo" width="240"/>
</p>

<p align="center">
  <strong>Hermes implementation of ESRA — Evolutionary Self-Recursive Architecture</strong>
</p>

<p align="center">
  Meta-skills, orchestrator, and tools that make Hermes self-development systematic, value-aligned, auditable, and compounding.
</p>

<p align="center">
  <a href="https://github.com/rrpauls/esra">ESRA specification</a> ·
  <a href="AGENTS.md">AGENTS.md</a> ·
  <a href="ROADMAP.md">ROADMAP</a> ·
  <a href="LICENSE">MIT License</a>
</p>

---

## What this is

Hermes already improves from experience. This repository adds a **meta-layer** on top of that loop so evolution is:

| Quality | How |
|---------|-----|
| **Structured** | OODA-powered orchestrator and skill sequence |
| **Automatic** | `evolution_hook.py` decides when to run a full ESRA cycle |
| **Value-aligned** | `value-clarifier` gate before experiments |
| **Auditable** | Logging, dashboard, metrics, and `loop-auditor` |
| **Antifragile** | Skills that improve under stress and uncertainty |

The pure architecture (principles, 8 levels, Loop Execution Protocol) lives in a separate repo:

→ **[rrpauls/esra](https://github.com/rrpauls/esra)** — specification only  

→ **hermes-esra** (this repo) — concrete Hermes implementation

---

## Quick start

```bash
git clone https://github.com/rrpauls/hermes-esra.git
cd hermes-esra

chmod +x install.sh
./install.sh
```

**What `install.sh` does:**
- Copies all meta-skills into `~/.hermes/skills/esra/`
- Copies `AGENTS.md` to `~/.hermes/AGENTS.md`

**What it does not do:** tools stay in this repository. Run them from a clone:

```bash
python tools/evolution_hook.py              # demo heuristics
python tools/evolution_hook.py --force-cycle  # force a full ESRA cycle prompt
python tools/skill_validator.py --verbose     # validate skill frontmatter + DAG
python tools/evolution_dashboard.py           # evolution metrics (CLI)
```

After install, restart Hermes (or use `/skills`) so the new skills load.

---

## How the system works

```
Hermes native learning loop
        │
        │  after complex task / skill creation
        ▼
evolution_hook.py  ── analyzes context, confidence, history ──┐
        │                                                       │
        │  trigger?                                             │ skip
        ▼                                                       ▼
hermes-evolution-orchestrator                          (no action)
        │
        ▼
ooda-framework
        │
        ▼
self-observer → value-clarifier → self-improver → mental-model-updater
        │              │
        │              └── gate before experiments
        ▼
experimenter → antifragility-builder → (domain skills as needed)
        │
        │  every 5–10 significant cycles
        ▼
loop-auditor
```

**Core rule (also in `AGENTS.md`):** after any complex task, skill creation, or significant improvement, run `hermes-evolution-orchestrator` — or say `orchestrate evolution` / `run full ESRA cycle`.

---

## Meta-skills (14)

Installed under `~/.hermes/skills/esra/`:

| Skill | Role |
|-------|------|
| `hermes-evolution-orchestrator` | Central conductor of the ESRA loop |
| `ooda-framework` | Observe → Orient → Decide → Act structuring |
| `self-observer` | Honest monitoring of internal state and patterns |
| `self-improver` | Systematic improvement of skills and processes |
| `value-clarifier` | Value alignment (**mandatory before experiments**) |
| `experimenter` | Safe, hypothesis-driven improvement tests |
| `mental-model-updater` | Integrate learnings into long-term models |
| `antifragility-builder` | Grow stronger from stress and uncertainty |
| `loop-auditor` | Meta-audit of the evolutionary process (every 5–10 cycles) |
| `optimizer-philosopher` | Trade-off, ethics, and meaning analysis |
| `system-dynamics-thinker` | Feedback loops, stocks & flows, leverage points |
| `crisis-manager` | High-stakes decisions under uncertainty |
| `hermes-codebase-engineer` | Code and integration work in the Hermes ecosystem |
| `github-actions-integrator` | CI/CD and GitHub Actions automation |

---

## Supporting tools

| Tool | Purpose |
|------|---------|
| `tools/evolution_hook.py` | Smart trigger: complexity, new skills, confidence, rate limits |
| `tools/esra_logger.py` | Structured JSON logs under `~/.hermes/evolution-logs/` |
| `tools/evolution_dashboard.py` | CLI view of cycle metrics and recent history |
| `tools/baseline_metrics.py` | KPI tracking and snapshots |
| `tools/skill_validator.py` | Frontmatter, branding, dependency DAG, stage/promote |
| `tools/experiment_runner.py` | Canary, staged, A/B, and stress experiment lifecycle |
| `tools/hermes_integration.py` | Post-task hooks, skill injection, config feedback |
| `tools/human_oversight.py` | GitHub issues/PRs and `evolve/skill-name-vN` branches |

---

## Development

Requirements: Python 3.11+ (CI uses 3.11), `pytest`, `pyyaml`.

```bash
# From repository root
pip install pytest pyyaml

# Validate skills
python tools/skill_validator.py --verbose

# Run the full test suite
PYTHONPATH=. pytest

# Syntax-check all tools
python -m py_compile tools/*.py
```

Continuous integration (`.github/workflows/ci.yml`) validates tool syntax, skill metadata/DAG, unit/integration/stress tests, frontmatter, branding, and `install.sh` executability.

---

## Repository layout

```
hermes-esra/
├── AGENTS.md              # Triggers and instructions for Hermes
├── ROADMAP.md             # Phases 1–5 complete; 6–7 planned
├── install.sh             # Install skills + AGENTS.md into ~/.hermes
├── assets/logo.png
├── skills/                # 14 ESRA meta-skills (SKILL.md each)
├── tools/                 # Hook, logging, metrics, validation, integration
└── tests/                 # Unit, integration, scenario, and stress tests
```

---

## Relationship to ESRA

| Repository | Role |
|------------|------|
| [esra](https://github.com/rrpauls/esra) | Architecture specification (what ESRA is) |
| **hermes-esra** (this repo) | Hermes-ready skills, tools, and install path |

Keeping the conceptual core separate allows other agents and engines to implement ESRA without inheriting Hermes-specific code.

---

## Contributing

1. Prefer branches `feature/…` for roadmap work or `evolve/skill-name-vN` for skill evolution (see `tools/human_oversight.py`).
2. Before larger changes: `python tools/skill_validator.py` and `PYTHONPATH=. pytest`.
3. After significant work, run an ESRA cycle: `python tools/evolution_hook.py --force-cycle` or trigger `hermes-evolution-orchestrator` in Hermes.

Details and phase plan: **[ROADMAP.md](ROADMAP.md)**.

---

**Status:** Active (July 2026) · **Version:** 1.2 · **License:** [MIT](LICENSE)
