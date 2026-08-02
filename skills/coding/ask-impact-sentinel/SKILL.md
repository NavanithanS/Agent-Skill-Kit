---
name: ask-impact-sentinel
description: Guidelines for impact analysis, breaking change detection, strategic database design, and comprehensive database indexing review.
---

# Impact Sentinel

A skill focused on impact analysis, breaking change detection, strategic database design, and comprehensive database indexing review.

<critical_constraints>
- ❌ NEVER introduce breaking changes to shared functions without verifying all dependents.
- ❌ NEVER optimize code at the expense of existing functionality or stability.
- ❌ DO NOT perform database operations without considering performance and indexing.
- ❌ NEVER skip the indexing review when a feature touches database queries.
- ✅ ALWAYS identify dependencies before modifying core logic.
- ✅ ALWAYS ensure optimizations are intelligent and verified.
- ✅ ALWAYS use strategic database access and query design.
- ✅ ALWAYS perform a full indexing review covering all related models, services, repositories, and tables — not just the modified controller.
</critical_constraints>

<heuristics>
- If modifying a shared function → Run full dependency check first.
- If optimizing → Verify "Before vs After" performance and correctness.
- If accessing database → Check for missing indexes or potential N+1 issues.
- If any feature touches a database query → Execute the full Database Indexing Review protocol.
- If breaking change is unavoidable → Propose a migration path or versioned API.
- If finalizing a system deployment → You MUST execute live automated validations (Syntax & Terminal Routing).
</heuristics>

## Purpose

The `ask-impact-sentinel` skill guides AI agents to think critically about the consequences of their changes. It ensures that optimizations don't break existing functionality and that database interactions are designed for performance and reliability.

## Usage

Apply this skill when:
- Modifying core functions or shared utilities.
- Refactoring existing logic that has many dependencies.
- Designing or optimizing database schemas and queries.
- Adding, modifying, or reviewing any feature that involves database reads or writes.
- Preparing for a release where stability is paramount.

### Core Protocol

1. **Impact Analysis**: Identify downstream effects of every code change.
2. **Regression Prevention**: Validate that existing features remain functional.
3. **Automated Validation**: Before clearing any code for production, you must explicitly run backend checks:
    - **Syntax & Core Framework Validation**: Run strict framework linting using the CLI (e.g. `php -l path/to/file.php` or `npm run lint`).
    - **Web Routing & Status Code Validation**: Spin up terminal clients to internally ping root routes directly from the framework engine to confirm HTTP 200 statuses and ensure global middlewares didn't crash the stack (e.g. for Laravel: `php artisan tinker --execute="echo app()->handle(Illuminate\Http\Request::create('/', 'GET'))->getStatusCode();"`).
4. **Intelligent Optimization**: Focus on high-impact areas without introducing side effects.
5. **Strategic Data Access**: Prioritize efficient query design and database best practices.
6. **Database Indexing Review**: For every module and controller touched, execute a comprehensive indexing analysis (see dedicated section below).

## Examples

### Before Impact Analysis
```python
# Modifying a shared utility without checking dependents
def get_user_data(user_id):
    return db.query("SELECT * FROM users WHERE id = ?", user_id)
```

### After Impact Analysis
```python
# Checking dependents and ensuring no breaking changes
def get_user_data(user_id):
    # Verified that 5 other modules use this. 
    # Adding a cache layer instead of changing the return structure.
    data = redis.get(f"user:{user_id}")
    if not data:
        data = db.query("SELECT * FROM users WHERE id = ?", user_id)
        redis.set(f"user:{user_id}", data)
    return data
```

## Database Indexing Review Protocol

For **every** module and controller the sentinel works on, a comprehensive database indexing review is **mandatory**. This analysis must extend beyond the modified file to cover **all related models, services, repositories, and database tables** involved in the request.

### Scope of Analysis

When triggered, the indexing review must cover:
- The modified controller or module itself.
- All Eloquent/ORM models referenced directly or indirectly.
- Service classes and repository layers that execute queries on behalf of the controller.
- Database tables involved in joins, subqueries, and relationship eager-loads.
- Scheduled jobs, observers, or event listeners that query the same tables.

### Step-by-Step Procedure

1. **Query Discovery**
   - Trace every database query executed by the feature (including relationships, scopes, and raw queries).
   - List each query with its origin (model, service, repository, or raw statement).
   - Flag N+1 patterns, full-table scans, and unoptimized joins.

2. **Existing Index Audit**
   - Retrieve the current index definitions for every involved table.
   - For SQL databases, run or simulate `SHOW INDEX FROM <table>` (MySQL) or `\d <table>` (PostgreSQL).
   - For MongoDB, inspect `db.collection.getIndexes()`.
   - Map each existing index to the queries it serves.

3. **Missing Index Identification**
   - For each discovered query, determine the optimal index strategy.
   - Identify `WHERE`, `ORDER BY`, `GROUP BY`, and `JOIN ON` columns that lack supporting indexes.
   - Recommend **compound indexes** where multiple columns are filtered or sorted together.
   - For MongoDB, consider field order in compound indexes to match query patterns.

4. **Inefficient Index Detection**
   - Identify indexes with poor selectivity (e.g., boolean columns indexed alone).
   - Detect over-broad indexes that could be narrowed with a prefix or partial index.
   - Flag indexes whose column order does not match the most common query patterns.

5. **Redundant / Unused Index Detection**
   - Identify indexes that are strict prefixes of other compound indexes (and therefore redundant).
   - Detect indexes on columns never referenced in any query path.
   - Flag duplicate indexes (same columns, same order).

6. **Recommendation & Justification**
   - For each recommendation, explain:
     - **What**: The exact index to add, modify, or drop.
     - **Why**: The query it serves and the performance problem it solves.
     - **Impact**: Expected improvement (e.g., "converts a full collection scan to an index seek on ~50k documents").
     - **Trade-off**: Write-performance cost or storage overhead, if relevant.

7. **Migration Script Generation**
   - Provide ready-to-use migration or index creation scripts.
   - For Laravel: generate a complete migration file using `Schema::table` with `$table->index()` or `$table->unique()`.
   - For MongoDB: provide `db.collection.createIndex()` commands or an equivalent migration.
   - For raw SQL: provide `CREATE INDEX` / `DROP INDEX` statements.
   - Include a rollback / `down()` method for every migration.

### Indexing Review Output Format

Present the indexing review in a structured table per table/collection:

```markdown
### Indexing Review: `<table_name>`

| # | Type        | Columns / Fields           | Rationale                              | Impact                                  |
|---|-------------|----------------------------|----------------------------------------|-----------------------------------------|
| 1 | ADD INDEX   | `status, created_at`       | Filters on status + date sort          | Eliminates full scan on 100k+ rows      |
| 2 | ADD COMPOUND| `tenant_id, category, name`| Multi-tenant filtered listing          | Index seek instead of collscan          |
| 3 | DROP INDEX  | `idx_old_status`           | Redundant — prefix of index #1         | Saves ~2MB storage, reduces write cost  |
| 4 | MODIFY      | `idx_name` → add `deleted_at` | Soft-delete queries not covered    | Avoids fetching trashed records         |
```

Followed by the migration script:

```php
// Example Laravel migration
public function up(): void
{
    Schema::table('components', function (Blueprint $table) {
        $table->index(['status', 'created_at'], 'idx_components_status_created');
        $table->index(['tenant_id', 'category', 'name'], 'idx_components_tenant_cat_name');
        $table->dropIndex('idx_old_status');
    });
}

public function down(): void
{
    Schema::table('components', function (Blueprint $table) {
        $table->dropIndex('idx_components_status_created');
        $table->dropIndex('idx_components_tenant_cat_name');
        $table->index(['status'], 'idx_old_status');
    });
}
```

## Best Practices

- **Comprehensive Verification**: Use automated tests and manual verification for all affected paths. Provide explicit terminal readout blocks proving execution paths.
- **Maintain Stability**: Treat the current stable state as sacred; change it only with full awareness.
- **Database Strategy**: Avoid expensive table scans; leverage existing architecture or propose minimal, high-impact improvements.
- **Index Discipline**: Every new query path must have a corresponding index justification. Every dropped index must be confirmed unused.
