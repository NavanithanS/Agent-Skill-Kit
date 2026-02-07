---
name: ask-laravel-mechanic
description: Laravel maintenance with Zero Data Loss policy, Mongo/SQL debugging.
triggers: ["fix n+1 query", "debug laravel queue", "check log files", "restore soft deleted"]
---

<critical_constraints>
❌ NO `migrate:fresh` on prod/staging → destroys DB
❌ NO `db:seed` on prod → overwrites data
❌ NO `Model::truncate()` on prod without backup
❌ NO `migrate:reset` on prod
✅ MUST run `php artisan env` before dangerous commands
✅ MUST use `migrate --pretend` when unsure
✅ MUST restart queue after code deployment
</critical_constraints>

<safety_commands>
✅ Allowed: `migrate` (forward only)
✅ Safe test: `migrate --pretend` (shows SQL without running)
✅ Cache clear: `optimize:clear`
✅ Queue restart: `queue:restart` (after deploy!)
</safety_commands>

<soft_delete_restore>
```php
User::withTrashed()->find($id)->restore();
```
</soft_delete_restore>

<debugging>
## Database Inspection
- SQL: `php artisan model:show User`
- Mongo: `php artisan tinker --execute="dump(App\Models\User::first()->getAttributes())"`

## N+1 Prevention
```php
// In AppServiceProvider::boot()
Model::preventLazyLoading(!app()->isProduction());
```

## Common Errors
- "member function on null" → Mongo relation with SQL syntax, check `with()`
- "MongoDB\... not found" → wrong namespace, check composer.json
</debugging>

<log_analysis>
```bash
# Single channel
tail -n 50 storage/logs/laravel.log

# Daily channel
tail -n 50 storage/logs/laravel-$(date +%Y-%m-%d).log

# Search with context
grep -C 5 "User ID 505" storage/logs/laravel.log
```

Keywords: local.ERROR, QueryException, ModelNotFound, MassAssignmentException
</log_analysis>

<queue_forensics>
- Status: `queue:monitor default`
- Failed: `queue:failed`
- Retry one: `queue:retry <UUID>`
- Flush all: `queue:flush` (careful!)
</queue_forensics>
