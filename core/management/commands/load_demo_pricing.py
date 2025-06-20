from django.core.management.base import BaseCommand
from core.models import Service, PricingPlan
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load demo services and pricing plans for Social Dots'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Loading demo services and pricing plans...')
        )

        # Load services
        self.load_services()
        
        # Load pricing plans
        self.load_pricing_plans()

        self.stdout.write(
            self.style.SUCCESS('✅ Demo services and pricing plans loaded successfully!')
        )

    def load_services(self):
        self.stdout.write('Loading services...')
        
        services_data = [
            {
                'title': 'Digital Strategy & Consulting',
                'slug': 'digital-strategy-consulting',
                'description': '''Comprehensive digital strategy development that aligns technology with your business objectives. We analyze your current digital presence, identify opportunities, and create a roadmap for sustainable growth.

Our strategic approach includes market analysis, competitor research, technology assessment, and ROI projections. Perfect for businesses looking to transform their digital operations or expand into new markets.''',
                'short_description': 'Comprehensive digital strategy development that connects business goals with smart execution.',
                'price': Decimal('150.00'),
                'price_type': 'hourly',
                'features': [
                    'Digital Audit & Assessment',
                    'Strategic Roadmap Development',
                    'Competitive Analysis',
                    'Technology Recommendations',
                    'ROI Projections & Timeline',
                    'Implementation Support'
                ],
                'is_featured': True,
                'is_active': True,
                'order': 1
            },
            {
                'title': 'Salesforce CRM Setup & Optimization',
                'slug': 'salesforce-crm-optimization',
                'description': '''Expert Salesforce configuration, customization, and optimization tailored to your Canadian business needs. From initial setup to advanced automation, we ensure your CRM drives real business results.

Includes data migration, custom fields, automation workflows, reporting dashboards, user training, and ongoing support. Designed for businesses wanting to maximize their Salesforce investment.''',
                'short_description': 'Expert Salesforce configuration, customization, and optimization for your business needs.',
                'price': Decimal('5000.00'),
                'price_type': 'fixed',
                'features': [
                    'Complete Salesforce Setup',
                    'Data Migration & Cleanup',
                    'Custom Fields & Objects',
                    'Automation Workflows',
                    'Reporting Dashboards',
                    'User Training & Support'
                ],
                'is_featured': True,
                'is_active': True,
                'order': 2
            },
            {
                'title': 'AI-Powered Marketing Automation',
                'slug': 'ai-marketing-automation',
                'description': '''Strategic AI integration for marketing campaigns, customer segmentation, and personalized content delivery. We implement smart automation that learns from customer behavior and optimizes performance.

Perfect for businesses ready to leverage AI for improved customer engagement, lead scoring, and conversion optimization. Includes setup, training, and performance monitoring.''',
                'short_description': 'Strategic AI integration for campaign optimization and measurable business benefits.',
                'price': Decimal('200.00'),
                'price_type': 'hourly',
                'features': [
                    'AI Strategy Development',
                    'Marketing Automation Setup',
                    'Customer Segmentation',
                    'Personalized Content Delivery',
                    'Performance Analytics',
                    'Continuous Optimization'
                ],
                'is_featured': True,
                'is_active': True,
                'order': 3
            },
            {
                'title': 'Website Development & Design',
                'slug': 'website-development-design',
                'description': '''Modern, responsive website development using the latest technologies. We create websites that not only look great but also drive conversions and support your business goals.

From simple business websites to complex web applications, we ensure optimal performance, SEO optimization, and mobile responsiveness. Includes ongoing maintenance and support.''',
                'short_description': 'Modern, responsive websites that drive conversions and support business growth.',
                'price_type': 'custom',
                'features': [
                    'Responsive Web Design',
                    'Modern Framework Implementation',
                    'SEO Optimization',
                    'Performance Optimization',
                    'Content Management System',
                    'Ongoing Maintenance'
                ],
                'is_featured': False,
                'is_active': True,
                'order': 4
            },
            {
                'title': 'Marketing Campaign Management',
                'slug': 'marketing-campaign-management',
                'description': '''End-to-end marketing campaign management across digital channels. We handle strategy, execution, monitoring, and optimization to ensure maximum ROI for your marketing spend.

Includes social media management, email marketing, paid advertising, content creation, and performance analytics. Perfect for businesses wanting professional marketing management.''',
                'short_description': 'Complete marketing campaign management for maximum ROI across all digital channels.',
                'price': Decimal('3000.00'),
                'price_type': 'monthly',
                'features': [
                    'Multi-Channel Strategy',
                    'Content Creation & Curation',
                    'Social Media Management',
                    'Email Marketing Campaigns',
                    'Paid Advertising Management',
                    'Performance Analytics & Reporting'
                ],
                'is_featured': False,
                'is_active': True,
                'order': 5
            },
            {
                'title': 'Business Process Automation',
                'slug': 'business-process-automation',
                'description': '''Streamline your business operations with intelligent automation solutions. We identify repetitive tasks and implement automated workflows that save time and reduce errors.

From simple task automation to complex business process optimization, we help Canadian businesses operate more efficiently while maintaining quality and compliance.''',
                'short_description': 'Intelligent automation solutions that streamline operations and reduce manual work.',
                'price': Decimal('4500.00'),
                'price_type': 'fixed',
                'features': [
                    'Process Analysis & Mapping',
                    'Automation Strategy Development',
                    'Workflow Implementation',
                    'Integration with Existing Tools',
                    'Quality Assurance Testing',
                    'Training & Documentation'
                ],
                'is_featured': False,
                'is_active': True,
                'order': 6
            }
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'  ✅ Created service: {service.title}')

    def load_pricing_plans(self):
        self.stdout.write('Loading pricing plans...')
        
        plans_data = [
            {
                'name': 'Starter',
                'description': 'Perfect for small businesses getting started with digital transformation. Includes essential tools and support to establish your digital presence.',
                'price': Decimal('500.00'),
                'price_period': 'monthly',
                'features': [
                    'Digital Strategy Consultation (2 hours/month)',
                    'Basic Salesforce Setup',
                    'Email Marketing Automation',
                    'Monthly Performance Reports',
                    'Email Support',
                    'Canadian Business Compliance'
                ],
                'is_popular': False,
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Professional',
                'description': 'Comprehensive digital solutions for growing businesses. Advanced automation, AI integration, and dedicated support for scaling operations.',
                'price': Decimal('1200.00'),
                'price_period': 'monthly',
                'features': [
                    'Digital Strategy Consultation (4 hours/month)',
                    'Advanced Salesforce Optimization',
                    'AI-Powered Marketing Automation',
                    'Custom Workflow Development',
                    'Bi-weekly Performance Reviews',
                    'Priority Phone & Email Support',
                    'Canadian Market Analysis',
                    'Integration with Existing Tools'
                ],
                'is_popular': True,
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Enterprise',
                'description': 'Full-service digital transformation for established businesses. Complete automation, custom development, and strategic partnership.',
                'price': Decimal('2500.00'),
                'price_period': 'monthly',
                'features': [
                    'Dedicated Strategy Consultant (8 hours/month)',
                    'Complete Salesforce Ecosystem Management',
                    'Advanced AI & Machine Learning Integration',
                    'Custom Application Development',
                    'Weekly Strategy Sessions',
                    '24/7 Priority Support',
                    'Canadian Compliance & Privacy Expertise',
                    'Multi-Platform Integration',
                    'Quarterly Business Reviews',
                    'White-Label Solutions Available'
                ],
                'is_popular': False,
                'is_active': True,
                'order': 3
            },
            {
                'name': 'Digital Transformation Package',
                'description': 'Complete one-time digital overhaul for businesses ready to modernize their entire operation. Includes strategy, implementation, and training.',
                'price': Decimal('15000.00'),
                'price_period': 'one_time',
                'features': [
                    'Complete Digital Audit & Strategy',
                    'Salesforce Implementation & Optimization',
                    'Website Development & Design',
                    'Marketing Automation Setup',
                    'Business Process Automation',
                    'Team Training & Documentation',
                    'Canadian Market Research',
                    '6 Months Post-Launch Support',
                    'Performance Optimization',
                    'ROI Tracking & Analytics'
                ],
                'is_popular': False,
                'is_active': True,
                'order': 4
            }
        ]

        for plan_data in plans_data:
            plan, created = PricingPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'  ✅ Created pricing plan: {plan.name}')