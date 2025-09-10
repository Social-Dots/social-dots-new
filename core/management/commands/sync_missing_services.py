from django.core.management.base import BaseCommand
from core.models import Service


class Command(BaseCommand):
    help = 'Add missing services from live site to localhost'

    def handle(self, *args, **options):
        self.stdout.write('Adding missing services from live site...')
        
        # Services that exist on live site but missing from localhost
        missing_services = [
            {
                'title': 'AI Business Assistant',
                'slug': 'ai-business-assistant',
                'description': 'Intelligent business assistant powered by AI to handle customer inquiries, appointment scheduling, lead qualification, and administrative tasks. Integrates seamlessly with your existing business systems.',
                'short_description': 'AI-powered business assistant for customer service and administrative tasks',
                'icon': 'fas fa-robot',
                'features': [
                    '24/7 Customer Support',
                    'Appointment Scheduling',
                    'Lead Qualification',
                    'Multi-language Support',
                    'CRM Integration',
                    'Analytics & Reporting'
                ],
                'price_type': 'custom',
                'order': 7
            },
            {
                'title': 'AI Concierge Service',
                'slug': 'ai-concierge-service',
                'description': 'Premium AI concierge service that provides personalized customer experiences, handles complex inquiries, and maintains the human touch while leveraging artificial intelligence for efficiency.',
                'short_description': 'Premium AI concierge for personalized customer experiences',
                'icon': 'fas fa-concierge-bell',
                'features': [
                    'Personalized Customer Interactions',
                    'Complex Inquiry Handling',
                    'Emotional Intelligence',
                    'Premium Support Experience',
                    'Human-AI Collaboration',
                    'Custom Training'
                ],
                'price_type': 'custom',
                'order': 8
            },
            {
                'title': 'AI Inbound Lead Assistant',
                'slug': 'ai-inbound-lead-assistant',
                'description': 'Automated lead capture and qualification system that engages website visitors, qualifies prospects, and routes high-quality leads to your sales team instantly.',
                'short_description': 'Automated lead capture and qualification using AI',
                'icon': 'fas fa-user-plus',
                'features': [
                    'Automated Lead Capture',
                    'Real-time Qualification',
                    'Instant Lead Routing',
                    'Lead Scoring',
                    'CRM Integration',
                    'Conversion Tracking'
                ],
                'price_type': 'custom',
                'order': 9
            },
            {
                'title': 'AI Outbound Sales Agent',
                'slug': 'ai-outbound-sales-agent',
                'description': 'AI-powered outbound sales agent that identifies prospects, initiates conversations, handles objections, and schedules appointments with qualified leads automatically.',
                'short_description': 'AI sales agent for automated outbound prospecting and appointment setting',
                'icon': 'fas fa-phone',
                'features': [
                    'Prospect Identification',
                    'Automated Outreach',
                    'Objection Handling',
                    'Appointment Scheduling',
                    'Follow-up Automation',
                    'Performance Analytics'
                ],
                'price_type': 'custom',
                'order': 10
            },
            {
                'title': 'AI SEO Optimization',
                'slug': 'ai-seo-optimization',
                'description': 'Advanced AI-powered SEO optimization that analyzes your website, identifies opportunities, creates optimized content, and monitors performance to improve search rankings.',
                'short_description': 'AI-driven SEO analysis, content optimization, and performance monitoring',
                'icon': 'fas fa-search',
                'features': [
                    'AI Content Analysis',
                    'Keyword Research & Optimization',
                    'Technical SEO Audit',
                    'Content Generation',
                    'Competitor Analysis',
                    'Performance Monitoring'
                ],
                'price_type': 'monthly',
                'price': '1500.00',
                'order': 11
            },
            {
                'title': 'AI-Driven Social Media Marketing',
                'slug': 'ai-driven-social-media-marketing',
                'description': 'Comprehensive AI-powered social media management including content creation, posting automation, audience engagement, and performance optimization across all platforms.',
                'short_description': 'AI-powered social media content creation and management',
                'icon': 'fas fa-share-alt',
                'features': [
                    'AI Content Creation',
                    'Automated Posting',
                    'Audience Engagement',
                    'Hashtag Optimization',
                    'Performance Analytics',
                    'Multi-Platform Management'
                ],
                'price_type': 'monthly',
                'price': '2000.00',
                'order': 12
            },
            {
                'title': 'AI-Powered CRM Setup & Customization',
                'slug': 'ai-powered-crm-setup-customization',
                'description': 'Complete CRM implementation enhanced with AI capabilities including predictive analytics, automated workflows, intelligent lead scoring, and personalized customer insights.',
                'short_description': 'CRM setup with AI-powered automation and predictive analytics',
                'icon': 'fas fa-database',
                'features': [
                    'AI-Enhanced CRM Setup',
                    'Predictive Analytics',
                    'Automated Workflows',
                    'Intelligent Lead Scoring',
                    'Customer Insights',
                    'Integration & Training'
                ],
                'price_type': 'fixed',
                'price': '5000.00',
                'order': 13
            },
            {
                'title': 'AI-Powered Web App Development',
                'slug': 'ai-powered-web-app-development',
                'description': 'Custom web application development integrated with AI capabilities including machine learning, natural language processing, and intelligent automation features.',
                'short_description': 'Custom web app development with integrated AI capabilities',
                'icon': 'fas fa-code',
                'features': [
                    'Custom Web Development',
                    'AI Integration',
                    'Machine Learning Features',
                    'Natural Language Processing',
                    'Intelligent Automation',
                    'Scalable Architecture'
                ],
                'price_type': 'custom',
                'order': 14
            },
            {
                'title': 'Automated Email Marketing with AI',
                'slug': 'automated-email-marketing-ai',
                'description': 'Intelligent email marketing automation with AI-powered content generation, send-time optimization, personalization, and predictive analytics for maximum engagement.',
                'short_description': 'AI-powered email marketing with smart automation and personalization',
                'icon': 'fas fa-envelope',
                'features': [
                    'AI Content Generation',
                    'Send-Time Optimization',
                    'Behavioral Triggers',
                    'Personalization',
                    'A/B Testing',
                    'Predictive Analytics'
                ],
                'price_type': 'monthly',
                'price': '800.00',
                'order': 15
            },
            {
                'title': 'Video Avatars Service',
                'slug': 'video-avatars-service',
                'description': 'Create AI-powered video avatars for personalized marketing videos, customer support, training content, and interactive presentations that engage your audience.',
                'short_description': 'AI video avatars for personalized marketing and customer engagement',
                'icon': 'fas fa-video',
                'features': [
                    'Custom Avatar Creation',
                    'Multi-language Support',
                    'Personalized Messaging',
                    'Interactive Presentations',
                    'Training Content',
                    'Marketing Videos'
                ],
                'price_type': 'fixed',
                'price': '2500.00',
                'order': 16
            },
            {
                'title': 'Voice AI & Call Automation',
                'slug': 'voice-ai-call-automation',
                'description': 'Advanced voice AI system for automated phone calls, customer service, appointment scheduling, and interactive voice response with natural conversation capabilities.',
                'short_description': 'Voice AI for automated calls and customer service',
                'icon': 'fas fa-microphone',
                'features': [
                    'Natural Voice Conversations',
                    'Automated Call Handling',
                    'Appointment Scheduling',
                    'Customer Service Automation',
                    'Multi-language Support',
                    'Call Analytics'
                ],
                'price_type': 'custom',
                'order': 17
            }
        ]
        
        created_count = 0
        existing_count = 0
        
        for service_data in missing_services:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults={
                    'title': service_data['title'],
                    'description': service_data['description'],
                    'short_description': service_data['short_description'],
                    'icon': service_data['icon'],
                    'features': service_data['features'],
                    'price': service_data.get('price'),
                    'price_type': service_data['price_type'],
                    'is_featured': False,
                    'is_active': True,
                    'order': service_data['order'],
                    'service_type': 'other'
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created service: {service_data["title"]}')
            else:
                existing_count += 1
                self.stdout.write(f'Service already exists: {service_data["title"]}')
        
        self.stdout.write(f'\nServices sync completed!')
        self.stdout.write(f'Created: {created_count} services')
        self.stdout.write(f'Already existed: {existing_count} services')
        
        # Show total count
        total_services = Service.objects.filter(is_active=True).count()
        self.stdout.write(f'Total active services: {total_services}')