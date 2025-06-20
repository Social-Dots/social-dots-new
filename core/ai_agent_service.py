import requests
import logging
from django.conf import settings
from .models import AIAgentLog, Lead, Order, Service

logger = logging.getLogger(__name__)


class AIAgentService:
    def __init__(self):
        self.webhook_url = settings.AI_AGENT_WEBHOOK_URL
        self.api_key = settings.AI_AGENT_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint, data=None, method='POST'):
        url = f"{self.webhook_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"AI Agent API request failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in AI Agent API request: {str(e)}")
            raise

    def health_check(self):
        try:
            result = self._make_request('health', method='GET')
            return result.get('status') == 'healthy'
        except Exception as e:
            logger.error(f"AI Agent health check failed: {str(e)}")
            return False

    def send_whatsapp_notification(self, phone_number, message, message_type='text'):
        data = {
            'phone_number': phone_number,
            'message': message,
            'message_type': message_type
        }
        
        try:
            result = self._make_request('whatsapp/send', data)
            
            AIAgentLog.objects.create(
                log_type='whatsapp',
                user_identifier=phone_number,
                message_content=message,
                response_content=str(result),
                webhook_data=data,
                status='sent'
            )
            
            logger.info(f"WhatsApp message sent to {phone_number}")
            return result
            
        except Exception as e:
            AIAgentLog.objects.create(
                log_type='whatsapp',
                user_identifier=phone_number,
                message_content=message,
                response_content=str(e),
                webhook_data=data,
                status='failed'
            )
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            raise

    def process_chatbot_message(self, user_id, message, context=None):
        data = {
            'user_id': user_id,
            'message': message,
            'context': context or {}
        }
        
        try:
            result = self._make_request('chatbot/process', data)
            
            AIAgentLog.objects.create(
                log_type='chatbot',
                user_identifier=user_id,
                message_content=message,
                response_content=result.get('response', ''),
                webhook_data=data,
                status='processed'
            )
            
            logger.info(f"Chatbot message processed for user {user_id}")
            return result
            
        except Exception as e:
            AIAgentLog.objects.create(
                log_type='chatbot',
                user_identifier=user_id,
                message_content=message,
                response_content=str(e),
                webhook_data=data,
                status='failed'
            )
            logger.error(f"Failed to process chatbot message: {str(e)}")
            raise

    def create_order_from_chatbot(self, user_id, order_data):
        try:
            service = None
            if order_data.get('service_id'):
                service = Service.objects.get(id=order_data['service_id'])
            
            order = Order.objects.create(
                customer_name=order_data.get('customer_name', ''),
                customer_email=order_data.get('customer_email', ''),
                customer_phone=order_data.get('customer_phone', ''),
                service=service,
                amount=order_data.get('amount', 0),
                status='pending',
                notes=f"Order created via AI chatbot - User ID: {user_id}"
            )
            
            webhook_data = {
                'user_id': user_id,
                'order_id': order.order_id,
                'order_data': order_data
            }
            
            result = self._make_request('order/created', webhook_data)
            
            AIAgentLog.objects.create(
                log_type='order_booking',
                user_identifier=user_id,
                message_content=f"Order created: {order.order_id}",
                response_content=str(result),
                webhook_data=webhook_data,
                status='created'
            )
            
            logger.info(f"Order {order.order_id} created from chatbot for user {user_id}")
            return order
            
        except Exception as e:
            logger.error(f"Failed to create order from chatbot: {str(e)}")
            raise

    def notify_new_lead(self, lead):
        data = {
            'lead_id': lead.id,
            'name': lead.name,
            'email': lead.email,
            'phone': lead.phone,
            'company': lead.company,
            'service_interest': lead.service_interest.title if lead.service_interest else None,
            'message': lead.message,
            'source': lead.source
        }
        
        try:
            result = self._make_request('lead/new', data)
            
            AIAgentLog.objects.create(
                log_type='notification',
                user_identifier=lead.email,
                message_content=f"New lead notification: {lead.name}",
                response_content=str(result),
                webhook_data=data,
                status='sent'
            )
            
            logger.info(f"New lead notification sent for {lead.name}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send new lead notification: {str(e)}")
            raise

    def notify_payment_success(self, order):
        data = {
            'order_id': order.order_id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'amount': float(order.amount),
            'service': order.service.title if order.service else None,
            'stripe_payment_intent_id': order.stripe_payment_intent_id
        }
        
        try:
            result = self._make_request('payment/success', data)
            
            AIAgentLog.objects.create(
                log_type='notification',
                user_identifier=order.customer_email,
                message_content=f"Payment success notification: {order.order_id}",
                response_content=str(result),
                webhook_data=data,
                status='sent'
            )
            
            logger.info(f"Payment success notification sent for order {order.order_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send payment success notification: {str(e)}")
            raise

    def get_service_recommendations(self, user_preferences):
        data = {
            'preferences': user_preferences,
            'available_services': [
                {
                    'id': service.id,
                    'title': service.title,
                    'description': service.description,
                    'price': float(service.price) if service.price else None,
                    'features': service.features
                }
                for service in Service.objects.filter(is_active=True)
            ]
        }
        
        try:
            result = self._make_request('services/recommend', data)
            logger.info("Service recommendations retrieved")
            return result
            
        except Exception as e:
            logger.error(f"Failed to get service recommendations: {str(e)}")
            raise

    def process_webhook_data(self, webhook_type, data):
        try:
            if webhook_type == 'whatsapp_message':
                return self._process_whatsapp_webhook(data)
            elif webhook_type == 'chatbot_conversation':
                return self._process_chatbot_webhook(data)
            elif webhook_type == 'order_inquiry':
                return self._process_order_inquiry_webhook(data)
            else:
                logger.warning(f"Unknown webhook type: {webhook_type}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to process webhook data: {str(e)}")
            raise

    def _process_whatsapp_webhook(self, data):
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        AIAgentLog.objects.create(
            log_type='whatsapp',
            user_identifier=phone_number,
            message_content=message,
            webhook_data=data,
            status='received'
        )
        
        response = self.process_chatbot_message(phone_number, message, {
            'channel': 'whatsapp',
            'phone_number': phone_number
        })
        
        if response.get('response'):
            self.send_whatsapp_notification(phone_number, response['response'])
        
        return response

    def _process_chatbot_webhook(self, data):
        user_id = data.get('user_id')
        message = data.get('message')
        
        return self.process_chatbot_message(user_id, message, data.get('context'))

    def _process_order_inquiry_webhook(self, data):
        lead_data = {
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'company': data.get('company', ''),
            'message': data.get('message', ''),
            'source': 'ai_agent'
        }
        
        if data.get('service_id'):
            try:
                service = Service.objects.get(id=data['service_id'])
                lead_data['service_interest'] = service
            except Service.DoesNotExist:
                pass
        
        lead = Lead.objects.create(**lead_data)
        self.notify_new_lead(lead)
        
        return {'lead_id': lead.id, 'status': 'created'}