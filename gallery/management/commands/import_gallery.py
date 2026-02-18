
import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from gallery.models import GalleryPhoto

class Command(BaseCommand):
    help = 'Import images from public_html structure'

    def handle(self, *args, **options):
        # Base paths
        base_path = r'C:\Users\Villex\dev\PowerGym'
        public_html = os.path.join(base_path, 'public_html')
        
        # Categories mapping
        # vestuarios, cardio, elgym, musculacion
        
        # Import Gallery (WebP)
        gallery_path = os.path.join(public_html, 'images', 'galeria_webp')
        if os.path.exists(gallery_path):
            self.stdout.write(f"Scanning {gallery_path}...")
            for filename in os.listdir(gallery_path):
                if not filename.endswith('.webp'):
                    continue
                    
                # Category detection
                category = 'elgym' # Default
                lower_name = filename.lower()
                
                try:
                    file_path = os.path.join(gallery_path, filename)
                    with open(file_path, 'rb') as f:
                        photo = GalleryPhoto(
                            title=filename,
                            category=category,
                            is_active=True
                        )
                        photo.image.save(filename, File(f), save=True)
                        self.stdout.write(self.style.SUCCESS(f"Imported {filename} as {category}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import {filename}: {e}"))

        # Import Slider/Hero (WebP)
        slider_path = os.path.join(public_html, 'images', 'slider_webp')
        if os.path.exists(slider_path):
            self.stdout.write(f"Scanning {slider_path}...")
            for filename in os.listdir(slider_path):
                if not filename.endswith('.webp'):
                    continue
                
                if GalleryPhoto.objects.filter(title=f"Hero-{filename}").exists():
                    continue

                try:
                    with open(os.path.join(slider_path, filename), 'rb') as f:
                        photo = GalleryPhoto(
                            title=f"Hero-{filename}",
                            category='elgym', # Default category
                            is_active=True,
                            is_hero=True
                        )
                        photo.image.save(filename, File(f), save=True)
                        self.stdout.write(self.style.SUCCESS(f"Imported Hero {filename}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import hero {filename}: {e}"))
