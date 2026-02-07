# SKILL.md Schema v2.0

Optimized schema for AI-consumable skill definitions.

## Goals

- **≤500 tokens** per skill (OK), 501-700 (warning), >700 (error)
- **High information density** via XML blocks
- **Machine-parsable** constraint format

---

## Required Structure

### YAML Frontmatter

```yaml
---
name: skill-name
description: One-line description (max 100 chars)
triggers: ["phrase1", "phrase2", "phrase3"]
---
```

### Required Block: `<critical_constraints>`

```markdown
<critical_constraints>
❌ NO [forbidden pattern] → [alternative]
❌ NO [another forbidden thing]
✅ MUST [required action]
✅ MUST [another requirement]
</critical_constraints>
```

---

## Optional Blocks

### `<detection>`

Environment inspection before execution:

```markdown
<detection>
Check `composer.json` for:
- `mongodb/laravel-mongodb` → MongoDB Official mode
- `jenssegers/mongodb` → MongoDB Legacy mode
- Neither → SQL mode
</detection>
```

### `<heuristics>`

Decision rules:

```markdown
<heuristics>
- If logic > 10 lines → extract to Service class
- If side effects → use Observer pattern
- SQL → generate migration
- Mongo → index migration only
</heuristics>
```

### `<templates>`

Minimal code examples:

```markdown
<templates>
```python
@router.post("/", response_model=Response)
async def create(data: Input, db: AsyncSession = Depends(get_db)):
    return await Service.create(db, data)
```
</templates>
```

### `<project_structure>`

Compact directory layout (one line):

```markdown
<project_structure>
app/{api/v1/endpoints,core,db,models,schemas,services,main.py}
</project_structure>
```

---

## Compression Rules

| ❌ Before | ✅ After |
|----------|---------|
| "It is important to always use..." | ✅ MUST use... |
| "We recommend that you consider..." | → [action] |
| "Please ensure that..." | ✅ [rule] |
| "You should avoid using..." | ❌ NO [thing] |
| "The best practice is to..." | → [action] |
| Explanatory paragraphs | Delete entirely |

---

## Example: Optimized Skill

```markdown
---
name: ask-fastapi-architect
description: FastAPI scaffolding. Pydantic V2, async DB, DI.
triggers: ["scaffold fastapi", "create api", "pydantic model"]
---

<critical_constraints>
❌ NO Pydantic V1 (Config class) → use model_config
❌ NO global sessions → use Depends(get_db)
❌ NO sync DB → use AsyncSession
✅ MUST use response_model on all routes
✅ MUST use alembic for migrations
</critical_constraints>

<project_structure>
app/{api/v1/endpoints,core,db,models,schemas,services,main.py}
</project_structure>

<templates>
```python
@router.post("/", response_model=ShowUser)
async def create(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.create(db, data)
```
</templates>
```

**Token count: ~180** (vs ~513 original = 65% reduction)

---

## Validation

Run `ask skill lint` to check compliance:

```bash
ask skill lint                    # Lint all
ask skill lint ask-fastapi        # Lint one
ask skill lint --strict           # Fail on warnings
```
