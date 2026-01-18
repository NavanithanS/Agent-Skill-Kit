# Skill Creator

A meta-skill that teaches AI agents how to create skills for Agent Skill Kit.

## Purpose

This skill enables AI agents to autonomously create new skills directly within the Agent Skill Kit repository. When you're working inside an AI agent (Antigravity, Claude Code, Gemini CLI, Codex), you can ask the agent to create a skill and it will follow this workflow.

**Key Insight**: AI-assisted skill creation happens *inside* the AI agent environment, not via external API calls. The AI reads this skill and generates the skill files directly.

## How to Use

### Inside an AI Agent Environment

Simply ask your AI agent:

```
Create a new skill called "git-workflow" that teaches best practices for Git branching and commits.
```

The AI agent will:
1. Read this skill-creator workflow
2. Generate appropriate `skill.yaml` and `README.md`
3. Write them to the correct location in `skills/`

### Via CLI (Interactive)

```bash
ask create skill
```

This starts an interactive prompt for manual skill creation.

---

## Skill Creation Workflow

### Step 1: Understand Requirements

When asked to create a skill, clarify:
- **Purpose**: What problem does this skill solve?
- **Category**: coding, reasoning, tooling, or other
- **Target Agents**: Which agents should support it?
- **Scope**: Is it focused enough for a single skill?

### Step 2: Choose a Name

Skill names must follow these rules:
- **Format**: lowercase with hyphens (kebab-case)
- **Length**: 2-50 characters
- **Start**: Must begin with a letter
- **Characters**: letters, numbers, hyphens only

```
✓ Good: python-refactor, git-workflow, code-review, api-design
✗ Bad:  MySkill, skill_1, 1st-skill, x
```

### Step 3: Determine Category

| Category | Use For |
|----------|---------|
| `coding` | Programming techniques, languages, refactoring |
| `reasoning` | Problem-solving, analysis, decision-making |
| `tooling` | Tools, workflows, automation, meta-skills |
| `other` | Everything else |

### Step 4: Generate skill.yaml

Create the metadata file:

```yaml
name: skill-name
version: 1.0.0
category: coding|reasoning|tooling|other
description: Brief one-line description (max 100 chars)
tags:
  - relevant
  - descriptive
  - tags
agents:
  - codex
  - gemini
  - claude
  - antigravity
```

### Step 5: Generate README.md

Write comprehensive documentation:

```markdown
# Skill Title

Brief description of what this skill does and why it's useful.

## Purpose

Explain the problem this skill solves and its goals.

## Usage

How to apply this skill effectively. Include:
- Step-by-step instructions
- Key principles
- Decision criteria

## Examples

Concrete examples demonstrating the skill:
- Before/after code samples
- Common scenarios
- Edge cases

## Best Practices

- Important tips
- Common pitfalls to avoid
- Performance considerations

## Notes

Additional context, limitations, or related skills.
```

### Step 6: Write Files

Create the skill directory structure:

```
skills/<category>/<skill-name>/
├── skill.yaml    # Metadata
└── README.md     # Documentation
```

**Location**: `/path/to/agent-skill-kit/skills/<category>/<skill-name>/`

### Step 7: Verify

Check that:
- [ ] `skill.yaml` is valid YAML
- [ ] All required fields are present
- [ ] `README.md` has all sections
- [ ] Name follows conventions
- [ ] Category is valid

---

## Quality Guidelines

### Do
- Be specific and actionable
- Include real examples
- Cover common use cases
- Keep it focused (one skill = one concept)
- Use clear, concise language

### Don't
- Be too generic or vague
- Include unrelated topics
- Skip examples
- Write walls of text without structure

---

## Example: Creating a Skill

**User Request**: "Create a skill for writing clean Python docstrings"

**AI Response**:

1. **Name**: `python-docstrings`
2. **Category**: `coding`
3. **Files created**:

`skills/coding/python-docstrings/skill.yaml`:
```yaml
name: python-docstrings
version: 1.0.0
category: coding
description: Guidelines for writing clear, consistent Python docstrings
tags:
  - python
  - documentation
  - docstrings
  - clean-code
agents:
  - codex
  - gemini
  - claude
  - antigravity
```

`skills/coding/python-docstrings/README.md`:
```markdown
# Python Docstrings

Guidelines for writing clear, consistent Python docstrings.

## Purpose
...
```

---

## Distributing This Skill

Copy this skill to your AI agents:

```bash
# Copy to all agents
ask copy codex --skill skill-creator
ask copy gemini --skill skill-creator
ask copy claude --skill skill-creator
ask copy antigravity --skill skill-creator

# Or sync all at once
ask sync all
```

Once copied, your AI agents will have this workflow available and can create new skills autonomously!
