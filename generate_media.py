from pathlib import Path
from PIL import Image, ImageEnhance

ROOT = Path('/home/user/harvest')
ASSETS = ROOT / 'assets'

BASE_IMAGES = {
    'kitchen': ASSETS / 'kitchen-base.jpg',
    'planning': ASSETS / 'planning-base.jpg',
}

GALLERY_SPECS = [
    ('gallery-kitchen-1.jpg', 'kitchen', (0.00, 0.02, 1.00, 0.77), (1200, 900), 1.03, 1.01),
    ('gallery-kitchen-2.jpg', 'kitchen', (0.10, 0.08, 0.86, 0.84), (1200, 900), 1.02, 1.04),
    ('gallery-kitchen-3.jpg', 'kitchen', (0.18, 0.00, 0.96, 0.78), (1200, 900), 1.04, 0.98),
    ('gallery-planning-1.jpg', 'planning', (0.00, 0.00, 1.00, 0.75), (1200, 900), 1.03, 1.0),
    ('gallery-planning-2.jpg', 'planning', (0.00, 0.10, 1.00, 0.86), (1200, 900), 1.02, 1.03),
    ('gallery-planning-3.jpg', 'planning', (0.00, 0.20, 1.00, 0.95), (1200, 900), 1.01, 1.02),
]

SERVICE_SPECS = [
    ('kitchen-hero.jpg', 'kitchen', (0.00, 0.00, 1.00, 0.82), (1600, 1000), 1.03, 1.01),
    ('bathroom-hero.jpg', 'planning', (0.00, 0.04, 1.00, 0.84), (1600, 1000), 1.02, 1.02),
    ('flooring-hero.jpg', 'kitchen', (0.04, 0.18, 0.96, 0.88), (1600, 1000), 1.04, 0.99),
    ('interior-painting-hero.jpg', 'planning', (0.00, 0.12, 1.00, 0.92), (1600, 1000), 1.02, 1.03),
    ('full-home-renovation-hero.jpg', 'kitchen', (0.08, 0.02, 0.98, 0.86), (1600, 1000), 1.02, 1.0),
]


def crop_and_export(base_path: Path, crop_box, size, brightness, color, out_path: Path):
    image = Image.open(base_path).convert('RGB')
    w, h = image.size
    left = int(crop_box[0] * w)
    top = int(crop_box[1] * h)
    right = int(crop_box[2] * w)
    bottom = int(crop_box[3] * h)
    cropped = image.crop((left, top, right, bottom))
    cropped = cropped.resize(size, Image.Resampling.LANCZOS)
    cropped = ImageEnhance.Brightness(cropped).enhance(brightness)
    cropped = ImageEnhance.Color(cropped).enhance(color)
    cropped.save(out_path, format='JPEG', quality=88, optimize=True, progressive=True)
    print(f'Wrote {out_path.name}')


def main():
    for file_name, base_key, crop_box, size, brightness, color in GALLERY_SPECS + SERVICE_SPECS:
        crop_and_export(BASE_IMAGES[base_key], crop_box, size, brightness, color, ASSETS / file_name)


if __name__ == '__main__':
    main()
