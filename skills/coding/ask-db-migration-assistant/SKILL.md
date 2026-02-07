---
name: ask-db-migration-assistant
description: Safe database schema updates with migration and rollback scripts.
triggers: ["add column", "database migration", "create table", "safe rollback"]
---

<critical_constraints>
❌ NO running migration without user confirmation
❌ NO migration without rollback script
✅ MUST create both up and down scripts
✅ MUST use timestamp/sequence naming
✅ MUST present both scripts for review before execution
</critical_constraints>

<workflow>
1. **Draft Up Script**: SQL to apply change
2. **Draft Down Script**: SQL to undo change
3. **Review**: Present both to user
4. **Confirm**: Wait for explicit approval before running
</workflow>

<naming>
- Migration: `migrations/20260118_add_users_table.sql`
- Rollback: `migrations/20260118_add_users_table_rollback.sql`
</naming>

<example>
User: "Add email column to users"

Up:
```sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

Down:
```sql
ALTER TABLE users DROP COLUMN email;
```
</example>
