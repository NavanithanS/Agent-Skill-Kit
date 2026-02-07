---
name: ask-fastapi-architect
description: FastAPI scaffolding. Pydantic V2, async database, dependency injection.
triggers: ["scaffold fastapi", "pydantic model", "structure python api", "dependency injection"]
---

<critical_constraints>
❌ NO global DB sessions → use Depends(get_db)
❌ NO manually instantiating services in routes → use Depends
❌ NO routes without response_model → prevents data leaks
✅ MUST use Pydantic V2 (model_config, ConfigDict)
✅ MUST use AsyncSession with select()
✅ MUST use alembic for migrations
</critical_constraints>

<structure>
app/
├── api/v1/endpoints/, api.py, deps.py
├── core/ (config, security)
├── db/ (session, base_class)
├── models/ (SQLAlchemy)
├── schemas/ (Pydantic)
├── services/ (business logic)
└── main.py
</structure>

<pydantic_v2>
```python
from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., min_length=3)
    email: str
```
</pydantic_v2>

<dependency_injection>
```python
@router.post("/", response_model=ShowUser)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await UserService.create(db, user_in)
```
</dependency_injection>

<async_db>
```python
result = await db.execute(select(User).where(User.id == user_id))
user = result.scalars().first()
```
</async_db>
