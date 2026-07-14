---
type: Agentic-Pattern
id: tool-composition
name: Tool Composition
description: >-
  Multiple MCP servers composed to accomplish complex tasks. This pattern describes how agents break down complex objectives into sub-tasks, each delegated to the most appropriate MCP server. The outputs of one tool become inputs to another, creating a pipeline of capabilities that exceeds what any single server could achieve alone.
examples:
    - filesystem
    - postgres
    - github
    - slack
relations:
  exemplified_by:
    - filesystem
    - postgres
    - github
    - slack
  related_to:
    - skill-realization
    - context-amplification
---
