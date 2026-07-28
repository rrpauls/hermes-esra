# Self-Evolution Loop

**Version:** 1.2  
**Date:** 2026-07-28

This is a closed system of skills that enables conscious, sustainable, and directed evolutionary development of the agent (ESRA — Evolutionary Self-Recursive Architecture).

## Overall Loop Structure

The loop consists of two interconnected circuits plus a meta-layer:

1. **Awareness and Direction Circuit** — determines *what* and *why* to improve.
2. **Experimentation and Integration Circuit** — handles *how* to test and absorb changes.
3. **Orchestration & Audit Layer** — connects Hermes' native learning loop to the circuits and audits the process itself.

### Main Work Cycle

```
hermes-evolution-orchestrator (conductor)
      ↓
ooda-framework (structure)
      ↓
Self-Observer 
      ↓
Self-Improver + Value-Clarifier 
      ↓
Optimizer-Philosopher + System-Dynamics-Thinker
      ↓
Experimenter (only after value-clarifier sign-off)
      ↓
Mental-Model-Updater 
      ↓
Antifragility-Builder 
      ↑ (feedback)
loop-auditor (every 5–10 significant cycles)
```

Domain specialists (`hermes-codebase-engineer`, `github-actions-integrator`, `crisis-manager`) engage when the task domain requires them.

## Role of Each Skill

| Skill | Primary function in the loop | Contribution type |
|------|------------------------------|-------------------|
| **hermes-evolution-orchestrator** | Conducts the ESRA cycle after complex tasks | Meta-conductor |
| **ooda-framework** | Structures Observe → Orient → Decide → Act | Process structure |
| **Self-Observer** | Clean observation of internal patterns | Input data |
| **Self-Improver** | Gap analysis and generation of improvement ideas | Diagnosis |
| **Value-Clarifier** | Clarifying values and long-term direction (mandatory before experiments) | “Why” and “Where” |
| **Optimizer-Philosopher** | Deep analysis of trade-offs, meaning, consequences | Wisdom and quality |
| **System-Dynamics-Thinker** | Analysis of system structures and long-term dynamics | Systems thinking |
| **Experimenter** | Designing and running safe experiments | Hypothesis testing |
| **Mental-Model-Updater** | Integrating results into updated models | Closing the learning loop |
| **Antifragility-Builder** | Growing capacity through stress and failure | Evolution resilience |
| **Loop-Auditor** | Meta-audit of the entire evolutionary process | Process health |
| **hermes-codebase-engineer** | Code and Hermes integration work | Domain execution |
| **github-actions-integrator** | CI/CD and workflow automation | Domain execution |
| **crisis-manager** | High-stakes decisions under uncertainty | Domain execution |

## Key Loop Properties

- **Closedness** — each stage has a clear input and output.
- **Self-reinforcement** — regular loop cycles strengthen the agent.
- **Antifragility** — the system grows stronger from failures and uncertainty.
- **Directionality** — improvements align with values.
- **Value gate** — `value-clarifier` sign-off is required before experiments.
- **Mechanism design** — interaction rules between skills are deliberately designed (especially Value-Clarifier ↔ Experimenter).
- **Evolutionary dynamics** — successful skill-interaction patterns strengthen over time.
- **Minimalism** — each skill performs a narrow but critical function; orchestrator activates only what adds value.

## How the Loop Works in Practice

1. **Trigger** — After a complex task or skill creation, `evolution_hook.py` / AGENTS.md triggers `hermes-evolution-orchestrator`.
2. **Structure** — `ooda-framework` makes Observe → Orient → Decide → Act explicit.
3. **Observation** — Self-Observer captures recurring patterns.
4. **Reflection and direction** — Self-Improver + Value-Clarifier set priorities.
5. **Deep analysis** — Optimizer-Philosopher and System-Dynamics-Thinker evaluate consequences.
6. **Experiment** — Experimenter validates ideas with small, safe tests (post value gate).
7. **Integration** — Mental-Model-Updater updates internal models.
8. **Strengthening** — Antifragility-Builder makes the system more resilient to future challenges.
9. **Meta-audit** — Loop-Auditor every 5–10 significant cycles reviews the process itself.
10. **Feedback** — results return to Hermes memory and the start of the loop.

## Supporting Tools

**Installed path:** `~/.hermes/esra/tools/` (see `esra-runtime` skill and `~/.hermes/esra/manifest.json`)

| Tool | Role |
|------|------|
| `evolution_hook.py` | Decides when to run the orchestrator |
| `esra_logger.py` | Structured cycle logging |
| `evolution_dashboard.py` | Metrics visualization |
| `baseline_metrics.py` | KPI snapshots |
| `skill_validator.py` | Skill validation and promotion |
| `experiment_runner.py` | Experiment lifecycle |
| `hermes_integration.py` | Native Hermes hooks and skill injection |
| `human_oversight.py` | Human audit trail (issues/PRs) |
| `esra_paths.py` | Shared Hermes/ESRA path resolution |

## Purpose

This loop moves the agent from **fragmented improvement** to **conscious evolution** — where development becomes systematic, directed, antifragile, and capable of self-reinforcement.
