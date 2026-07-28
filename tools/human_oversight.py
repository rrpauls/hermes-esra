#!/usr/bin/env python3
"""
human_oversight.py

Provides utilities for integrating human oversight into the ESRA loop.
Includes generation of GitHub issue templates (for crisis interventions and weekly reports)
and helpers for enforcing branch naming conventions.
"""

import os
import re
from pathlib import Path
from datetime import datetime

try:
    from tools.esra_paths import is_safe_path_component, secure_mkdir
except ImportError:
    from esra_paths import is_safe_path_component, secure_mkdir

class HumanOversight:
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir or Path.home() / ".hermes" / "oversight-reports")
        secure_mkdir(self.output_dir, 0o700)

    def generate_crisis_issue_template(self, crisis_details):
        """
        Generates a markdown template for a GitHub issue representing a crisis intervention.
        In a full implementation, this would use the GitHub API to open the issue.
        """
        timestamp = datetime.now().isoformat()

        template = f"""# ESRA Crisis Intervention Alert

**Timestamp:** {timestamp}
**Severity:** {crisis_details.get('severity', 'UNKNOWN')}

## Description
The `crisis-manager` meta-skill was triggered during the recent ESRA cycle.
**Reason:** {crisis_details.get('reason', 'No reason provided.')}

## Context
- Task Context: {crisis_details.get('task_context', 'N/A')}
- Suggested Action: {crisis_details.get('suggested_action', 'Human review required.')}

## Human Action Required
Please review the evolution logs and provide guidance on how to resolve this anomaly.
"""
        filename = f"crisis_issue_{timestamp.replace(':', '-')}.md"
        filepath = self.output_dir / filename
        fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(template)

        return str(filepath)

    def generate_weekly_report_issue(self, metrics):
        """
        Generates a summary issue template for the Weekly Evolution Report.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")

        template = f"""# Weekly Evolution Report ({date_str})

## Summary of Evolution
- Total Cycles this week: {metrics.get('total_cycles', 0)}
- Success Rate: {metrics.get('success_rate', 0.0)}%

## Skill Updates
- New Skills Created: {metrics.get('new_skills_created', 0)}
- Improvements Applied: {metrics.get('improvements_applied', 0)}

## System Health
- Value Changes Detected: {metrics.get('value_changes_count', 0)}
- Anomalies / Crises: {metrics.get('anomalies_count', 0)}

Please review this summary to ensure Hermes is evolving safely and remaining aligned with core values.
"""
        filename = f"weekly_report_{date_str}.md"
        filepath = self.output_dir / filename
        fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(template)

        return str(filepath)

    @staticmethod
    def format_pr_branch_name(skill_name, version=1):
        """
        Enforces the branch naming convention: evolve/skill-name-vN

        Strips path separators and unsafe characters so the result cannot be
        used for git path / ref injection (e.g. ``../`` or spaces).
        """
        if not isinstance(version, int) or isinstance(version, bool) or version < 1 or version > 10_000:
            raise ValueError(f"Invalid version: {version!r}")
        # Normalize to kebab-case, then allowlist
        cleaned = skill_name.lower().replace("_", "-").replace(" ", "-")
        cleaned = re.sub(r"[^a-z0-9.-]+", "-", cleaned)
        cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-.")
        if not is_safe_path_component(cleaned):
            raise ValueError(f"Invalid skill_name for branch: {skill_name!r}")
        return f"evolve/{cleaned}-v{version}"


if __name__ == "__main__":
    oversight = HumanOversight()

    print("Generating mock crisis issue template...")
    crisis_path = oversight.generate_crisis_issue_template({
        "severity": "HIGH",
        "reason": "Value drift detected during skill generation.",
        "task_context": "Creating a new code refactoring skill"
    })
    print(f"Crisis template saved to: {crisis_path}")

    print("\nGenerating mock weekly report template...")
    report_path = oversight.generate_weekly_report_issue({
        "total_cycles": 12,
        "success_rate": 95.5,
        "new_skills_created": 2,
        "improvements_applied": 5
    })
    print(f"Weekly report template saved to: {report_path}")

    print("\nTesting Branch Naming Utility:")
    print("Input: 'Advanced Reasoning'", "Output:", HumanOversight.format_pr_branch_name("Advanced Reasoning", version=2))
