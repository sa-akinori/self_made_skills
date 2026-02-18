#!/bin/bash
#
# Discord notification helper for Claude Code hooks
# Usage: discord-notify.sh "message" ["color"]
#

# ⚠️ IMPORTANT: Set your Discord Webhook URL here
# DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
DISCORD_WEBHOOK_URL="https://discordapp.com/api/webhooks/1468619539880218757/-rAMyeR1TjEP_DEFPh7cKd_ApBQqipDl1bsGha8MRsPneiiOBJxfDKIo7fBxk3PNQZWh"

# You can also use environment variable (recommended for security)
if [ -n "$DISCORD_WEBHOOK_URL_CLAUDE" ]; then
    DISCORD_WEBHOOK_URL="$DISCORD_WEBHOOK_URL_CLAUDE"
fi

# Arguments
MESSAGE="${1:-No message provided}"
COLOR="${2:-3066993}"  # Default: green (decimal format for Discord)

# Check if webhook URL is configured
if [ "$DISCORD_WEBHOOK_URL" = "https://discord.com/api/webhooks/YOUR/WEBHOOK/URL" ]; then
    echo "Warning: Discord Webhook URL not configured in discord-notify.sh" >&2
    exit 0  # Don't fail, just skip notification
fi

# Send notification to Discord
curl -X POST "$DISCORD_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d @- <<EOF
{
    "username": "Claude Code",
    "avatar_url": "https://www.anthropic.com/favicon.ico",
    "embeds": [
        {
            "description": "$MESSAGE",
            "color": $COLOR,
            "footer": {
                "text": "Research Kit Project"
            },
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
        }
    ]
}
EOF

exit 0
