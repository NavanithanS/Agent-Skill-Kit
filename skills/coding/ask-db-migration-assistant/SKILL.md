---
name: ask-db-migration-assistant
description: Ensures safe database schema updates by requiring migration and rollback scripts before execution.
---

# DB Migration Assistant

Ensures safe database updates.

## Purpose

To prevent data loss and ensure recoverability during database schema changes by enforcing a strict migration/rollback pattern.

## When to Use

- **Trigger**: "Modify the schema to add a column."
- **Trigger**: "Create a new table for users."
- **Trigger**: Any request that involves running `ALTER`, `CREATE`, or `DROP` SQL commands.

## Instructions

1.  **Draft Migration (Up Script)**
    *   Write the SQL to apply the change.
    *   Save it to `/migrations/` (create this folder if it doesn't exist).
    *   Use a timestamp or sequence number naming convention (e.g., `migrations/20260118_add_users_table.sql`).

2.  **Draft Rollback (Down Script)**
    *   Write the SQL to **undo** the change (e.g., `DROP TABLE`).
    *   Save it to `/migrations/` with a `_rollback` suffix (e.g., `migrations/20260118_add_users_table_rollback.sql`).

3.  **Review and Confirm**
    *   Present both scripts to the user.
    *   **CRITICAL**: Do NOT run the migration script until explicitly confirmed by the user.

## Example

**User**: "Add an `email` column to the `users` table."

**Action**:
1.  Create `migrations/001_add_email_to_users.sql`:
    ```sql
    ALTER TABLE users ADD COLUMN email VARCHAR(255);
    ```
2.  Create `migrations/001_add_email_to_users_rollback.sql`:
    ```sql
    ALTER TABLE users DROP COLUMN email;
    ```
3.  Ask: "I've prepared the migration and rollback scripts. Ready to apply?"

## Trigger Phrases

Activate this skill when the user says things like:
- "Add a column to this table"
- "Draft a database migration"
- "Create a new table schema"
- "Prepare a safe rollback script"

