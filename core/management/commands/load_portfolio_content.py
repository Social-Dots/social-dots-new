from django.core.management.base import BaseCommand
from core.models import Portfolio, PortfolioCategory


class Command(BaseCommand):
    help = 'Load portfolio content including categories and portfolio items'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Loading portfolio content for Social Dots...')
        )

        # Create categories
        self.load_categories()
        
        # Create portfolio items
        self.load_portfolio_items()

        self.stdout.write(
            self.style.SUCCESS('✅ Portfolio content loaded successfully!')
        )

    def load_categories(self):
        self.stdout.write('Loading portfolio categories...')
        
        categories_data = [
            {
                'name': 'Social Media',
                'slug': 'social-media',
                'description': 'Social media content including Instagram posts, LinkedIn content, and social media campaigns'
            },
            {
                'name': 'Web Design',
                'slug': 'web-design', 
                'description': 'Modern website designs, UI/UX projects, and web development showcases'
            },
            {
                'name': 'AI Solutions',
                'slug': 'ai-solutions',
                'description': 'AI integration projects, automation solutions, and intelligent system implementations'
            },
            {
                'name': 'Marketing',
                'slug': 'marketing',
                'description': 'Marketing campaigns, email templates, and digital marketing content'
            }
        ]

        for cat_data in categories_data:
            category, created = PortfolioCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                    'order': len(PortfolioCategory.objects.all())
                }
            )
            if created:
                self.stdout.write(f'  ✅ Created category: {category.name}')

    def load_portfolio_items(self):
        self.stdout.write('Loading portfolio items...')
        
        portfolio_data = [
            {
                'title': 'Instagram Business Campaign - TechCorp',
                'slug': 'instagram-business-campaign-techcorp',
                'description': 'Modern Instagram marketing campaign featuring AI and technology themes with blue gradient backgrounds and professional icons. Created engaging content that increased follower engagement by 150%.',
                'content_type': 'post',
                'portfolio_type': 'social',
                'category_slug': 'social-media',
                'is_featured': True
            },
            {
                'title': 'LinkedIn Professional Content Series',
                'slug': 'linkedin-professional-content-series',
                'description': 'Professional LinkedIn content series focusing on Canadian business insights and digital transformation. Developed thought leadership content that generated 500+ new connections for the client.',
                'content_type': 'post',
                'portfolio_type': 'social',
                'category_slug': 'social-media',
                'is_featured': True
            },
            {
                'title': 'AI Automation Blog Series',
                'slug': 'ai-automation-blog-series',
                'description': 'Comprehensive blog content covering AI integration strategies for Canadian businesses. This series helped establish our client as a thought leader in the AI space with over 10K views.',
                'content_type': 'blog',
                'portfolio_type': 'ai',
                'category_slug': 'ai-solutions',
                'is_featured': True
            },
            {
                'title': 'Modern Website Design - Startup Portfolio',
                'slug': 'modern-website-design-startup',
                'description': 'Clean, modern website design featuring blue gradient backgrounds, professional icons, and responsive layouts. Increased client conversion rates by 85% and improved user engagement significantly.',
                'content_type': 'technology',
                'portfolio_type': 'website',
                'category_slug': 'web-design',
                'is_featured': True
            },
            {
                'title': 'Email Marketing Campaign Templates',
                'slug': 'email-marketing-campaign-templates',
                'description': 'Professional email templates with blue accent colors and modern card designs for business communications. Achieved 45% open rates and 12% click-through rates for client campaigns.',
                'content_type': 'email',
                'portfolio_type': 'social',
                'category_slug': 'marketing',
                'is_featured': True
            },
            {
                'title': 'Social Media Card Design System',
                'slug': 'social-media-card-design-system',
                'description': 'Comprehensive design system for social media content featuring modern cards with blue backgrounds, professional icons, and consistent branding. Used across all client social platforms.',
                'content_type': 'post',
                'portfolio_type': 'social',
                'category_slug': 'social-media',
                'is_featured': False
            },
            {
                'title': 'Customer Service AI Chatbot Interface',
                'slug': 'customer-service-ai-chatbot-interface',
                'description': 'Modern chat interface design with blue accent colors and intuitive user experience. Reduced customer service response times by 60% and improved satisfaction scores.',
                'content_type': 'technology',
                'portfolio_type': 'ai',
                'category_slug': 'ai-solutions',
                'is_featured': False
            },
            {
                'title': 'Digital Marketing Dashboard Design',
                'slug': 'digital-marketing-dashboard-design',
                'description': 'Clean dashboard interface for marketing analytics with modern card layouts and blue color scheme. Provides clear insights for data-driven marketing decisions.',
                'content_type': 'technology',
                'portfolio_type': 'website',
                'category_slug': 'marketing',
                'is_featured': False
            }
        ]

        for portfolio_item in portfolio_data:
            try:
                category = PortfolioCategory.objects.get(slug=portfolio_item['category_slug'])
                portfolio, created = Portfolio.objects.get_or_create(
                    slug=portfolio_item['slug'],
                    defaults={
                        'title': portfolio_item['title'],
                        'description': portfolio_item['description'],
                        'content_type': portfolio_item['content_type'],
                        'portfolio_type': portfolio_item['portfolio_type'],
                        'category': category,
                        'is_featured': portfolio_item['is_featured'],
                        'is_active': True,
                        'order': len(Portfolio.objects.all())
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Created portfolio: {portfolio.title}')
            except PortfolioCategory.DoesNotExist:
                self.stdout.write(f'  ❌ Category not found: {portfolio_item["category_slug"]}')