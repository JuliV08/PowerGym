import os
from PIL import Image
from django.conf import settings

# Configuration
# Hero: High quality, large dimensions (4K friendly but optimized)
HERO_OPTS = {'max_width': 2560, 'quality': 90} 
# Gallery: Good quality, standard web dimensions
GALLERY_OPTS = {'max_width': 1600, 'quality': 85}

PUBLIC_HTML = os.path.join(os.getcwd(), 'public_html')

def optimize_folder(source_subpath, target_subpath, opts):
    source_dir = os.path.join(PUBLIC_HTML, source_subpath)
    target_dir = os.path.join(PUBLIC_HTML, target_subpath)
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    print(f"\nProcessing {source_subpath} -> {target_subpath}")
    print(f"Settings: Max Width {opts['max_width']}px, Quality {opts['quality']}%")
    
    files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    for filename in files:
        source_path = os.path.join(source_dir, filename)
        target_filename = os.path.splitext(filename)[0] + '.webp'
        target_path = os.path.join(target_dir, target_filename)
        
        try:
            with Image.open(source_path) as img:
                # Convert to RGB if necessary (e.g. PNG with alpha)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if larger than max_width
                if img.width > opts['max_width']:
                    ratio = opts['max_width'] / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((opts['max_width'], new_height), Image.Resampling.LANCZOS)
                    print(f"  Resized {filename}: {img.width}x{img.height} -> {opts['max_width']}x{new_height}")
                else:
                    print(f"  Processing {filename} (Original size: {img.width}x{img.height})")
                
                # Save as WebP
                img.save(target_path, 'WEBP', quality=opts['quality'])
                
                # Compare sizes
                original_size = os.path.getsize(source_path) / (1024*1024)
                new_size = os.path.getsize(target_path) / (1024*1024)
                print(f"  ✅ Saved: {target_filename} ({original_size:.2f}MB -> {new_size:.2f}MB)")
                
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")

if __name__ == '__main__':
    # Optimize Gallery
    optimize_folder(os.path.join('images', 'galeria'), os.path.join('images', 'galeria_webp'), GALLERY_OPTS)
    
    # Optimize Slider (Hero)
    optimize_folder(os.path.join('images', 'slider'), os.path.join('images', 'slider_webp'), HERO_OPTS)
