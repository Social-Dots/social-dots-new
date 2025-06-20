from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SiteConfiguration, TeamMember, Service


class Command(BaseCommand):
    help = 'Set up initial Social Dots configuration and data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser for Ali Shafique',
        )
        parser.add_argument(
            '--load-fixtures',
            action='store_true',
            help='Load initial team members and services',
        )
        parser.add_argument(
            '--setup-site-config',
            action='store_true',
            help='Create or update site configuration',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up Social Dots Inc. platform...')
        )

        if options['create_superuser']:
            self.create_superuser()

        if options['setup_site_config']:
            self.setup_site_config()

        if options['load_fixtures']:
            self.load_fixtures()

        if not any([options['create_superuser'], options['setup_site_config'], options['load_fixtures']]):
            # Run all if no specific option is provided
            self.create_superuser()
            self.setup_site_config()
            self.load_fixtures()

        self.stdout.write(
            self.style.SUCCESS('✅ Social Dots setup completed successfully!')
        )

    def create_superuser(self):
        """Create superuser for Ali Shafique if it doesn't exist"""
        username = 'alishafique'
        email = 'ali@socialdots.ca'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists, skipping...')
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password='change_me_in_production',  # Should be changed in production
            first_name='Ali',
            last_name='Shafique'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Created superuser: {username}')
        )
        self.stdout.write(
            self.style.WARNING('⚠️  Please change the default password in production!')
        )

    def setup_site_config(self):
        """Create or update site configuration"""
        config, created = SiteConfiguration.objects.get_or_create(
            defaults={
                'site_name': 'Social Dots Inc.',
                'tagline': 'Empowering Canadian businesses to thrive in a constantly evolving digital world',
                'phone': '416-556-6961',
                'email': 'hello@socialdots.ca',
                'contact_email': 'ali@socialdots.ca',
                'address': 'Toronto, Ontario, Canada',
                'website_url': 'https://socialdots.ca',
                'primary_color': '#2563EB',
                'secondary_color': '#1E40AF',
                'accent_color': '#3B82F6',
                'meta_description': 'Strategic AI integration and digital solutions for Canadian businesses. 15+ years of Salesforce and marketing automation expertise.',
                'legal_name': 'Social Dots Inc.',
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Created site configuration')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Site configuration already exists, skipping...')
            )

    def load_fixtures(self):
        """Load initial team members and services"""
        self.stdout.write('Loading team members...')
        
        # Ali Shafique - Founder & CEO
        ali, created = TeamMember.objects.get_or_create(
            email='ali@socialdots.ca',
            defaults={
                'name': 'Ali Shafique',
                'position': 'Founder & CEO',
                'bio': '15+ years of Canadian IT industry experience with deep Salesforce ecosystem expertise. AI Strategy & Marketing Coach and spiritual guide for purpose-driven entrepreneurs.',
                'phone': '416-556-6961',
                'linkedin': 'https://linkedin.com/in/alishafique',
                'is_active': True,
                'order': 1
            }
        )
        if created:
            self.stdout.write(f'  ✅ Created team member: {ali.name}')

        # Other team members
        team_members = [
            {
                'name': 'Hooria Amiri',
                'position': 'Video Editor & Content Creator',
                'bio': 'Skilled video editor and content creator specializing in creating engaging visual content that aligns with brand messaging and strategic goals.',
                'order': 2
            },
            {
                'name': 'Ali Hayyan',
                'position': 'Content & SEO Specialist', 
                'bio': 'Expert in content strategy and SEO optimization, focused on creating compelling content that drives organic growth and engagement.',
                'order': 3
            },
            {
                'name': 'The Ghana',
                'position': 'Digital Strategist & Social Media Manager',
                'bio': 'Digital strategist specializing in social media management and comprehensive digital marketing strategies for business growth.',
                'order': 4
            }
        ]

        for member_data in team_members:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'  ✅ Created team member: {member.name}')

        self.stdout.write('Loading services...')
        
        # Core services based on company documentation
        services = [
            {
                'title': 'Digital Strategy & Consulting',
                'slug': 'digital-strategy-consulting',
                'description': 'Comprehensive digital strategy development that connects business goals with smart, technology-enabled execution. We provide strategic planning, technology assessment, and AI integration strategy tailored to your unique business needs.',
                'short_description': 'Strategic planning and technology assessment for sustainable digital growth',
                'icon': 'fas fa-chart-line',
                'price_type': 'custom',
                'features': [
                    'Comprehensive digital strategy document',
                    'Technology roadmap and recommendations', 
                    'AI integration plan',
                    'Implementation timeline',
                    'ROI projections',
                    'Competitive analysis',
                    'Market research'
                ],
                'is_featured': True,
                'order': 1
            },
            {
                'title': 'Salesforce + CRM Optimization',
                'slug': 'salesforce-crm-optimization',
                'description': 'Expert Salesforce configuration, customization, and optimization. We handle system setup, process optimization through workflow automation, lead scoring, pipeline management, and comprehensive training and support.',
                'short_description': 'Expert Salesforce setup, optimization, and automation',
                'icon': 'fas fa-users-cog',
                'price_type': 'custom',
                'features': [
                    'Configured Salesforce instance',
                    'Automated workflows',
                    'Lead scoring setup',
                    'Pipeline management',
                    'Training materials',
                    'Documentation',
                    'Performance dashboards'
                ],
                'is_featured': True,
                'order': 2
            },
            {
                'title': 'AI-Driven Campaign Optimization',
                'slug': 'ai-driven-campaign-optimization',
                'description': 'Strategic AI integration for campaign optimization using tools like ChatGPT, Jasper, and advanced analytics. We set up automation workflows, performance optimization, AI-powered insights, and predictive analytics for measurable business benefits.',
                'short_description': 'AI integration and automation for campaign optimization',
                'icon': 'fas fa-robot',
                'price_type': 'custom',
                'features': [
                    'AI integration strategy',
                    'Automated workflows',
                    'Performance dashboards',
                    'Predictive analytics',
                    'Optimization reports',
                    'ROI tracking',
                    'Tool integration'
                ],
                'is_featured': True,
                'order': 3
            }
        ]

        for service_data in services:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'  ✅ Created service: {service.title}')

        self.stdout.write(
            self.style.SUCCESS('✅ All fixtures loaded successfully!')
        )