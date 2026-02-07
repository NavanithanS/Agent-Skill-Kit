---
name: ask-fastapi-architect
description: Expert scaffolding for FastAPI projects. Enforces Pydantic V2, Async Database patterns, and Dependency Injection.
---

## 1. Project Structure
When scaffolding a new API:

*   **Modular Layout:**
    ```
    app/
      ├── api/
      │   ├── v1/
      │   │   ├── endpoints/
      │   │   └── api.py
      │   └── deps.py
      ├── core/ (config, security)
      ├── db/ (session, base_class)
      ├── models/ (SQLAlchemy models)
      ├── schemas/ (Pydantic models)
      ├── services/ (Business logic)
      └── main.py
    ```

## 2. API Design & Pydantic
*   **Pydantic V2:** Use `model_config` and `Field`.
    ```python
    from pydantic import BaseModel, ConfigDict, Field

    class UserCreate(BaseModel):
        model_config = ConfigDict(from_attributes=True)
        
        username: str = Field(..., min_length=3)
        email: str
    ```
*   **Response Model:** ALWAYS define `response_model` in route decorators to prevent data leaks.

## 3. Dependency Injection
*   ❌ **FORBIDDEN:** Creating global DB sessions or manually instantiating services in routes.
*   ✅ **REQUIRED:** Use `Depends`.
    ```python
    @router.post("/", response_model=ShowUser)
    async def create_user(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
    ):
        return await UserService.create(db, user_in)
    ```

## 4. Database (Async SQLAlchemy)
*   ALWAYS use `AsyncSession` and `select`.
    ```python
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    ```
*   Use `alembic` for migrations.

## 5. Error Handling
*   Use `HTTPException` with clear detail messages.
*   Create custom exception handlers in `main.py` for global errors.

## Trigger Phrases

Activate this skill when the user says things like:
- "Scaffold a FastAPI endpoint"
- "Create a unified Pydantic model"
- "Structure this Python API"
- "Implement dependency injection here"

