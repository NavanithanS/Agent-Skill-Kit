# Laravel Architect

Senior scaffolding skill. Handles SQL vs Mongo (Jenssegers/Official), SoftDeletes, and strict API standards.

## 1. Context & Driver Detection
**CRITICAL:** Before generating code, read `composer.json` to detect the database driver.

* **Scenario A: SQL (Standard)**
    * **Trigger:** No mongo packages found.
    * **Base Class:** `Illuminate\Database\Eloquent\Model`

* **Scenario B: Official MongoDB (`mongodb/laravel-mongodb`)**
    * **Base Class:** `MongoDB\Laravel\Eloquent\Model`
    * **Connection:** `$connection = 'mongodb';`

* **Scenario C: Legacy MongoDB (`jenssegers/mongodb`)**
    * **Base Class:** `Jenssegers\Mongodb\Eloquent\Model`
    * **Connection:** `$connection = 'mongodb';`

## 2. "The Golden Standard" Blueprint

### Step A: Data Layer (The Foundation)
**Command:** `php artisan make:model <Name>` (Do not use `-m` for Mongo unless specifically asked).

**Model Rules (`app/Models/<Name>.php`):**
1.  **Header:** `declare(strict_types=1);`
2.  **Inheritance:** Extend the correct Base Class found in Step 1.
3.  **Soft Deletes:**
    * **SQL:** `use Illuminate\Database\Eloquent\SoftDeletes;`
    * **Mongo (Official):** `use MongoDB\Laravel\Eloquent\SoftDeletes;`
    * **Mongo (Legacy):** `use Jenssegers\Mongodb\Eloquent\SoftDeletes;`
4.  **Dates:** If using Mongo, add `protected $dates = ['deleted_at'];` for legacy support.

### Step B: Migration Strategy
* **SQL:** ALWAYS generate a migration. Use `$table->softDeletes()`.
* **MongoDB:**
    * **Skip Migration** for creating tables (schema-less).
    * **Create Migration** ONLY for creating indexes (`php artisan make:migration create_indexes_for_users`).
    * **Index Rule:** Always index `slug`, `email`, and foreign keys.

### Step C: Logic Layer (Controller, Services & Resources)
**Command:** `php artisan make:controller <Name>Controller`
**Command:** `php artisan make:resource <Name>Resource`
**Command:** `php artisan make:test <Name>Test` (**MANDATORY**)

**Strict Guidelines:**
1.  **Response Format:** ALWAYS return `new <Name>Resource($model)`.
2.  **Input Safety:** NEVER use `request()->all()`. Use `FormRequest` validation only.
3.  **Route Model Binding:** Use scoped bindings where possible (e.g., `/users/{user}/posts/{post}`).
4.  **No Fat Controllers:** If logic exceeds 10 lines or involves multiple models, move it to a Service or Action class (e.g., `App\Services\<Name>Service` or `App\Actions\Create<Name>`).

**Mongo Specific:**
* Do not use `->join()` (it doesn't exist). Use `->with()` or embedding.
* Use `where('field', 'like', ...)` carefully; prefer regex or text search if high volume.

**Hybrid Relationships (The "Unicorn"):**
* *Scenario:* SQL User `hasMany` Mongo Logs.
* *Solution:* Standard relationships often fail across drivers. Use manual key lookups in Accessors or dedicated Service methods if standard `hasMany` throws driver errors.

### Step D: The "Senior" Touch
* **Observers:** If the logic involves "sending emails" or "logging activity" after saving, DO NOT put it in the Controller. Create an Observer (`php artisan make:observer <Name>Observer`).
