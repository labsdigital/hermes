---
name: composio-mcp-integration
description: "Connect Hermes to Composio MCP for 1000+ app integrations."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [composio, mcp, integration]
---

# Composio MCP Integration

Connect Hermes Agent to Composio for 500+ app integrations via MCP.

## Setup

Add to `~/.hermes/config.yaml` (or profile config):

```yaml
mcp_servers:
  composio:
    url: "https://connect.composio.dev/mcp"
    headers:
      x-consumer-api-key: "ck_YOUR_KEY"
    timeout: 180
    connect_timeout: 60
```

## Available Apps (500+)

Popular apps in catalog:
- **Productivity**: Notion, Linear, ClickUp, Asana, Craft
- **Communication**: Slack, Gmail, Outlook, Teams, Discord
- **Social**: Twitter/X, LinkedIn, Instagram, TikTok, Moltbook
- **Dev**: GitHub, GitLab, Bitbucket, Jira, Atlassian
- **Storage**: Google Drive, Dropbox, Box
- **Design**: Figma, Canva
- **Analytics**: Amplitude, Algolia, Datadog, Better Stack

## Workflow

### Step 1: Check Connection Status
```bash
hermes mcp test composio
```

### Step 2: Search for Available Tools
Use `COMPOSIO_SEARCH_TOOLS` to discover relevant tools for your use case:
```
Query: "search notion pages"
Query: "send slack message to channel"
Query: "create github issue"
```

### Step 3: Manage Connections (Auth)
Use `COMPOSIO_MANAGE_CONNECTIONS` to authenticate:
- **add**: Create new connection (returns redirect_url for OAuth)
- **list**: Show all connected accounts
- **rename**: Rename existing connection alias
- **remove**: Delete a connection

### Step 4: Wait for Authentication
After user clicks the OAuth link, use `COMPOSIO_WAIT_FOR_CONNECTIONS` to verify auth is complete.

### Step 5: Execute Tools
Use `COMPOSIO_MULTI_EXECUTE_TOOL` to run tools in parallel (up to 50 at once).

## Available Tools (11 Core)

1. `COMPOSIO_GET_TOOL_SCHEMAS` - Get parameter definitions for tools
2. `COMPOSIO_MANAGE_CONNECTIONS` - Create/manage app connections (add/list/rename/remove)
3. `COMPOSIO_MULTI_EXECUTE_TOOL` - Execute up to 50 tools in parallel
4. `COMPOSIO_REMOTE_BASH_TOOL` - Run bash in remote sandbox
5. `COMPOSIO_REMOTE_WORKBENCH` - Run Python code in Jupyter sandbox
6. `COMPOSIO_SEARCH_TOOLS` - Search 500+ apps for relevant tools
7. `COMPOSIO_SUBMIT_FEEDBACK` - Report tool errors/issues
8. `COMPOSIO_WAIT_FOR_CONNECTIONS` - Wait for OAuth auth to complete
9. `COMPOSIO_MANAGE_SKILL` - Create/update/delete Skills
10. `COMPOSIO_SEARCH_SKILLS` - Search reusable organization Skills
11. `COMPOSIO_USE_SKILL` - Load and follow a Skill's guidance

## Connection Requirements

⚠️ **Never execute toolkit tools without an ACTIVE connection.**

Always follow this sequence:
1. Search tools first → check if connection exists
2. If no connection → `COMPOSIO_MANAGE_CONNECTIONS` with action="add"
3. Show redirect_url to user (as clickable link)
4. User completes OAuth
5. Call `COMPOSIO_WAIT_FOR_CONNECTIONS`
6. Verify with `COMPOSIO_MANAGE_CONNECTIONS` action="list"
7. Only then execute the actual tool

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Auth error | Check header: `x-consumer-api-key` not `x-api-key` |
| Tools missing | Verify connection is active before execution |
| Timeout | Increase `connect_timeout` to 120s |
| Empty results | Use `search_strategy: "tool_search"` to bypass cache |

## References

- [Composio Docs](https://docs.composio.dev)
- [Hermes MCP Guide](native-mcp.md)
- [Notion Setup Example](references/notion-setup.md)
