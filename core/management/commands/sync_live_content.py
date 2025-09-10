from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import BlogPost, Project, Service, Portfolio
import json
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Sync content from live site based on known URLs and data'

    def handle(self, *args, **options):
        self.stdout.write('Starting targeted live content sync...')
        
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@socialdots.ca',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Add the missing blog posts that are on live site but not localhost
        self.add_missing_blog_posts(admin_user)
        
        # Add the missing projects
        self.add_missing_projects()
        
        self.stdout.write('Live content sync completed!')

    def add_missing_blog_posts(self, admin_user):
        """Add the blog posts that exist on live site but not in localhost"""
        self.stdout.write('Adding missing blog posts...')
        
        missing_blogs = [
            {
                'title': 'AI Concierge: The Future of Personalized Customer Experience',
                'slug': 'ai-concierge-future-personalized-customer-experience',
                'excerpt': 'Discover how AI concierge services are revolutionizing customer interactions, providing personalized experiences that enhance satisfaction and drive business growth.',
                'content': '''<h1>AI Concierge: The Future of Personalized Customer Experience</h1>

<p>In today's competitive business landscape, providing exceptional customer service is more crucial than ever. AI concierge services are emerging as a game-changing solution that combines the efficiency of artificial intelligence with the personal touch customers expect.</p>

<h2>What is an AI Concierge?</h2>

<p>An AI concierge is an intelligent virtual assistant that provides personalized customer service and support. Unlike traditional chatbots, AI concierges leverage advanced machine learning and natural language processing to understand context, emotions, and individual preferences.</p>

<h2>Key Benefits for Canadian Businesses</h2>

<ul>
<li><strong>24/7 Availability:</strong> Provide round-the-clock customer support without increasing staff costs</li>
<li><strong>Personalized Interactions:</strong> Tailor responses based on customer history and preferences</li>
<li><strong>Scalable Solution:</strong> Handle multiple customers simultaneously without compromising quality</li>
<li><strong>Cost Efficiency:</strong> Reduce operational costs while improving customer satisfaction</li>
</ul>

<h2>Implementation Strategy</h2>

<p>Successfully implementing an AI concierge requires careful planning and integration with existing systems. Our approach ensures seamless deployment while maintaining the human touch your customers value.</p>

<p>Ready to enhance your customer experience with AI? Contact Social Dots for a consultation on AI concierge implementation.</p>''',
                'tags': ['AI Concierge', 'Customer Experience', 'Personalization', 'AI Automation'],
                'meta_description': 'Discover how AI concierge services are revolutionizing customer interactions, providing personalized experiences that enhance satisfaction and drive business growth.'
            },
            {
                'title': 'Digital Landing Pages – Why Every Business Needs a Digital Address',
                'slug': 'digital-landing-pages-business-digital-address',
                'excerpt': 'Learn why digital landing pages are essential for modern businesses and how they serve as your digital address for converting visitors into customers.',
                'content': '''<h1>Digital Landing Pages – Why Every Business Needs a Digital Address</h1>

<p>In the digital age, your landing page serves as your business's digital address – the first impression potential customers get of your brand. A well-designed landing page can be the difference between a visitor and a customer.</p>

<h2>The Power of First Impressions</h2>

<p>Studies show that users form opinions about websites within milliseconds. Your landing page needs to immediately communicate value, build trust, and guide visitors toward taking action.</p>

<h2>Essential Elements of Effective Landing Pages</h2>

<ul>
<li><strong>Clear Value Proposition:</strong> Instantly communicate what you offer and why it matters</li>
<li><strong>Compelling Headlines:</strong> Grab attention and clearly state your benefits</li>
<li><strong>Trust Signals:</strong> Include testimonials, certifications, and social proof</li>
<li><strong>Strong Call-to-Action:</strong> Make it obvious what you want visitors to do next</li>
</ul>

<h2>Canadian Market Considerations</h2>

<p>For Canadian businesses, landing pages should reflect local values, compliance requirements, and cultural nuances that resonate with Canadian audiences.</p>

<p>Ready to create landing pages that convert? Contact Social Dots for professional landing page design and optimization.</p>''',
                'tags': ['Digital Landing Pages', 'Business Online Presence', 'Lead Generation', 'Conversion Optimization'],
                'meta_description': 'Learn why digital landing pages are essential for modern businesses and how they serve as your digital address for converting visitors into customers.'
            },
            {
                'title': 'CRM Systems: Personalized Solutions for Every Business\'s Needs and Processes',
                'slug': 'crm-systems-personalized-solutions-business-processes',
                'excerpt': 'Discover how personalized CRM systems can transform your business processes, improve customer relationships, and drive sustainable growth.',
                'content': '''<h1>CRM Systems: Personalized Solutions for Every Business's Needs and Processes</h1>

<p>Customer Relationship Management (CRM) systems are no longer one-size-fits-all solutions. Modern businesses require personalized CRM implementations that align with their unique processes, industry requirements, and growth objectives.</p>

<h2>Understanding Your CRM Needs</h2>

<p>Every business has unique customer interaction patterns, sales processes, and service requirements. A personalized CRM solution takes these factors into account to create a system that truly serves your business goals.</p>

<h2>Benefits of Personalized CRM Implementation</h2>

<ul>
<li><strong>Improved User Adoption:</strong> Systems designed for your team's workflow are easier to adopt and use</li>
<li><strong>Better Data Quality:</strong> Custom fields and validation rules ensure accurate, relevant data</li>
<li><strong>Enhanced Productivity:</strong> Automated workflows that match your processes save time and reduce errors</li>
<li><strong>Scalable Growth:</strong> Systems that grow with your business without requiring complete overhauls</li>
</ul>

<h2>Canadian Business Compliance</h2>

<p>For Canadian businesses, CRM systems must comply with PIPEDA and provincial privacy regulations while supporting your growth objectives.</p>

<p>Ready to implement a CRM system tailored to your business? Contact Social Dots for personalized CRM consulting and implementation.</p>''',
                'tags': ['CRM Systems', 'Business Solutions', 'Personalized CRM', 'Process Automation'],
                'meta_description': 'Discover how personalized CRM systems can transform your business processes, improve customer relationships, and drive sustainable growth.'
            },
            {
                'title': 'AI Callers: Revolutionizing Inbound and Outbound Communication',
                'slug': 'ai-callers-revolutionizing-communication',
                'excerpt': 'Explore how AI-powered calling systems are transforming business communication, improving efficiency while maintaining the human touch customers expect.',
                'content': '''<h1>AI Callers: Revolutionizing Inbound and Outbound Communication</h1>

<p>AI calling technology is transforming how businesses handle phone communications. From appointment scheduling to customer support, AI callers provide efficient, consistent service while freeing up human agents for more complex interactions.</p>

<h2>The Evolution of Business Communication</h2>

<p>Traditional phone systems often struggle with high call volumes, after-hours support, and consistent service quality. AI callers address these challenges while maintaining the personal connection customers value.</p>

<h2>Key Applications</h2>

<ul>
<li><strong>Appointment Scheduling:</strong> Automated booking and rescheduling with calendar integration</li>
<li><strong>Lead Qualification:</strong> Initial screening and information gathering for sales teams</li>
<li><strong>Customer Support:</strong> 24/7 assistance for common inquiries and issue resolution</li>
<li><strong>Follow-up Calls:</strong> Automated follow-ups for surveys, reminders, and check-ins</li>
</ul>

<h2>Benefits for Canadian Businesses</h2>

<ul>
<li>Reduce operational costs while improving service quality</li>
<li>Handle multiple languages common in Canadian markets</li>
<li>Ensure consistent service during peak times and holidays</li>
<li>Maintain compliance with Canadian telecommunications regulations</li>
</ul>

<p>Ready to implement AI calling solutions for your business? Contact Social Dots for AI communication strategy and implementation.</p>''',
                'tags': ['AI Call Automation', 'Inbound Communication', 'Outbound Communication', 'Customer Service'],
                'meta_description': 'Explore how AI-powered calling systems are transforming business communication, improving efficiency while maintaining the human touch customers expect.'
            },
            {
                'title': 'Why Choosing the Right Digital Marketing Agency in Canada Matters More Than Ever',
                'slug': 'choosing-right-digital-marketing-agency-canada',
                'excerpt': 'Discover the key factors that make a digital marketing agency truly effective for Canadian businesses and how to choose the right partner for growth.',
                'content': '''<h1>Why Choosing the Right Digital Marketing Agency in Canada Matters More Than Ever</h1>

<p>The Canadian digital marketing landscape is unique, with distinct cultural nuances, regulatory requirements, and market dynamics. Choosing the right agency partner can make the difference between marketing success and wasted investment.</p>

<h2>Understanding the Canadian Market</h2>

<p>Canada's diverse market includes bilingual requirements, cultural considerations across regions, and specific compliance needs that international agencies may not fully understand.</p>

<h2>What to Look for in a Canadian Digital Marketing Agency</h2>

<ul>
<li><strong>Local Market Expertise:</strong> Deep understanding of Canadian consumer behavior and preferences</li>
<li><strong>Compliance Knowledge:</strong> Familiarity with PIPEDA, CASL, and provincial regulations</li>
<li><strong>Cultural Sensitivity:</strong> Ability to create campaigns that resonate across Canada's diverse population</li>
<li><strong>Proven Results:</strong> Track record with Canadian businesses and market conditions</li>
</ul>

<h2>The Social Dots Advantage</h2>

<p>As a Toronto-based agency, Social Dots combines 15+ years of Canadian market experience with cutting-edge AI and automation technologies. We understand what works in the Canadian market and why.</p>

<p>Ready to partner with a digital marketing agency that truly understands Canada? Contact Social Dots for a consultation tailored to your Canadian market needs.</p>''',
                'tags': ['Digital Marketing Agency', 'Canadian Business', 'Marketing Strategy', 'Local Expertise'],
                'meta_description': 'Discover the key factors that make a digital marketing agency truly effective for Canadian businesses and how to choose the right partner for growth.'
            },
            {
                'title': 'How We Built a WhatsApp Automation System Using n8n for Canadian Businesses',
                'slug': 'whatsapp-automation-system-n8n-canadian-businesses',
                'excerpt': 'Learn how we developed a comprehensive WhatsApp automation system using n8n to help Canadian businesses streamline customer communication and boost engagement.',
                'content': '''<h1>How We Built a WhatsApp Automation System Using n8n for Canadian Businesses</h1>

<p>WhatsApp has become an essential communication channel for Canadian businesses. We developed a comprehensive automation system using n8n that helps businesses manage WhatsApp communications efficiently while maintaining personal connections with customers.</p>

<h2>The Challenge</h2>

<p>Canadian businesses were struggling to manage high volumes of WhatsApp messages while providing timely, personalized responses. Manual management was becoming unsustainable as customer expectations for quick responses increased.</p>

<h2>Our n8n-Powered Solution</h2>

<p>Using n8n's visual workflow automation platform, we created a system that:</p>

<ul>
<li><strong>Automated Responses:</strong> Instant replies to common inquiries with personalized information</li>
<li><strong>Lead Qualification:</strong> Automated collection and organization of customer information</li>
<li><strong>CRM Integration:</strong> Seamless sync with existing customer management systems</li>
<li><strong>Escalation Rules:</strong> Smart routing of complex inquiries to appropriate team members</li>
</ul>

<h2>Results for Canadian Businesses</h2>

<ul>
<li>80% reduction in response time for common inquiries</li>
<li>60% increase in customer engagement rates</li>
<li>Significant cost savings on customer service operations</li>
<li>Improved customer satisfaction scores</li>
</ul>

<h2>Compliance Considerations</h2>

<p>Our WhatsApp automation system ensures compliance with Canadian privacy laws and messaging regulations while providing businesses with powerful automation capabilities.</p>

<p>Interested in implementing WhatsApp automation for your Canadian business? Contact Social Dots to learn more about our n8n-powered solutions.</p>''',
                'tags': ['WhatsApp Automation', 'n8n', 'Business Automation', 'Customer Communication'],
                'meta_description': 'Learn how we developed a comprehensive WhatsApp automation system using n8n to help Canadian businesses streamline customer communication and boost engagement.'
            },
            {
                'title': 'AI Development Company in Canada: Leading Innovation in the Great White North',
                'slug': 'ai-development-company-canada-innovation',
                'excerpt': 'Explore Canada\'s growing AI development landscape and discover why Canadian AI companies are leading global innovation in artificial intelligence solutions.',
                'content': '''<h1>AI Development Company in Canada: Leading Innovation in the Great White North</h1>

<p>Canada has emerged as a global leader in artificial intelligence development, with cities like Toronto, Montreal, and Vancouver becoming major AI innovation hubs. Canadian AI companies are at the forefront of developing practical, ethical AI solutions for businesses worldwide.</p>

<h2>Canada\'s AI Advantage</h2>

<p>Several factors make Canada a premier destination for AI development:</p>

<ul>
<li><strong>World-Class Research:</strong> Leading universities and research institutions</li>
<li><strong>Government Support:</strong> Significant investment in AI research and development</li>
<li><strong>Ethical Approach:</strong> Strong focus on responsible AI development</li>
<li><strong>Diverse Talent Pool:</strong> Multicultural workforce bringing global perspectives</li>
</ul>

<h2>AI Innovation Across Industries</h2>

<p>Canadian AI companies are developing solutions across multiple sectors:</p>

<ul>
<li>Healthcare: Diagnostic tools and treatment optimization</li>
<li>Finance: Risk assessment and fraud detection</li>
<li>Retail: Customer experience and inventory optimization</li>
<li>Manufacturing: Process automation and predictive maintenance</li>
</ul>

<h2>Why Choose a Canadian AI Development Partner</h2>

<ul>
<li>Strong privacy and data protection standards</li>
<li>Ethical AI development practices</li>
<li>Proven track record in delivering practical solutions</li>
<li>Understanding of both North American and global markets</li>
</ul>

<p>Ready to partner with a leading Canadian AI development company? Contact Social Dots to explore AI solutions tailored to your business needs.</p>''',
                'tags': ['AI Development', 'Canadian Technology', 'Innovation', 'Artificial Intelligence'],
                'meta_description': 'Explore Canada\'s growing AI development landscape and discover why Canadian AI companies are leading global innovation in artificial intelligence solutions.'
            }
        ]
        
        for blog_data in missing_blogs:
            blog_post, created = BlogPost.objects.get_or_create(
                slug=blog_data['slug'],
                defaults={
                    'title': blog_data['title'],
                    'author': admin_user,
                    'content': blog_data['content'],
                    'excerpt': blog_data['excerpt'],
                    'status': 'published',
                    'tags': blog_data['tags'],
                    'meta_description': blog_data['meta_description'],
                    'is_featured': False,
                    'published_at': datetime.now()
                }
            )
            if created:
                self.stdout.write(f'Created blog post: {blog_data["title"]}')
            else:
                self.stdout.write(f'Blog post already exists: {blog_data["title"]}')

    def add_missing_projects(self):
        """Add the projects that exist on live site but not in localhost"""
        self.stdout.write('Adding missing projects...')
        
        missing_projects = [
            {
                'title': 'CricketCadets - Sports Training Platform',
                'slug': 'cricketcadets-sports-training-platform',
                'client_name': 'CricketCadets Academy',
                'description': 'Comprehensive sports training and management platform for cricket coaching academies. Features player progress tracking, skill assessment, training schedules, and parent communication tools.',
                'technologies': ['React', 'Node.js', 'MongoDB', 'Video Analytics'],
                'portfolio_type': 'web'
            },
            {
                'title': 'Social Media Growth & Engagement Campaign',
                'slug': 'social-media-growth-engagement-campaign',
                'client_name': 'Various Clients',
                'description': 'Comprehensive social media growth strategy combining organic content creation, paid advertising, and engagement optimization across multiple platforms.',
                'technologies': ['Python', 'JavaScript', 'Meta Ads Manager', 'ChatGPT', 'Midjourney'],
                'portfolio_type': 'social'
            },
            {
                'title': 'AI-Powered WhatsApp Chat Automation',
                'slug': 'ai-whatsapp-chat-automation',
                'client_name': 'Social Dots Inc.',
                'description': 'Intelligent WhatsApp automation system that handles customer inquiries, lead qualification, and appointment scheduling while maintaining natural conversation flow.',
                'technologies': ['AI', 'WhatsApp Business API', 'Natural Language Processing', 'n8n'],
                'portfolio_type': 'ai'
            },
            {
                'title': 'Lawn Cleaning Services Website',
                'slug': 'lawn-cleaning-services-website',
                'client_name': 'Pull & Push Lawn',
                'description': 'Professional service website for lawn care and maintenance company featuring online booking, service area mapping, and customer portal for lawn care in the Greater Toronto Area.',
                'technologies': ['WordPress', 'Custom Development', 'Booking System', 'Google Maps'],
                'portfolio_type': 'web'
            },
            {
                'title': 'Barber Shop Website in Milton, Ontario',
                'slug': 'barber-shop-website-milton-ontario',
                'client_name': 'New Style Barber Shop',
                'description': 'Modern barbershop website with online appointment booking, service showcase, and customer management system for a growing barbershop in Milton, Ontario.',
                'technologies': ['React', 'Booking System', 'Payment Integration', 'Customer Management'],
                'portfolio_type': 'web'
            }
        ]
        
        for project_data in missing_projects:
            project, created = Project.objects.get_or_create(
                slug=project_data['slug'],
                defaults={
                    'title': project_data['title'],
                    'client_name': project_data['client_name'],
                    'description': project_data['description'],
                    'technologies': project_data['technologies'],
                    'portfolio_type': project_data['portfolio_type'],
                    'status': 'completed',
                    'is_featured': False,
                    'order': 0
                }
            )
            if created:
                self.stdout.write(f'Created project: {project_data["title"]}')
            else:
                self.stdout.write(f'Project already exists: {project_data["title"]}')