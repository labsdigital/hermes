#!/bin/bash
# Fast version probe for Multica daemon
# MUST EXIT IMMEDIATELY - no ACP startup
export HOME="/opt/data/home"
/opt/data/hermes-agent/venv/bin/python /opt/data/hermes-agent/hermes --version 2>/dev/null | head -1