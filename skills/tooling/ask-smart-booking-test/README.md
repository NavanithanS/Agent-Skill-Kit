---
title: Smart Booking Test — Agent Skill Kit
description: An advanced autonomous testing skill for verifying end-to-end booking flows. Specializes in Flights, Movies, and Tours with integrated Payment Gateway…
---

# Smart Booking Test

An autonomous "grey box" testing skill for end-to-end booking flows. It reads the source code to plan tests before executing them, and specialises in Flights, Movies and Tours with integrated payment-gateway coverage.

## Purpose

Black-box browser tests break constantly because they guess at selectors and flow order. This skill reads the codebase first — routes, form components, state handling, payment integration — and uses that knowledge to plan a test that matches how the application actually works, then drives the flow and reports what failed and why.

## When to Use

Trigger this skill when the user:

- Wants an end-to-end test of a booking or checkout flow
- Says "test the booking flow", "verify checkout", or "run a payment test"
- Has changed routing, form validation, or payment integration
- Needs regression coverage on a multi-step transactional journey

## Supported Flows

| Flow | Covers |
|---|---|
| **Flights** | Search, passenger details, seat/fare selection, payment |
| **Movies** | Showtime selection, seat map, ticket types, payment |
| **Tours** | Date and party selection, add-ons, traveller details, payment |

Payment-gateway steps are exercised as part of each flow rather than stubbed out, so integration failures surface in the same run.

## How It Works

1. **Read** — inspect routes, components and state to map the real flow
2. **Plan** — derive the steps, inputs and assertions from what the code does
3. **Execute** — drive the flow, including the payment step
4. **Report** — state which step failed, with the observed vs. expected behaviour

Because step 1 precedes step 2, the test adapts to the codebase instead of assuming a canonical booking shape.

## Install

```bash
ask copy ask-smart-booking-test --agent claude
```

Supported agents: Claude Code, Codex, Gemini CLI, Cursor, Antigravity.

## Notes

Use test credentials and a sandbox payment environment. This skill drives real flows and will submit real forms — point it at staging, never production.
