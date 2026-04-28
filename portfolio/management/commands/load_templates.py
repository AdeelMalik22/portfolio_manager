from django.core.management.base import BaseCommand
from portfolio.models import PortfolioTemplate


class Command(BaseCommand):
    help = 'Load 20 portfolio templates into the database'

    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Minimalist Black & White',
                'slug': 'minimalist-bw',
                'description': 'Clean, elegant black and white portfolio. Perfect for minimalist design lovers.',
                'category': 'minimalist',
                'color_scheme': 'black-white',
                'template_file': 'portfolio_templates/template_1_minimalist.html',
                'order': 1,
            },
            {
                'name': 'Dark Modern Blue',
                'slug': 'dark-modern-blue',
                'description': 'Modern dark theme with vibrant blue accents. Great for developers and tech professionals.',
                'category': 'developer',
                'color_scheme': 'dark-blue',
                'template_file': 'portfolio_templates/template_2_dark_modern.html',
                'order': 2,
            },
            {
                'name': 'Gradient Purple',
                'slug': 'gradient-purple',
                'description': 'Stunning purple gradient background with modern layout.',
                'category': 'creative',
                'color_scheme': 'purple',
                'template_file': 'portfolio_templates/template_3_gradient_purple.html',
                'order': 3,
            },
            {
                'name': 'Corporate Blue',
                'slug': 'corporate-blue',
                'description': 'Professional corporate style with sidebar layout. Ideal for business professionals.',
                'category': 'corporate',
                'color_scheme': 'corporate-blue',
                'template_file': 'portfolio_templates/template_4_corporate_blue.html',
                'order': 4,
            },
            {
                'name': 'Creative Orange',
                'slug': 'creative-orange',
                'description': 'Bold orange and warm colors. Perfect for creative professionals and designers.',
                'category': 'creative',
                'color_scheme': 'orange',
                'template_file': 'portfolio_templates/template_5_creative_orange.html',
                'order': 5,
            },
            {
                'name': 'Teal Gradient',
                'slug': 'teal-gradient',
                'description': 'Fresh teal gradient design with modern card layout.',
                'category': 'developer',
                'color_scheme': 'teal',
                'template_file': 'portfolio_templates/template_6_teal_gradient.html',
                'order': 6,
            },
            {
                'name': 'Slate Blue',
                'slug': 'slate-blue',
                'description': 'Professional slate blue color scheme with clean typography.',
                'category': 'corporate',
                'color_scheme': 'slate-blue',
                'template_file': 'portfolio_templates/template_7_slate_blue.html',
                'order': 7,
            },
            {
                'name': 'Terminal Green',
                'slug': 'terminal-green',
                'description': 'Retro terminal-style green on black. For hardcore developers and tech enthusiasts.',
                'category': 'developer',
                'color_scheme': 'green',
                'template_file': 'portfolio_templates/template_8_terminal_green.html',
                'order': 8,
            },
            {
                'name': 'Red Accent',
                'slug': 'red-accent',
                'description': 'Bold red accent color with modern gradient header.',
                'category': 'creative',
                'color_scheme': 'red',
                'template_file': 'portfolio_templates/template_9_red_accent.html',
                'order': 9,
            },
            {
                'name': 'Gold Luxury',
                'slug': 'gold-luxury',
                'description': 'Elegant gold and dark background for premium look.',
                'category': 'corporate',
                'color_scheme': 'gold',
                'template_file': 'portfolio_templates/template_10_gold_luxury.html',
                'order': 10,
            },
            {
                'name': 'Indigo Professional',
                'slug': 'indigo-professional',
                'description': 'Deep indigo color scheme perfect for professionals.',
                'category': 'corporate',
                'color_scheme': 'indigo',
                'template_file': 'portfolio_templates/template_11_indigo_professional.html',
                'order': 11,
            },
            {
                'name': 'Emerald Green',
                'slug': 'emerald-green',
                'description': 'Fresh emerald green for nature-inspired designs.',
                'category': 'creative',
                'color_scheme': 'emerald',
                'template_file': 'portfolio_templates/template_12_emerald.html',
                'order': 12,
            },
            {
                'name': 'Slate Dark',
                'slug': 'slate-dark',
                'description': 'Sophisticated dark slate color for tech professionals.',
                'category': 'developer',
                'color_scheme': 'slate',
                'template_file': 'portfolio_templates/template_13_slate_dark.html',
                'order': 13,
            },
            {
                'name': 'Pink Vibrant',
                'slug': 'pink-vibrant',
                'description': 'Vibrant pink theme perfect for designers and creatives.',
                'category': 'creative',
                'color_scheme': 'pink',
                'template_file': 'portfolio_templates/template_14_pink_vibrant.html',
                'order': 14,
            },
            {
                'name': 'Amber Warm',
                'slug': 'amber-warm',
                'description': 'Warm amber tones for a cozy professional feel.',
                'category': 'corporate',
                'color_scheme': 'amber',
                'template_file': 'portfolio_templates/template_15_amber_warm.html',
                'order': 15,
            },
            {
                'name': 'Sky Blue',
                'slug': 'sky-blue',
                'description': 'Light sky blue theme, clean and professional.',
                'category': 'developer',
                'color_scheme': 'blue',
                'template_file': 'portfolio_templates/template_16_sky_blue.html',
                'order': 16,
            },
            {
                'name': 'Cyan Tech',
                'slug': 'cyan-tech',
                'description': 'Modern cyan color for tech-focused portfolios.',
                'category': 'developer',
                'color_scheme': 'cyan',
                'template_file': 'portfolio_templates/template_17_cyan_tech.html',
                'order': 17,
            },
            {
                'name': 'Violet Modern',
                'slug': 'violet-modern',
                'description': 'Elegant violet theme for modern creative professionals.',
                'category': 'creative',
                'color_scheme': 'violet',
                'template_file': 'portfolio_templates/template_18_violet_modern.html',
                'order': 18,
            },
            {
                'name': 'Stone Minimal',
                'slug': 'stone-minimal',
                'description': 'Minimalist stone gray design, ultra-clean.',
                'category': 'minimalist',
                'color_scheme': 'stone',
                'template_file': 'portfolio_templates/template_19_stone_minimal.html',
                'order': 19,
            },
            {
                'name': 'Rose Elegant',
                'slug': 'rose-elegant',
                'description': 'Elegant rose theme for sophisticated portfolios.',
                'category': 'creative',
                'color_scheme': 'rose',
                'template_file': 'portfolio_templates/template_20_rose_elegant.html',
                'order': 20,
            },
        ]

        for template_data in templates:
            obj, created = PortfolioTemplate.objects.get_or_create(
                slug=template_data['slug'],
                defaults=template_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created template: {template_data['name']}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"~ Template already exists: {template_data['name']}")
                )

        self.stdout.write(
            self.style.SUCCESS('\nSuccessfully loaded all 20 portfolio templates!')
        )

