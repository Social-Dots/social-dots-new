# Slack Webhook Integration Guide

This guide explains how to set up Slack webhook notifications for new leads and orders in the Social Dots platform.

## Overview

The Slack webhook integration automatically sends notifications to a designated Slack channel whenever:
- A new lead is created (via contact forms, API, or AI agent)
- A new order is placed (via checkout or AI agent)

## Setup Instructions

### 1. Create a Slack Channel

1. Go to your Slack workspace
2. Create a new channel (recommended: `#notifications` or `#socialdots-alerts`)
3. Invite relevant team members to the channel

### 2. Create a Slack App and Webhook

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Give your app a name (e.g., "Social Dots Notifications")
4. Select your workspace
5. Go to "Incoming Webhooks" in the left sidebar
6. Toggle "Activate Incoming Webhooks" to ON
7. Click "Add New Webhook to Workspace"
8. Select your channel and click "Allow"
9. Copy the webhook URL (starts with `https://hooks.slack.com/services/`)

### 3. Configure Environment Variables

Add the following to your `.env` file:

```bash
# Slack Configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
SLACK_CHANNEL=#notifications
```

### 4. Test the Integration

You can test the integration by:

1. **Creating a test lead:**
   - Go to the contact page and submit a test inquiry
   - Check your Slack channel for the notification

2. **Creating a test order:**
   - Go to the services page and complete a test checkout
   - Check your Slack channel for the order notification

## Notification Format

### Lead Notifications
Lead notifications include:
- Customer name and contact information
- Service interest
- Budget and timeline (if provided)
- Source of the lead
- Full message content

### Order Notifications
Order notifications include:
- Order ID
- Customer details
- Service and pricing plan
- Order amount
- Current status

## Customization

### Changing the Notification Channel

To change the notification channel, update the `SLACK_CHANNEL` environment variable:

```bash
SLACK_CHANNEL=#your-preferred-channel
```

### Customizing Notification Messages

To customize the notification format, edit the `format_lead_notification()` and `format_order_notification()` methods in `core/slack_service.py`.

### Disabling Notifications

To temporarily disable notifications without removing the configuration:

1. Set `SLACK_WEBHOOK_URL` to empty in your `.env` file:
   ```bash
   SLACK_WEBHOOK_URL=
   ```

2. Or set a different channel that doesn't exist:
   ```bash
   SLACK_CHANNEL=#disabled
   ```

## Troubleshooting

### Common Issues

1. **No notifications received:**
   - Check that `SLACK_WEBHOOK_URL` is correctly set in `.env`
   - Verify the webhook URL is active in Slack
   - Check server logs for error messages

2. **Incorrect channel:**
   - Ensure the channel exists and the bot has access
   - Check the spelling of the channel name (include #)

3. **Formatting issues:**
   - Verify the webhook URL format
   - Check for special characters in customer data

### Debugging

Enable debug logging by adding to your `.env`:

```bash
DEBUG=True
```

Then check the server logs for Slack-related messages.

## Security Considerations

- Keep your webhook URL secure and never commit it to version control
- Use environment variables for all sensitive configuration
- Consider rotating webhook URLs periodically
- Monitor your Slack channel for any suspicious activity

## Support

If you encounter issues with the Slack integration:

1. Check the application logs for error messages
2. Verify your webhook URL works using curl:
   ```bash
   curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"Hello from Social Dots!"}' \
        YOUR_WEBHOOK_URL
   ```
3. Contact your development team for assistance

## API Reference

### SlackWebhookService

The main service class for Slack notifications:

```python
from core.slack_service import slack_service

# Send a custom message
slack_service.send_notification("Your custom message here")

# Format and send a lead notification
message = slack_service.format_lead_notification(lead_object)
slack_service.send_notification(message)
```