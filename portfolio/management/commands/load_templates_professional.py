from django.core.management.base import BaseCommand
from portfolio.models import PortfolioTemplate


class Command(BaseCommand):
    help = 'Load 20 professional portfolio templates into the database'

    def handle(self, *args, **options):
        """Load all 20 professional enterprise templates"""
        templates = [
            # MINIMALIST (4)
            {
                'name': 'Minimalist Dark Elegance',
                'slug': 'minimalist-dark-elegance',
                'description': 'Dark background with white text and red accent. Extreme simplicity, typography-first design.',
                'category': 'minimalist',
                'color_scheme': 'navy-red',
                'template_file': 'portfolio_templates/template_1_minimalist_dark_elegance.html',
                'order': 1,
            },
            {
                'name': 'Minimalist Light Clean',
                'slug': 'minimalist-light-clean',
                'description': 'White background with minimal colors. Maximum readability and clarity.',
                'category': 'minimalist',
                'color_scheme': 'light-blue',
                'template_file': 'portfolio_templates/template_2_minimalist_light_clean.html',
                'order': 2,
            },
            {
                'name': 'Minimalist Monochrome',
                'slug': 'minimalist-monochrome',
                'description': 'Pure black & white. Ultimate simplicity, print-ready design.',
                'category': 'minimalist',
                'color_scheme': 'black-white',
                'template_file': 'portfolio_templates/template_3_minimalist_monochrome.html',
                'order': 3,
            },
            {
                'name': 'Minimalist Serif Classic',
                'slug': 'minimalist-serif-classic',
                'description': 'Serif typography focused design. Timeless, editorial aesthetic.',
                'category': 'minimalist',
                'color_scheme': 'cream-gold',
                'template_file': 'portfolio_templates/template_4_minimalist_serif_classic.html',
                'order': 4,
            },
            # DEVELOPER (6)
            {
                'name': 'Developer Dark Tech',
                'slug': 'developer-dark-tech',
                'description': 'Terminal-inspired dark theme. Perfect for software engineers.',
                'category': 'developer',
                'color_scheme': 'terminal-green',
                'template_file': 'portfolio_templates/template_5_developer_dark_tech.html',
                'order': 5,
            },
            {
                'name': 'Modern Portfolio Showcase',
                'slug': 'developer-modern-blue',
                'description': 'Clean editorial layout with bold typography, balanced whitespace, and premium hero layout.',
                'category': 'developer',
                'color_scheme': 'mono-ink',
                'template_file': 'portfolio_templates/template_6_modern_portfolio_showcase.html',
                'order': 6,
            },
            {
                'name': 'Developer Neon Cyberpunk',
                'slug': 'developer-neon-cyberpunk',
                'description': 'Cyberpunk aesthetic with neon colors and glowing effects.',
                'category': 'developer',
                'color_scheme': 'neon-cyber',
                'template_file': 'portfolio_templates/template_7_developer_neon_cyberpunk.html',
                'order': 7,
            },
            {
                'name': 'Developer Corporate Tech',
                'slug': 'developer-corporate-tech',
                'description': 'Professional tech company aesthetic. Data-focused design.',
                'category': 'developer',
                'color_scheme': 'corporate-cyan',
                'template_file': 'portfolio_templates/template_8_developer_corporate_tech.html',
                'order': 8,
            },
            {
                'name': 'Developer Gradient Sunset',
                'slug': 'developer-gradient-sunset',
                'description': 'Warm gradients with sunset colors. Modern creative feel.',
                'category': 'developer',
                'color_scheme': 'sunset',
                'template_file': 'portfolio_templates/template_9_developer_gradient_sunset.html',
                'order': 9,
            },
            {
                'name': 'Developer Glassmorphism',
                'slug': 'developer-glassmorphism',
                'description': 'Frosted glass effect cards. Modern depth and transparency.',
                'category': 'developer',
                'color_scheme': 'glass-dark',
                'template_file': 'portfolio_templates/template_10_developer_glassmorphism.html',
                'order': 10,
            },
            # CREATIVE (6)
            {
                'name': 'Creative Forest Green',
                'slug': 'creative-forest-green',
                'description': 'Natural, organic feel with forest green colors.',
                'category': 'creative',
                'color_scheme': 'forest',
                'template_file': 'portfolio_templates/template_11_creative_forest_green.html',
                'order': 11,
            },
            {
                'name': 'Creative Vibrant Rainbow',
                'slug': 'creative-vibrant-rainbow',
                'description': 'Colorful, energetic, and bold. Dynamic layouts.',
                'category': 'creative',
                'color_scheme': 'rainbow',
                'template_file': 'portfolio_templates/template_12_creative_vibrant_rainbow.html',
                'order': 12,
            },
            {
                'name': 'Creative Pastel Dream',
                'slug': 'creative-pastel-dream',
                'description': 'Soft pastels. Dreamy, gentle aesthetic.',
                'category': 'creative',
                'color_scheme': 'pastel',
                'template_file': 'portfolio_templates/template_13_creative_pastel_dream.html',
                'order': 13,
            },
            {
                'name': 'Creative Bold Typography',
                'slug': 'creative-bold-typography',
                'description': 'Large, artistic typography. Design-driven layout.',
                'category': 'creative',
                'color_scheme': 'bold-type',
                'template_file': 'portfolio_templates/template_14_creative_bold_typography.html',
                'order': 14,
            },
            {
                'name': 'Creative 3D Modern',
                'slug': 'creative-3d-modern',
                'description': '3D effects and perspective transforms. Modern depth.',
                'category': 'creative',
                'color_scheme': '3d-depth',
                'template_file': 'portfolio_templates/template_15_creative_3d_modern.html',
                'order': 15,
            },
            {
                'name': 'Creative Retro Vintage',
                'slug': 'creative-retro-vintage',
                'description': 'Retro 80s/90s aesthetic. Nostalgic feel.',
                'category': 'creative',
                'color_scheme': 'vintage',
                'template_file': 'portfolio_templates/template_16_creative_retro_vintage.html',
                'order': 16,
            },
            # CORPORATE (4)
            {
                'name': 'Corporate Executive Blue',
                'slug': 'corporate-executive-blue',
                'description': 'Traditional corporate. Trustworthy and professional.',
                'category': 'corporate',
                'color_scheme': 'executive',
                'template_file': 'portfolio_templates/template_17_corporate_executive_blue.html',
                'order': 17,
            },
            {
                'name': 'Corporate Modern Gradient',
                'slug': 'corporate-modern-gradient',
                'description': 'Corporate with modern gradient touch.',
                'category': 'corporate',
                'color_scheme': 'corp-gradient',
                'template_file': 'portfolio_templates/template_18_corporate_modern_gradient.html',
                'order': 18,
            },
            {
                'name': 'Corporate Minimal Business',
                'slug': 'corporate-minimal-business',
                'description': 'Strict corporate minimal. Professional and serious.',
                'category': 'corporate',
                'color_scheme': 'minimal-corp',
                'template_file': 'portfolio_templates/template_19_corporate_minimal_business.html',
                'order': 19,
            },
            {
                'name': 'Corporate Modern Serif',
                'slug': 'corporate-modern-serif',
                'description': 'Elegant serif typography with luxury feel.',
                'category': 'corporate',
                'color_scheme': 'serif-luxury',
                'template_file': 'portfolio_templates/template_20_corporate_modern_serif.html',
                'order': 20,
            },
            # LATEST (5)
            {
                'name': 'Bold Dark Neon',
                'slug': 'latest-bold-dark-neon',
                'description': 'High-contrast neon design with cyberpunk energy and bold typography.',
                'category': 'latest',
                'color_scheme': 'neon-dark',
                'template_file': 'portfolio_templates/template_bold_dark_neon.html',
                'order': 21,
            },
            {
                'name': 'Creative Vibrant',
                'slug': 'latest-creative-vibrant',
                'description': 'Vibrant color blocks with playful layout and strong visual hierarchy.',
                'category': 'latest',
                'color_scheme': 'vibrant',
                'template_file': 'portfolio_templates/template_creative_vibrant.html',
                'order': 22,
            },
            {
                'name': 'Elegant Classic',
                'slug': 'latest-elegant-classic',
                'description': 'Timeless editorial layout with refined typography and calm spacing.',
                'category': 'latest',
                'color_scheme': 'classic',
                'template_file': 'portfolio_templates/template_elegant_classic.html',
                'order': 23,
            },
            {
                'name': 'Minimalist Mono',
                'slug': 'latest-minimalist-mono',
                'description': 'Monochrome, minimal design focused on clarity and balance.',
                'category': 'latest',
                'color_scheme': 'mono',
                'template_file': 'portfolio_templates/template_minimalist_mono.html',
                'order': 24,
            },
            {
                'name': 'Tech Glassmorphism',
                'slug': 'latest-tech-glassmorphism',
                'description': 'Frosted glass panels with a modern tech-forward aesthetic.',
                'category': 'latest',
                'color_scheme': 'glass',
                'template_file': 'portfolio_templates/template_tech_glassmorphism.html',
                'order': 25,
            },
        ]

        for template_data in templates:
            obj, created = PortfolioTemplate.objects.update_or_create(
                slug=template_data['slug'],
                defaults=template_data
            )
            status = "✓ Created" if created else "✓ Updated"
            self.stdout.write(
                self.style.SUCCESS(f"{status}: {template_data['name']}")
            )

        total = PortfolioTemplate.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ All 20 professional templates loaded! Total: {total}')
        )

