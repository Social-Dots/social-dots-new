from .models import SiteConfiguration

def site_config(request):
    """
    Context processor to add site_config to all templates.
    """
    try:
        config = SiteConfiguration.objects.first()
        return {'site_config': config}
    except Exception as e:
        # Return an empty dict if there's an error
        return {'site_config': None}