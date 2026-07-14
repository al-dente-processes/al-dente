---
type: MCP-Server
id: redis
name: Redis
publisher: community
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-redis"
capabilities:
  tools:
    - redis_get
    - redis_set
    - redis_delete
    - redis_list_keys
    - redis_expire
    - redis_incr
    - redis_decr
    - redis_hget
    - redis_hset
    - redis_lpush
    - redis_lrange
    - redis_publish
    - redis_subscribe
  resources:
    - redis://keys
    - redis://databases
  prompts:
stars: 2800
last_updated: 2025-04-05
verified: false
tier: Community
categories:
    - data
    - infrastructure
skills_realized:
    - database-query
relations:
  exposes:
    - redis://keys
    - redis://databases
  belongs_to:
    - data
    - infrastructure
  commonly_composed_with:
    - postgres
    - sqlite
  realizes_skills:
    - database-query
license: MIT
source_url: https://github.com/modelcontextprotocol/server-redis
homepage: https://github.com/modelcontextprotocol/server-redis
description: Redis MCP server providing high-performance key-value store operations including strings, hashes, lists, and pub/sub messaging.
---

The Redis MCP server provides high-performance key-value store operations for AI agents. It supports the full range of Redis data structures including strings, hashes, lists, sets, and pub/sub messaging.

## Key Features

- **String Operations**: get, set, delete, expire, increment/decrement
- **Hash Operations**: Field-level get and set for structured data
- **List Operations**: Push, pop, and range queries
- **Key Management**: Pattern matching, scanning, and TTL management
- **Pub/Sub**: Publish and subscribe to channels for real-time messaging
- **Cache Strategies**: Built-in TTL and expiration management

## Connection

Configure via `REDIS_HOST`, `REDIS_PORT`, and optionally `REDIS_PASSWORD` environment variables. Supports both standalone and clustered Redis deployments.

## Use Cases

- High-speed caching and session storage
- Real-time leaderboards and counters
- Message queuing and job scheduling
- Rate limiting and throttling
- Real-time analytics and event streaming
