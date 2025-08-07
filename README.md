# Social Dots Inc. - Modern Digital Marketing Agency Website

A modern, professional website for Social Dots Inc., a Toronto-based digital marketing agency specializing in strategic AI integration and Salesforce optimization for Canadian businesses. Built with Django and featuring a contemporary design system using shadcn/ui and Tailwind CSS.

## Features

### Modern Design System
- **VaynerMedia-Inspired Light Theme**: Sophisticated design with elegant rounded components
- **Unsplash Photography**: High-quality business imagery throughout the interface
- **Advanced Glassmorphism**: Professional backdrop blur effects with subtle transparency
- **Elegant Pill-Shaped Buttons**: 50px border radius with enhanced shadow effects
- **Premium Visual Components**: Gradient icons, floating animations, and sophisticated hover effects
- **Responsive Design**: Mobile-first approach with smooth transitions and micro-interactions

### Core Platform
- **Dynamic Content Management**: Full Django admin interface for managing services, blog posts, team members, and more
- **Blog System**: Full-featured blog with SEO optimization and demo content
- **Portfolio Management**: Project showcase with case studies and client testimonials
- **Lead Management**: Contact form handling with service-specific inquiries
- **Team Showcase**: Professional team member profiles with social links
- **Service Pages**: Comprehensive service offerings with pricing information

### Advanced Integrations (Optional)
- **Stripe**: Secure payment processing and subscription management
- **Frappe ERP**: Customer, sales order, and project management
- **AI Agents**: WhatsApp notifications and RAG-based chatbots
- **Google Calendar**: Appointment booking and availability checking
- **Email**: SMTP integration for notifications
- **Slack**: Real-time notifications for new leads and orders

## Project Structure

```
webapp/
├── manage.py
├── requirements.txt
├── .env.example
├── PRD.md
├── socialdots/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── admin.py           # Django admin configuration
│   ├── views.py           # View controllers
│   ├── urls.py            # URL routing
│   ├── fixtures/          # Demo content data
│   │   ├── initial_data.json
│   │   └── demo_content.json
│   ├── management/
│   │   └── commands/
│   │       ├── setup_socialdots.py   # Initial setup command
│   │       └── load_demo_content.py  # Demo content loader
│   ├── payment_service.py # Stripe integration
│   ├── frappe_services.py # Frappe ERP integration
│   ├── ai_agent_service.py # AI agent integration
│   └── calendar_service.py # Google Calendar integration
└── templates/
    ├── base.html              # Modern base template with shadcn/ui
    └── core/
        ├── home.html          # Homepage with hero and features
        ├── services.html      # Services showcase
        ├── portfolio.html     # Portfolio/projects gallery
        ├── about.html         # About page with team
        ├── contact.html       # Contact form and info
        ├── blog.html          # Blog listing page
        └── blog_detail.html   # Individual blog post
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- SQLite (default) or PostgreSQL (optional)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd webapp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration values
   ```

5. **Database setup**
   ```bash
   # Run migrations (SQLite database will be created automatically)
   python manage.py makemigrations
   python manage.py migrate
   
   # Load Social Dots initial data (team, services, site config, demo content)
   python manage.py setup_socialdots
   python manage.py load_demo_content
   ```

6. **Admin Access**
   - Default superuser created: `alishafique` / `change_me_in_production`
   - Access admin at: http://127.0.0.1:8000/admin/
   - Or create custom: `python manage.py createsuperuser`

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **View the website**
   - Homepage: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - All pages: Home, Services, Portfolio, About, Contact, Blog

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=socialdots
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Frappe ERP
FRAPPE_API_URL=https://your-frappe-instance.com
FRAPPE_API_KEY=your-api-key
FRAPPE_API_SECRET=your-api-secret

# AI Agent (n8n)
AI_AGENT_WEBHOOK_URL=https://your-n8n-instance.com/webhook
AI_AGENT_API_KEY=your-api-key

# Google Calendar
GOOGLE_CALENDAR_CLIENT_ID=your-client-id
GOOGLE_CALENDAR_CLIENT_SECRET=your-client-secret
GOOGLE_CALENDAR_REDIRECT_URI=http://localhost:8000/calendar/callback/

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
SLACK_CHANNEL=#sales-alerts
```}]}

## API Endpoints

### Public APIs
- `GET /api/services/` - List all active services
- `GET /api/pricing/` - List all pricing plans
- `POST /api/lead/` - Submit lead information

### Webhooks
- `POST /webhooks/stripe/` - Stripe payment webhooks
- `POST /webhooks/ai-agent/` - AI agent notifications

### Utility
- `GET /health/` - System health check

## Slack Integration

The application includes automatic Slack notifications for new leads and orders.

### Setup Instructions

1. **Create a Slack Channel**
   - Go to your Slack workspace
   - Create a new channel (e.g., `#sales-alerts`)
   - Invite relevant team members

2. **Create a Slack App**
   - Visit https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Choose your workspace
   - Go to "Incoming Webhooks"
   - Enable webhooks and create a new webhook URL
   - Select your channel (#sales-alerts)

3. **Configure Environment**
   - Add the webhook URL to your `.env` file:
   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
   SLACK_CHANNEL=#sales-alerts
   ```

4. **Test Integration**
   - Create a new lead via the contact form
   - Create a new order via Stripe checkout
   - Check your Slack channel for notifications

### Notification Format

**New Lead Notifications** include:
- Lead name and contact information
- Service interest and budget
- Timeline and message
- Source attribution

**New Order Notifications** include:
- Order ID and customer details
- Service and pricing plan
- Order amount and currency
- Stripe payment status

### Customization

The notification format can be customized in `core/slack_service.py`. You can modify the message templates, add custom fields, or change the notification channel based on order value or lead source.

## Recent Updates (June 2025)

### ✅ Complete E-commerce Integration
- **Full Stripe Payment System**: Secure checkout for services and pricing plans
- **Modern Pricing Page**: VaynerMedia-inspired design with interactive purchase modals
- **Canadian Currency Support**: All pricing in CAD with proper localization
- **Order Management**: Complete order tracking and payment confirmation system
- **Payment Templates**: Beautiful success/cancellation pages with professional design

### ✅ Modern Visual Design System
- **Elegant Rounded Design**: 50px pill-shaped buttons and 24px card radius throughout
- **Unsplash Photography**: High-quality images on all pages with 40-60% opacity overlays
- **Enhanced Glassmorphism**: Sophisticated backdrop blur effects with subtle transparency
- **Floating Animations**: Multi-directional animations with rotation and varied timing
- **Professional Color Palette**: Light theme with blue gradients and elegant shadows

### ✅ Advanced Template System
- **Homepage**: Hero with Unsplash backgrounds, visual showcase section, floating elements
- **Services Page**: Strategic business imagery with glassmorphism components
- **Pricing Page**: Modern card designs with Stripe integration and FAQ section
- **Portfolio Page**: Project showcase with case studies and client testimonials
- **About Page**: Team collaboration backgrounds with professional headshots
- **Contact Page**: Modern form design with business information
- **Blog System**: Content platform with search, categorization, and visual elements

### ✅ Premium Visual Components
- **Hero Visual Elements**: Large prominent images (384px height) with play button overlays
- **Visual Showcase**: Three-column image grid highlighting AI, Analytics, and Collaboration
- **Icon Containers**: 60px gradient containers with hover scale and shadow effects
- **Gradient Text**: Beautiful blue gradient headings throughout the site
- **Enhanced Shadows**: Multi-layer shadows with color tints for depth

### ✅ Complete Demo Content
- **6 Professional Services**: Strategy, Salesforce, AI, Website Development, Marketing, Automation
- **4 Pricing Plans**: Starter ($500), Professional ($1200), Enterprise ($2500), One-time ($15000)
- **3 Strategic Blog Posts**: AI integration, Salesforce optimization, marketing automation
- **4 Portfolio Projects**: Real case studies with Canadian business focus
- **6 Client Testimonials**: Authentic reviews from diverse Canadian companies

### ✅ Technical Excellence
- **Management Commands**: `setup_socialdots`, `load_demo_content`, `load_demo_pricing`
- **Stripe Configuration**: Complete payment processing with webhook support
- **Image Optimization**: Unsplash integration with responsive image loading
- **Modern CSS**: Advanced animations, glassmorphism, and sophisticated hover effects
- **Canadian Localization**: Toronto timezone, CAD currency, local business compliance

## Models Overview

### Core Business Models

#### SiteConfiguration
Global site settings including Social Dots branding, Canadian contact info, brand colors, and social media links.

#### Service
Service offerings with pricing, features, and Stripe integration.

#### PricingPlan
Structured pricing tiers with feature comparisons.

#### Project
Portfolio items showcasing completed work.

#### BlogPost
Content management with SEO optimization.

#### TeamMember
Staff profiles and contact information.

#### Lead
Prospect management and lead tracking.

#### Order
Purchase records with payment processing.

#### CalendarEvent
Appointment scheduling and management.

#### AIAgentLog
Automation activity logging.

## Django Admin

Access the admin interface at `/admin/` with your superuser credentials:
- **Username**: `alishafique`
- **Password**: `change_me_in_production`

### Key Admin Features
- **Content Management**: Blog posts, projects, testimonials, team members
- **Site Configuration**: Branding, colors, contact information, social media
- **Lead Management**: Contact form submissions and follow-up tracking
- **Service Management**: Service offerings and pricing plans
- **Demo Content**: Pre-loaded Canadian business case studies and testimonials
- **User Management**: Team access and permissions

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core

# Run specific test file
pytest core/tests/test_models.py
```

## Deployment

### Production Setup

1. **Set production environment variables**
   ```env
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   SECURE_SSL_REDIRECT=True
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn socialdots.wsgi:application
   ```

### Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "socialdots.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Monitoring

### Health Checks
- Database connectivity
- Frappe ERP integration status
- AI agent service status
- System performance metrics

### Logging
- Application logs in `logs/django.log`
- Payment processing logs
- Integration service logs
- Error tracking and notifications

## Development Guidelines

### Code Standards
- Follow Django best practices
- PEP 8 compliance
- Comprehensive documentation
- Unit test coverage

### Git Workflow
- Feature branches for new development
- Pull request reviews
- Automated testing before merge
- Semantic versioning

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running
   - Check database credentials in `.env`
   - Ensure database exists

2. **Stripe Integration Issues**
   - Verify API keys are correct
   - Check webhook endpoint configuration
   - Test with Stripe CLI

3. **External Service Failures**
   - Check service URLs and credentials
   - Review API documentation
   - Monitor service status pages

## Live Demo Content

The website includes professional demo content showcasing Social Dots' capabilities:

### Blog Posts
1. **Strategic AI Integration: A Canadian Business Perspective** - Comprehensive guide on AI adoption
2. **Salesforce Optimization: Maximizing ROI for Canadian Companies** - CRM best practices
3. **Digital Marketing Automation: A Guide for Toronto Businesses** - Local market strategies

### Portfolio Projects
1. **AI-Powered Customer Service for TechCorp Toronto** - 60% response time improvement
2. **Salesforce CRM Overhaul for MapleTech Inc.** - 65% productivity increase
3. **Marketing Automation for VancouverStart** - 300% lead increase
4. **E-commerce Platform for Ottawa Retail** - 250% sales growth

### Client Testimonials
Authentic reviews from Sarah Johnson (TechCorp), Mike Chen (MapleTech), David Lee (VancouverStart), and other Canadian business leaders.

## Support

For technical support and questions:
- Review the PRD.md for detailed specifications
- Check Django documentation
- Access admin panel for content management
- Contact development team

## License

[Your License Here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

---

**Social Dots Inc.** - Empowering Canadian businesses to thrive in a constantly evolving digital world through strategic AI integration and comprehensive digital solutions.

Built with ❤️ in Toronto using Django, shadcn/ui, and modern web technologies.