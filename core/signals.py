from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead, Order
from .slack_service import slack_service
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Lead)
def send_lead_slack_notification(sender, instance, created, **kwargs):
    """Send Slack notification when a new lead is created"""
    if created:
        try:
            message = slack_service.format_lead_notification(instance)
            slack_service.send_notification(message)
            logger.info(f"Slack notification sent for new lead: {instance.id}")
        except Exception as e:
            logger.error(f"Error sending Slack notification for lead {instance.id}: {str(e)}")

@receiver(post_save, sender=Order)
def send_order_slack_notification(sender, instance, created, **kwargs):
    """Send Slack notification when a new order is created"""
    if created:
        try:
            message = slack_service.format_order_notification(instance)
            slack_service.send_notification(message)
            logger.info(f"Slack notification sent for new order: {instance.order_id}")
        except Exception as e:
            logger.error(f"Error sending Slack notification for order {instance.order_id}: {str(e)}")