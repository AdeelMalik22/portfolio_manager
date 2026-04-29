"""
Image Processing Service - Background removal and image merging with template themes
"""
from PIL import Image, ImageFilter
from io import BytesIO
import io
import numpy as np
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

# Lazy import rembg to avoid heavy compilation at startup
_rembg_loaded = False
_remove_func = None

def _lazy_load_rembg():
    """Lazy load rembg module"""
    global _rembg_loaded, _remove_func
    if not _rembg_loaded:
        try:
            from rembg import remove
            _remove_func = remove
            _rembg_loaded = True
        except ImportError:
            logger.warning("rembg not available, will use basic background removal")
            _rembg_loaded = True

# Template theme color configurations
TEMPLATE_THEMES = {
    'modern_corporate': {
        'primary': (26, 32, 46),      # Dark blue-gray
        'secondary': (45, 55, 72),    # Lighter blue-gray
        'accent': (255, 153, 0),      # Orange
    },
    'bold_dark_neon': {
        'primary': (10, 10, 10),      # Almost black
        'secondary': (30, 30, 30),    # Dark gray
        'accent': (0, 255, 255),      # Cyan neon
    },
    'clean_minimal': {
        'primary': (255, 255, 255),   # White
        'secondary': (240, 240, 240), # Off-white
        'accent': (51, 51, 51),       # Dark gray
    },
    'creative_vibrant': {
        'primary': (255, 87, 34),     # Deep orange
        'secondary': (255, 152, 0),   # Orange
        'accent': (76, 175, 80),      # Green
    },
    'dev_terminal': {
        'primary': (0, 0, 0),         # Black
        'secondary': (51, 51, 51),    # Dark gray
        'accent': (0, 255, 0),        # Neon green
    },
    'elegant_classic': {
        'primary': (44, 44, 44),      # Dark charcoal
        'secondary': (100, 100, 100), # Medium gray
        'accent': (192, 155, 85),     # Gold
    },
    'forest_dark': {
        'primary': (27, 51, 34),      # Dark green
        'secondary': (51, 102, 68),   # Medium green
        'accent': (144, 238, 144),    # Light green
    },
    'gradient_purple': {
        'primary': (103, 58, 183),    # Deep purple
        'secondary': (142, 68, 173),  # Medium purple
        'accent': (233, 30, 99),      # Pink
    },
    'indigo_modern': {
        'primary': (63, 81, 181),     # Indigo
        'secondary': (88, 86, 214),   # Medium indigo
        'accent': (255, 64, 129),     # Pink accent
    },
    'luxury_elegant': {
        'primary': (0, 0, 0),         # Black
        'secondary': (45, 45, 45),    # Very dark gray
        'accent': (218, 165, 32),     # Goldenrod
    },
    'minimalist_mono': {
        'primary': (255, 255, 255),   # White
        'secondary': (200, 200, 200), # Light gray
        'accent': (0, 0, 0),          # Black
    },
    'nature_green': {
        'primary': (56, 142, 60),     # Green
        'secondary': (102, 187, 106), # Light green
        'accent': (165, 214, 167),    # Pale green
    },
    'navy_business': {
        'primary': (13, 71, 161),     # Navy
        'secondary': (30, 136, 229),  # Medium blue
        'accent': (255, 193, 7),      # Amber
    },
    'ocean_blue': {
        'primary': (0, 150, 136),     # Teal
        'secondary': (38, 198, 218),  # Cyan
        'accent': (255, 235, 59),     # Yellow
    },
    'rose_minimal': {
        'primary': (255, 255, 255),   # White
        'secondary': (245, 245, 245), # Very light gray
        'accent': (194, 24, 91),      # Rose
    },
    'sidebar_layout': {
        'primary': (37, 211, 102),    # Green
        'secondary': (52, 152, 219),  # Blue
        'accent': (255, 193, 7),      # Amber
    },
}


class ImageProcessor:
    """Service for processing images with background removal and theme integration"""

    def __init__(self, template_slug='modern_corporate'):
        """Initialize processor with template theme"""
        self.template_slug = template_slug
        self.theme = TEMPLATE_THEMES.get(template_slug, TEMPLATE_THEMES['modern_corporate'])

    def remove_background(self, image_file):
        """
        Remove background from image using rembg (with fallback)
        Args:
            image_file: Django file object or file path
        Returns:
            PIL Image with transparent background
        """
        try:
            # Read image
            if hasattr(image_file, 'read'):
                image_data = image_file.read()
                image_file.seek(0)  # Reset file pointer
            else:
                with open(image_file, 'rb') as f:
                    image_data = f.read()

            image = Image.open(BytesIO(image_data))

            # Convert to RGBA if needed
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Try to use rembg if available
            _lazy_load_rembg()
            if _remove_func:
                try:
                    image_array = np.array(image)
                    output_array = _remove_func(image_array)
                    image = Image.fromarray(output_array)
                    logger.info(f"Successfully removed background using rembg")
                except Exception as e:
                    logger.warning(f"rembg failed, using fallback: {e}")
                    image = self._fallback_background_removal(image)
            else:
                # Fallback if rembg is not available
                image = self._fallback_background_removal(image)

            return image
        except Exception as e:
            logger.error(f"Error removing background: {e}")
            raise

    def _fallback_background_removal(self, image):
        """
        Fallback background removal using PIL only
        Removes solid background colors
        """
        try:
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Convert to array
            data = np.array(image)

            # Get the background color (assume it's the color at corners)
            corners = [
                data[0, 0],  # top-left
                data[0, -1],  # top-right
                data[-1, 0],  # bottom-left
                data[-1, -1],  # bottom-right
            ]

            # Find most common corner color
            from collections import Counter
            bg_color = Counter([tuple(c[:3]) for c in corners]).most_common(1)[0][0]

            # Create mask for background color (with tolerance)
            r, g, b = bg_color
            r_min, r_max = max(0, r - 50), min(255, r + 50)
            g_min, g_max = max(0, g - 50), min(255, g + 50)
            b_min, b_max = max(0, b - 50), min(255, b + 50)

            mask = (
                (data[:, :, 0] >= r_min) & (data[:, :, 0] <= r_max) &
                (data[:, :, 1] >= g_min) & (data[:, :, 1] <= g_max) &
                (data[:, :, 2] >= b_min) & (data[:, :, 2] <= b_max)
            )

            # Set background to transparent
            data[mask, 3] = 0

            image = Image.fromarray(data)
            logger.info("Successfully removed background using fallback method")
            return image
        except Exception as e:
            logger.warning(f"Fallback background removal also failed: {e}, returning original")
            return image

    def create_themed_background(self, width, height):
        """
        Create a themed gradient background
        Args:
            width: Image width
            height: Image height
        Returns:
            PIL Image with gradient background
        """
        try:
            primary = self.theme['primary']
            secondary = self.theme['secondary']

            # Create gradient background
            background = Image.new('RGB', (width, height), primary)
            pixels = background.load()

            # Create vertical gradient
            for y in range(height):
                ratio = y / height
                r = int(primary[0] + (secondary[0] - primary[0]) * ratio)
                g = int(primary[1] + (secondary[1] - primary[1]) * ratio)
                b = int(primary[2] + (secondary[2] - primary[2]) * ratio)

                for x in range(width):
                    pixels[x, y] = (r, g, b)

            logger.info(f"Created themed background with colors {primary} to {secondary}")
            return background
        except Exception as e:
            logger.error(f"Error creating background: {e}")
            raise

    def merge_image_with_background(self, foreground_image, bg_width=600, bg_height=600):
        """
        Merge foreground image (with transparent background) onto themed background
        Args:
            foreground_image: PIL Image with transparent background
            bg_width: Background width
            bg_height: Background height
        Returns:
            PIL Image with foreground merged on background
        """
        try:
            # Create themed background
            background = self.create_themed_background(bg_width, bg_height)

            # Ensure foreground is RGBA
            if foreground_image.mode != 'RGBA':
                foreground_image = foreground_image.convert('RGBA')

            # Calculate dimensions and position
            fg_ratio = foreground_image.width / foreground_image.height

            # Scale foreground to fit 70% of background height
            target_height = int(bg_height * 0.7)
            target_width = int(target_height * fg_ratio)

            # If too wide, scale by width instead
            if target_width > int(bg_width * 0.8):
                target_width = int(bg_width * 0.8)
                target_height = int(target_width / fg_ratio)

            foreground_image = foreground_image.resize(
                (target_width, target_height),
                Image.Resampling.LANCZOS
            )

            # Center the image
            x_offset = (bg_width - target_width) // 2
            y_offset = (bg_height - target_height) // 2 - 30  # Slight upward bias

            # Paste foreground onto background
            background.paste(foreground_image, (x_offset, y_offset), foreground_image)

            # Add accent border
            accent_color = self.theme['accent']
            draw = Image.new('RGBA', (bg_width, bg_height), (0, 0, 0, 0))
            draw_pixels = draw.load()

            # Draw subtle accent line at bottom
            for x in range(bg_width):
                for y in range(bg_height - 5, bg_height):
                    draw_pixels[x, y] = accent_color + (150,)

            background = Image.alpha_composite(background.convert('RGBA'), draw)

            logger.info(f"Successfully merged image with themed background")
            return background
        except Exception as e:
            logger.error(f"Error merging image: {e}")
            raise

    def process_image(self, image_file, template_slug='modern_corporate'):
        """
        Complete image processing pipeline:
        1. Remove background
        2. Create themed background
        3. Merge images
        Args:
            image_file: Django file object or file path
            template_slug: Template theme slug
        Returns:
            PIL Image (merged result)
        """
        try:
            self.template_slug = template_slug
            self.theme = TEMPLATE_THEMES.get(template_slug, TEMPLATE_THEMES['modern_corporate'])

            # Remove background
            foreground = self.remove_background(image_file)

            # Merge with themed background
            result = self.merge_image_with_background(foreground)

            logger.info(f"Completed image processing for template: {template_slug}")
            return result
        except Exception as e:
            logger.error(f"Error in process_image: {e}")
            raise

    def save_processed_image(self, image_file, template_slug='modern_corporate'):
        """
        Process image and save as Django file
        Args:
            image_file: Django file object
            template_slug: Template theme slug
        Returns:
            Django ContentFile object
        """
        try:
            # Process the image
            processed_image = self.process_image(image_file, template_slug)

            # Save to file
            output = io.BytesIO()
            processed_image = processed_image.convert('RGB')  # Convert RGBA to RGB
            processed_image.save(output, format='PNG')
            output.seek(0)

            # Create Django ContentFile
            filename = f"processed_profile_{template_slug}.png"
            return ContentFile(output.read(), name=filename)
        except Exception as e:
            logger.error(f"Error saving processed image: {e}")
            raise

