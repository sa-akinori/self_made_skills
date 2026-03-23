#!/bin/bash
#
# Research Kit Docker launcher
#
# Usage:
#   ./docker-run.sh
#
# First time setup:
#   1. Run 'claude' on your HOST machine first and complete login
#   2. Then use this script - it shares your login credentials with the container
#
# Inside the container:
#   claude                                # Normal mode
#   claude --dangerously-skip-permissions # Autonomous mode
#
# Environment variables (optional):
#   GEMINI_API_KEY     - Google Gemini API key (for conceptual figures)
#   ANTHROPIC_API_KEY  - Anthropic API key (if using API instead of subscription)
#

set -e

IMAGE_NAME="research-kit"
CONTAINER_NAME="research-kit-$(date +%s)"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Build image if not exists
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "Building Research Kit Docker image (first time only, may take several minutes)..."
    docker build -t "${IMAGE_NAME}" "${PROJECT_DIR}"
fi

# Auth mount: share host's Claude credentials with container
AUTH_FLAGS=""
if [ -d "${HOME}/.claude" ]; then
    AUTH_FLAGS="-v ${HOME}/.claude:/home/researcher/.claude"
    echo "  Auth: Using credentials from ~/.claude"
fi
if [ -f "${HOME}/.claude.json" ]; then
    AUTH_FLAGS="${AUTH_FLAGS} -v ${HOME}/.claude.json:/home/researcher/.claude.json"
fi

# Env flags
ENV_FLAGS=""
if [ -n "${GEMINI_API_KEY}" ]; then
    ENV_FLAGS="${ENV_FLAGS} -e GEMINI_API_KEY=${GEMINI_API_KEY}"
fi
if [ -n "${ANTHROPIC_API_KEY}" ]; then
    ENV_FLAGS="${ENV_FLAGS} -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}"
fi

echo "Starting Research Kit container..."
echo "  Project: ${PROJECT_DIR}"
echo "  Mounted: /workspace"
echo ""
echo "  Run 'claude' to start Claude Code"
echo "  Run 'claude --dangerously-skip-permissions' for autonomous mode"
echo ""

docker run -it --rm \
    --name "${CONTAINER_NAME}" \
    -v "${PROJECT_DIR}:/workspace" \
    ${AUTH_FLAGS} \
    ${ENV_FLAGS} \
    "${IMAGE_NAME}"