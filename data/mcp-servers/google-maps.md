---
type: MCP-Server
id: google-maps
name: Google Maps
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-google-maps"
capabilities:
  tools:
    - maps_geocode
    - maps_reverse_geocode
    - maps_search_places
    - maps_place_details
    - maps_directions
    - maps_distance_matrix
    - maps_elevation
  resources:
  prompts:
    - plan_route
    - find_nearby
stars: 3100
last_updated: 2025-04-06
verified: true
tier: Official
categories:
    - web
skills_realized:
relations:
  exposes:
  belongs_to:
    - web
  commonly_composed_with:
    - brave-search
    - fetch
  realizes_skills:
license: MIT
source_url: https://github.com/modelcontextprotocol/server-google-maps
homepage: https://github.com/modelcontextprotocol/server-google-maps
description: Official Google Maps MCP server providing geocoding, place search, directions, distance matrix, and elevation APIs.
---

The official Google Maps MCP server enables AI agents to access Google's geocoding, places, directions, and elevation APIs through the Model Context Protocol.

## Key Features

- **Geocoding**: Convert addresses to coordinates and vice versa
- **Place Search**: Find businesses and points of interest with text queries
- **Place Details**: Retrieve reviews, photos, and detailed place information
- **Directions**: Get driving, walking, biking, and transit directions
- **Distance Matrix**: Calculate travel times and distances for multiple points
- **Elevation**: Query elevation data for coordinates and paths

## Authentication

Requires a `GOOGLE_MAPS_API_KEY` environment variable. Enable the relevant APIs (Geocoding, Places, Directions, Distance Matrix, Elevation) in the Google Cloud Console.

## Use Cases

- Location-based service recommendations
- Route planning and logistics optimization
- Address validation and standardization
- Travel time analysis and planning
