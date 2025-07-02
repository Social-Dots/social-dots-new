import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    SiteConfiguration, Service, PricingPlan, Project, BlogPost, 
    Testimonial, TeamMember, Lead, Order, CalendarEvent, ServicePricingOption,
    Portfolio, PortfolioCategory
)
from .payment_service import StripePaymentService
from .frappe_services import process_order_to_frappe
from .ai_agent_service import AIAgentService
from .calendar_service import GoogleCalendarService, book_appointment

logger = logging.getLogger(__name__)


def home(request):
    site_config = SiteConfiguration.objects.first()
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:3]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    featured_testimonials = Testimonial.objects.filter(is_featured=True, is_active=True)[:3]
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    recent_blog_posts = BlogPost.objects.filter(status='published')[:3]
    
    # Get portfolio categories and items
    portfolio_categories = PortfolioCategory.objects.filter(is_active=True)
    
    # Get selected category or content type filter
    category_filter = request.GET.get('category')
    selected_category = None
    content_type_filter = None
    
    # Check if it's a special content type filter
    if category_filter in ['posts', 'videos', 'blogs', 'emails', 'featured']:
        if category_filter == 'featured':
            # Featured is a special case - we'll show featured items
            pass
        else:
            content_type_filter = category_filter
            if content_type_filter == 'posts':
                content_type_filter = 'post'
            elif content_type_filter == 'blogs':
                content_type_filter = 'blog'
            elif content_type_filter == 'videos':
                content_type_filter = 'video'
            elif content_type_filter == 'emails':
                content_type_filter = 'email'
    elif category_filter:
        # Try to get the category by slug
        try:
            selected_category = PortfolioCategory.objects.get(slug=category_filter)
        except PortfolioCategory.DoesNotExist:
            selected_category = portfolio_categories.first() if portfolio_categories.exists() else None
    else:
        # Default view - show featured items
        pass
    
    # Get portfolios based on selected filter
    if content_type_filter:
        portfolios = Portfolio.objects.filter(content_type=content_type_filter, is_active=True)
    elif selected_category:
        portfolios = Portfolio.objects.filter(category=selected_category, is_active=True)
    elif category_filter == 'featured' or not category_filter:
        # Show featured items for both explicit 'featured' filter and default view
        portfolios = Portfolio.objects.filter(is_active=True, is_featured=True)[:6]
    
    context = {
        'site_config': site_config,
        'featured_services': featured_services,
        'featured_projects': featured_projects,
        'featured_testimonials': featured_testimonials,
        'team_members': team_members,
        'recent_blog_posts': recent_blog_posts,
        'portfolio_categories': portfolio_categories,
        'selected_category': selected_category,
        'content_type_filter': content_type_filter,
        'portfolios': portfolios,
    }
    
    return render(request, 'core/home.html', context)


def services(request):
    # Only get services and their pricing options
    services_list = Service.objects.filter(is_active=True).prefetch_related('pricing_options')
    
    # Add pricing options for each service
    for service in services_list:
        # Get pricing options from ServicePricingOption model
        db_pricing_options = service.pricing_options.all().order_by('order', 'price')
        
        if db_pricing_options.exists():
            # Use database pricing options
            service.pricing_options_list = db_pricing_options
            print(f"Service '{service.title}': Found {db_pricing_options.count()} pricing options")
        else:
            # Only use fallback if no database options exist
            base_price = service.price or Decimal('100.00')
            service.pricing_options_list = [
                {
                    'name': 'Standard', 
                    'price': base_price, 
                    'period': 'one_time',
                    'description': 'Basic package'
                },
                {
                    'name': 'Premium', 
                    'price': base_price + Decimal('30.00'), 
                    'period': 'one_time',
                    'description': 'Enhanced package'
                },
                {
                    'name': 'Enterprise', 
                    'price': base_price + Decimal('60.00'), 
                    'period': 'one_time',
                    'description': 'Full-featured package'
                }
            ]
            print(f"Service '{service.title}': Using fallback pricing options")
    
    context = {
        'services_list': services_list,
    }
    
    return render(request, 'core/services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(is_active=True).exclude(id=service.id)[:3]
    
    # Prefetch pricing options if this is a tiered pricing service
    if service.price_type == 'tiered':
        pricing_options = service.pricing_options.all().order_by('order', 'price')
    else:
        pricing_options = None
    
    context = {
        'service': service,
        'related_services': related_services,
        'pricing_options': pricing_options,
    }
    
    return render(request, 'core/service_details.html', context)


def portfolio(request):
    projects_list = Project.objects.filter(status='completed')
    
    # Filter by technology if provided
    tech_filter = request.GET.get('tech')
    if tech_filter:
        projects_list = projects_list.filter(technologies__contains=[tech_filter])
    
    # Pagination
    paginator = Paginator(projects_list, 12)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    # Get all unique technologies for filter
    all_technologies = set()
    for project in Project.objects.filter(status='completed'):
        all_technologies.update(project.technologies)
    
    context = {
        'projects': projects,
        'all_technologies': sorted(list(all_technologies)),
        'current_tech': tech_filter,
    }
    
    return render(request, 'core/portfolio.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(status='completed').exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'core/project_detail.html', context)


def blog(request):
    blog_posts = BlogPost.objects.filter(status='published')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        blog_posts = blog_posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__contains=[search_query])
        )
    
    # Pagination
    paginator = Paginator(blog_posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    # Get all unique tags
    all_tags = set()
    for post in BlogPost.objects.filter(status='published'):
        all_tags.update(post.tags)
    
    context = {
        'posts': posts,
        'all_tags': sorted(list(all_tags)),
        'search_query': search_query,
    }
    
    return render(request, 'core/blog.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    related_posts = BlogPost.objects.filter(status='published').exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'core/blog_detail.html', context)


def about(request):
    team_members = TeamMember.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'team_members': team_members,
        'testimonials': testimonials,
    }
    
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        try:
            lead_data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone', ''),
                'company': request.POST.get('company', ''),
                'message': request.POST.get('message', ''),
                'source': 'contact_form'
            }
            
            service_id = request.POST.get('service_interest')
            if service_id:
                try:
                    service = Service.objects.get(id=service_id)
                    lead_data['service_interest'] = service
                except Service.DoesNotExist:
                    pass
            
            lead = Lead.objects.create(**lead_data)
            
            # Notify AI agent about new lead
            try:
                ai_agent = AIAgentService()
                ai_agent.notify_new_lead(lead)
            except Exception as e:
                logger.error(f"Failed to notify AI agent about new lead: {e}")
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
            
        except Exception as e:
            logger.error(f"Error processing contact form: {e}")
            messages.error(request, 'There was an error sending your message. Please try again.')
    
    services_list = Service.objects.filter(is_active=True)
    
    context = {
        'services': services_list,
    }
    
    return render(request, 'core/contact.html', context)

def cart(request):
    """View for the shopping cart page"""
    return render(request, 'core/cart.html')


@require_http_methods(["POST"])
def checkout(request):
    try:
        # Get form data
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone', '')
        cart_items = request.POST.get('cart_items')
        
        if not customer_name or not customer_email:
            return JsonResponse({'error': 'Name and email are required'}, status=400)
        
        if not cart_items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
            
        import json
        cart_items = json.loads(cart_items)
        
        if not cart_items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Calculate total amount
        total_amount = 0
        for item in cart_items:
            total_amount += float(item.get('price', 0)) * int(item.get('quantity', 1))
            # Add maintenance fees if applicable
            if item.get('maintenance'):
                total_amount += float(item.get('maintenance', 0)) * int(item.get('quantity', 1))
        
        # Create order
        order_data = {
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'amount': total_amount,
            'notes': f'Cart order with {len(cart_items)} items'
        }
        
        order = Order.objects.create(**order_data)
        
        # Create Stripe checkout session
        stripe_service = StripePaymentService()
        session_data = {
            'order_id': order.order_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'cart_items': cart_items
        }
        
        session = stripe_service.create_checkout_session(session_data, request)
        
        order.stripe_session_id = session.id
        order.save()
        
        return JsonResponse({
            'checkout_url': session.url,
            'session_id': session.id
        })
        
    except Exception as e:
        logger.error(f"Checkout error: {e}")
        return JsonResponse({'error': 'Failed to create checkout session'}, status=500)


def payment_success(request):
    session_id = request.GET.get('session_id')
    
    if not session_id:
        messages.error(request, 'Invalid payment session')
        return redirect('home')
    
    try:
        stripe_service = StripePaymentService()
        session = stripe_service.retrieve_session(session_id)
        order = stripe_service.handle_successful_payment(session)
        
        if order:
            # Process order to Frappe
            try:
                process_order_to_frappe(order.order_id)
            except Exception as e:
                logger.error(f"Failed to process order to Frappe: {e}")
            
            # Notify AI agent
            try:
                ai_agent = AIAgentService()
                ai_agent.notify_payment_success(order)
            except Exception as e:
                logger.error(f"Failed to notify AI agent about payment: {e}")
            
            context = {
                'order': order,
                'session': session
            }
            return render(request, 'core/payment_success.html', context)
        else:
            messages.error(request, 'Payment processed but order not found')
            return redirect('home')
            
    except Exception as e:
        logger.error(f"Payment success error: {e}")
        messages.error(request, 'Error processing payment confirmation')
        return redirect('home')


def payment_cancelled(request):
    messages.info(request, 'Payment was cancelled')
    return render(request, 'core/payment_cancelled.html')


@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    stripe_service = StripePaymentService()
    success = stripe_service.handle_webhook(payload, sig_header)
    
    if success:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
@require_http_methods(["POST"])
def ai_agent_webhook(request):
    try:
        data = json.loads(request.body)
        webhook_type = data.get('type')
        
        ai_agent = AIAgentService()
        result = ai_agent.process_webhook_data(webhook_type, data)
        
        return JsonResponse({'status': 'success', 'result': result})
        
    except Exception as e:
        logger.error(f"AI agent webhook error: {e}")
        return JsonResponse({'error': 'Webhook processing failed'}, status=500)


@require_http_methods(["GET"])
def api_services(request):
    services_list = Service.objects.filter(is_active=True).values(
        'id', 'title', 'description', 'price', 'price_type', 'features'
    )
    return JsonResponse({'services': list(services_list)})


@require_http_methods(["GET"])
def api_pricing(request):
    pricing_plans = PricingPlan.objects.filter(is_active=True).values(
        'id', 'name', 'description', 'price', 'price_period', 'features'
    )
    return JsonResponse({'pricing_plans': list(pricing_plans)})

@api_view(['GET'])
def api_pricing_option(request, option_id):
    try:
        option = ServicePricingOption.objects.get(id=option_id)
        return Response({
            'id': option.id,
            'name': option.name,
            'price': option.price,
            'period': option.period,
            'features': option.features
        })
    except ServicePricingOption.DoesNotExist:
        return Response({'error': 'Pricing option not found'}, status=404)


@require_http_methods(["POST"])
def api_lead(request):
    try:
        data = json.loads(request.body)
        
        lead_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'company': data.get('company', ''),
            'message': data.get('message', ''),
            'source': data.get('source', 'api')
        }
        
        service_id = data.get('service_id')
        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                lead_data['service_interest'] = service
            except Service.DoesNotExist:
                pass
        
        lead = Lead.objects.create(**lead_data)
        
        return JsonResponse({
            'status': 'success',
            'lead_id': lead.id,
            'message': 'Lead created successfully'
        })
        
    except Exception as e:
        logger.error(f"API lead creation error: {e}")
        return JsonResponse({'error': 'Failed to create lead'}, status=500)


def calendar_auth(request):
    calendar_service = GoogleCalendarService()
    auth_url, state = calendar_service.get_authorization_url()
    
    request.session['calendar_state'] = state
    return redirect(auth_url)


def calendar_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    session_state = request.session.get('calendar_state')
    
    if not code or state != session_state:
        messages.error(request, 'Invalid calendar authorization')
        return redirect('contact')
    
    try:
        calendar_service = GoogleCalendarService()
        credentials = calendar_service.exchange_code_for_tokens(code, state)
        
        request.session['calendar_credentials'] = credentials
        messages.success(request, 'Calendar authorized successfully!')
        
        return redirect('book_appointment')
        
    except Exception as e:
        logger.error(f"Calendar callback error: {e}")
        messages.error(request, 'Failed to authorize calendar access')
        return redirect('contact')


def book_appointment_view(request):
    if request.method == 'POST':
        try:
            credentials = request.session.get('calendar_credentials')
            if not credentials:
                return redirect('calendar_auth')
            
            appointment_data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone', ''),
                'service': request.POST.get('service', ''),
                'message': request.POST.get('message', ''),
                'start_time': datetime.fromisoformat(request.POST.get('start_time')),
                'end_time': datetime.fromisoformat(request.POST.get('end_time'))
            }
            
            calendar_event = book_appointment(appointment_data, credentials)
            
            messages.success(request, f'Appointment booked successfully! Event ID: {calendar_event.google_event_id}')
            return redirect('contact')
            
        except Exception as e:
            logger.error(f"Appointment booking error: {e}")
            messages.error(request, 'Failed to book appointment')
    
    services_list = Service.objects.filter(is_active=True)
    
    context = {
        'services': services_list,
    }
    
    return render(request, 'core/book_appointment.html', context)


@require_http_methods(["GET"])
def health_check(request):
    try:
        # Check database connection
        SiteConfiguration.objects.exists()
        
        # Check external services
        health_status = {
            'database': 'healthy',
            'frappe': 'unknown',
            'ai_agent': 'unknown',
            'timestamp': timezone.now().isoformat()
        }
        
        # Check Frappe connection
        try:
            from .frappe_services import FrappeService
            frappe_service = FrappeService()
            if frappe_service.health_check():
                health_status['frappe'] = 'healthy'
            else:
                health_status['frappe'] = 'unhealthy'
        except Exception:
            health_status['frappe'] = 'error'
        
        # Check AI Agent connection
        try:
            ai_agent = AIAgentService()
            if ai_agent.health_check():
                health_status['ai_agent'] = 'healthy'
            else:
                health_status['ai_agent'] = 'unhealthy'
        except Exception:
            health_status['ai_agent'] = 'error'
        
        return JsonResponse(health_status)
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JsonResponse({
            'database': 'error',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)