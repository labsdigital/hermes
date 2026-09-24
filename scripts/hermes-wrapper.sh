#!/bin/bash
export HOME="/opt/data/home"
export PATH="/opt/data/hermes-agent/venv/bin:$PATH"
exec /opt/data/hermes-agent/hermes acp
