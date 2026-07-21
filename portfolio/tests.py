import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Portfolio, PortfolioTemplate


class TemplatePreviewTests(TestCase):
    def setUp(self):
        self.template = PortfolioTemplate.objects.create(
            name="Preview Test Template",
            slug="preview-test-template",
            description="Template used to test the no-save preview flow.",
            category="minimalist",
            color_scheme="mono",
            template_file="portfolio_templates/template_clean_minimal.html",
            is_active=True,
            order=1,
        )
        self.url = reverse("portfolio:template_preview", args=[self.template.id])

    def test_public_example_contains_complete_sample_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Morgan Lee")
        self.assertContains(response, "PortfolioForge Studio")
        self.assertContains(response, "data:image/svg+xml;base64")
        self.assertEqual(response["Cache-Control"], "no-store")

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


class ShippedTemplateStructureTests(TestCase):
    """Guard the content structure that every public template promises."""

    TEMPLATE_FILES = [
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
