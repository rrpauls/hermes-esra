---
name: hermes-evolution-orchestrator
description: Run one bounded ESRA review after a major architecture or skill change, repeated failure, or an explicit full-cycle request. Select only the meta-skills justified by observable evidence; skip routine successful work. Triggered by "orchestrate evolution", "run full ESRA cycle", "improve self-development cycle", "hermes learning loop", "self-evolution" or similar.
---

# Hermes Evolution Orchestrator

## Role
You are a task-scoped conductor for a deliberate, multi-layered
**Evolutionary Self-Recursive Architecture (ESRA)** review. Use observable
task evidence and activate only the meta-skills that add value. Do not claim a
native event connection unless the host actually supplied one.

## When This Skill Activates
- After a major, evidenced skill or architecture change.
- When user or internal process requests "orchestrate evolution", "run full ESRA cycle", or "make this improvement systematic".
- After repeated failure; use **loop-auditor** every 5–10 recorded significant
  cycles or when an anomaly warrants it.
- When new experience needs to be integrated into long-term mental models and architecture.

## Core Orchestration Process (OODA-powered)

### Observe (What just happened in Hermes loop?)
- What new skill/experience/knowledge did Hermes create or improve?
- What was the context, outcome, and feedback from the task?
- Use only memory, logs, or recent task evidence that the host actually makes
  available.
- Note any signals of success, friction, or unexpected results.

### Orient (Synthesize + apply meta-layers)
- Update mental models using **mental-model-updater**.
- Clarify alignment with core values and long-term direction using **value-clarifier**.
- Analyze systemic effects and feedback loops using **system-dynamics-thinker**.
- Apply philosophical optimization using **optimizer-philosopher**.
- Build honest internal picture using **self-observer**.

### Decide (What meta-improvements to run?)
- Decide which ESRA meta-skills to activate and in what sequence.
- Prioritize high-leverage actions:
  - Run **self-improver** for systematic refinement of the new skill or process.
  - Run **experimenter** to design safe tests of the improvement.
  - Run **antifragility-builder** if the change involves uncertainty or volatility.
  - Schedule **loop-auditor** for later meta-review of the entire cycle.
- Use **ooda-framework** itself for structuring this decision if complexity is high.

### Act (Execute the orchestrated improvements)
- Activate the chosen meta-skills in sequence.
- Document the orchestration (what was triggered, why, expected outcomes).
- Prepare concise results for an authorized host-supported record when one is
  available.
- Make the entire process observable and auditable.

## Integration boundary
- **Caller point**: A user, agent, or future host adapter activates this skill
  after relevant work.
- **Non-invasive**: Lives in `skills/`. Does not modify core Hermes code.
- **Recommended trigger in AGENTS.md**:
  ```
  After a major change, repeated failure, or explicit full-cycle request:
  1. Run hermes-evolution-orchestrator
  2. Select only the necessary meta-skills
  3. Save a concise result only through an available, authorized mechanism
  ```
- Delegation is optional and depends on capabilities actually available in the
  host.

## Recommended Default Sequence (can be customized)
1. hermes-evolution-orchestrator (this skill)
2. ooda-framework (structure the improvement)
3. self-observer → value-clarifier (mandatory gate before experiments)
4. self-improver + mental-model-updater (with optimizer-philosopher / system-dynamics-thinker as needed)
5. experimenter (only after value-clarifier sign-off, if testing needed)
6. antifragility-builder (when relevant)
7. loop-auditor (every 5–10 significant cycles, not every run)
8. hermes-codebase-engineer / github-actions-integrator / crisis-manager (when domain requires)

## Key Principles
- **Make the implicit explicit**: Hermes already improves — we make the improvement process itself improvable, auditable, and wise.
- **Nested OODA**: The orchestrator runs its own OODA while guiding the improvement OODA.
- **Evidence before antifragility claims**: survival of one failure is not
  proof that the system became stronger.
- **Minimal overhead**: Only activate what adds real value. Avoid over-orchestration.
- **Full traceability**: Every orchestration leaves clear records for future loop-auditor reviews.
- **ESRA alignment**: Always respect Value Alignment as a non-negotiable gate and keep the process recursive.

## Output Format
Record:
- **Observed from Hermes loop**
- **Orientation & models updated**
- **Decided meta-actions**
- **Actions taken / skills activated**
- **Expected next observations / feedback loop**

This makes improvement proposals deliberate and auditable. Compounding benefit
must be demonstrated by later outcomes rather than assumed.

## Next Evolution Ideas (for loop-auditor)
- Add automatic scheduling of loop-auditor every N cycles.
- Create visual or structured reports of evolution progress.
- Allow user to define custom orchestration policies.
- Deeper native integration of evolution_hook.py into Hermes.
