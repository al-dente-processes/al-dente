---
type: MCP-Server
id: everart
name: EverArt
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-everart"
capabilities:
  tools:
    - generate_image
    - list_styles
    - get_generation_status
    - upscale_image
    - vary_image
  resources:
    - everart://generations
    - everart://styles
  prompts:
    - create_image_prompt
    - refine_image_idea
stars: 1600
last_updated: 2025-04-01
verified: true
tier: Official
categories:
    - ai-operations
skills_realized:
relations:
  exposes:
    - everart://generations
    - everart://styles
  belongs_to:
    - ai-operations
  commonly_composed_with:
    - filesystem
    - fetch
  realizes_skills:
license: MIT
source_url: https://github.com/modelcontextprotocol/server-everart
homepage: https://github.com/modelcontextprotocol/server-everart
description: Official EverArt MCP server enabling AI image generation with style controls, upscaling, and variation capabilities.
---

The official EverArt MCP server enables AI agents to generate and manipulate images through the Model Context Protocol. It provides access to AI image generation with style controls, upscaling, and variation capabilities.

## Key Features

- **Image Generation**: Create images from text prompts with parameter control
- **Style Library**: Browse and apply predefined artistic styles
- **Generation Tracking**: Monitor generation status and retrieve results
- **Upscaling**: Increase resolution of generated images
- **Variations**: Create alternative versions of existing images
- **Prompt Engineering**: Built-in prompts for refining image ideas

## Authentication

Requires an `EVERART_API_KEY` environment variable. Sign up at EverArt to obtain API credentials.

## Use Cases

- Marketing asset and social media image generation
- UI/UX mockup and wireframe creation
- Concept art and illustration prototyping
- Image variation exploration for creative workflows
