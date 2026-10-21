from django.contrib.auth.models import User
from django.test import TestCase

from portfolio.models import Portfolio, PortfolioTemplate, PublicPortfolio
from portfolio.preview_context import build_draft_preview_context
from portfolio.schema_registry import get_schema
from portfolio.schema_validation import (
    StructuredContentValidationError,
    validate_structured_content,
)
from portfolio.serializers import PublicPortfolioEditSerializer
from portfolio.services import PortfolioRenderer


class SchemaPhaseOneTests(TestCase):
    def setUp(self):
        self.template = PortfolioTemplate.objects.create(
            name="Schema Phase Template",
            slug="schema-phase-template",
            description="Schema phase test template.",
            category="developer",
            color_scheme="test",
            template_file="portfolio_templates/template_base_dark.html",
        )

    def test_migration_fields_have_backward_compatible_defaults(self):
        self.assertEqual(self.template.schema_key, "portfolio")
        self.assertEqual(self.template.schema_version, 1)

        portfolio = Portfolio.objects.create(
            full_name="Legacy Owner",
            title="Engineer",
            bio="A legacy portfolio.",
            email="legacy@example.com",
            template=self.template,
        )
        public = PublicPortfolio.objects.create(
            user=User.objects.create_user("schema-default-user"),
            username_slug="schema-default-user",
            full_name="Legacy Public Owner",
            title="Engineer",
            bio="A legacy public portfolio.",
            email="public@example.com",
            template=self.template,
        )

        self.assertEqual(portfolio.structured_content, {})
        self.assertEqual(portfolio.content_schema_version, 1)
        self.assertEqual(public.structured_content, {})
        self.assertEqual(public.content_schema_version, 1)

    def test_schema_composes_shared_category_and_template_layers(self):
        self.template.slug = "architect_portfolio"
        self.template.save(update_fields=["slug"])

        schema = get_schema(self.template)
        section_ids = {section["id"] for section in schema["sections"]}

        self.assertIn("profile", section_ids)
        self.assertIn("developer_context", section_ids)
        self.assertIn("architect_context", section_ids)
        self.assertEqual(schema["schema_key"], "portfolio")
        self.assertEqual(schema["schema_version"], 1)

    def test_validation_applies_defaults_and_preserves_unknown_keys(self):
        content = {"future_section": {"enabled": True}}

        normalized = validate_structured_content(self.template, content)

        self.assertEqual(normalized["projects"], [])
        self.assertEqual(normalized["experience"], [])
        self.assertEqual(normalized["future_section"], {"enabled": True})

    def test_strict_validation_reports_required_fields(self):
        with self.assertRaises(StructuredContentValidationError) as raised:
            validate_structured_content(self.template, {}, strict=True)

        self.assertIn("full_name", raised.exception.errors)
        self.assertIn("email", raised.exception.errors)

    def test_legacy_content_is_available_through_new_context_without_data_loss(self):
        legacy_projects = [{"title": "Legacy Project", "description": "Still here."}]
        portfolio = Portfolio.objects.create(
            full_name="Legacy Owner",
            title="Engineer",
            bio="A legacy portfolio.",
            email="legacy@example.com",
            projects=legacy_projects,
            structured_content={"future_section": {"value": "keep me"}},
            content_schema_version=7,
            template=self.template,
        )

        context = PortfolioRenderer(portfolio).get_context_data()

        self.assertEqual(context["projects"], legacy_projects)
        self.assertEqual(context["structured_content"]["projects"], legacy_projects)
        self.assertEqual(
            context["structured_content"]["future_section"],
            {"value": "keep me"},
        )
        self.assertEqual(
            context["structured_content"]["_legacy"]["projects"],
            legacy_projects,
        )
        self.assertEqual(context["content_schema_version"], 7)

    def test_draft_preview_exposes_structured_content_without_changing_legacy_aliases(self):
        context = build_draft_preview_context(
            self.template,
            {
                "full_name": "Preview Owner",
                "title": "Developer",
                "bio": "A preview draft.",
                "email": "preview@example.com",
                "projects": "[]",
                "experience": "[]",
                "education": "[]",
                "skills": "[]",
                "stats": "[]",
            },
        )

        self.assertEqual(context["full_name"], "Preview Owner")
        self.assertEqual(context["projects"], [])
        self.assertEqual(context["structured_content"]["projects"], [])
        self.assertEqual(context["content_schema_version"], 1)

    def test_public_update_and_html_export_preserve_structured_content(self):
        user = User.objects.create_user("schema-public-user")
        public = PublicPortfolio.objects.create(
            user=user,
            username_slug="schema-public-user",
            full_name="Public Owner",
            title="Engineer",
            bio="A published portfolio.",
            email="public@example.com",
            template=self.template,
            is_published=True,
        )
        payload = {"future_section": {"label": "published"}}

        serializer = PublicPortfolioEditSerializer(
            public,
            data={"structured_content": payload},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        public.refresh_from_db()

        self.assertEqual(public.structured_content["future_section"], payload["future_section"])
        response = self.client.get("/portfolio/schema-public-user/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Public Owner")

        portfolio = Portfolio.objects.create(
            full_name="Download Owner",
            title="Engineer",
            bio="An exported portfolio.",
            email="download@example.com",
            template=self.template,
            structured_content=payload,
        )
        export_context = PortfolioRenderer(portfolio).get_context_data()
        self.assertEqual(
            export_context["structured_content"]["future_section"],
            payload["future_section"],
        )
