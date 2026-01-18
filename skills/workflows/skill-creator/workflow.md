# Skill Creator Workflow

A meta-workflow that teaches AI agents how to create skills for Agent Skill Kit.

## Purpose

This workflow guides AI agents through the process of creating new skills, ensuring consistent format and quality across all skills in the repository.

## Workflow Steps

### 1. Understand the Request

When asked to create a new skill:
- Clarify the skill's purpose and target use cases
- Identify the category (coding, reasoning, tooling, other)
- Determine which agents should support it

### 2. Choose a Name

Skill names must be:
- Lowercase with hyphens (kebab-case)
- Descriptive but concise
- 2-50 characters
- Start with a letter

Good: `python-refactor`, `git-workflow`, `code-review`
Bad: `MySkill`, `skill_1`, `x`

### 3. Create skill.yaml

Generate the metadata file:

```yaml
name: skill-name
version: 1.0.0
category: coding|reasoning|tooling|other
description: Brief one-line description
tags:
  - relevant
  - tags
agents:
  - codex
  - gemini
  - claude
  - antigravity
  - cursor
```

### 4. Create README.md

Write comprehensive documentation:

```markdown
# Skill Title

Brief description of what this skill does.

## Purpose

Why this skill exists and what problems it solves.

## Usage

How to apply this skill effectively.

## Examples

Concrete examples demonstrating the skill.

## Notes

Additional considerations or caveats.
```

### 5. Validate Structure

Ensure the skill directory is complete:
```
skills/<category>/<skill-name>/
├── skill.yaml    ✓
└── README.md     ✓
```

### 6. Test Distribution

Verify the skill can be copied to agents:
```bash
ask copy codex --skill skill-name --dry-run
```

## Best Practices

- **Be specific**: Vague skills are less useful
- **Include examples**: Show don't just tell
- **Consider edge cases**: Document limitations
- **Keep it focused**: One skill per concept
- **Version thoughtfully**: Use semantic versioning

## Automation

Use the CLI to bootstrap:
```bash
ask create skill
```

This creates the directory structure and templates automatically.
