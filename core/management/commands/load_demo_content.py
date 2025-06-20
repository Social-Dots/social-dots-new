from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import BlogPost, Project, Testimonial
from datetime import datetime, date


class Command(BaseCommand):
    help = 'Load demo content including blog posts, projects, and testimonials'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Loading demo content for Social Dots...')
        )

        # Get or create the author (Ali Shafique)
        try:
            author = User.objects.get(username='alishafique')
        except User.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('⚠️  Admin user not found, creating author...')
            )
            author = User.objects.create_user(
                username='alishafique',
                email='ali@socialdots.ca',
                password='change_me_in_production',
                first_name='Ali',
                last_name='Shafique'
            )

        # Load blog posts
        self.load_blog_posts(author)
        
        # Load projects
        self.load_projects(author)
        
        # Load testimonials
        self.load_testimonials()

        self.stdout.write(
            self.style.SUCCESS('✅ Demo content loaded successfully!')
        )

    def load_blog_posts(self, author):
        self.stdout.write('Loading blog posts...')
        
        blog_posts_data = [
            {
                'title': 'Strategic AI Integration: A Canadian Business Perspective',
                'slug': 'strategic-ai-integration-canadian-business',
                'content': '''# Strategic AI Integration: A Canadian Business Perspective

As Canadian businesses navigate an increasingly digital landscape, artificial intelligence (AI) has emerged as a transformative force. However, successful AI integration requires more than just adopting the latest technology—it demands a strategic approach that aligns with your business values and long-term objectives.

## Understanding AI's Role in Canadian Business

The Canadian market presents unique opportunities and challenges for AI implementation. From privacy regulations like PIPEDA to cultural considerations around data usage, Canadian businesses must approach AI integration thoughtfully.

### Key Considerations for AI Strategy

1. **Regulatory Compliance**: Ensuring AI implementations meet Canadian privacy and data protection standards
2. **Cultural Alignment**: Technology solutions that reflect Canadian values of privacy, transparency, and inclusivity
3. **Market Specificity**: AI applications tailored to Canadian market conditions and consumer behavior

## Building Your AI Strategy

Successful AI integration begins with understanding your business objectives. We recommend a phased approach:

### Phase 1: Assessment and Planning
- Audit current processes and identify automation opportunities
- Evaluate data quality and availability
- Define success metrics and ROI expectations

### Phase 2: Pilot Implementation
- Start with low-risk, high-impact use cases
- Implement robust testing and validation processes
- Gather feedback and iterate

### Phase 3: Scale and Optimize
- Expand successful pilots across the organization
- Continuous monitoring and optimization
- Training and change management

## Real-World Applications

We've helped Canadian businesses implement AI solutions across various sectors:

- **Customer Service**: Intelligent chatbots that understand Canadian context and language nuances
- **Sales Optimization**: Predictive analytics for Canadian market trends
- **Process Automation**: Streamlining compliance with Canadian regulations

## The Social Dots Approach

At Social Dots, we believe AI should serve your business soul, not the other way around. Our approach ensures that technology implementation aligns with your values while delivering measurable business results.

Ready to explore AI opportunities for your business? [Contact us](/contact/) for a free strategic consultation.''',
                'excerpt': 'Discover how Canadian businesses can strategically integrate AI to drive growth while maintaining compliance and cultural alignment. Learn our proven three-phase approach to successful AI implementation.',
                'status': 'published',
                'published_at': datetime(2024, 12, 15, 10, 0),
                'tags': ['AI Integration', 'Canadian Business', 'Digital Strategy', 'Technology', 'Business Growth'],
                'is_featured': True
            },
            {
                'title': 'Salesforce Optimization: Maximizing ROI for Canadian Companies',
                'slug': 'salesforce-optimization-roi-canadian-companies',
                'content': '''# Salesforce Optimization: Maximizing ROI for Canadian Companies

Salesforce is a powerful platform, but many Canadian businesses aren't maximizing their investment. With proper optimization, companies can see ROI improvements of 300% or more within the first year.

## Common Salesforce Challenges in Canada

We've identified several patterns among Canadian Salesforce implementations:

### Data Quality Issues
- Inconsistent data entry standards
- Duplicate records and incomplete information
- Lack of data validation rules

### Underutilized Features
- Basic lead scoring or none at all
- Manual processes that could be automated
- Limited reporting and analytics usage

### Integration Gaps
- Disconnected marketing and sales tools
- Poor email marketing integration
- Limited customer service connectivity

## Our Optimization Framework

### 1. Data Audit and Cleanup
We start every optimization project with a comprehensive data audit:
- Identify and merge duplicate records
- Standardize data entry formats
- Implement validation rules for future data quality

### 2. Process Automation
Streamline your sales processes with smart automation:
- Lead assignment and routing
- Follow-up task creation
- Opportunity progression tracking

### 3. Advanced Analytics Setup
Unlock insights with proper reporting:
- Sales pipeline analytics
- Lead source performance tracking
- Revenue forecasting dashboards

### 4. Integration Strategy
Connect Salesforce with your existing tools:
- Marketing automation platforms
- Customer service systems
- Financial and ERP systems

## Case Study: Toronto Manufacturing Company

A Toronto-based manufacturing company approached us with a stagnant Salesforce implementation. Their challenges included:
- 40% duplicate lead records
- Manual lead assignment causing delays
- No visibility into sales pipeline health

**Results after 6 months:**
- 65% increase in lead conversion rates
- 50% reduction in sales cycle length
- 300% improvement in sales team productivity

## Canadian Compliance Considerations

Salesforce optimization in Canada requires attention to:
- PIPEDA compliance for data handling
- Provincial privacy regulations
- Industry-specific requirements (healthcare, finance, etc.)

## Getting Started

Ready to optimize your Salesforce investment? Our team offers:
- Free Salesforce health assessments
- Custom optimization roadmaps
- Implementation and training support

[Schedule your free assessment](/contact/) today and discover your Salesforce potential.''',
                'excerpt': 'Learn how Canadian companies can optimize their Salesforce investment for maximum ROI. Discover our proven framework and real case study results showing 300% productivity improvements.',
                'status': 'published',
                'published_at': datetime(2024, 12, 10, 9, 0),
                'tags': ['Salesforce', 'CRM Optimization', 'Sales Productivity', 'Canadian Business', 'ROI'],
                'is_featured': True
            },
            {
                'title': 'Digital Marketing Automation: A Guide for Toronto Businesses',
                'slug': 'digital-marketing-automation-toronto-businesses',
                'content': '''# Digital Marketing Automation: A Guide for Toronto Businesses

The Toronto business landscape is increasingly competitive, with companies vying for attention in both local and national markets. Marketing automation has become essential for businesses looking to scale their marketing efforts while maintaining personalized customer experiences.

## Why Marketing Automation Matters in Toronto

Toronto's diverse market presents unique challenges:
- Multicultural audience requiring personalized messaging
- Competitive landscape demanding efficient resource allocation
- High customer acquisition costs necessitating better nurturing

## Key Areas for Automation

### Email Marketing Sequences
Automate your email marketing to nurture leads effectively:
- Welcome series for new subscribers
- Abandoned cart recovery sequences
- Post-purchase follow-up campaigns

### Lead Scoring and Nurturing
Implement intelligent lead scoring to:
- Prioritize high-value prospects
- Trigger appropriate follow-up actions
- Optimize sales team efficiency

### Social Media Management
Streamline your social presence with:
- Scheduled content posting
- Automated engagement responses
- Social listening and sentiment tracking

### Customer Journey Mapping
Create automated touchpoints throughout the customer journey:
- Awareness stage content delivery
- Consideration phase nurturing
- Decision stage conversion optimization

## Toronto Market Considerations

### Local SEO Automation
- Automated local business listing updates
- Review management and response
- Location-based content optimization

### Multicultural Marketing
- Language-specific campaign automation
- Cultural event-based messaging
- Demographic-targeted content delivery

## Implementation Strategy

### Phase 1: Foundation (Months 1-2)
- Marketing automation platform selection
- Data integration and cleanup
- Basic email sequences setup

### Phase 2: Expansion (Months 3-4)
- Lead scoring implementation
- Social media automation
- Advanced segmentation

### Phase 3: Optimization (Months 5-6)
- A/B testing and optimization
- Advanced analytics setup
- Cross-channel integration

## Measuring Success

Key metrics for Toronto businesses:
- Lead quality and conversion rates
- Customer acquisition cost reduction
- Marketing qualified lead (MQL) volume
- Revenue attribution to automated campaigns

## Tools We Recommend

For Toronto businesses, we typically recommend:
- **HubSpot**: Comprehensive platform ideal for growing companies
- **Marketo**: Enterprise-level automation for larger organizations
- **Mailchimp**: Cost-effective solution for smaller businesses
- **Pardot**: Salesforce-native option for existing Salesforce users

## Getting Started

Ready to automate your marketing efforts? Our team specializes in:
- Marketing automation strategy development
- Platform selection and implementation
- Campaign setup and optimization
- Training and ongoing support

[Contact us](/contact/) for a free marketing automation assessment tailored to the Toronto market.''',
                'excerpt': 'Discover how Toronto businesses can leverage marketing automation to compete effectively in the diverse local market. Learn our proven implementation strategy and platform recommendations.',
                'status': 'published',
                'published_at': datetime(2024, 12, 5, 11, 0),
                'tags': ['Marketing Automation', 'Toronto Business', 'Digital Marketing', 'Lead Generation', 'Customer Journey'],
                'is_featured': False
            }
        ]

        for post_data in blog_posts_data:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    'title': post_data['title'],
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'author': author,
                    'status': post_data['status'],
                    'published_at': post_data['published_at'],
                    'tags': post_data['tags'],
                    'is_featured': post_data['is_featured'],
                    'meta_description': post_data['excerpt'][:155] + '...'
                }
            )
            if created:
                self.stdout.write(f'  ✅ Created blog post: {post.title}')

    def load_projects(self, author):
        self.stdout.write('Loading projects...')
        
        projects_data = [
            {
                'title': 'AI-Powered Customer Service Platform for TechCorp Toronto',
                'slug': 'ai-customer-service-techcorp-toronto',
                'description': 'Complete transformation of customer service operations using AI chatbots, automated ticket routing, and predictive analytics. Resulted in 60% reduction in response times and 40% improvement in customer satisfaction scores.',
                'client_name': 'TechCorp Toronto',
                'status': 'completed',
                'start_date': date(2024, 6, 1),
                'end_date': date(2024, 9, 15),
                'technologies': ['ChatGPT API', 'Salesforce Service Cloud', 'Python', 'React', 'AWS Lambda'],
                'is_featured': True
            },
            {
                'title': 'Salesforce CRM Overhaul for MapleTech Inc.',
                'slug': 'salesforce-crm-overhaul-mapletech',
                'description': 'Complete Salesforce implementation and optimization including custom objects, automated workflows, advanced reporting, and team training. Increased sales productivity by 65% and improved lead conversion rates by 45%.',
                'client_name': 'MapleTech Inc.',
                'status': 'completed',
                'start_date': date(2024, 3, 1),
                'end_date': date(2024, 7, 30),
                'technologies': ['Salesforce Sales Cloud', 'Salesforce Service Cloud', 'Apex', 'Lightning Components', 'Pardot'],
                'is_featured': True
            },
            {
                'title': 'Digital Marketing Automation for VancouverStart',
                'slug': 'digital-marketing-automation-vancouverstart',
                'description': 'End-to-end marketing automation implementation including lead nurturing campaigns, social media automation, and analytics dashboard. Achieved 300% increase in qualified leads and 40% reduction in customer acquisition costs.',
                'client_name': 'VancouverStart',
                'status': 'completed',
                'start_date': date(2024, 1, 15),
                'end_date': date(2024, 5, 20),
                'technologies': ['HubSpot', 'Google Analytics', 'Facebook Ads API', 'Zapier', 'Custom Integrations'],
                'is_featured': True
            },
            {
                'title': 'E-commerce Platform Integration for Ottawa Retail',
                'slug': 'ecommerce-platform-integration-ottawa-retail',
                'description': 'Comprehensive e-commerce platform development with inventory management, payment processing, and customer analytics. Increased online sales by 250% and improved operational efficiency by 70%.',
                'client_name': 'Ottawa Retail Solutions',
                'status': 'completed',
                'start_date': date(2024, 2, 1),
                'end_date': date(2024, 6, 15),
                'technologies': ['Shopify Plus', 'React', 'Node.js', 'Stripe', 'Google Analytics', 'Mailchimp'],
                'is_featured': False
            }
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                slug=project_data['slug'],
                defaults={
                    'title': project_data['title'],
                    'description': project_data['description'],
                    'client_name': project_data['client_name'],
                    'status': project_data['status'],
                    'start_date': project_data['start_date'],
                    'end_date': project_data['end_date'],
                    'technologies': project_data['technologies'],
                    'is_featured': project_data['is_featured']
                }
            )
            if created:
                self.stdout.write(f'  ✅ Created project: {project.title}')

    def load_testimonials(self):
        self.stdout.write('Loading testimonials...')
        
        testimonials_data = [
            {
                'client_name': 'Sarah Johnson',
                'client_title': 'CTO',
                'client_company': 'TechCorp Toronto',
                'content': 'Social Dots transformed our customer service operations completely. The AI integration they designed feels natural to our customers while dramatically improving our efficiency. Our response times improved by 60% and customer satisfaction scores increased by 40%.',
                'rating': 5,
                'is_featured': True,
                'project_slug': 'ai-customer-service-techcorp-toronto'
            },
            {
                'client_name': 'Mike Chen',
                'client_title': 'VP of Sales',
                'client_company': 'MapleTech Inc.',
                'content': 'The Salesforce optimization Ali\'s team delivered exceeded our expectations. Our sales process is now streamlined and our visibility into the pipeline is incredible. We\'ve seen a 65% increase in productivity and 45% better conversion rates.',
                'rating': 5,
                'is_featured': True,
                'project_slug': 'salesforce-crm-overhaul-mapletech'
            },
            {
                'client_name': 'David Lee',
                'client_title': 'Founder',
                'client_company': 'VancouverStart',
                'content': 'Social Dots\' marketing automation strategy transformed our startup from struggling with lead generation to having a consistent pipeline of qualified prospects. We achieved a 300% increase in qualified leads and reduced acquisition costs by 40%.',
                'rating': 5,
                'is_featured': True,
                'project_slug': 'digital-marketing-automation-vancouverstart'
            },
            {
                'client_name': 'Jennifer Walsh',
                'client_title': 'CEO',
                'client_company': 'Ottawa Retail Solutions',
                'content': 'The e-commerce platform Social Dots built for us is exactly what we needed to compete in today\'s digital marketplace. The results speak for themselves - 250% increase in online sales and much better operational efficiency.',
                'rating': 5,
                'is_featured': False,
                'project_slug': 'ecommerce-platform-integration-ottawa-retail'
            },
            {
                'client_name': 'Robert Kim',
                'client_title': 'Marketing Director',
                'client_company': 'Calgary Innovations',
                'content': 'Working with Social Dots was a game-changer for our digital strategy. Their strategic approach and deep understanding of the Canadian market helped us achieve results we didn\'t think were possible. Highly recommended for any Canadian business looking to scale.',
                'rating': 5,
                'is_featured': True,
                'project_slug': None
            },
            {
                'client_name': 'Lisa Thompson',
                'client_title': 'Operations Manager',
                'client_company': 'Montreal Manufacturing',
                'content': 'The team at Social Dots doesn\'t just implement technology - they ensure it aligns with your business values and long-term vision. Their holistic approach made all the difference in our digital transformation journey.',
                'rating': 5,
                'is_featured': True,
                'project_slug': None
            }
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                client_company=testimonial_data['client_company'],
                defaults={
                    'client_position': testimonial_data['client_title'],
                    'content': testimonial_data['content'],
                    'rating': testimonial_data['rating'],
                    'is_featured': testimonial_data['is_featured'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✅ Created testimonial: {testimonial.client_name} from {testimonial.client_company}')