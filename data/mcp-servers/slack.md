---
type: MCP-Server
id: slack
name: Slack
publisher: modelcontextprotocol
transport: stdio
install:
  type: npm
  command: "npx -y @modelcontextprotocol/server-slack"
capabilities:
  tools:
    - slack_list_channels
    - slack_post_message
    - slack_reply_to_thread
    - slack_add_reaction
    - slack_get_channel_history
    - slack_get_thread_replies
    - slack_get_users
    - slack_get_user_profile
  resources:
    - slack://channels
    - slack://users
  prompts:
    - summarize_conversation
    - draft_announcement
stars: 6200
last_updated: 2025-04-08
verified: true
tier: Official
categories:
    - communication
skills_realized:
relations:
  exposes:
    - slack://channels
    - slack://users
  belongs_to:
    - communication
  commonly_composed_with:
    - github
    - sentry
  realizes_skills:
license: MIT
source_url: https://github.com/modelcontextprotocol/server-slack
homepage: https://github.com/modelcontextprotocol/server-slack
description: Official Slack MCP server enabling agents to read channel history, post messages, reply to threads, and manage reactions in Slack workspaces.
---

The official Slack MCP server allows AI agents to interact with Slack workspaces. Agents can read channel history, post messages, reply to threads, and manage reactions — enabling rich team collaboration workflows.

## Key Features

- **Channel Operations**: List channels and retrieve message history
- **Messaging**: Post messages to channels and reply in threads
- **Reactions**: Add emoji reactions to messages for lightweight interactions
- **Thread Context**: Retrieve full thread replies for contextual conversations
- **User Directory**: List workspace users and view profiles

## Authentication

Requires a `SLACK_BOT_TOKEN` environment variable. The bot needs appropriate scopes including `chat:write`, `channels:read`, `channels:history`, and `users:read`.

## Use Cases

- Automated status updates and announcements
- Conversation summarization and action item extraction
- Interactive team assistance and Q&A
- Incident response coordination
