# Conceptual Integrity Sentinel

A Principal-level engineering agent that audits repositories for architectural drift, bloated abstractions, and "dead code." It enforces Agentic Engineering protocols: Assumption Surfacing, Confusion Management, and Simplicity First.

## Purpose

To fight "Code Slop"—the tendency of AI models to over-engineer, over-abstract, and leave dead code behind. This skill helps maintain conceptual integrity by identifying and eliminating unnecessary complexity.

## Usage

Activate the sentinel with phrases like:
* "Study this repository and provide a detailed list of improvements."
* "Audit the auth module for complexity bloat."
* "Why is the codebase becoming fragile?"

## Features

- **Complexity Bloat Detection**: Detects files where abstraction cost outweighs utility.
- **Dead Paths Identification**: Identifies exported functions/components that have zero consumers.
- **Assumption Surfacing**: Prompts the agent to explicitly list architectural assumptions before analyzing.

## Tools

* **verify_complexity_bloat**: Detects files where abstraction cost outweighs utility.
* **detect_dead_paths**: Identifies exported functions/components that have zero consumers.
* **surface_assumptions**: Prompts the agent to explicitly list architectural assumptions.

## Best Practices

- Run the `verify_complexity_bloat` tool regularly to catch bloat early.
- Perform `detect_dead_paths` scans before major refactors.
- Always review the `SENTINEL_REPORT.md` for critical insights.
