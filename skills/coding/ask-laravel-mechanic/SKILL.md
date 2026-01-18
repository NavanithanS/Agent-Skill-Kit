---
name: ask-laravel-mechanic
description: Senior maintenance skill. Enforces "Zero Data Loss" policies and handles Mongo/SQL debugging.
---

## 1. The "Death Ground" Safety Protocol
**RULE ZERO:** You are forbidden from causing data loss.

### Migration & Database Safety
1.  **Check Environment:** Run `php artisan env`.
2.  **Forbidden Commands (Prod/Staging):**
    * `migrate:fresh` (Destroys SQL DB)
    * `db:seed` (Overwrites Data)
    * `migrate:reset`
3.  **MongoDB Danger:**
    * **NEVER** run `Model::truncate()` on Production.
    * **NEVER** drop collections manually via script without backup confirmation.
4.  **Allowed:** 
    * `migrate` (Forward only).
5.  **The "Pretend" Trick:** If unsure what a migration will do, run `php artisan migrate --pretend` to see the raw SQL first.

### Soft Delete Restoration
* **Intent:** "I accidentally deleted User 5."
* **Action:**
    ```php
    // Detect ID Type: If string (MongoObjectId) vs Int (SQL)
    $id = '...'; 
    User::withTrashed()->find($id)->restore();
    ```

## 2. Inspection & Debugging

### Database Inspection (Driver Aware)
* **SQL:** `php artisan model:show User`
* **MongoDB:** `model:show` often fails. Use **Tinker** instead:
    * **Command:** `php artisan tinker --execute="dump(App\Models\User::first()->getAttributes())"`
    * **Why:** This reveals the *actual* document structure, including dynamic fields not in any PHP property.

### N+1 Assassin (Lazy Loading Prevention)
* **The silent killer:** Accidental N+1 queries.
* **The Fix:** Add this to `AppServiceProvider::boot()`:
    ```php
    Model::preventLazyLoading(!app()->isProduction());
    ```
* **Debug Mode:** If you suspect a slowdown, toggle this on temporarily in staging to force exceptions on any lazy load.

### Common Errors Guide
* **"Call to member function on null":** You likely queried a Mongo relation using SQL syntax. Check `with()` usage.
* **"Class 'MongoDB\...' not found":** You imported the Official namespace but the project uses `jenssegers`. Check `composer.json` again.

## 3. Maintenance Commands
* **Cache:** `php artisan optimize:clear` (Nukes everything safely).
* **Queue Restart:** `php artisan queue:restart` (Run this after ANY code deployment).
* **MongoDB Indexes:** `php artisan mongodb:sync-indexes` (Essential if using the Mongo driver).

### Queue Forensics
* **Status:** `php artisan queue:monitor default`
* **Failed Jobs:** `php artisan queue:failed`
* **The Surgical Fix:**
    * Retry specific job: `php artisan queue:retry <UUID>`
    * Flush all (Careful!): `php artisan queue:flush`

### Tinker God Mode
* **Quick Login:** Login as a specific user to test authenticated routes/policies.
    ```php
    auth()->loginUsingId(1);
    ```

## 4. Log Analysis & Observability (Smart Mode)

**Goal:** Retrieve the most recent 50 lines (get more if needed) of the *active* log file.

### Step A: Identify Log Channel
Do not blindly `cat` a file. Check which log file is active:

1.  **Try Standard (Single Channel):**
    * Command: `tail -n 50 storage/logs/laravel.log`
    * *If file exists:* Analyze it.
    * *If file is missing:* Proceed to Step 2.

2.  **Try Daily (Date-Based Channel):**
    * Command: `tail -n 50 storage/logs/laravel-$(date +%Y-%m-%d).log`
    * *Note:* The `$(date ...)` sub-command automatically inserts today's date (e.g., `2024-03-20`).

### Step B: Pattern Recognition
When reading the output, focus on these keywords:
* `local.ERROR`: The start of a crash.
* `QueryException`: Database syntax or connection issue.
* `ModelNotFound`: ID doesn't exist (check SoftDeletes).
* `MassAssignmentException`: Missing `$fillable` property.

### Step C: Contextual Search
If looking for a specific bug, use `grep` with context:
* `grep -C 5 "User ID 505" storage/logs/laravel.log`
    * *(This shows 5 lines before and after the match)*
