from django.shortcuts import render
from gallery.models import GalleryPhoto


def home_view(request):
    """Home page view with gallery integration"""
    # Get featured/recent photos for the landing
    featured_photos = GalleryPhoto.objects.filter(is_active=True)[:12]
    
    context = {
        'featured_photos': featured_photos,
    }
    
    return render(request, 'landing/home.html', context)
