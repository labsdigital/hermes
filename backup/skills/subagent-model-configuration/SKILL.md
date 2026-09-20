---
name: subagent-model-configuration
description: "Configure subagent LLM models via delegation settings."
version: 1.1.0
author: Hermes Agent + labsdigital
license: MIT
tags: [subagent, model, delegation, openrouter, configuration]
---

# Subagent Model Configuration

Configure subagents to use different LLM models than the main agent.

## Current Configuration (2026-09-16)

### Main Agent (Zetta)
```yaml
model:
  default: agnes-2.5-flash
  provider: custom:apihub.agnes-ai.com
  base_url: https://apihub.agnes-ai.com/v1
```

### All Profiles (zetta, atlas, chalbi, irfan, default)
- Main: `agnes-2.5-flash` via apihub.agnes-ai.com
- Delegation: `agnes-2.5-flash` (same as main)

## Important Notes

1. **agnes-2.5-flash is primary**: All profiles use this via apihub.agnes-ai.com
2. **minimax-m2.7:free is BROKEN**: Returns HTTP 404 - do not use for delegation
3. **Write articles manually**: Subagent delegation often fails; write articles directly instead
4. **API keys in .env only**: Never put API keys in config.yaml

## Verification

```bash
# Check configuration
cat /opt/data/profiles/zetta/config.yaml | grep -A 3 "model:"

# List all profiles
grep -r "model:" /opt/data/profiles/*/config.yaml | head -10
```

## Related Skills
- `multi-subagent-orchestration` - Overall subagent management
- `chalbi-workflow` - Chalbi article writing