from django.shortcuts import render
from gallery.models import GalleryPhoto


def home(request):
    """Home page view with gallery integration"""
    # Get featured/recent photos for the landing
    featured_photos = GalleryPhoto.objects.filter(is_active=True, is_hero=False)[:12]
    
    # Get hero photos
    hero_photos = GalleryPhoto.objects.filter(is_active=True, is_hero=True).order_by('sort_order', '?')
    return render(request, 'landing/home.html', {
        'hero_photos': hero_photos,
        'featured_photos': featured_photos,
    })

def privacy(request):
    return render(request, 'landing/privacy.html')
