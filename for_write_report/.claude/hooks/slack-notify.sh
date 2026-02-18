#!/bin/bash
#
# Slack notification helper for Claude Code hooks
# Usage: slack-notify.sh "message" ["emoji"] ["color"]
#

# ⚠️ IMPORTANT: Set your Slack Webhook URL here
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# You can also use environment variable (recommended for security)
if [ -n "$SLACK_WEBHOOK_URL_CLAUDE" ]; then
    SLACK_WEBHOOK_URL="$SLACK_WEBHOOK_URL_CLAUDE"
fi

# Arguments
MESSAGE="${1:-No message provided}"
EMOJI="${2:-:robot_face:}"
COLOR="${3:-#36a64f}"

# Check if webhook URL is configured
if [ "$SLACK_WEBHOOK_URL" = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" ]; then
    echo "Warning: Slack Webhook URL not configured in slack-notify.sh" >&2
    exit 0  # Don't fail, just skip notification
fi

# Send notification to Slack
curl -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d @- <<EOF
{
    "username": "Claude Code",
    "icon_emoji": "$EMOJI",
    "attachments": [
        {
            "color": "$COLOR",
            "text": "$MESSAGE",
            "footer": "Research Kit Project",
            "footer_icon": "https://www.anthropic.com/favicon.ico",
            "ts": $(date +%s)
        }
    ]
}
EOF

exit 0
