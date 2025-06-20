import stripe
import logging
from django.conf import settings
from django.urls import reverse
from .models import Order, Service, PricingPlan

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentService:
    @staticmethod
    def create_checkout_session(order_data, request):
        try:
            domain = request.build_absolute_uri('/')[:-1]
            
            line_items = []
            
            if order_data.get('service_id'):
                service = Service.objects.get(id=order_data['service_id'])
                if service.stripe_price_id:
                    line_items.append({
                        'price': service.stripe_price_id,
                        'quantity': 1,
                    })
                else:
                    line_items.append({
                        'price_data': {
                            'currency': 'cad',
                            'product_data': {
                                'name': service.title,
                                'description': service.short_description or service.description[:100],
                            },
                            'unit_amount': int(service.price * 100) if service.price else 0,
                        },
                        'quantity': 1,
                    })
            
            elif order_data.get('pricing_plan_id'):
                pricing_plan = PricingPlan.objects.get(id=order_data['pricing_plan_id'])
                if pricing_plan.stripe_price_id:
                    line_items.append({
                        'price': pricing_plan.stripe_price_id,
                        'quantity': 1,
                    })
                else:
                    line_items.append({
                        'price_data': {
                            'currency': 'cad',
                            'product_data': {
                                'name': pricing_plan.name,
                                'description': pricing_plan.description[:100] if pricing_plan.description else '',
                            },
                            'unit_amount': int(pricing_plan.price * 100),
                            'recurring': {
                                'interval': 'month' if pricing_plan.price_period == 'monthly' else 'year'
                            } if pricing_plan.price_period in ['monthly', 'yearly'] else None,
                        },
                        'quantity': 1,
                    })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment' if not any('recurring' in item.get('price_data', {}) for item in line_items) else 'subscription',
                success_url=domain + reverse('payment_success') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain + reverse('payment_cancelled'),
                customer_email=order_data.get('customer_email'),
                metadata={
                    'order_id': order_data.get('order_id', ''),
                    'customer_name': order_data.get('customer_name', ''),
                    'customer_phone': order_data.get('customer_phone', ''),
                }
            )
            
            return session
            
        except Exception as e:
            logger.error(f"Error creating Stripe checkout session: {str(e)}")
            raise

    @staticmethod
    def retrieve_session(session_id):
        try:
            return stripe.checkout.Session.retrieve(session_id)
        except Exception as e:
            logger.error(f"Error retrieving Stripe session: {str(e)}")
            raise

    @staticmethod
    def handle_successful_payment(session):
        try:
            order_id = session.metadata.get('order_id')
            if order_id:
                order = Order.objects.get(order_id=order_id)
                order.status = 'paid'
                order.stripe_session_id = session.id
                order.stripe_payment_intent_id = session.payment_intent
                order.save()
                
                logger.info(f"Order {order_id} marked as paid")
                return order
            else:
                logger.warning("No order_id found in session metadata")
                return None
                
        except Order.DoesNotExist:
            logger.error(f"Order {order_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error handling successful payment: {str(e)}")
            raise

    @staticmethod
    def handle_webhook(payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                StripePaymentService.handle_successful_payment(session)
            
            elif event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                logger.info(f"Payment intent succeeded: {payment_intent['id']}")
            
            return True
            
        except ValueError as e:
            logger.error(f"Invalid payload: {e}")
            return False
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {e}")
            return False
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return False