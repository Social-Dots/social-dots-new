from django import forms
from .models import Portfolio, PortfolioCategory

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'slug', 'description', 'category', 'content_type', 
                 'image', 'video_url', 'blog_link', 'technology_used', 'is_featured', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'technology_used': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field_name != 'is_featured' and field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
        
        # Make slug field optional as it will be auto-generated if empty
        self.fields['slug'].required = False
        
        # Set help text for image field
        self.fields['image'].help_text = 'Image will be uploaded to Cloudinary for optimized delivery'