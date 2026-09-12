# Contributing

Keep changes small, evidence-backed, and compatible with the ESRA
specification.

1. Prefer branches `feature/...` for roadmap work and
   `evolve/skill-name-vN` for skill evolution.
2. Add or update tests for runtime, security, or skill-contract changes.
3. Distinguish measured Hermes behavior from simulations and proposed native
   integration.
4. Preserve human review before promotion or configuration changes.

Before opening a pull request, run:

```bash
python tools/skill_validator.py --verbose
PYTHONPATH=. pytest
python -m py_compile tools/*.py
```

By submitting a contribution, you agree that it is licensed under the
Apache License, Version 2.0, without additional terms or conditions.
