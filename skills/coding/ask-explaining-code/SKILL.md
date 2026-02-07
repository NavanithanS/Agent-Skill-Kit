# Explaining Code

A skill that helps users understand code through analogies, ASCII diagrams, and conversational step-by-step walkthroughs.

## Purpose

To make complex code accessible and understandable by breaking down technical concepts into relatable analogies, visual representations, and clear explanations. This skill is triggered when users ask questions like "How does this work?", "Explain this code", or "What's happening here?"

## Core Principles

1. **Use Multiple Analogies** — Different analogies resonate with different people
2. **Visualize with ASCII** — Diagrams make abstract concepts concrete
3. **Step-by-Step Walkthroughs** — Break complex flows into digestible chunks
4. **Conversational Tone** — Explain like you're talking to a friend, not writing documentation
5. **Highlight Misconceptions** — Address common misunderstandings proactively

## Usage

When asked to explain code, follow this approach:

### 1. Start with the Big Picture

Begin with a high-level analogy that captures the essence:

```
"Think of this function like a restaurant kitchen:
- Orders come in (input parameters)
- Chefs process them (business logic)
- Dishes go out (return values)"
```

### 2. Create Visual Diagrams

Use ASCII art to show structure, flow, or relationships:

```
┌─────────────┐
│   Request   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validation  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Database   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Response   │
└─────────────┘
```

### 3. Walk Through Step-by-Step

Break down the execution flow with numbered steps and inline comments:

```python
# Step 1: Receive the user's data
def process_user(user_data):
    # Step 2: Check if the data is valid (like checking ID at a club entrance)
    if not validate(user_data):
        return "Invalid data"
    
    # Step 3: Transform the data (like formatting a letter before mailing)
    cleaned = sanitize(user_data)
    
    # Step 4: Save to database (like filing a document)
    save_to_db(cleaned)
    
    # Step 5: Send confirmation (like a receipt)
    return "Success!"
```

### 4. Use Relatable Analogies

Connect technical concepts to everyday experiences:

| Technical Concept | Analogy |
|------------------|---------|
| Variables | Labeled boxes that hold things |
| Functions | Vending machines (input → process → output) |
| Loops | Assembly line workers repeating tasks |
| Conditionals | Forks in the road with signs |
| Classes | Cookie cutters (template for objects) |
| APIs | Restaurant menu (you order, kitchen handles it) |
| Caching | Keeping frequently used items on your desk |
| Recursion | Russian nesting dolls |
| Async/Await | Ordering food delivery while doing other things |
| Database indexes | Book index (quick lookup) |

### 5. Address Common Misconceptions

Proactively clarify confusing points:

```
⚠️ Common Misconception:
"Does this loop run forever?"

No! The loop stops when i reaches 10. Think of it like climbing stairs:
you start at step 0 and stop when you reach step 10.
```

## Response Structure

When explaining code, use this format:

1. **Quick Summary** (1-2 sentences)
2. **Big Picture Analogy** (relatable comparison)
3. **Visual Diagram** (ASCII art showing structure/flow)
4. **Step-by-Step Walkthrough** (numbered explanation)
5. **Key Concepts** (important takeaways)
6. **Common Pitfalls** (what could go wrong)

## Examples

### Example 1: Explaining a Simple Function

**User**: "How does this work?"

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

**AI Response**:

> **Quick Summary**: This calculates Fibonacci numbers using recursion.
>
> **Analogy**: Think of this like a family tree working backwards. To find out how many ancestors you have at generation N, you need to count ancestors from both your parents' sides (N-1 and N-2), then add them together.
>
> **Visual Flow**:
> ```
> fibonacci(4)
>     ├─ fibonacci(3)
>     │   ├─ fibonacci(2)
>     │   │   ├─ fibonacci(1) → 1
>     │   │   └─ fibonacci(0) → 0
>     │   └─ fibonacci(1) → 1
>     └─ fibonacci(2)
>         ├─ fibonacci(1) → 1
>         └─ fibonacci(0) → 0
> ```
>
> **Step-by-Step**:
> 1. **Base case check**: If n is 0 or 1, just return n (these are the "leaves" of our tree)
> 2. **Recursive split**: Otherwise, split into two smaller problems
> 3. **Combine results**: Add the results from both branches
>
> **Key Concept**: Each call spawns two more calls, creating a tree of calculations that eventually hit the base cases and bubble back up.
>
> ⚠️ **Common Pitfall**: This is elegant but slow! It recalculates the same values many times. For fibonacci(4), it calculates fibonacci(2) twice. For larger numbers, this becomes exponentially wasteful.

### Example 2: Explaining a Complex Pattern

**User**: "What's happening in this decorator?"

```python
def retry(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
            return None
        return wrapper
    return decorator
```

**AI Response**:

> **Quick Summary**: This is a decorator that automatically retries a function if it fails.
>
> **Analogy**: Think of this like a persistent salesperson:
> - **retry** = The company policy ("try up to 3 times")
> - **decorator** = The training manual for the salesperson
> - **wrapper** = The actual salesperson who follows the policy
>
> **Nesting Structure**:
> ```
> ┌─────────────────────────────────────┐
> │ retry(max_attempts=3)               │  ← Policy setter
> │  ┌───────────────────────────────┐  │
> │  │ decorator(func)               │  │  ← Training manual
> │  │  ┌─────────────────────────┐  │  │
> │  │  │ wrapper(*args, **kwargs)│  │  │  ← Actual worker
> │  │  │  • Try the task         │  │  │
> │  │  │  • If fail, retry       │  │  │
> │  │  │  • Give up after N tries│  │  │
> │  │  └─────────────────────────┘  │  │
> │  └───────────────────────────────┘  │
> └─────────────────────────────────────┘
> ```
>
> **Step-by-Step**:
> 1. **Outer function** (`retry`): Sets the retry policy (how many attempts)
> 2. **Middle function** (`decorator`): Receives the function to be wrapped
> 3. **Inner function** (`wrapper`): Does the actual work:
>    - Loops up to `max_attempts` times
>    - Tries to run the original function
>    - If it succeeds, returns immediately
>    - If it fails, catches the error and tries again
>    - On the last attempt, lets the error bubble up
>
> **Usage**:
> ```python
> @retry(max_attempts=3)
> def fetch_data():
>     # This will auto-retry up to 3 times if it fails
>     return requests.get(url)
> ```
>
> ⚠️ **Common Misconception**: "Why three nested functions?"
> 
> Each level serves a purpose:
> - Level 1: Configuration (how many retries?)
> - Level 2: Wrapping (which function to retry?)
> - Level 3: Execution (actually doing the retries)

## Best Practices

### Do's ✅

- **Use concrete examples** with actual values
- **Show before/after** states when explaining transformations
- **Draw diagrams** for anything with structure or flow
- **Use emojis sparingly** to highlight important points
- **Provide multiple analogies** if the first might not land
- **Explain the "why"** not just the "what"

### Don'ts ❌

- Don't use jargon without explaining it first
- Don't assume prior knowledge of advanced concepts
- Don't skip the "obvious" parts (they're often not obvious)
- Don't make analogies too complex (defeats the purpose)
- Don't just restate the code in English

## Tone Guidelines

- **Conversational**: "So what's happening here is..." not "The function performs..."
- **Encouraging**: "This is a clever trick!" not "This is standard practice"
- **Patient**: Explain as many times as needed, in different ways
- **Honest**: If something is confusing or poorly written, acknowledge it

## Visual Elements to Use

### Flow Diagrams
```
Start → Check → Process → Save → End
          ↓
        Error? → Retry
```

### State Transitions
```
[Idle] --request--> [Loading] --success--> [Done]
                         |
                       error
                         ↓
                     [Error]
```

### Data Structures
```
Array: [1, 2, 3, 4, 5]
       ↑        ↑
     index 0  index 4

Tree:     10
         /  \
        5    15
       / \
      2   7
```

### Call Stacks
```
main()
  └─ processData()
      └─ validate()
          └─ checkEmail()  ← Currently executing
```

## Notes

- Adapt complexity to the user's apparent skill level
- If they ask follow-up questions, they're engaged—go deeper
- If they seem lost, back up and use simpler analogies
- Always validate understanding: "Does that make sense?"
- Encourage questions: "What part would you like me to clarify?"

## Trigger Phrases

Activate this skill when the user says things like:
- "Explain this code to me"
- "How does this function work?"
- "Break down this logic"
- "Walk me through this file"

