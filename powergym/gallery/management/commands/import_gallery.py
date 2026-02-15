
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
        
        # 1. Import Gallery
        gallery_path = os.path.join(public_html, 'images', 'galeria')
        if os.path.exists(gallery_path):
            self.stdout.write(f"Scanning {gallery_path}...")
            for filename in os.listdir(gallery_path):
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    continue
                
                # Determine category
                category = 'elgym' # Default
                lower_name = filename.lower()
                
                if 'vest' in lower_name:
                    category = 'vestuarios'
                elif 'cardio' in lower_name:
                    category = 'cardio'
                elif 'muscu' in lower_name:
                    category = 'musculacion'
                elif 'elgym' in lower_name:
                    category = 'elgym'
                
                file_path = os.path.join(gallery_path, filename)
                
                # Check if exists to avoid dups (simple check by title)
                if GalleryPhoto.objects.filter(title=filename).exists():
                    self.stdout.write(f"Skipping {filename}, already exists")
                    continue
                
                try:
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

        # 2. Import Slider (Hero)
        slider_path = os.path.join(public_html, 'images', 'slider')
        if os.path.exists(slider_path):
            self.stdout.write(f"Scanning {slider_path}...")
            for filename in os.listdir(slider_path):
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
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
