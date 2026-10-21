import json

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..models import Portfolio, PortfolioTemplate, PublicPortfolio


class TemplatePreviewTests(TestCase):
    def setUp(self):
        self.template = PortfolioTemplate.objects.create(
            name="Preview Test Template",
            slug="preview-test-template",
            description="Template used to test the no-save preview flow.",
            category="minimalist",
            color_scheme="mono",
            template_file="portfolio_templates/template_base_dark.html",
            is_active=True,
            order=1,
        )
        self.url = reverse("portfolio:template_preview", args=[self.template.id])

    def test_public_example_contains_complete_sample_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Morgan Lee")
        self.assertContains(response, "PortfolioForge Studio")
        self.assertContains(response, "50+")
        self.assertContains(response, "Projects delivered")
        self.assertContains(response, "data:image/svg+xml;base64")
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_draft_preview_renders_custom_stats_without_saving(self):
        response = self.client.post(
            self.url,
            {
                "full_name": "Ayesha Khan",
                "stats": json.dumps([
                    {"value": "12", "label": "Products launched", "detail": "Since 2021"},
                ]),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "12")
        self.assertContains(response, "Products launched")
        self.assertContains(response, "Since 2021")
        self.assertNotContains(response, "50+")
        self.assertEqual(Portfolio.objects.count(), 0)

    def test_draft_preview_uses_unsaved_content_and_uploaded_portrait(self):
        response = self.client.post(
            self.url,
            {
                "full_name": "Ayesha Khan",
                "title": "Product Designer",
                "bio": "I design clear digital tools for complex services.",
                "email": "ayesha@example.com",
                "location": "Karachi, Pakistan",
                "skills": json.dumps(["Design systems", "Research"]),
                "projects": json.dumps([
                    {
                        "title": "Client Portal",
                        "description": "A clearer way for customers to manage their accounts.",
                        "tech_stack": "Research · Figma · React",
                    }
                ]),
                "experience": json.dumps([
                    {
                        "company": "Studio One",
                        "role": "Lead Designer",
                        "duration": "2024 — Present",
                        "description": "Leading end-to-end product design.",
                    }
                ]),
                "education": json.dumps([]),
                "profile_image": SimpleUploadedFile(
                    "portrait.png",
                    b"preview-image-bytes",
                    content_type="image/png",
                ),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ayesha Khan")
        self.assertContains(response, "Client Portal")
        self.assertContains(response, "data:image/png;base64")
        self.assertNotContains(response, "Morgan Lee")
        self.assertEqual(Portfolio.objects.count(), 0)


class ArchitectRenderingFlowTests(TestCase):
    def setUp(self):
        self.template = PortfolioTemplate.objects.create(
            name="The Architect",
            slug="architect_portfolio",
            description="Editorial portfolio for technical architects.",
            category="developer",
            color_scheme="ink-bone-copper",
            template_file="portfolio_templates/template_architect_portfolio.html",
            is_active=True,
            order=34,
        )
        self.preview_url = reverse("portfolio:template_preview", args=[self.template.id])

    def test_draft_preview_handles_missing_optional_content(self):
        response = self.client.post(
            self.preview_url,
            {
                "full_name": "Priya N.",
                "title": "Senior Backend Engineer",
                "bio": "I build dependable systems for teams doing consequential work.",
                "email": "priya@example.com",
                "skills": json.dumps(["Python", "PostgreSQL"]),
                "stats": json.dumps([]),
                "projects": json.dumps([]),
                "experience": json.dumps([]),
                "education": json.dumps([]),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Priya N.")
        self.assertContains(response, "Senior Backend Engineer")
        self.assertNotContains(response, "Morgan Lee")
        self.assertNotContains(response, "Evidence, not volume.")
        self.assertContains(response, "No selected work has been added yet.")

    def test_architect_sample_uses_abstract_fallback_portraits(self):
        response = self.client.get(self.preview_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "figure-fallback")
        self.assertContains(response, "fallback-frame")
        self.assertContains(response, "about-fallback")
        self.assertNotContains(response, "data:image/svg+xml;base64")

    def test_saved_preview_and_download_handle_multiple_projects_without_images(self):
        portfolio = Portfolio.objects.create(
            full_name="Ravi Sharma",
            title="Principal Software Engineer",
            bio="A long-form introduction about designing reliable platforms and useful abstractions for teams with complex constraints.",
            email="ravi@example.com",
            template=self.template,
            skills=["Python", "Distributed systems"],
            stats=[],
            projects=[
                {
                    "title": "Lattice <script>",
                    "description": "A long project description that should remain escaped and readable in the case-study layout.",
                    "tech_stack": "Python · PostgreSQL",
                    "live_link": "https://example.com/lattice",
                },
                {
                    "title": "Second System",
                    "description": "A second project without an image asset.",
                    "tech_stack": "Django · APIs",
                },
            ],
            experience=[],
            education=[],
        )

        preview = self.client.get(f"/api/portfolios/{portfolio.id}/preview/")
        download = self.client.get(f"/api/portfolios/{portfolio.id}/download/")

        self.assertEqual(preview.status_code, 200)
        self.assertContains(preview, "Lattice &lt;script&gt;")
        self.assertContains(preview, "Second System")
        self.assertContains(preview, "project-visual")
        self.assertNotContains(preview, "<script>")
        self.assertEqual(download.status_code, 200)
        self.assertIn("attachment; filename=\"ravi_sharma_portfolio.html\"", download["Content-Disposition"])
        self.assertContains(download, "Second System")

    def test_architect_project_gallery_uses_distinct_visual_compositions(self):
        response = self.client.post(
            self.preview_url,
            {
                "full_name": "Ravi Sharma",
                "projects": json.dumps([
                    {"title": "Signal Dashboard"},
                    {"title": "Field Notes Mobile"},
                    {"title": "Signal Commerce"},
                    {"title": "Ledger AI"},
                    {"title": "Operations Platform"},
                ]),
            },
        )

        self.assertEqual(response.status_code, 200)
        for visual_variant in (
            "project-visual--dashboard",
            "project-visual--mobile",
            "project-visual--commerce",
            "project-visual--ai",
            "project-visual--operations",
        ):
            self.assertContains(response, visual_variant)
        self.assertContains(response, "architect-project--feature")
        self.assertContains(response, "architect-project--editorial")

    def test_public_render_uses_the_architect_template(self):
        user = User.objects.create_user(username="architect-public")
        PublicPortfolio.objects.create(
            user=user,
            username_slug="architect-public",
            full_name="Nadia Chen",
            title="Technical Architect",
            bio="I make complex systems easier to understand and operate.",
            email="nadia@example.com",
            template=self.template,
            is_published=True,
            skills=["System design"],
            stats=[],
            projects=[],
            experience=[],
            education=[],
        )

        response = self.client.get("/portfolio/architect-public/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nadia Chen")
        self.assertContains(response, "Technical Architect")
        self.assertContains(response, "Start a conversation")


class ShippedTemplateStructureTests(TestCase):
    """Guard the content structure that every public template promises."""

    NEW_TEMPLATE_FILES = [
        "portfolio_templates/template_editorial_linen.html",
        "portfolio_templates/template_aurora_studio.html",
        "portfolio_templates/template_boardroom_blue.html",
        "portfolio_templates/template_summit_narrative.html",
        "portfolio_templates/template_tide_glass.html",
        "portfolio_templates/template_heritage_copper.html",
        "portfolio_templates/template_monograph_ink.html",
        "portfolio_templates/template_signal_grid.html",
        "portfolio_templates/template_organic_clay.html",
        "portfolio_templates/template_product_bento.html",
        "portfolio_templates/template_sunrise_mosaic.html",
        "portfolio_templates/template_case_study_magazine.html",
        "portfolio_templates/template_architect_portfolio.html",
        "portfolio_templates/template_brutalist_index.html",
        "portfolio_templates/template_field_manual.html",
        "portfolio_templates/template_kinetic_type.html",
    ]

    TEMPLATE_FILES = [
        "portfolio_templates/template_base_dark.html",
        "portfolio_templates/template_modern_corporate.html",
        "portfolio_templates/template_clean_minimal.html",
        "portfolio_templates/template_luxury_elegant.html",
        "portfolio_templates/template_dev_terminal.html",
        "portfolio_templates/template_gradient_purple.html",
        "portfolio_templates/template_nature_green.html",
        "portfolio_templates/template_indigo_modern.html",
        "portfolio_templates/template_navy_business.html",
        "portfolio_templates/template_rose_minimal.html",
        "portfolio_templates/template_teal_modern.html",
        "portfolio_templates/template_sunset_gradient.html",
        "portfolio_templates/template_slate_professional.html",
        "portfolio_templates/template_ocean_blue.html",
        "portfolio_templates/template_forest_dark.html",
        "portfolio_templates/template_bold_dark_neon.html",
        "portfolio_templates/template_creative_vibrant.html",
        "portfolio_templates/template_elegant_classic.html",
        "portfolio_templates/template_minimalist_mono.html",
        "portfolio_templates/template_tech_glassmorphism.html",
        "portfolio_templates/template_sidebar_layout.html",
        "portfolio_templates/template_two_column.html",
        "portfolio_templates/template_editorial_linen.html",
        "portfolio_templates/template_aurora_studio.html",
        "portfolio_templates/template_boardroom_blue.html",
        "portfolio_templates/template_summit_narrative.html",
        "portfolio_templates/template_tide_glass.html",
        "portfolio_templates/template_heritage_copper.html",
        "portfolio_templates/template_monograph_ink.html",
        "portfolio_templates/template_signal_grid.html",
        "portfolio_templates/template_organic_clay.html",
        "portfolio_templates/template_product_bento.html",
        "portfolio_templates/template_sunrise_mosaic.html",
        "portfolio_templates/template_case_study_magazine.html",
        "portfolio_templates/template_architect_portfolio.html",
        "portfolio_templates/template_brutalist_index.html",
        "portfolio_templates/template_field_manual.html",
        "portfolio_templates/template_kinetic_type.html",
    ]

    def setUp(self):
        self.templates = []
        for index, template_file in enumerate(self.TEMPLATE_FILES, start=1):
            template = PortfolioTemplate.objects.create(
                name=f"Structure Test {index}",
                slug=f"structure-test-{index}",
                description="Template structure regression test.",
                category="minimalist",
                color_scheme="test",
                template_file=template_file,
                is_active=True,
                order=index,
            )
            self.templates.append(template)

    def test_all_templates_render_explicit_experience_and_education(self):
        for template in self.templates:
            with self.subTest(template=template.template_file):
                response = self.client.get(
                    reverse("portfolio:template_preview", args=[template.id])
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Experience")
                self.assertContains(response, "Education")

    def test_new_templates_keep_theme_css_in_the_outer_stylesheet(self):
        for template in self.templates:
            if template.template_file not in self.NEW_TEMPLATE_FILES:
                continue

            with self.subTest(template=template.template_file):
                response = self.client.get(
                    reverse("portfolio:template_preview", args=[template.id])
                )

                self.assertEqual(response.status_code, 200)
                html = response.content.decode()
                self.assertEqual(html.count("<style>"), 1)
                self.assertEqual(html.count("</style>"), 1)

    def test_nature_green_keeps_each_project_number_before_the_project_content(self):
        nature_green = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_nature_green.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[nature_green.id])
        )
        cards = response.content.decode().split('<article class="plant">')

        self.assertGreaterEqual(len(cards), 3)
        second_project = cards[2]
        self.assertLess(second_project.index(">02<"), second_project.index("<h3>"))

    def test_base_dark_theme_exposes_its_reference_direction(self):
        base_dark = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_base_dark.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[base_dark.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-base-dark")
        self.assertContains(response, "Building digital solutions for a better tomorrow.")
        self.assertContains(response, "Selected work with real-world impact.")
        self.assertContains(response, "50+")
        self.assertContains(response, "Projects delivered")

    def test_sidebar_layout_uses_a_compact_top_navigation(self):
        sidebar_layout = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_sidebar_layout.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[sidebar_layout.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-sidebar-layout")
        self.assertContains(response, "width: 100%; max-width: none")
        self.assertContains(response, "border-radius: 0; background: transparent")
        self.assertContains(response, "white-space: nowrap")
        self.assertContains(response, "Profile")
        self.assertContains(response, "Work")
        self.assertContains(response, "Experience")
        self.assertContains(response, "Contact")

    def test_luxury_elegant_uses_its_own_gallery_structure(self):
        luxury_elegant = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_luxury_elegant.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[luxury_elegant.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-luxury-elegant")
        self.assertContains(response, "collection-nav")
        self.assertContains(response, "project-ledger")
        self.assertContains(response, "Measured taste. Exacting execution.")
        self.assertNotContains(response, "portfolio-page")

    def test_slate_professional_keeps_profile_fixed_and_exposes_contact_details(self):
        slate_professional = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_slate_professional.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[slate_professional.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "width:100%")
        self.assertContains(response, "height:100vh")
        self.assertContains(response, "overflow-y:auto")
        self.assertContains(response, "Contact / base")
        self.assertContains(response, "San Francisco, California")
        self.assertContains(response, "morgan@example.com")
        self.assertContains(response, "LinkedIn ↗")
        self.assertContains(response, "GitHub ↗")

    def test_elegant_classic_fills_the_viewport(self):
        elegant_classic = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_elegant_classic.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[elegant_classic.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "width:100%")
        self.assertContains(response, "min-height:100vh")
        self.assertContains(response, 'class="folio"')
        self.assertContains(response, "Have an idea?")
        self.assertContains(response, "Let’s discuss.")
        self.assertContains(response, "Start a conversation ↗")
        self.assertNotContains(response, "Correspondence")

    def test_editorial_linen_theme_exposes_its_reference_direction(self):
        editorial_linen = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_editorial_linen.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[editorial_linen.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-editorial-linen")
        self.assertContains(response, "Making complex ideas feel simple.")
        self.assertContains(response, "Selected case studies.")

    def test_aurora_studio_theme_exposes_its_reference_direction(self):
        aurora_studio = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_aurora_studio.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[aurora_studio.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-aurora-studio")
        self.assertContains(response, "aurora-page")
        self.assertContains(response, "Ideas into experiences.")
        self.assertContains(response, "Let’s make something magnetic.")
        self.assertNotContains(response, "portfolio-page")

    def test_boardroom_blue_theme_exposes_its_reference_direction(self):
        boardroom_blue = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_boardroom_blue.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[boardroom_blue.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-boardroom-blue")
        self.assertContains(response, "boardroom-sheet")
        self.assertContains(response, "brief-nav")
        self.assertContains(response, "width:100%")
        self.assertContains(response, "Practical thinking for ambitious teams.")
        self.assertContains(response, "Ready to build something useful?")
        self.assertNotContains(response, "portfolio-page")

    def test_gradient_purple_uses_an_independent_journal_layout(self):
        gradient_purple = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_gradient_purple.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[gradient_purple.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-gradient-purple")
        self.assertContains(response, "journal")
        self.assertContains(response, "story-list")
        self.assertContains(response, "width:100%")
        self.assertContains(response, "Ideas, released into the world.")
        self.assertNotContains(response, "portfolio-page")

    def test_indigo_modern_uses_an_independent_casebook_layout(self):
        indigo_modern = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_indigo_modern.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[indigo_modern.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-indigo-modern")
        self.assertContains(response, "casebook")
        self.assertContains(response, "case-list")
        self.assertContains(response, "width:min(100% - 64px,1440px)")
        self.assertContains(response, "Building useful things, end to end.")
        self.assertNotContains(response, "portfolio-page")

    def test_teal_modern_uses_an_independent_signal_board_layout(self):
        teal_modern = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_teal_modern.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[teal_modern.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-teal-modern")
        self.assertContains(response, "signal-list")
        self.assertContains(response, "live_profile.log")
        self.assertContains(response, "width:min(100% - 64px,1440px)")
        self.assertContains(response, "Practical work with a visible signal.")
        self.assertNotContains(response, "portfolio-page")

    def test_summit_narrative_theme_exposes_its_reference_direction(self):
        summit_narrative = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_summit_narrative.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[summit_narrative.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-summit-narrative")
        self.assertContains(response, "Tools for the climb.")
        self.assertContains(response, "Have a project worth the climb?")

    def test_tide_glass_theme_exposes_its_reference_direction(self):
        tide_glass = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_tide_glass.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[tide_glass.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-tide-glass")
        self.assertContains(response, "Useful design for real people.")
        self.assertContains(response, "Let’s find the right current.")

    def test_heritage_copper_theme_exposes_its_reference_direction(self):
        heritage_copper = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_heritage_copper.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[heritage_copper.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-heritage-copper")
        self.assertContains(response, "Experience, shaped with intention.")
        self.assertContains(response, "Let’s begin a conversation.")

    def test_monograph_ink_theme_exposes_its_reference_direction(self):
        monograph_ink = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_monograph_ink.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[monograph_ink.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-monograph-ink")
        self.assertContains(response, "Notes on making meaningful things.")
        self.assertContains(response, "Write when the question is interesting.")

    def test_signal_grid_theme_exposes_its_reference_direction(self):
        signal_grid = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_signal_grid.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[signal_grid.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-signal-grid")
        self.assertContains(response, "Clarity at every layer.")
        self.assertContains(response, "Let’s build a clearer system.")

    def test_organic_clay_theme_exposes_its_reference_direction(self):
        organic_clay = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_organic_clay.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[organic_clay.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-organic-clay")
        self.assertContains(response, "A softer way to solve hard problems.")
        self.assertContains(response, "Want to make something feel right?")

    def test_product_bento_theme_exposes_its_reference_direction(self):
        product_bento = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_product_bento.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[product_bento.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-product-bento")
        self.assertContains(response, "From fuzzy problems to focused products.")
        self.assertContains(response, "Have a product problem to solve?")

    def test_sunrise_mosaic_theme_exposes_its_reference_direction(self):
        sunrise_mosaic = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_sunrise_mosaic.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[sunrise_mosaic.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-sunrise-mosaic")
        self.assertContains(response, "Every good brand has a pulse.")
        self.assertContains(response, "Let’s make the next chapter vivid.")

    def test_case_study_magazine_has_an_independent_editorial_structure(self):
        case_study_magazine = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_case_study_magazine.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[case_study_magazine.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CASE STUDY MAGAZINE")
        self.assertContains(response, "Case studies with a point of view.")
        self.assertContains(response, "A practice made of many small disciplines.")
        self.assertNotContains(response, "portfolio-page")

    def test_architect_portfolio_has_an_independent_editorial_structure(self):
        architect = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_architect_portfolio.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[architect.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Architect")
        self.assertContains(response, "Systems")
        self.assertContains(response, "clarity.")
        self.assertContains(response, "Selected work")
        self.assertContains(response, "Make the complex feel inevitable.")
        self.assertContains(response, "Have a system worth building?")
        self.assertContains(response, "PortfolioForge Studio")
        self.assertContains(response, "project-visual")
        self.assertNotContains(response, "portfolio-page")

    def test_brutalist_index_has_an_index_led_project_and_record_structure(self):
        brutalist = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_brutalist_index.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[brutalist.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-brutalist-index")
        self.assertContains(response, "Brutalist Index")
        self.assertContains(response, "An index of useful things.")
        self.assertContains(response, "PortfolioForge Studio")
        self.assertContains(response, "Experience")
        self.assertContains(response, "Education")
        self.assertContains(response, "Let’s make a useful dent.")
        self.assertContains(response, "project-visual--type")
        self.assertNotContains(response, "portfolio-page")

    def test_field_manual_has_a_dossier_archive_and_career_record(self):
        field_manual = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_field_manual.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[field_manual.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-field-manual")
        self.assertContains(response, "Field Manual")
        self.assertContains(response, "Work worth keeping notes on.")
        self.assertContains(response, "PortfolioForge Studio")
        self.assertContains(response, "Experience")
        self.assertContains(response, "Education")
        self.assertContains(response, "Leave the door open.")
        self.assertContains(response, "art-type")
        self.assertNotContains(response, "portfolio-page")

    def test_kinetic_type_has_typographic_project_bands_and_contact_close(self):
        kinetic = next(
            template
            for template in self.templates
            if template.template_file.endswith("template_kinetic_type.html")
        )
        response = self.client.get(
            reverse("portfolio:template_preview", args=[kinetic.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "template-kinetic-type")
        self.assertContains(response, "Kinetic Type")
        self.assertContains(response, "Selected signals.")
        self.assertContains(response, "PortfolioForge Studio")
        self.assertContains(response, "Experience")
        self.assertContains(response, "Education")
        self.assertContains(response, "Let’s make it move.")
        self.assertContains(response, "type-art")
        self.assertNotContains(response, "portfolio-page")
