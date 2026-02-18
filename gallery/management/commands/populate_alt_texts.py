from django.core.management.base import BaseCommand
from gallery.models import GalleryPhoto

class Command(BaseCommand):
    help = 'Populates empty alt_text fields in GalleryPhoto with default values'

    def handle(self, *args, **kwargs):
        photos = GalleryPhoto.objects.filter(alt_text__exact='') | GalleryPhoto.objects.filter(alt_text__isnull=True)
        count = photos.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No photos found with empty alt_text.'))
            return

        self.stdout.write(f'Found {count} photos with empty alt_text. Updating...')

        for photo in photos:
            # Generate alt text: "PowerGym - [Title] ([Category])"
            # Title is usually something like "DSC01234", so maybe just Category is safer if title is ugly.
            # But the user said "descripciones genéricas", so let's use the format:
            # "PowerGym - [Category] - [Title]"
            
            clean_category = photo.get_category_display()
            new_top_text = f"PowerGym - {clean_category} - {photo.title}"
            
            photo.alt_text = new_top_text
            photo.save(update_fields=['alt_text'])
            self.stdout.write(f'Updated: {photo.id} -> {new_top_text}')

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} photos.'))
