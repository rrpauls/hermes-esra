---
name: esra-runtime
description: Activate esra-runtime when locating, explaining, or running ESRA Python tools (evolution_hook, skill_validator, evolution_dashboard, experiment_runner, hermes_integration, baseline_metrics, esra_logger, human_oversight). Documents the installed package path under Hermes home. Triggered by ESRA tools, where are ESRA tools, evolution_hook path, run ESRA tool, esra-runtime or similar.
---

# ESRA Runtime

## Role
You know where the **ESRA runtime tools** are installed for this Hermes profile and how to invoke them. Skills under `esra/` are procedural knowledge; tools under the ESRA package root are executable Python helpers.

## Install layout (Hermes-native)

```
$HERMES_HOME/                    # default: ~/.hermes
├── AGENTS.md                    # ESRA triggers for Hermes
├── skills/esra/                 # Meta-skills (this skill lives here)
│   ├── esra-runtime/            # this skill
│   └── …                        # orchestrator, ooda-framework, …
└── esra/                        # ESRA package (not a skill)
    ├── manifest.json            # install metadata + tool inventory
    └── tools/                   # Python CLIs — single source of truth
        ├── evolution_hook.py
        ├── skill_validator.py
        ├── evolution_dashboard.py
        ├── experiment_runner.py
        ├── hermes_integration.py
        ├── baseline_metrics.py
        ├── esra_logger.py
        ├── human_oversight.py
        └── esra_paths.py
```

**Canonical tools directory:** `~/.hermes/esra/tools/`  
(or `$HERMES_HOME/esra/tools` / `$ESRA_HOME/tools` when those env vars are set)

## Why tools live outside `skills/`

- Hermes discovers **skills** via `SKILL.md` under `~/.hermes/skills/` (progressive disclosure).
- ESRA tools are shared Python modules with cross-imports; they form one **package**, not 14 copies of scripts.
- This skill bridges discovery: Hermes loads *you* to learn the path, then runs tools by absolute path.

## How to run tools (always prefer installed absolute paths)

Do **not** require a git clone or a particular working directory after install.

```bash
python ~/.hermes/esra/tools/evolution_hook.py
python ~/.hermes/esra/tools/evolution_hook.py --force-cycle
python ~/.hermes/esra/tools/skill_validator.py --verbose --skills-dir ~/.hermes/skills/esra
python ~/.hermes/esra/tools/evolution_dashboard.py
python ~/.hermes/esra/tools/baseline_metrics.py
python ~/.hermes/esra/tools/experiment_runner.py list
```

If `$HERMES_HOME` is set, substitute it for `~/.hermes`.  
If `$ESRA_HOME` is set, tools are at `$ESRA_HOME/tools/`.

## Tool map

| Tool | When to use |
|------|-------------|
| `evolution_hook.py` | Decide whether to run `hermes-evolution-orchestrator` after a task |
| `skill_validator.py` | Validate skill frontmatter, branding, dependency DAG |
| `evolution_dashboard.py` | View cycle metrics and recent history |
| `baseline_metrics.py` | KPI snapshots |
| `experiment_runner.py` | Canary / staged / A/B / stress experiments |
| `hermes_integration.py` | Post-task hooks, skill injection, config feedback |
| `esra_logger.py` | Structured cycle logging API |
| `human_oversight.py` | Issues/PRs and `evolve/skill-name-vN` branches |
| `esra_paths.py` | Shared path resolution (importable) |

## Integration rules

1. After install, **prefer** `~/.hermes/esra/tools/…` over a repository-relative `tools/…` path.
2. Meta-skills (`hermes-evolution-orchestrator`, etc.) stay under `~/.hermes/skills/esra/`.
3. Logs: `~/.hermes/evolution-logs/`; history: `~/.hermes/evolution_history.json`.
4. When unsure of paths, read `~/.hermes/esra/manifest.json` if present.
5. Combine with `hermes-evolution-orchestrator` after complex work; use this skill only for **where/how to run** the helpers.

## Output style
Be concrete: give full paths and copy-pasteable commands. Prefer the installed layout over developer clone paths unless the user is working inside the git repository.
