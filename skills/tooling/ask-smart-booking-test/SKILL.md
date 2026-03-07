---
name: ask-smart-booking-test
description: >-
  Context-Aware "Grey Box" Test Engineer. Reads source code to plan tests before execution.
  Verifies booking flows (Flights, Movies, Tours) using codebase insights.
version: 1.0.0
license: MIT
permissions:
  - browser:navigate
  - browser:interact
  - payment:sandbox_injection
  - filesystem:read
inputs:
  target_url:
    description: The specific URL to test. If omitted, the agent MUST find the route in the code.
    required: false
  flow_type:
    description: Override for flow detection.
    required: false
---

# Context-Aware SmartBooking Protocol

## <critical_constraints>
1. **Recon First**: ALWAYS scan `routes/` and `tests/` BEFORE opening the browser. Codebase truth TRUMPS assumptions.
2. **Persona Integrity**: ALWAYS act as "Lex Luthor" (`config/identity.json`).
3. **Temporal Safety**: ALWAYS calculate T+30 using `scripts/date_calculator.js`.
4. **Fiscal Safety**: NEVER use real cards. DETECT gateway in code or UI; inject Sandbox creds (`config/payment_cards.json`).
5. **Resilience**: NO `sleep()`. Use Semantic Polling.
</critical_constraints>

## <process>
### 1. Codebase Reconnaissance (Grey Box Phase)
- **Goal**: Identify the *Entry Point* and *Data Constraints* by reading the code.
- **Action**:
  1. **Locate Routes**: Scan `routes/web.php`, `config/routes.rb`, or `app/router.js`.
     - *Search*: "booking", "checkout", "reserve", "cart".
     - *Extract*: The concrete URL path (e.g., `/tours/book/{id}`).
  2. **Inspect Models**: Check `app/Models/` or `src/types/` for validation rules.
     - *If* `Flight` has `requires_passport`, *Then* PREPARE passport data.
     - *If* `Tour` has `waiver_required`, *Then* EXPECT a signature pad.
  3. **Review Existing Tests**: Peek at `tests/Feature` or `cypress/e2e`.
     - *Learn*: What is the "Happy Path"? Are there specific query params needed?

### 2. Strategy Synthesis
- **Target Definition**:
  - IF `target_url` is provided: USE it.
  - IF NOT: CONSTRUCT it from the Route Scan (e.g., `localhost:8000/tours/1`).
- **Data Prep**: Load `config/identity.json`. MERGE with specific constraints found in CodeScan (e.g., "Add Passport Number" if model requires it).

### 3. Execution (Browser Phase)
- **Navigate**: Go to the Target URL.
- **Detect & Adapt**:
  - **Flight**: "IATA", Plane icons. -> Route `MCI`->`IAD`. TSA: `01/01/1980`/M.
  - **Movie**: "Showtime", Grid. -> Center-seek seat. Handle "Gap Error".
  - **Tour**: "Guide", Cal. -> 1 Adult. Sign Waiver.
- **Smart Navigation (T+30)**:
  - Locate Calendar.
  - CLICK "Next" (`>`) until T+30 month matches.
  - SELECT day.

### 4. Payment & Validation
- **Gateway Detection (Code + UI)**:
  - *Code Check*: Does `config/services.php` mention `stripe`, `paypal`, `razorpay`?
  - *UI Check*: look for `iframe` or redirect.
- **Injection**:
  - **Stripe**: `iframe` `__privateStripeFrame`. Visa `4242...`.
  - **PayPal**: Login `config/identity.json` (email/pwd).
  - **Razorpay**: Click "Success".
  - **Square**: Zip `66632`.

## <heuristics>
### Code-Guided Recovery
- **404 Not Found**: IF Url fails, RECHECK `routes/` for prefix (e.g., `/api/v1` vs `/v1`).
- **Validation Error**: IF form rejects input, GREP the error message in the codebase to find the specific regex validation rule (e.g., `Regex('/^\d{10}$/')`) and ADAPT input.

### Modal Warfare
- **Z-Index Overlays**: Close popups ("Sign up", "Cookies").
</heuristics>
