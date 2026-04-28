from django.core.management.base import BaseCommand
from portfolio.models import PortfolioTemplate


class Command(BaseCommand):
    help = 'Load 20 professional portfolio templates into the database'

    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Modern Corporate',
                'slug': 'modern-corporate',
                'description': 'Clean and professional corporate design with blue accents and smooth transitions.',
                'category': 'corporate',
                'color_scheme': 'blue',
                'template_file': 'portfolio_templates/template_modern_corporate.html',
                'order': 1,
            },
            {
                'name': 'Clean Minimal',
                'slug': 'clean-minimal',
                'description': 'Minimalist design with clean typography and perfect spacing for professionals.',
                'category': 'minimalist',
                'color_scheme': 'gray-blue',
                'template_file': 'portfolio_templates/template_clean_minimal.html',
                'order': 2,
            },
            {
                'name': 'Luxury Elegant',
                'slug': 'luxury-elegant',
                'description': 'Sophisticated dark theme with gold accents for premium portfolios.',
                'category': 'corporate',
                'color_scheme': 'gold',
                'template_file': 'portfolio_templates/template_luxury_elegant.html',
                'order': 3,
            },
            {
                'name': 'Developer Terminal',
                'slug': 'dev-terminal',
                'description': 'Dark tech-inspired design with cyan and neon accents for developers.',
                'category': 'developer',
                'color_scheme': 'cyan',
                'template_file': 'portfolio_templates/template_dev_terminal.html',
                'order': 4,
            },
            {
                'name': 'Gradient Purple',
                'slug': 'gradient-purple',
                'description': 'Beautiful purple gradient background with smooth animations and hover effects.',
                'category': 'creative',
                'color_scheme': 'purple',
                'template_file': 'portfolio_templates/template_gradient_purple.html',
                'order': 5,
            },
            {
                'name': 'Nature Green',
                'slug': 'nature-green',
                'description': 'Fresh green theme inspired by nature with modern card layouts.',
                'category': 'creative',
                'color_scheme': 'green',
                'template_file': 'portfolio_templates/template_nature_green.html',
                'order': 6,
            },
            {
                'name': 'Indigo Modern',
                'slug': 'indigo-modern',
                'description': 'Modern indigo and violet design with tech-forward aesthetic.',
                'category': 'developer',
                'color_scheme': 'indigo',
                'template_file': 'portfolio_templates/template_indigo_modern.html',
                'order': 7,
            },
            {
                'name': 'Navy Business',
                'slug': 'navy-business',
                'description': 'Professional navy and gold business portfolio with elegant styling.',
                'category': 'corporate',
                'color_scheme': 'navy-gold',
                'template_file': 'portfolio_templates/template_navy_business.html',
                'order': 8,
            },
            {
                'name': 'Rose Minimal',
                'slug': 'rose-minimal',
                'description': 'Soft rose and blush tones with minimalist design for creatives.',
                'category': 'creative',
                'color_scheme': 'rose',
                'template_file': 'portfolio_templates/template_rose_minimal.html',
                'order': 9,
            },
            {
                'name': 'Teal Modern',
                'slug': 'teal-modern',
                'description': 'Modern teal and dark grey design with professional appeal.',
                'category': 'developer',
                'color_scheme': 'teal',
                'template_file': 'portfolio_templates/template_teal_modern.html',
                'order': 10,
            },
            {
                'name': 'Sunset Gradient',
                'slug': 'sunset-gradient',
                'description': 'Warm orange to pink gradient design perfect for creative professionals.',
                'category': 'creative',
                'color_scheme': 'orange-pink',
                'template_file': 'portfolio_templates/template_sunset_gradient.html',
                'order': 11,
            },
            {
                'name': 'Slate Professional',
                'slug': 'slate-professional',
                'description': 'Dark slate gray with blue accents for serious professionals.',
                'category': 'corporate',
                'color_scheme': 'slate-blue',
                'template_file': 'portfolio_templates/template_slate_professional.html',
                'order': 12,
            },
            {
                'name': 'Ocean Blue',
                'slug': 'ocean-blue',
                'description': 'Deep ocean blue gradient with cyan accents for tech enthusiasts.',
                'category': 'developer',
                'color_scheme': 'ocean',
                'template_file': 'portfolio_templates/template_ocean_blue.html',
                'order': 13,
            },
            {
                'name': 'Forest Dark',
                'slug': 'forest-dark',
                'description': 'Natural dark green forest theme with earthy tones.',
                'category': 'creative',
                'color_scheme': 'forest',
                'template_file': 'portfolio_templates/template_forest_dark.html',
                'order': 14,
            },
            {
                'name': 'Bold Dark Neon',
                'slug': 'bold-dark-neon',
                'description': 'High-contrast dark theme with neon pink and cyan accents.',
                'category': 'developer',
                'color_scheme': 'neon',
                'template_file': 'portfolio_templates/template_bold_dark_neon.html',
                'order': 15,
            },
            {
                'name': 'Creative Vibrant',
                'slug': 'creative-vibrant',
                'description': 'Vibrant and colorful design for creative professionals and artists.',
                'category': 'creative',
                'color_scheme': 'vibrant',
                'template_file': 'portfolio_templates/template_creative_vibrant.html',
                'order': 16,
            },
            {
                'name': 'Elegant Classic',
                'slug': 'elegant-classic',
                'description': 'Timeless elegant design with classic color schemes.',
                'category': 'corporate',
                'color_scheme': 'classic',
                'template_file': 'portfolio_templates/template_elegant_classic.html',
                'order': 17,
            },
            {
                'name': 'Minimalist Mono',
                'slug': 'minimalist-mono',
                'description': 'Pure minimalist monochrome design with focus on content.',
                'category': 'minimalist',
                'color_scheme': 'mono',
                'template_file': 'portfolio_templates/template_minimalist_mono.html',
                'order': 18,
            },
            {
                'name': 'Tech Glassmorphism',
                'slug': 'tech-glassmorphism',
                'description': 'Modern glassmorphism design with frosted glass effects.',
                'category': 'developer',
                'color_scheme': 'glass',
                'template_file': 'portfolio_templates/template_tech_glassmorphism.html',
                'order': 19,
            },
            {
                'name': 'Sidebar Professional',
                'slug': 'sidebar-professional',
                'description': 'Fixed sidebar layout with gradient styling - completely different design.',
                'category': 'corporate',
                'color_scheme': 'purple-gradient',
                'template_file': 'portfolio_templates/template_sidebar_layout.html',
                'order': 20,
            },
            {
                'name': 'Two Column Showcase',
                'slug': 'two-column',
                'description': 'Modern two-column layout with sticky hero section - unique design.',
                'category': 'developer',
                'color_scheme': 'blue-purple',
                'template_file': 'portfolio_templates/template_two_column.html',
                'order': 21,
            },
        ]

        # Deactivate old deprecated templates (don't delete - they may be referenced by portfolios)
        old_slugs = [
            'minimalist-bw', 'dark-modern-blue', 'corporate-blue', 'creative-orange',
            'teal-gradient', 'slate-blue', 'terminal-green', 'red-accent',
            'gold-luxury', 'indigo-professional', 'emerald-green', 'slate-dark',
            'pink-vibrant', 'amber-warm', 'sky-blue', 'cyan-tech', 'violet-modern',
            'stone-minimal', 'rose-elegant'
        ]
        deactivated_count = 0
        for slug in old_slugs:
            try:
                old_template = PortfolioTemplate.objects.get(slug=slug)
                old_template.is_active = False
                old_template.save(update_fields=['is_active'])
                deactivated_count += 1
            except PortfolioTemplate.DoesNotExist:
                pass

        if deactivated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"✓ Deactivated {deactivated_count} old deprecated templates")
            )

        # Also deactivate the 5 templates that still have "latest-" prefix
        latest_slugs = ['latest-bold-dark-neon', 'latest-creative-vibrant', 'latest-elegant-classic', 'latest-minimalist-mono', 'latest-tech-glassmorphism']
        for slug in latest_slugs:
            try:
                old = PortfolioTemplate.objects.get(slug=slug)
                old.is_active = False
                old.save()
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Deactivated old version: {old.name}")
                )
            except PortfolioTemplate.DoesNotExist:
                pass

        for template_data in templates:
            # Try to get by slug first
            try:
                obj = PortfolioTemplate.objects.get(slug=template_data['slug'])
                # Update if exists
                for key, value in template_data.items():
                    if key != 'slug':
                        setattr(obj, key, value)
                obj.is_active = True  # Ensure it's active
                obj.save()
                self.stdout.write(
                    self.style.WARNING(f"~ Updated template: {template_data['name']}")
                )
            except PortfolioTemplate.DoesNotExist:
                # Check if a template with the same name exists (to handle conflicts)
                existing_by_name = PortfolioTemplate.objects.filter(name=template_data['name']).first()
                if existing_by_name:
                    # Update the existing template with new slug and data
                    existing_by_name.slug = template_data['slug']
                    existing_by_name.template_file = template_data['template_file']
                    existing_by_name.description = template_data['description']
                    existing_by_name.category = template_data['category']
                    existing_by_name.color_scheme = template_data['color_scheme']
                    existing_by_name.order = template_data['order']
                    existing_by_name.is_active = True
                    existing_by_name.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Updated and activated template: {template_data['name']}")
                    )
                else:
                    # Create new if doesn't exist at all
                    obj = PortfolioTemplate.objects.create(**template_data, is_active=True)
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Created template: {template_data['name']}")
                    )

        self.stdout.write(
            self.style.SUCCESS('\n✅ Successfully loaded all 19 professional portfolio templates!')
        )

