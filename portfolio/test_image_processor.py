#!/usr/bin/env python
"""
Test script for image processing functionality
Run with: python manage.py shell < portfolio/test_image_processor.py
"""

import os
from django.core.files.storage import default_storage
from portfolio.models import Portfolio, PublicPortfolio, PortfolioTemplate
from portfolio.image_processor import ImageProcessor, TEMPLATE_THEMES

def test_image_processor():
    """Test the image processor with various scenarios"""

    print("=" * 80)
    print("IMAGE PROCESSOR TEST SUITE")
    print("=" * 80)

    # Test 1: Available themes
    print("\n[TEST 1] Available Themes")
    print("-" * 80)
    themes = list(TEMPLATE_THEMES.keys())
    print(f"Found {len(themes)} templates:")
    for theme in themes:
        colors = TEMPLATE_THEMES[theme]
        print(f"  • {theme}")
        print(f"    Primary: RGB{colors['primary']}")
        print(f"    Secondary: RGB{colors['secondary']}")
        print(f"    Accent: RGB{colors['accent']}")

    # Test 2: Initialize processor
    print("\n[TEST 2] Initialize ImageProcessor")
    print("-" * 80)
    try:
        processor = ImageProcessor(template_slug='modern_corporate')
        print("✓ Processor initialized successfully")
        print(f"  Theme: {processor.template_slug}")
        print(f"  Theme colors: {processor.theme}")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return

    # Test 3: Theme switching
    print("\n[TEST 3] Theme Switching")
    print("-" * 80)
    try:
        for theme_slug in ['bold_dark_neon', 'clean_minimal', 'forest_dark']:
            processor = ImageProcessor(template_slug=theme_slug)
            print(f"✓ Switched to {theme_slug}")
    except Exception as e:
        print(f"✗ Theme switching failed: {e}")

    # Test 4: Background generation
    print("\n[TEST 4] Generate Themed Backgrounds")
    print("-" * 80)
    try:
        processor = ImageProcessor(template_slug='modern_corporate')
        background = processor.create_themed_background(600, 600)
        print(f"✓ Generated background: {background.size} {background.mode}")
        print(f"  Format: {background.format}")
    except Exception as e:
        print(f"✗ Background generation failed: {e}")

    # Test 5: List available portfolios
    print("\n[TEST 5] Available Portfolios and Templates")
    print("-" * 80)

    templates_count = PortfolioTemplate.objects.filter(is_active=True).count()
    portfolios_count = Portfolio.objects.count()
    public_portfolios_count = PublicPortfolio.objects.count()

    print(f"Active Templates: {templates_count}")
    print(f"Portfolios: {portfolios_count}")
    print(f"Public Portfolios: {public_portfolios_count}")

    # Test 6: Check existing processed images
    print("\n[TEST 6] Processed Images in Database")
    print("-" * 80)

    portfolios_with_processed = Portfolio.objects.exclude(processed_profile_image='').count()
    public_with_processed = PublicPortfolio.objects.exclude(processed_profile_image='').count()

    print(f"Portfolios with processed images: {portfolios_with_processed}")
    print(f"Public portfolios with processed images: {public_with_processed}")

    # Test 7: Show recommendations
    print("\n[TEST 7] Recommendations")
    print("-" * 80)
    print("""
Steps to test image processing:

1. Via Web Dashboard:
   - Navigate to Dashboard → Edit Portfolio
   - Upload a profile image
   - Click "🎨 Process Image" button
   - Review side-by-side comparison
   - Save portfolio

2. Via API:
   curl -X POST \\
     -H "Authorization: Bearer YOUR_TOKEN" \\
     -F "image=@/path/to/image.jpg" \\
     -F "template_slug=modern_corporate" \\
     http://localhost:8000/api/my-portfolio/process-image/

3. Via Python:
   from portfolio.image_processor import ImageProcessor
   processor = ImageProcessor()
   processed = processor.process_image(image_file, 'modern_corporate')

Best Practices:
✓ Use high-quality images with clear subjects
✓ Ensure good contrast between subject and background
✓ Supported formats: JPG, PNG, GIF, BMP, WEBP
✓ Try different templates to find the best match
✓ Check processed_profile_image field in portfolio data
    """)

    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    test_image_processor()

