---
type: MCP-Server
id: sequential-thinking
name: Sequential Thinking
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-sequential-thinking"
capabilities:
  tools:
    - sequentialthinking
    - think
    - revise_thought
  resources:
  prompts:
    - chain_of_thought
    - step_by_step_analysis
stars: 9500
last_updated: 2025-04-13
verified: true
tier: Official
categories:
    - ai-operations
skills_realized:
    - reasoning
relations:
  exposes:
  belongs_to:
    - ai-operations
  commonly_composed_with:
    - brave-search
    - fetch
    - github
  realizes_skills:
    - reasoning
license: MIT
source_url: https://github.com/modelcontextprotocol/server-sequential-thinking
homepage: https://github.com/modelcontextprotocol/server-sequential-thinking
description: Official Sequential Thinking MCP server enabling structured, step-by-step reasoning with chain-of-thought patterns and thought revision capabilities.
---

The official Sequential Thinking MCP server enables structured, step-by-step reasoning for AI agents. It implements a chain-of-thought pattern where each reasoning step builds on previous ones, with support for revision and branching.

## Key Features

- **Step-by-Step Reasoning**: Progressive thought building with full memory of prior steps
- **Thought Revision**: Ability to revisit and correct previous thoughts when new information arises
- **Branching**: Explore multiple reasoning paths and hypotheses simultaneously
- **Configurable Depth**: Control the complexity and depth of reasoning chains
- **Integration Prompts**: Built-in chain-of-thought and analysis prompts

## Philosophy

Rather than generating a single response, this server encourages agents to think through problems methodically, tracking their reasoning process and allowing course correction — mimicking human analytical thinking.

## Use Cases

- Complex problem decomposition and analysis
- Multi-step planning and strategy formulation
- Debugging and root cause analysis
- Research synthesis from multiple sources
- Decision-making with transparent reasoning
