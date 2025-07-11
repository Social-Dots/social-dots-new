from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # Admin portfolio management
    path('admin/portfolio/', admin_views.portfolio_list, name='admin_portfolio_list'),
    path('admin/portfolio/create/', admin_views.portfolio_create, name='admin_portfolio_create'),
    path('admin/portfolio/<int:pk>/edit/', admin_views.portfolio_edit, name='admin_portfolio_edit'),
    path('admin/portfolio/<int:pk>/delete/', admin_views.portfolio_delete, name='admin_portfolio_delete'),
    path('admin/portfolio/category/create/', admin_views.portfolio_category_create, name='admin_portfolio_category_create'),
    # Main website pages
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    
    # Payment endpoints
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
    
    # AI Agent webhooks
    path('webhooks/ai-agent/', views.ai_agent_webhook, name='ai_agent_webhook'),
    
    # API endpoints
    path('api/services/', views.api_services, name='api_services'),
    path('api/pricing/', views.api_pricing, name='api_pricing'),
    path('api/pricing-option/<int:option_id>/', views.api_pricing_option, name='api_pricing_option'),
    path('api/portfolio/', views.api_portfolio, name='api_portfolio'),
    path('api/lead/', views.api_lead, name='api_lead'),
    
    # Calendar functionality
    path('calendar/auth/', views.calendar_auth, name='calendar_auth'),
    path('calendar/callback/', views.calendar_callback, name='calendar_callback'),
    path('book-appointment/', views.book_appointment_view, name='book_appointment'),
    
    # Health check
    path('health/', views.health_check, name='health_check'),
]