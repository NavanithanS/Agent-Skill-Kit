# Test Case: N+1 Detection

## Input
"Review this PHP code for performance issues:"
```php
$users = User::all();
foreach ($users as $user) {
    echo $user->profile->bio;
}
```

## Expected Output
- **Issue**: N+1 Query Problem
- **Category**: Performance
- **Remediation**: Use eager loading (`User::with('profile')->get()`)
