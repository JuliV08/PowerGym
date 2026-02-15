
from django.core.management.base import BaseCommand
from gallery.models import GalleryPhoto
from PIL import Image

class Command(BaseCommand):
    help = 'Filter hero images by resolution'

    def handle(self, *args, **options):
        hero_photos = GalleryPhoto.objects.filter(is_hero=True)
        
        valid_heroes = []
        
        for photo in hero_photos:
            try:
                with Image.open(photo.image.path) as img:
                    width, height = img.size
                    # Filter: Must be landscape and high res (e.g. width > 1920)
                    if width > 1920 and width > height:
                        valid_heroes.append((photo, width * height))
                    else:
                        photo.is_hero = False
                        photo.save()
                        self.stdout.write(f"Removed {photo.title} from hero (Low Res: {width}x{height})")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {photo.title}: {e}"))
        
        # Sort by resolution (desc) and keep top 8
        valid_heroes.sort(key=lambda x: x[1], reverse=True)
        
        # Keep top 8, remove others
        for i, (photo, resolution) in enumerate(valid_heroes):
            if i < 8:
                self.stdout.write(self.style.SUCCESS(f"Kept {photo.title} as hero ({resolution} px)"))
            else:
                photo.is_hero = False
                photo.save()
                self.stdout.write(f"Removed {photo.title} from hero (Exceeds limit of 8)")
