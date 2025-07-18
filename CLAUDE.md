# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based digital marketing agency website for Social Dots Inc., a Toronto-based company specializing in AI integration and Salesforce optimization for Canadian businesses. The platform features a modern design system with e-commerce capabilities, content management, and external service integrations.

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env  # Edit with your configuration
```

### Database Operations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Load initial data
python manage.py setup_socialdots
python manage.py load_demo_content
python manage.py load_demo_pricing

# Create superuser (optional - setup_socialdots creates one)
python manage.py createsuperuser
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Access points:
# - Homepage: http://127.0.0.1:8000/
# - Admin: http://127.0.0.1:8000/admin/
# - Default admin: alishafique / change_me_in_production
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core

# Run specific test file
pytest core/tests/test_models.py
```

## Architecture Overview

### Core Application Structure
The project follows Django's MVT (Model-View-Template) pattern with a single `core` app containing all business logic:

- **Models** (`core/models.py`): 13 main models including SiteConfiguration, Service, Project, BlogPost, Portfolio, Order, Lead, etc.
- **Views** (`core/views.py`): Class-based and function-based views handling all pages and API endpoints
- **Templates** (`templates/`): Jinja2 templates with modern design system using shadcn/ui and Tailwind CSS
- **Static Files** (`static/`): CSS, JS, and images with automated compression

### Key Models and Relationships

#### Business Configuration
- `SiteConfiguration`: Singleton model for site-wide settings (colors, contact info, branding)
- `TeamMember`: Staff profiles with social links and ordering
- `Service`: Service offerings with pricing options and Stripe integration
- `PricingPlan`: Structured pricing tiers with features comparison

#### Content Management
- `BlogPost`: Full-featured blog with SEO, tags, and rich text editing
- `Project`: Portfolio items with case studies and technology tracking
- `Portfolio`: Social media content with category organization and Cloudinary integration
- `Testimonial`: Client reviews with ratings and featured status

#### E-commerce & CRM
- `Order`: Purchase records with Stripe payment processing
- `Lead`: Contact form submissions and lead management
- `CalendarEvent`: Appointment scheduling with Google Calendar integration

### External Service Integrations

#### Payment Processing
- **Stripe**: Full e-commerce integration with checkout sessions, webhooks, and subscription management
- Key files: `core/payment_service.py`, webhooks at `/webhooks/stripe/`

#### Cloud Storage
- **Cloudinary**: Image optimization and delivery
- Integration: `core/cloudinary_utils.py`, automatic upload on model save

#### Business Systems
- **Frappe ERP**: Optional integration for customer and order management
- **Google Calendar**: Appointment booking and availability checking
- **AI Agent Services**: WhatsApp notifications and RAG-based chatbots

### Canadian Business Focus
- **Localization**: Toronto timezone, CAD currency, Canadian business compliance
- **Content**: Demo content focuses on Canadian companies and use cases
- **Pricing**: All pricing displayed in CAD with Canadian tax considerations

## Development Guidelines

### Model Modifications
- Use Django migrations for all database changes: `python manage.py makemigrations`
- Business logic validation should be in model `clean()` methods
- Use JSONField for flexible data storage (features, tags, etc.)
- Implement `__str__()` methods for admin readability

### View Development
- Follow RESTful conventions for API endpoints (`/api/`)
- Use Django's built-in pagination for list views
- Implement proper error handling with logging
- Return JSON responses for AJAX requests

### Template Updates
- Base template: `templates/base.html` with shadcn/ui components
- Maintain responsive design with Tailwind CSS
- Use Django's template inheritance system
- Implement proper SEO meta tags

### Static File Management
- CSS: Custom animations in `static/css/portfolio-animations.css`
- JavaScript: Portfolio interactions in `static/js/portfolio-animations.js`
- Images: Use Cloudinary for user uploads, local storage for static assets

### Security Considerations
- Never commit sensitive data (API keys, passwords)
- Use environment variables for all configuration
- Implement proper CSRF protection
- Validate all user inputs in forms and APIs

## Common Development Tasks

### Adding New Services
1. Create service in admin or via management command
2. Add pricing options through ServicePricingOption model
3. Create service detail template if needed
4. Configure Stripe pricing if e-commerce enabled

### Managing Portfolio Content
1. Use Portfolio model for social media content
2. Upload images through Cloudinary integration
3. Organize content with PortfolioCategory
4. Use content_type field for filtering (post, video, blog, etc.)

### Payment Integration
1. Configure Stripe keys in environment variables
2. Test webhooks with Stripe CLI: `stripe listen --forward-to localhost:8000/webhooks/stripe/`
3. Orders automatically sync with Frappe ERP if configured

### Content Management
1. Use Django admin for content management
2. Blog posts support rich text with CKEditor
3. SEO fields available for meta descriptions and keywords
4. Image optimization handled automatically via Cloudinary

## Production Deployment

### Environment Variables
Required environment variables for production:
- `SECRET_KEY`: Django secret key
- `DEBUG=False`: Disable debug mode
- `DATABASE_URL`: PostgreSQL connection string
- `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`: Payment processing
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: Image storage

### Deployment Steps
1. Set `DEBUG=False` in settings
2. Configure `ALLOWED_HOSTS` with your domain
3. Run `python manage.py collectstatic`
4. Configure Gunicorn or similar WSGI server
5. Set up SSL certificate and security headers
6. Configure database backups and monitoring

### Vercel Deployment
The project includes `vercel.json` for Vercel deployment:
- Python 3.9 runtime configured
- Static files served via WhiteNoise
- Database should be PostgreSQL (configured via DATABASE_URL)

## Management Commands

### Initial Setup
- `python manage.py setup_socialdots`: Creates superuser, site config, and core services
- `python manage.py load_demo_content`: Loads blog posts, projects, and testimonials
- `python manage.py load_demo_pricing`: Loads pricing plans and service options

### Development Utilities
- `python manage.py shell`: Django shell with models imported
- `python manage.py dbshell`: Direct database access
- `python manage.py runserver 0.0.0.0:8000`: Allow external connections

## API Endpoints

### Public APIs
- `GET /api/services/`: List all active services
- `GET /api/pricing/`: List all pricing plans
- `GET /api/portfolio/`: Portfolio items with filtering
- `POST /api/lead/`: Submit lead information

### Webhook Endpoints
- `POST /webhooks/stripe/`: Stripe payment notifications
- `POST /webhooks/ai-agent/`: AI agent notifications

### Health Check
- `GET /health/`: System health status including database and external services

## Troubleshooting

### Common Issues
1. **Database connection errors**: Check DATABASE_URL and PostgreSQL service
2. **Static files not loading**: Run `python manage.py collectstatic`
3. **Payment issues**: Verify Stripe keys and webhook endpoints
4. **Image upload failures**: Check Cloudinary configuration
5. **Admin access**: Default credentials are `alishafique` / `change_me_in_production`

### Debug Mode
- Set `DEBUG=True` in settings for development
- Use Django Debug Toolbar for SQL query analysis
- Check Django logs for error details

### Performance Optimization
- Use `select_related()` and `prefetch_related()` for database queries
- Implement caching for frequently accessed data
- Optimize images through Cloudinary transformations
- Use database indexes for frequently queried fields