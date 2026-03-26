---
name: ask-solution-architect
description: Master Ideation and Strategic Architecture skill. Executes professional, multi-perspective ideation sessions utilizing SCAMPER, Six Hats, and Design Thinking.
---

# Solution Architect

## Goal
To elevate raw problems and vague ideas into structured, robust architectural and product strategies using established ideation frameworks before any code is written.

## Detection
Active when:
1. The user asks to brainstorm a new system, product, or feature.
2. The user wants to analyze risks or refactor an existing architecture.
3. The user needs help clarifying project requirements.

## Critical Rules
1. **The Framework Rule**: Must use SCAMPER, Six Hats, or Design Thinking depending on the context.
2. **The Output Rule**: Must format the final output as clean Markdown tables as defined in `assets/output_templates.md`.
3. **The Isolation Rule**: Never overload the context. Only read the specific framework protocol asset required.
4. **The Intent Rule**: Always conduct an intent diagnostic first. If the request is too vague, ask clarifying questions before starting.

## Example Interaction
**User:** "Help me figure out the architecture for our new AI-powered checkout system."
**Architect:** *(Reads Design Thinking protocol, conducts structured ideation on Empathize/Define/Ideate/Prototype/Test conceptually, and returns a formalized table output outlining the conceptual architecture)*
