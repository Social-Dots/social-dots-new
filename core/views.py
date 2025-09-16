import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
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
# from .calendar_service import GoogleCalendarService, book_appointment

logger = logging.getLogger(__name__)


@require_GET
def robots_txt(request):
    content = render_to_string('robots.txt', {'request': request})
    return HttpResponse(content, content_type='text/plain')


def home(request):
    site_config = SiteConfiguration.objects.first()
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:3]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    featured_testimonials = Testimonial.objects.filter(is_featured=True, is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
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
        'testimonials': testimonials,
        'team_members': team_members,
        'recent_blog_posts': recent_blog_posts,
        'portfolio_categories': portfolio_categories,
        'selected_category': selected_category,
        'content_type_filter': content_type_filter,
        'portfolios': portfolios,
    }
    
    return render(request, 'core/home.html', context)


def services(request):
    """Services view displaying all active services and pricing packages"""
    services = Service.objects.filter(is_active=True).order_by('order', 'title')
    packages = Service.objects.filter(is_active=True, price_type='package').order_by('order', 'title')
    individual_services = services  # For the individual services section
    site_config = SiteConfiguration.objects.first()
    
    context = {
        'services': services,
        'packages': packages,
        'individual_services': individual_services,
        'site_config': site_config,
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
    
    # Filter by portfolio type if provided
    portfolio_type = request.GET.get('type')
    if portfolio_type and portfolio_type != 'all':
        # Check if we're using the Project model or Portfolio model
        if hasattr(Project, 'portfolio_type'):
            # If Project model has portfolio_type field, use it directly
            projects_list = projects_list.filter(portfolio_type=portfolio_type)
        else:
            # Otherwise, use the technology-based filtering as a fallback
            if portfolio_type == 'website':
                # Filter for website portfolio projects
                projects_list = projects_list.filter(technologies__overlap=['WordPress', 'HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'Django', 'Flask', 'PHP'])
            elif portfolio_type == 'ai':
                # Filter for AI automation projects
                projects_list = projects_list.filter(technologies__overlap=['AI', 'Machine Learning', 'Python', 'TensorFlow', 'PyTorch', 'NLP', 'Computer Vision', 'Data Science', 'Automation'])
            elif portfolio_type == 'social':
                # Filter for social media content projects
                projects_list = projects_list.filter(technologies__overlap=['Social Media', 'Content Creation', 'Marketing', 'Graphic Design', 'Video Editing', 'Instagram', 'Facebook', 'Twitter', 'LinkedIn'])
    
    # Pagination
    paginator = Paginator(projects_list, 12)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    # Get all unique technologies for filter
    all_technologies = set()
    for project in Project.objects.filter(status='completed'):
        all_technologies.update(project.technologies)
    
    # Get testimonials for the testimonials section
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'projects': projects,
        'all_technologies': sorted(list(all_technologies)),
        'current_tech': tech_filter,
        'current_type': portfolio_type,
        'testimonials': testimonials,
    }
    
    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'core/portfolio.html', context)
    
    return render(request, 'core/portfolio.html', context)


def project_detail(request, slug):
    # Check if this is a React app project first, before hitting the database
    if slug == 'thumb-ai':
        return render(request, 'thumb_ai_app.html')
    elif slug == 'ai-real-estate-fraud-detector':
        return render(request, 'real_estate_app.html')
    
    # Default behavior for regular project detail pages
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
    # for member in team_members:
    #     print({
    #         "id": member.id,
    #         "name": member.name,
    #         "position": member.position,
    #         "bio": member.bio,
    #         "image": member.image,
    #         "email": member.email,
    #         "phone": member.phone,
    #         "linkedin": member.linkedin,
    #        "twitter": member.twitter,
    #       "is_active": member.is_active,
    #         "order": member.order,
    #      "created_at": member.created_at,
    #       "updated_at": member.updated_at,
    #     })
    
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

@csrf_exempt
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
            'notes': f'Cart order with {len(cart_items)} items',
            'service_name': 'Custom Service',
            'pricing_plan_name': 'Custom Plan'
        }
        
        # Extract service and pricing plan names from cart items if available
        if cart_items and len(cart_items) > 0:
            first_item = cart_items[0]
            if 'name' in first_item:
                item_name = first_item.get('name', '')
                if ' - ' in item_name:
                    service_part, plan_part = item_name.split(' - ', 1)
                    order_data['service_name'] = service_part
                    order_data['pricing_plan_name'] = plan_part
                else:
                    order_data['service_name'] = item_name
        
        # Add more details to notes
        order_data['notes'] = f'Cart order with {len(cart_items)} items | Service: {order_data["service_name"]} | Plan: {order_data["pricing_plan_name"]}'

        
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
        
        try:
            session = stripe_service.create_checkout_session(session_data, request)
            
            order.stripe_session_id = session.id
            order.save()
            
            return JsonResponse({
                'checkout_url': session.url,
                'session_id': session.id
            })
        except ValueError as e:
            # Configuration error (missing API keys)
            logger.error(f"Stripe configuration error: {e}")
            return JsonResponse({
                'error': 'Payment system is not properly configured. Please contact support.',
                'details': str(e)
            }, status=500)
        except AttributeError as e:
            # Stripe module error
            logger.error(f"Stripe module error: {e}")
            return JsonResponse({
                'error': 'Payment system is currently unavailable. Please try again later or contact support.',
                'details': str(e)
            }, status=500)
        
    except json.JSONDecodeError:
        logger.error("Invalid cart data format")
        return JsonResponse({'error': 'Invalid cart data format'}, status=400)
    except Exception as e:
        logger.error(f"Checkout error: {e}")
        return JsonResponse({'error': 'Failed to create checkout session', 'details': str(e)}, status=500)


def payment_success(request):
    session_id = request.GET.get('session_id')
    # return render(request, 'core/payment_success.html')
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
        
        # Get content counts
        blog_count = BlogPost.objects.count()
        project_count = Project.objects.count()
        portfolio_count = Portfolio.objects.count()
        service_count = Service.objects.count()
        
        # Check external services
        health_status = {
            'database': 'healthy',
            'content': {
                'blogs': blog_count,
                'projects': project_count,
                'portfolio': portfolio_count,
                'services': service_count,
                'has_content': blog_count > 0 or project_count > 0 or portfolio_count > 0
            },
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

@require_http_methods(["GET"])
def api_portfolio(request):
    category_filter = request.GET.get('category')
    content_type_filter = request.GET.get('content_type')
    
    # Initialize the queryset
    portfolios = Portfolio.objects.filter(is_active=True)
    
    # Apply filters if provided
    if category_filter:
        portfolios = portfolios.filter(category__slug=category_filter)
    
    if content_type_filter:
        portfolios = portfolios.filter(content_type=content_type_filter)
    
    # Prepare the portfolio data
    portfolio_data = []
    for p in portfolios:
        item = {
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'description': p.description,
            'category': {
                'id': p.category.id,
                'name': p.category.name,
                'slug': p.category.slug
            },
            'content_type': p.content_type,
            'video_url': p.video_url,
            'blog_link': p.blog_link,
            'technology_used': p.technology_used,
            'is_featured': p.is_featured,
            'created_at': p.created_at.isoformat() if p.created_at else None,
        }
        
        # Use Cloudinary URL if available, otherwise fall back to regular image URL
        if p.cloudinary_image_id:
            item['image'] = p.get_cloudinary_url()
        elif p.image:
            item['image'] = p.image.url
        else:
            item['image'] = None
        
        portfolio_data.append(item)
    
    return JsonResponse({'portfolios': portfolio_data})

def portfolio_detail(request, slug):
    try:
        portfolio = Portfolio.objects.get(slug=slug, is_active=True)
        
        # Get related portfolios from the same category
        related_portfolios = Portfolio.objects.filter(
            category=portfolio.category, 
            is_active=True
        ).exclude(id=portfolio.id)[:3]
        
        # Prepare portfolio data with Cloudinary URL if available
        portfolio_data = {
            'id': portfolio.id,
            'title': portfolio.title,
            'slug': portfolio.slug,
            'description': portfolio.description,
            'category': {
                'id': portfolio.category.id,
                'name': portfolio.category.name,
                'slug': portfolio.category.slug
            },
            'content_type': portfolio.content_type,
            'video_url': portfolio.video_url,
            'blog_link': portfolio.blog_link,
            'technology_used': portfolio.technology_used,
            'created_at': portfolio.created_at,
        }
        
        # Use Cloudinary URL if available, otherwise fall back to regular image URL
        if portfolio.cloudinary_image_id:
            portfolio_data['image'] = portfolio.get_cloudinary_url()
            # Add a transformed version for thumbnails
            portfolio_data['thumbnail'] = portfolio.get_cloudinary_url(width=400, height=300, crop='fill')
        elif portfolio.image:
            portfolio_data['image'] = portfolio.image.url
            portfolio_data['thumbnail'] = portfolio.image.url
        else:
            portfolio_data['image'] = None
            portfolio_data['thumbnail'] = None
        
        context = {
            'portfolio': portfolio_data,
            'related_portfolios': related_portfolios,
            'meta_title': f"{portfolio.title} | Portfolio | Social Dots",
            'meta_description': portfolio.description[:160] if portfolio.description else None,
        }
        
        return render(request, 'core/portfolio_detail.html', context)
        
    except Portfolio.DoesNotExist:
        raise Http404("Portfolio not found")


def portfolio_detail_api(request, portfolio_id):
    """API endpoint to get portfolio details by ID for the modal"""
    print(f"\n\nPortfolio detail API called with ID: {portfolio_id}\n\n")
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id, is_active=True)
        
        # Prepare portfolio data with Cloudinary URL if available
        portfolio_data = {
            'id': portfolio.id,
            'title': portfolio.title,
            'slug': portfolio.slug,
            'description': portfolio.description,
            'category': {
                'id': portfolio.category.id,
                'name': portfolio.category.name,
                'slug': portfolio.category.slug
            },
            'content_type': portfolio.content_type,
            'video_url': portfolio.video_url,
            'blog_link': portfolio.blog_link,
            'technology_used': portfolio.technology_used,
            'created_at': portfolio.created_at.isoformat() if portfolio.created_at else None,
        }
        
        # Use Cloudinary URL if available, otherwise fall back to regular image URL
        if portfolio.cloudinary_image_id:
            portfolio_data['image'] = portfolio.get_cloudinary_url()
            # Add a transformed version for thumbnails
            portfolio_data['thumbnail'] = portfolio.get_cloudinary_url(width=400, height=300, crop='fill')
        elif portfolio.image:
            portfolio_data['image'] = portfolio.image.url
            portfolio_data['thumbnail'] = portfolio.image.url
        else:
            portfolio_data['image'] = None
            portfolio_data['thumbnail'] = None
        
        # Add bio field if available
        if portfolio.bio:
            portfolio_data['content'] = portfolio.bio
        
        return JsonResponse(portfolio_data)
        
    except Portfolio.DoesNotExist:
        return JsonResponse({"error": "Portfolio not found"}, status=404)


@require_http_methods(["GET", "POST"])
def setup_database(request):
    """Trigger database setup with content loading"""
    
    # Handle GET request with a simple interface
    if request.method == 'GET':
        return HttpResponse('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Database Setup - Social Dots</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .button { background: #2563EB; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
                .button:hover { background: #1E40AF; }
                .info { background: #f0f9ff; padding: 20px; border-radius: 5px; margin: 20px 0; }
                .warning { background: #fef3cd; padding: 20px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <h1>🔧 Database Setup - Social Dots Inc.</h1>
            <div class="info">
                <h3>This tool will:</h3>
                <ul>
                    <li>Load your actual localhost content and branding</li>
                    <li>Set up Social Dots Inc. site configuration</li>
                    <li>Import your blog posts, projects, and team data</li>
                    <li>Ensure the site matches your localhost development</li>
                </ul>
            </div>
            <div class="warning">
                <strong>⚠️ Note:</strong> This will replace any existing content with your localhost data.
            </div>
            
            <button class="button" onclick="setupDatabase()">🚀 Setup Database Now</button>
            
            <div id="results" style="margin-top: 20px; display: none;">
                <h3>Results:</h3>
                <pre id="output" style="background: #f5f5f5; padding: 15px; border-radius: 5px;"></pre>
            </div>
            
            <script>
                async function setupDatabase() {
                    document.getElementById('results').style.display = 'block';
                    document.getElementById('output').textContent = 'Setting up database...';
                    
                    try {
                        const response = await fetch('/setup-database/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        });
                        
                        const data = await response.json();
                        document.getElementById('output').textContent = JSON.stringify(data, null, 2);
                    } catch (error) {
                        document.getElementById('output').textContent = 'Error: ' + error.message;
                    }
                }
                
                function getCookie(name) {
                    let cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        const cookies = document.cookie.split(';');
                        for (let i = 0; i < cookies.length; i++) {
                            const cookie = cookies[i].trim();
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
            </script>
        </body>
        </html>
        ''')
    
    # Handle POST request with actual database setup
    try:
        from django.core.management import call_command
        
        results = {
            'status': 'success',
            'operations': [],
            'timestamp': timezone.now().isoformat()
        }
        
        # Check current content counts
        initial_blogs = BlogPost.objects.count()
        initial_projects = Project.objects.count() 
        initial_portfolio = Portfolio.objects.count()
        
        results['initial_counts'] = {
            'blogs': initial_blogs,
            'projects': initial_projects,
            'portfolio': initial_portfolio
        }
        
        # Run migrations
        call_command('migrate', verbosity=1)
        results['operations'].append('migrations_complete')
        
        # Setup initial data if needed
        try:
            site_config = SiteConfiguration.objects.first()
            if not site_config:
                call_command('setup_socialdots', verbosity=1)
                results['operations'].append('site_configuration_created')
        except Exception as e:
            results['operations'].append(f'site_config_error: {str(e)}')
        
        # Deploy complete localhost regardless of existing content
        try:
            call_command('deploy_complete_localhost', verbosity=1)
            results['operations'].append('complete_localhost_deployed')
        except Exception as e:
            results['operations'].append(f'complete_deployment_error: {str(e)}')
            
            # Try fresh data as backup
            try:
                from pathlib import Path
                fresh_data_file = Path(__file__).resolve().parent.parent / 'fresh_localhost_data.json'
                if fresh_data_file.exists():
                    call_command('loaddata', str(fresh_data_file), verbosity=1)
                    results['operations'].append('fresh_localhost_data_loaded')
                else:
                    raise Exception("Fresh localhost data file not found")
            except Exception as e2:
                results['operations'].append(f'fresh_data_error: {str(e2)}')
                
                # Final fallback to demo content
                try:
                    call_command('load_demo_content', verbosity=1)
                    results['operations'].append('demo_content_loaded')
                except Exception as e3:
                    results['operations'].append(f'demo_content_error: {str(e3)}')
                
                try:
                    call_command('load_demo_pricing', verbosity=1)
                    results['operations'].append('demo_pricing_loaded')
                except Exception as e4:
                    results['operations'].append(f'demo_pricing_error: {str(e4)}')
        
        # Final content counts
        final_blogs = BlogPost.objects.count()
        final_projects = Project.objects.count()
        final_portfolio = Portfolio.objects.count()
        
        results['final_counts'] = {
            'blogs': final_blogs,
            'projects': final_projects,
            'portfolio': final_portfolio
        }
        
        results['content_added'] = {
            'blogs': final_blogs - initial_blogs,
            'projects': final_projects - initial_projects,
            'portfolio': final_portfolio - initial_portfolio
        }
        
        return JsonResponse(results)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)

# ThumbAI React App View
def thumb_ai(request, path=''):
    """Serve the ThumbAI React application"""
    import os
    from django.conf import settings
    from django.http import FileResponse, HttpResponse
    from django.shortcuts import redirect
    
    # In development, redirect directly to Vite dev server
    if settings.DEBUG and os.environ.get('DJANGO_ENV') != 'production':
        vite_dev_url = f'http://localhost:5178/portfolio/thumbai/'
        if path:
            vite_dev_url += path
        return redirect(vite_dev_url)
    
    # Production: Serve built files
    # Path to the React app's build files
    static_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'portfolio', 'thumbai')
    
    if path and path != '/':
        # Serve specific files (CSS, JS, etc.)
        file_path = os.path.join(static_path, path)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'))
    
    # Serve the index.html for all routes (SPA routing)
    index_path = os.path.join(static_path, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    
    # Fallback if files not found
    raise Http404("ThumbAI app not found")


def thumb_ai_login(request):
    """Handle Base44 authentication for ThumbAI"""
    from django.shortcuts import redirect
    from urllib.parse import urlparse, parse_qs
    
    # Get the from_url parameter to redirect back after login
    from_url = request.GET.get('from_url', '/portfolio/thumbai/')
    
    # Check if we're in development (localhost/127.0.0.1)
    parsed_url = urlparse(from_url)
    is_development = parsed_url.hostname in ['localhost', '127.0.0.1']
    
    if is_development:
        # For development, create a mock authentication token and redirect back
        # This simulates what Base44 would do after successful authentication
        mock_token = "dev_mock_token_12345"
        
        # Add the mock token as a URL parameter (Base44 typically adds this)
        separator = '&' if '?' in from_url else '?'
        redirect_url = f"{from_url}{separator}access_token={mock_token}"
        
        return redirect(redirect_url)
    else:
        # For production, redirect to the actual Base44 login page
        base44_login_url = f"https://base44.app/login?next={from_url}&app_id=6883d8876847402fc656950d"
        return redirect(base44_login_url)


@require_GET
def favicon_view(request):
    """Serve favicon.ico from static files"""
    from django.conf import settings
    from django.contrib.staticfiles import finders
    import os

    # Find favicon in static files
    favicon_path = finders.find('images/favicon.ico')
    if favicon_path and os.path.exists(favicon_path):
        with open(favicon_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/x-icon')

    # Return 404 if favicon not found
    raise Http404("Favicon not found")