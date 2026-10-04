#!/usr/bin/env python3
"""Structural check for ask-explaining-code.

Fails if the format ladder or the ask-ste-writing dependency is lost in an edit.
"""
import sys
from pathlib import Path

import yaml

SKILL_DIR = Path(__file__).resolve().parent.parent

skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
meta = yaml.safe_load((SKILL_DIR / "skill.yaml").read_text(encoding="utf-8"))

errors = []
for tag in ("<format_ladder>", "<html_style>"):
    if tag not in skill_md:
        errors.append(f"SKILL.md is missing {tag}")
if "ask-ste-writing" not in (meta.get("depends_on") or []):
    errors.append("skill.yaml must declare depends_on: [ask-ste-writing]")

for e in errors:
    print(f"❌ {e}")
if errors:
    sys.exit(1)
print("Validation passed.")
