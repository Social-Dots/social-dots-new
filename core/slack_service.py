import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class SlackWebhookService:
    """Service for sending notifications to Slack via webhooks"""
    
    def __init__(self):
        self.webhook_url = getattr(settings, 'SLACK_WEBHOOK_URL', None)
        self.channel = getattr(settings, 'SLACK_CHANNEL', '#notifications')
        
    def send_notification(self, message, channel=None):
        """Send a notification to Slack"""
        if not self.webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not configured, skipping Slack notification")
            return False
            
        payload = {
            'text': message,
            'channel': channel or self.channel,
            'username': 'SocialDots Bot',
            'icon_emoji': ':robot_face:'
        }
        
        try:
            response = requests.post(
                self.webhook_url, 
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Slack notification sent successfully: {message[:50]}...")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Slack notification: {str(e)}")
            return False
    
    def format_lead_notification(self, lead):
        """Format a lead notification for Slack"""
        service_name = lead.service_interest.title if lead.service_interest else "Not specified"
        
        message = f"""
🎯 *New Lead Created*

*Name:* {lead.name}
*Email:* {lead.email}
*Phone:* {lead.phone or 'Not provided'}
*Company:* {lead.company or 'Not provided'}
*Service Interest:* {service_name}
*Source:* {lead.source or 'Website'}
*Budget:* {lead.budget or 'Not specified'}
*Timeline:* {lead.timeline or 'Not specified'}
*Message:* {lead.message or 'No message provided'}

*Status:* {lead.status.title()}
*Created:* {lead.created_at.strftime('%Y-%m-%d %H:%M')}
        """
        return message.strip()
    
    def format_order_notification(self, order):
        """Format an order notification for Slack"""
        message = f"""
💰 *New Order Created*

*Order ID:* {order.order_id}
*Customer:* {order.customer_name}
*Email:* {order.customer_email}
*Phone:* {order.customer_phone or 'Not provided'}
*Service:* {order.service_name}
*Plan:* {order.pricing_plan_name}
*Amount:* ${order.amount} {order.currency}
*Status:* {order.status.title()}
*Created:* {order.created_at.strftime('%Y-%m-%d %H:%M')}
        """
        return message.strip()

# Create a singleton instance
slack_service = SlackWebhookService()