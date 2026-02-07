---
name: ask-laravel-architect
description: Laravel scaffolding for SQL or Mongo (Official/Jenssegers), SoftDeletes, API standards.
triggers: ["scaffold laravel controller", "create model migration", "structure laravel", "eloquent practices"]
---

<critical_constraints>
❌ NO `request()->all()` → use FormRequest validation
❌ NO fat controllers (>10 lines) → extract to Service/Action
❌ NO `-m` flag for Mongo → schema-less, migrations only for indexes
✅ MUST detect DB driver from composer.json first
✅ MUST return `new <Name>Resource($model)` always
✅ MUST generate test: `make:test <Name>Test`
</critical_constraints>

<detection>
Check `composer.json`:
- No mongo packages → SQL (Illuminate\Eloquent\Model)
- `mongodb/laravel-mongodb` → Official Mongo (MongoDB\Laravel\Eloquent\Model)
- `jenssegers/mongodb` → Legacy Mongo (Jenssegers\Mongodb\Eloquent\Model)
</detection>

<model_blueprint>
```php
declare(strict_types=1);
use MongoDB\Laravel\Eloquent\Model;  // or appropriate base
use MongoDB\Laravel\Eloquent\SoftDeletes;  // driver-specific

class Example extends Model {
    use SoftDeletes;
    protected $connection = 'mongodb';  // for Mongo only
    protected $dates = ['deleted_at'];  // for legacy Mongo
}
```
</model_blueprint>

<migration_strategy>
- SQL: ALWAYS generate migration with `$table->softDeletes()`
- Mongo: Skip table migration, create index migration only
- Always index: slug, email, foreign keys
</migration_strategy>

<controller_rules>
- Response: `new <Name>Resource($model)`
- Input: FormRequest only
- Routing: scoped bindings `/users/{user}/posts/{post}`
- Side effects: use Observer, not Controller
</controller_rules>

<mongo_gotchas>
- No `->join()` → use `->with()` or embedding
- Careful with `like` → prefer regex/text search at volume
- Hybrid relations may fail → use manual lookups in Accessors
</mongo_gotchas>
