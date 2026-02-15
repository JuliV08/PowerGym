
from django.core.management.base import BaseCommand
from gallery.models import GalleryPhoto
from PIL import Image

class Command(BaseCommand):
    help = 'Check for black borders without numpy'

    def handle(self, *args, **options):
        # Check only active hero images
        photos = GalleryPhoto.objects.filter(is_hero=True)
        
        for photo in photos:
            try:
                with Image.open(photo.image.path) as img:
                    img = img.convert('RGB')
                    width, height = img.size
                    
                    # Helper function to get average brightness of a region
                    def get_avg_brightness(region):
                        pixels = list(region.getdata())
                        if not pixels: return 255
                        total_brightness = sum(sum(p) / 3 for p in pixels)
                        return total_brightness / len(pixels)

                    # crop(left, top, right, bottom)
                    top_bar = img.crop((0, 0, width, 50))
                    bottom_bar = img.crop((0, height-50, width, height))
                    left_bar = img.crop((0, 0, 50, height))
                    right_bar = img.crop((width-50, 0, width, height))
                    
                    top_b = get_avg_brightness(top_bar)
                    bottom_b = get_avg_brightness(bottom_bar)
                    left_b = get_avg_brightness(left_bar)
                    right_b = get_avg_brightness(right_bar)
                    
                    self.stdout.write(f"Checking {photo.title}:")
                    self.stdout.write(f"  Top: {top_b:.2f}")
                    self.stdout.write(f"  Bottom: {bottom_b:.2f}")
                    
                    # Threshold for "Black" (allow some compression noise)
                    if top_b < 10 or bottom_b < 10:
                         self.stdout.write(self.style.WARNING(f"POTENTIAL BLACK BORDERS in {photo.title}"))
                         if top_b < 5 or bottom_b < 5:
                             self.stdout.write(self.style.ERROR(f"Removing {photo.title} due to dark borders"))
                             photo.is_hero = False
                             photo.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error {photo.title}: {e}"))
