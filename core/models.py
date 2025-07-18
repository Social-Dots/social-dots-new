from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from ckeditor_uploader.fields import RichTextUploadingField


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Social Dots Inc.")
    tagline = models.CharField(max_length=200, default="Empowering Canadian businesses to thrive in a constantly evolving digital world", blank=True)
    logo = models.CharField(max_length=200, blank=True, null=True, help_text="Logo file path")
    logo_dark = models.CharField(max_length=200, blank=True, null=True, help_text="Dark version of logo file path")
    favicon = models.CharField(max_length=200, blank=True, null=True, help_text="Favicon file path")
    phone = models.CharField(max_length=20, default="416-556-6961", blank=True)
    email = models.EmailField(default="hello@socialdots.ca", blank=True)
    contact_email = models.EmailField(default="ali@socialdots.ca", blank=True, help_text="Primary contact email")
    address = models.TextField(default="Toronto, Ontario, Canada", blank=True)
    website_url = models.URLField(default="https://socialdots.ca", blank=True)
    
    # Brand Colors
    primary_color = models.CharField(
        max_length=7, 
        default="#2563EB", 
        help_text="Primary Blue color",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code')]
    )
    secondary_color = models.CharField(
        max_length=7, 
        default="#1E40AF", 
        help_text="Secondary Blue color",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code')]
    )
    accent_color = models.CharField(
        max_length=7, 
        default="#3B82F6", 
        help_text="Accent Blue color",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code')]
    )
    
    # Social Media
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    
    # SEO & Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)
    meta_description = models.CharField(max_length=160, default="Strategic AI integration and comprehensive digital solutions for Canadian businesses. 15+ years of expertise in Salesforce, marketing automation, and business growth.", blank=True)
    
    # Business Information
    legal_name = models.CharField(max_length=200, default="Social Dots Inc.", blank=True)
    business_number = models.CharField(max_length=50, blank=True, help_text="Canadian Business Number")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def clean(self):
        """Ensure only one site configuration exists"""
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValidationError("Only one site configuration is allowed")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.CharField(max_length=200, blank=True, null=True, help_text="Team member photo path")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.position}"


class ServicePricingOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price in CAD"
    )
    period = models.CharField(max_length=20, choices=[
        ('one_time', 'One Time'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], default='one_time')
    features = models.JSONField(default=list, blank=True)
    is_popular = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='pricing_options')
    stripe_price_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.period} - {self.service.title}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextUploadingField()
    short_description = models.CharField(max_length=300, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Base price in CAD"
    )
    price_type = models.CharField(max_length=20, choices=[
        ('fixed', 'Fixed Price'),
        ('hourly', 'Per Hour'),
        ('monthly', 'Per Month'),
        ('custom', 'Custom Quote'),
        ('tiered', 'Tiered Pricing')
    ], default='custom')
    features = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    stripe_price_id = models.CharField(max_length=100, blank=True)
    service_type = models.CharField(max_length=50, choices=[
        ('social_media', 'Social Media'),
        ('seo', 'SEO'),
        ('blog', 'Blog'),
        ('video', 'Video'),
        ('other', 'Other')
    ], default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def clean(self):
        """Business rule validation for Social Dots services"""
        if self.price_type not in ['custom', 'tiered'] and not self.price:
            raise ValidationError("Price is required for non-custom pricing types")
        
        if self.price and self.price_type == 'custom':
            raise ValidationError("Custom quote services should not have a fixed price")
            
        # Ensure Salesforce and AI services are marked as featured (core offerings)
        core_services = ['salesforce', 'ai', 'strategy']
        if any(term in self.title.lower() for term in core_services):
            if not self.is_featured:
                self.is_featured = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_period = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one_time', 'One Time')
    ], default='monthly')
    features = models.JSONField(default=list)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    stripe_price_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.price_period}"


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    client_name = models.CharField(max_length=100, blank=True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    cloudinary_image_id = models.CharField(max_length=255, blank=True, null=True)
    gallery = models.JSONField(default=list, blank=True, help_text="List of image URLs")
    technologies = models.JSONField(default=list, blank=True)
    portfolio_type = models.CharField(
        max_length=20,
        choices=[
            ('website', 'Website Portfolio'),
            ('ai', 'AI Automation'),
            ('social', 'Social Media Content'),
            ('other', 'Other')
        ],
        default='other'
    )
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Handle image upload to Cloudinary if image field has a file
        if self.image and not self.cloudinary_image_id and hasattr(self.image, 'file') and not self.image.name.endswith('/'): 
            # Check if the image is not empty and not a directory
            if hasattr(self.image, 'size') and self.image.size > 0:
                from .cloudinary_utils import upload_image
                try:
                    # Upload the image to Cloudinary
                    result = upload_image(self.image, folder=f'project_images/{self.slug}')
                    # Store the Cloudinary public ID
                    self.cloudinary_image_id = result['public_id']
                except Exception as e:
                    # Log the error but continue saving the model
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error uploading image to Cloudinary: {e}")
            else:
                # If the image file is empty, set the image field to None to prevent upload errors
                self.image = None
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    excerpt = models.TextField(max_length=300, blank=True)
    content = RichTextUploadingField()
    featured_image = models.CharField(max_length=200, blank=True, null=True, help_text="Blog post featured image path")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tags = models.JSONField(default=list, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Handle image upload to Cloudinary if image field has a file
        if self.image and not self.cloudinary_image_id and hasattr(self.image, 'file') and not self.image.name.endswith('/'): 
            # Check if the image is not empty and not a directory
            if hasattr(self.image, 'size') and self.image.size > 0:
                from .cloudinary_utils import upload_image
                try:
                    # Upload the image to Cloudinary
                    result = upload_image(self.image, folder=f'portfolio_images/{self.slug}')
                    # Store the Cloudinary public ID
                    self.cloudinary_image_id = result['public_id']
                except Exception as e:
                    # Log the error but continue saving the model
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Error uploading image to Cloudinary: {e}")
            else:
                # If the image file is empty, set the image field to None to prevent upload errors
                self.image = None
                
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100, blank=True)
    client_company = models.CharField(max_length=100, blank=True)
    client_image = models.CharField(max_length=200, blank=True, null=True, help_text="Client photo path")
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    service_interest = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=50, blank=True, help_text="Where the lead came from")
    budget = models.CharField(max_length=50, blank=True)
    timeline = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    order_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    service_name = models.CharField(max_length=200)
    pricing_plan_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='CAD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    stripe_session_id = models.CharField(max_length=100, blank=True)
    frappe_document_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_id:
            import uuid
            self.order_id = f"SD{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    attendee_name = models.CharField(max_length=100, blank=True)
    attendee_email = models.EmailField(blank=True)
    attendee_phone = models.CharField(max_length=20, blank=True)
    google_event_id = models.CharField(max_length=100, blank=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Portfolio Category"
        verbose_name_plural = "Portfolio Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

from django.core.validators import FileExtensionValidator

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    cloudinary_image_id = models.CharField(max_length=255, blank=True, null=True, help_text="Cloudinary public ID for the image")
    category = models.ForeignKey(PortfolioCategory, on_delete=models.CASCADE, related_name='portfolios')
    
    content_type = models.CharField(max_length=20, choices=[
        ('post', 'Post'),
        ('video', 'Video'),
        ('blog', 'Blog'),
        ('email', 'Email'),
        ('technology', 'Technology')
    ], default='post')

    portfolio_type = models.CharField(max_length=20, choices=[
        ('website', 'Website Portfolio'),
        ('ai', 'AI Automation'),
        ('social', 'Social Media Content'),
        ('other', 'Other')
    ], default='other')

    video_url = models.URLField(blank=True, help_text="YouTube video URL")
    blog_link = models.URLField(blank=True, help_text="Link to blog post")
    technology_used = models.JSONField(default=list, blank=True, help_text="List of technologies used")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio_detail', kwargs={'slug': self.slug})

    def get_cloudinary_url(self, **options):
        """
        Get the Cloudinary URL for the image with optional transformations
        """
        if self.cloudinary_image_id:
            from .cloudinary_utils import get_optimized_url
            return get_optimized_url(self.cloudinary_image_id, **options)
        elif self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.title


class AIAgentLog(models.Model):
    LOG_TYPES = [
        ('whatsapp', 'WhatsApp'),
        ('chatbot', 'Chatbot'),
        ('order_booking', 'Order Booking'),
        ('notification', 'Notification'),
    ]

    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    user_identifier = models.CharField(max_length=100, blank=True)
    message_content = models.TextField()
    response_content = models.TextField(blank=True)
    webhook_data = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default='processed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.log_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"