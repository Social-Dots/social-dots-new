import requests
import logging
from django.conf import settings
from .models import Order

logger = logging.getLogger(__name__)


class FrappeService:
    def __init__(self):
        self.api_url = settings.FRAPPE_API_URL
        self.api_key = settings.FRAPPE_API_KEY
        self.api_secret = settings.FRAPPE_API_SECRET
        self.headers = {
            'Authorization': f'token {self.api_key}:{self.api_secret}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
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
            logger.error(f"Frappe API request failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Frappe API request: {str(e)}")
            raise

    def create_customer(self, customer_data):
        data = {
            "doctype": "Customer",
            "customer_name": customer_data.get('name'),
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "Canada",
            "email_id": customer_data.get('email'),
            "mobile_no": customer_data.get('phone', ''),
        }
        
        try:
            result = self._make_request('POST', '/api/resource/Customer', data)
            logger.info(f"Customer created in Frappe: {result.get('data', {}).get('name')}")
            return result.get('data', {}).get('name')
        except Exception as e:
            logger.error(f"Failed to create customer in Frappe: {str(e)}")
            raise

    def create_sales_order(self, order):
        try:
            customer_name = self.create_customer({
                'name': order.customer_name,
                'email': order.customer_email,
                'phone': order.customer_phone
            })
            
            items = []
            if order.service:
                items.append({
                    "item_code": f"SERVICE-{order.service.id}",
                    "item_name": order.service.title,
                    "description": order.service.description,
                    "qty": 1,
                    "rate": float(order.amount),
                    "amount": float(order.amount)
                })
            elif order.pricing_plan:
                items.append({
                    "item_code": f"PLAN-{order.pricing_plan.id}",
                    "item_name": order.pricing_plan.name,
                    "description": order.pricing_plan.description or order.pricing_plan.name,
                    "qty": 1,
                    "rate": float(order.amount),
                    "amount": float(order.amount)
                })

            data = {
                "doctype": "Sales Order",
                "customer": customer_name,
                "order_type": "Sales",
                "transaction_date": order.created_at.strftime('%Y-%m-%d'),
                "delivery_date": order.created_at.strftime('%Y-%m-%d'),
                "items": items,
                "custom_order_id": order.order_id,
                "custom_stripe_payment_intent": order.stripe_payment_intent_id,
                "custom_notes": order.notes or f"Order from SocialDots.ca - {order.order_id}"
            }
            
            result = self._make_request('POST', '/api/resource/Sales Order', data)
            sales_order_name = result.get('data', {}).get('name')
            
            if sales_order_name:
                order.frappe_document_id = sales_order_name
                order.save()
                logger.info(f"Sales Order created in Frappe: {sales_order_name}")
                
                self.submit_sales_order(sales_order_name)
                
            return sales_order_name
            
        except Exception as e:
            logger.error(f"Failed to create sales order in Frappe: {str(e)}")
            raise

    def submit_sales_order(self, sales_order_name):
        try:
            data = {"docstatus": 1}
            result = self._make_request('PUT', f'/api/resource/Sales Order/{sales_order_name}', data)
            logger.info(f"Sales Order submitted in Frappe: {sales_order_name}")
            return result
        except Exception as e:
            logger.error(f"Failed to submit sales order in Frappe: {str(e)}")
            raise

    def get_sales_order(self, sales_order_name):
        try:
            result = self._make_request('GET', f'/api/resource/Sales Order/{sales_order_name}')
            return result.get('data')
        except Exception as e:
            logger.error(f"Failed to get sales order from Frappe: {str(e)}")
            raise

    def create_project_from_order(self, order):
        try:
            if not order.frappe_document_id:
                raise ValueError("Order must have a Frappe document ID")
                
            project_data = {
                "doctype": "Project",
                "project_name": f"{order.service.title if order.service else order.pricing_plan.name} - {order.customer_name}",
                "customer": order.customer_name,
                "sales_order": order.frappe_document_id,
                "expected_start_date": order.created_at.strftime('%Y-%m-%d'),
                "project_type": "External",
                "status": "Open",
                "custom_order_id": order.order_id,
                "custom_client_email": order.customer_email,
                "custom_client_phone": order.customer_phone
            }
            
            result = self._make_request('POST', '/api/resource/Project', project_data)
            project_name = result.get('data', {}).get('name')
            logger.info(f"Project created in Frappe: {project_name}")
            return project_name
            
        except Exception as e:
            logger.error(f"Failed to create project in Frappe: {str(e)}")
            raise

    def create_task(self, project_name, task_data):
        try:
            data = {
                "doctype": "Task",
                "subject": task_data.get('subject'),
                "description": task_data.get('description', ''),
                "project": project_name,
                "priority": task_data.get('priority', 'Medium'),
                "status": "Open"
            }
            
            result = self._make_request('POST', '/api/resource/Task', data)
            task_name = result.get('data', {}).get('name')
            logger.info(f"Task created in Frappe: {task_name}")
            return task_name
            
        except Exception as e:
            logger.error(f"Failed to create task in Frappe: {str(e)}")
            raise

    def health_check(self):
        try:
            result = self._make_request('GET', '/api/method/frappe.ping')
            return result.get('message') == 'pong'
        except Exception as e:
            logger.error(f"Frappe health check failed: {str(e)}")
            return False


def process_order_to_frappe(order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        if order.status != 'paid':
            logger.warning(f"Order {order_id} is not paid, skipping Frappe processing")
            return False
            
        frappe_service = FrappeService()
        
        sales_order_name = frappe_service.create_sales_order(order)
        
        if sales_order_name and order.service:
            project_name = frappe_service.create_project_from_order(order)
            
            default_tasks = [
                {
                    'subject': f'Initial consultation for {order.service.title}',
                    'description': 'Schedule and conduct initial consultation with client',
                    'priority': 'High'
                },
                {
                    'subject': f'Project planning for {order.service.title}',
                    'description': 'Create detailed project plan and timeline',
                    'priority': 'Medium'
                },
                {
                    'subject': f'Execute {order.service.title}',
                    'description': 'Complete the main deliverables for the service',
                    'priority': 'High'
                }
            ]
            
            for task_data in default_tasks:
                frappe_service.create_task(project_name, task_data)
        
        logger.info(f"Order {order_id} successfully processed to Frappe")
        return True
        
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to process order {order_id} to Frappe: {str(e)}")
        return False