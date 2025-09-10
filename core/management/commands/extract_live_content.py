from django.core.management.base import BaseCommand
from django.core.management import call_command
from core.models import BlogPost, Project, Service, Portfolio
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os


class Command(BaseCommand):
    help = 'Extract content from live Vercel site and sync to localhost'

    def __init__(self):
        super().__init__()
        self.base_url = 'https://social-dots-new.vercel.app'
        self.extracted_data = {
            'blog_posts': [],
            'projects': [],
            'services': []
        }

    def handle(self, *args, **options):
        self.stdout.write('Starting live site content extraction...')
        
        try:
            # Extract blog posts
            self.extract_blog_posts()
            
            # Extract portfolio/projects
            self.extract_projects()
            
            # Extract services
            self.extract_services()
            
            # Save extracted data to JSON files
            self.save_extracted_data()
            
            # Import the data into localhost database
            self.import_to_database()
            
            self.stdout.write('Live content extraction and sync completed!')
            
        except Exception as e:
            self.stdout.write(f'Error during extraction: {str(e)}')
            raise e

    def extract_blog_posts(self):
        """Extract all blog posts from live site"""
        self.stdout.write('Extracting blog posts...')
        
        try:
            # Get blog listing page
            response = requests.get(f'{self.base_url}/blog/', timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find blog post links
            blog_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/blog/' in href and href != '/blog/' and not href.endswith('/blog/'):
                    if href.startswith('/'):
                        href = self.base_url + href
                    blog_links.append(href)
            
            self.stdout.write(f'Found {len(blog_links)} blog post links')
            
            # Extract each blog post
            for i, blog_url in enumerate(blog_links, 1):
                self.stdout.write(f'Extracting blog post {i}/{len(blog_links)}: {blog_url}')
                try:
                    self.extract_single_blog_post(blog_url)
                except Exception as e:
                    self.stdout.write(f'Warning: Error extracting blog post {blog_url}: {str(e)}')
                    continue
                    
        except Exception as e:
            self.stdout.write(f'Error extracting blog posts: {str(e)}')

    def extract_single_blog_post(self, blog_url):
        """Extract a single blog post"""
        response = requests.get(blog_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = None
        title_tags = soup.find_all(['h1', 'title'])
        for tag in title_tags:
            if tag.get_text().strip():
                title = tag.get_text().strip()
                break
        
        if not title:
            title = "Untitled Post"
            
        # Create slug from title
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug).strip('-')
        
        # Extract content
        content = ""
        content_selectors = [
            '.blog-content', '.post-content', '.content', 
            'main', 'article', '.blog-post'
        ]
        
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                content = str(content_div)
                break
        
        if not content:
            # Fallback to body content
            body = soup.find('body')
            if body:
                content = str(body)
        
        # Extract excerpt (first paragraph or truncated content)
        excerpt = ""
        if content:
            text_content = BeautifulSoup(content, 'html.parser').get_text()
            # Get first 200 characters
            excerpt = text_content[:200].strip()
            if len(text_content) > 200:
                excerpt += "..."
        
        # Extract tags from meta or content
        tags = []
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            tags = [tag.strip() for tag in meta_keywords.get('content', '').split(',')]
        
        # Extract meta description
        meta_desc = ""
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            meta_desc = meta_description.get('content', '')
        
        blog_data = {
            'title': title,
            'slug': slug,
            'content': content,
            'excerpt': excerpt,
            'tags': tags,
            'meta_description': meta_desc,
            'url': blog_url
        }
        
        self.extracted_data['blog_posts'].append(blog_data)

    def extract_projects(self):
        """Extract projects from live site portfolio"""
        self.stdout.write('Extracting projects...')
        
        try:
            response = requests.get(f'{self.base_url}/portfolio/', timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find project cards or sections
            project_elements = soup.find_all(['div', 'article'], 
                                           class_=re.compile(r'(project|portfolio|card)', re.I))
            
            for element in project_elements:
                try:
                    self.extract_single_project(element)
                except Exception as e:
                    self.stdout.write(f'Warning: Error extracting project: {str(e)}')
                    continue
                    
        except Exception as e:
            self.stdout.write(f'Error extracting projects: {str(e)}')

    def extract_single_project(self, element):
        """Extract a single project from HTML element"""
        # Extract title
        title = ""
        title_tags = element.find_all(['h1', 'h2', 'h3', 'h4'])
        for tag in title_tags:
            text = tag.get_text().strip()
            if text and len(text) > 3:  # Avoid empty or very short titles
                title = text
                break
        
        if not title:
            return  # Skip if no title found
        
        # Create slug
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug).strip('-')
        
        # Extract description
        description = ""
        text_elements = element.find_all(['p', 'div'], 
                                        class_=re.compile(r'(description|content|summary)', re.I))
        for elem in text_elements:
            text = elem.get_text().strip()
            if len(text) > 20:  # Avoid very short descriptions
                description = text
                break
        
        # Extract client name
        client_name = ""
        client_elements = element.find_all(text=re.compile(r'(client|for)\s*:?\s*([^\n]+)', re.I))
        if client_elements:
            match = re.search(r'(client|for)\s*:?\s*([^\n]+)', str(client_elements[0]), re.I)
            if match:
                client_name = match.group(2).strip()
        
        # Extract technologies
        technologies = []
        tech_text = element.get_text()
        common_techs = ['React', 'Python', 'JavaScript', 'Node.js', 'Django', 'AI', 'Machine Learning', 
                       'TensorFlow', 'ChatGPT', 'Salesforce', 'HubSpot', 'Shopify', 'AWS']
        
        for tech in common_techs:
            if tech.lower() in tech_text.lower():
                technologies.append(tech)
        
        # Determine portfolio type
        portfolio_type = "other"
        if any(word in title.lower() for word in ['ai', 'artificial intelligence', 'machine learning']):
            portfolio_type = "ai"
        elif any(word in title.lower() for word in ['website', 'web', 'design']):
            portfolio_type = "web"
        elif any(word in title.lower() for word in ['social', 'media', 'content']):
            portfolio_type = "social"
        
        project_data = {
            'title': title,
            'slug': slug,
            'description': description,
            'client_name': client_name,
            'technologies': technologies,
            'portfolio_type': portfolio_type
        }
        
        self.extracted_data['projects'].append(project_data)

    def extract_services(self):
        """Extract services from live site"""
        self.stdout.write('Extracting services...')
        
        try:
            # Try different service page URLs
            service_urls = ['/services/', '/services', '/#services', '/']
            
            for url in service_urls:
                try:
                    response = requests.get(f'{self.base_url}{url}', timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find service sections
                    service_elements = soup.find_all(['div', 'section'], 
                                                   class_=re.compile(r'service', re.I))
                    
                    for element in service_elements:
                        self.extract_single_service(element)
                        
                    if service_elements:
                        break  # Found services, no need to try other URLs
                        
                except Exception as e:
                    self.stdout.write(f'Warning: Could not extract from {url}: {str(e)}')
                    continue
                    
        except Exception as e:
            self.stdout.write(f'Error extracting services: {str(e)}')

    def extract_single_service(self, element):
        """Extract a single service from HTML element"""
        # Extract title
        title = ""
        title_tags = element.find_all(['h1', 'h2', 'h3', 'h4'])
        for tag in title_tags:
            text = tag.get_text().strip()
            if text and len(text) > 3:
                title = text
                break
        
        if not title:
            return
        
        # Create slug
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug).strip('-')
        
        # Extract description
        description = ""
        text_elements = element.find_all(['p', 'div'])
        for elem in text_elements:
            text = elem.get_text().strip()
            if len(text) > 20 and text != title:
                description = text
                break
        
        service_data = {
            'title': title,
            'slug': slug,
            'description': description
        }
        
        self.extracted_data['services'].append(service_data)

    def save_extracted_data(self):
        """Save extracted data to JSON files"""
        self.stdout.write('Saving extracted data to JSON files...')
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        # Save to live_site_content.json
        output_file = os.path.join(base_dir, 'live_site_content.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(f'Data saved to {output_file}')
        self.stdout.write(f'Extracted: {len(self.extracted_data["blog_posts"])} blogs, {len(self.extracted_data["projects"])} projects, {len(self.extracted_data["services"])} services')

    def import_to_database(self):
        """Import extracted data to localhost database"""
        self.stdout.write('Importing data to localhost database...')
        
        try:
            # Get or create admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@socialdots.ca',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            
            # Import blog posts
            for blog_data in self.extracted_data['blog_posts']:
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
            
            # Import projects
            for project_data in self.extracted_data['projects']:
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
            
            self.stdout.write('Database import completed!')
            
        except Exception as e:
            self.stdout.write(f'Error importing to database: {str(e)}')
            raise e