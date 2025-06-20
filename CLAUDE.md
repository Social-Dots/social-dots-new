# Social Dots Inc. - Claude Code Memory File

## Project Overview
This is a Django-based digital services platform for Social Dots Inc., a Canadian digital marketing company founded by Ali Shafique. The platform integrates with Stripe, Frappe ERP, AI agents (n8n), and Google Calendar.

## Recent Improvements Completed (2025-06-19)

### ✅ High Priority Tasks Completed
1. **Updated SiteConfiguration Model** - Added Social Dots brand identity including:
   - Brand colors (#2563EB primary, #1E40AF secondary, #3B82F6 accent)
   - Contact information (416-556-6961, ali@socialdots.ca, hello@socialdots.ca)
   - Toronto, Ontario, Canada address
   - Logo/favicon fields including dark version
   - SEO meta description with Canadian focus
   - Business validation rules

2. **Team Members Integration** - Created fixtures for:
   - Ali Shafique (Founder & CEO) - 15+ years Salesforce expertise
   - Hooria Amiri (Video Editor & Content Creator)
   - Ali Hayyan (Content & SEO Specialist)  
   - The Ghana (Digital Strategist & Social Media Manager)

3. **Service Offerings Updated** - Implemented 8 core services:
   - Digital Strategy & Consulting (Featured)
   - Website & Funnel Design
   - Social Media Management
   - Salesforce + CRM Optimization (Featured)
   - Marketing Automation
   - Content Creation & Video Editing
   - SEO & Paid Advertising
   - AI-Driven Campaign Optimization (Featured)

### ✅ Medium Priority Tasks Completed
4. **Admin Interface Customization**:
   - Updated fieldsets for new SiteConfiguration fields
   - Added brand color management section
   - Updated admin titles to "Social Dots Inc. Administration"
   - Enhanced field organization and help text

5. **Canadian Localization**:
   - Changed timezone to 'America/Toronto'
   - Set language to 'en-ca'
   - Added Canadian business settings (first day Monday)

6. **Brand-Compliant Email Templates**:
   - Base email template with Social Dots branding
   - Lead welcome email template
   - Order confirmation email template
   - Uses brand colors and professional styling
   - Mobile responsive design

### ✅ Low Priority Tasks Completed  
7. **Data Fixtures**: Created `/core/fixtures/initial_data.json` with team and service data

8. **Management Commands**: Created `setup_socialdots.py` command for:
   - Creating Ali Shafique superuser
   - Setting up site configuration
   - Loading initial team and service data

9. **Business Rules & Validation**:
   - Hex color validation for brand colors
   - Price validation (minimum 0.01 CAD)
   - Service pricing logic validation
   - Auto-featuring of core services (Salesforce, AI, Strategy)
   - Singleton pattern for SiteConfiguration

## Current Project Status

### Phase 1 & 2: COMPLETE ✅
- Core Django platform with all models
- External integrations configured (Stripe, Frappe, n8n, Google Calendar)
- Social Dots branding fully implemented
- Canadian localization completed
- Admin interface customized
- Email templates created
- Business validation rules implemented

### Phase 3: READY TO START 🚀
**Frontend Development** - Prerequisites needed:

#### Critical Before Frontend:
1. **Database Setup** (5 mins):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py setup_socialdots
   ```

2. **Core Views Implementation** (30 mins):
   - Home page view
   - Services listing/detail views
   - Team page view
   - Portfolio/projects views
   - Blog listing/detail views
   - Contact/lead submission view

3. **Static Files Structure** (15 mins):
   - Create `/static/css/`, `/static/js/`, `/static/images/`
   - Implement brand colors CSS variables
   - Set up responsive framework

4. **Template Base Structure** (30 mins):
   - `base.html` with Social Dots navigation
   - Header/footer templates
   - Error pages (404, 500)

### Phase 4: Future Enhancements
- 3D UI implementation
- Advanced AI features
- Performance optimization
- SEO enhancements

## Company Context
- **Founded by**: Ali Shafique (15+ years Canadian IT/Salesforce experience)
- **Location**: Toronto, Ontario, Canada
- **Focus**: Canadian businesses, strategic AI integration
- **Team**: Hybrid Canadian strategy + International execution (Pakistan team)
- **Core Values**: Holistic problem-solving, strategic agility, transparent partnership
- **Brand**: Professional blue palette, clear communication, empathetic approach

## Technical Stack
- **Backend**: Django 4.2+ with PostgreSQL
- **Payments**: Stripe integration
- **ERP**: Frappe integration  
- **AI/Automation**: n8n webhooks
- **Calendar**: Google Calendar API
- **Frontend**: HTML5, CSS3, JavaScript (3D ready)
- **Deployment**: Gunicorn + WhiteNoise

## Development Commands
```bash
# Setup from scratch
python manage.py setup_socialdots

# Development
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Load initial data
python manage.py loaddata core/fixtures/initial_data.json

# Admin access
# Username: alishafique  
# Password: change_me_in_production
```

## Files Modified/Created Today
- `core/models.py` - Enhanced with Social Dots branding and validation
- `socialdots/settings.py` - Canadian localization
- `core/admin.py` - Social Dots admin customization
- `core/fixtures/initial_data.json` - Team and service data
- `templates/emails/` - Brand-compliant email templates
- `core/management/commands/setup_socialdots.py` - Setup command
- `CLAUDE.md` - This memory file

## Next Session Goals
1. Run database migrations and setup
2. Implement core views and URL patterns  
3. Create static file structure with brand CSS
4. Build responsive template foundation
5. Begin 3D UI implementation

## Business Rules to Remember
- All services with "Salesforce", "AI", or "Strategy" auto-feature
- Custom quote services should not have fixed prices
- Only one SiteConfiguration allowed
- All prices in CAD
- Core brand colors must be used consistently
- Canadian timezone and localization required