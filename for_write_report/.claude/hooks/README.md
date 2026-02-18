# Claude Code Hooks Setup Guide

## Configured Hooks

The following hooks are now active for this project:

### 1. **Session Start** 📚
- **Trigger**: When Claude Code session starts
- **Action**: Displays project context (available skills, key files, output locations)

### 2. **Task Completion** ✅
- **Trigger**: When a task/skill completes successfully
- **Action**: Sends Discord notification with success message

### 3. **Permission Request** 🔔
- **Trigger**: When Claude needs user permission for an action
- **Action**: Sends Discord notification alerting you to respond

### 4. **Quality Check Reminder** 📋
- **Trigger**: After editing or writing a LaTeX (.tex) file
- **Action**: Displays reminder about quality checks (Japanese rendering, captions, etc.)

## Discord Webhook Configuration

To enable Discord notifications, you need to configure your webhook URL:

### Option 1: Direct Configuration (Recommended)

Edit the file: `.claude/hooks/discord-notify.sh`

Replace line 8:
```bash
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
```

With your actual webhook URL:
```bash
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"
```

### Option 2: Environment Variable (More Secure)

Set the environment variable before starting Claude Code:

```bash
export DISCORD_WEBHOOK_URL_CLAUDE="https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"
claude
```

Or add it to your shell profile (~/.bashrc or ~/.zshrc):
```bash
echo 'export DISCORD_WEBHOOK_URL_CLAUDE="https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"' >> ~/.bashrc
source ~/.bashrc
```

## Getting a Discord Webhook URL

1. Open your Discord server
2. Go to Server Settings → Integrations
3. Click "Webhooks" or "Create Webhook"
4. Click "New Webhook"
5. Set a name (e.g., "Claude Code")
6. Select the channel where you want notifications
7. Click "Copy Webhook URL"

## Testing Hooks

After configuration, test the Discord notification:

```bash
/home/sato/Research/Kit/.claude/hooks/discord-notify.sh "Test message 🧪" "3066993"
```

If configured correctly, you'll see a message in your Discord channel.

**Color codes for Discord (decimal format):**
- Green (success): 3066993
- Orange (warning): 16753920
- Red (error): 15158332
- Blue (info): 3447003

## Customizing Notifications

Edit `.claude/hooks/discord-notify.sh` to customize:
- Message format
- Username (default: "Claude Code")
- Avatar URL
- Embed colors
- Footer text

## Disabling Hooks

To temporarily disable all hooks:

1. Add to `.claude/settings.local.json`:
   ```json
   {
     "disableAllHooks": true
   }
   ```

Or comment out specific hooks in the configuration.

## Troubleshooting

### "Warning: Discord Webhook URL not configured"
- The webhook URL is still set to the placeholder
- Configure it using Option 1 or Option 2 above

### Notifications not appearing in Discord
- Verify the webhook URL is correct
- Check that the webhook hasn't been deleted in Discord settings
- Test the webhook with curl manually
- Ensure the bot has permission to post in the selected channel

### Hook not triggering
- Check `.claude/settings.local.json` syntax is valid
- Ensure the hook script is executable: `chmod +x .claude/hooks/discord-notify.sh`
- Review Claude Code logs for errors

## Alternative: Slack Support

If you prefer Slack notifications instead, the original `slack-notify.sh` script is still available in the same directory. To switch back to Slack:

1. Edit `.claude/settings.local.json`
2. Replace `discord-notify.sh` with `slack-notify.sh` in the hooks
3. Configure the Slack webhook URL in `slack-notify.sh`

---

**Note**: Hooks run automatically in the background. You don't need to manually invoke them during normal Claude Code usage.
