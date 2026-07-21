"""Generate a self-contained, locally browsable preview for every active template."""

import base64
import html
import mimetypes
import shutil
from pathlib import Path
from types import SimpleNamespace

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from portfolio.models import PortfolioTemplate


class Command(BaseCommand):
    help = (
        "Create a locally browsable HTML preview pack for all active portfolio templates. "
        "Each page uses rich demo content and an embedded profile image."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--image",
            required=True,
            help="Path to the profile image to embed in every generated portfolio.",
        )
        parser.add_argument(
            "--output-dir",
            default="generated_portfolio_previews",
            help="Directory, relative to the project root or absolute, for the preview pack.",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Replace the generator's existing preview files in the output directory.",
        )

    def handle(self, *args, **options):
        image_path = Path(options["image"]).expanduser().resolve()
        if not image_path.is_file():
            raise CommandError(f"Profile image was not found: {image_path}")

        output_dir = Path(options["output_dir"]).expanduser()
        if not output_dir.is_absolute():
            output_dir = Path(settings.BASE_DIR) / output_dir
        output_dir = output_dir.resolve()

        if output_dir.exists() and any(output_dir.iterdir()) and not options["overwrite"]:
            raise CommandError(
                f"Preview output directory already contains files: {output_dir}. "
                "Choose a new --output-dir or pass --overwrite to refresh generator output."
            )

        portfolio_dir = output_dir / "portfolios"
        portfolio_dir.mkdir(parents=True, exist_ok=True)

        image_data = image_path.read_bytes()
        mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
        profile_image_base64 = f"data:{mime_type};base64,{base64.b64encode(image_data).decode('ascii')}"
        profile_copy_name = f"profile-photo{image_path.suffix.lower() or '.png'}"
        profile_copy_path = output_dir / profile_copy_name
        if image_path != profile_copy_path:
            shutil.copy2(image_path, profile_copy_path)

        templates = list(PortfolioTemplate.objects.filter(is_active=True).order_by("order", "name"))
        if not templates:
            raise CommandError("There are no active portfolio templates to render.")

        generated_pages = []
        for position, template in enumerate(templates, start=1):
            filename = f"{position:02d}-{template.slug}.html"
            page_path = portfolio_dir / filename
            context = self._preview_context(template, profile_image_base64)
            rendered_html = render_to_string(template.template_file, context)
            page_path.write_text(
                self._ensure_profile_image(rendered_html, profile_image_base64),
                encoding="utf-8",
            )
            generated_pages.append({
                "name": template.name,
                "category": template.get_category_display(),
                "description": template.description,
                "filename": filename,
                "position": position,
            })

        (output_dir / "index.html").write_text(
            self._index_html(generated_pages, profile_copy_name),
            encoding="utf-8",
        )
        (output_dir / "README.txt").write_text(
            self._readme_text(len(generated_pages), profile_copy_name),
            encoding="utf-8",
        )

        self.stdout.write(self.style.SUCCESS(
            f"Generated {len(generated_pages)} complete portfolio previews in {output_dir}"
        ))
        self.stdout.write(f"Open {output_dir / 'index.html'} to browse them locally.")

    @staticmethod
    def _preview_context(template, profile_image_base64):
        """Return a deliberately complete context that supports all template families."""
        profile_image = SimpleNamespace(
            url=profile_image_base64,
            name="profile-photo.png",
        )
        projects = [
            {
                "title": "PortfolioForge Studio",
                "description": (
                    "A complete portfolio platform that turns a guided content workflow into "
                    "a refined, responsive site owners can publish anywhere."
                ),
                "tech_stack": "Django · Design systems · Product strategy",
                "technologies": "Django, Python, JavaScript, HTML, CSS",
                "github_link": "https://github.example/adeel-m/portfolioforge-studio",
                "live_link": "https://portfolioforge.example/studio",
                "project_url": "https://portfolioforge.example/studio",
            },
            {
                "title": "Atlas Operations Platform",
                "description": (
                    "A decision-support workspace that brought reporting, workflows, and "
                    "operational visibility into one calm, role-aware experience."
                ),
                "tech_stack": "Product architecture · Python · Analytics",
                "technologies": "Python, Django, PostgreSQL, REST APIs",
                "github_link": "https://github.example/adeel-m/atlas-operations",
                "live_link": "https://portfolioforge.example/atlas",
                "project_url": "https://portfolioforge.example/atlas",
            },
            {
                "title": "Signal Commerce",
                "description": (
                    "A commerce intelligence product that helped teams see the customer "
                    "journey, find conversion gaps, and act on reliable performance signals."
                ),
                "tech_stack": "Research · Dashboards · API design",
                "technologies": "React, Python, PostgreSQL, Data visualisation",
                "github_link": "https://github.example/adeel-m/signal-commerce",
                "live_link": "https://portfolioforge.example/signal",
                "project_url": "https://portfolioforge.example/signal",
            },
            {
                "title": "Ledger AI Assistant",
                "description": (
                    "A secure internal assistant that converted scattered documentation into "
                    "clear answers, repeatable workflows, and auditable operational guidance."
                ),
                "tech_stack": "AI workflows · Information design · Governance",
                "technologies": "Python, LLM orchestration, Django, Vector search",
                "github_link": "https://github.example/adeel-m/ledger-assistant",
                "live_link": "https://portfolioforge.example/ledger",
                "project_url": "https://portfolioforge.example/ledger",
            },
            {
                "title": "Field Notes Mobile",
                "description": (
                    "A lightweight mobile workflow for teams working away from a desk, with "
                    "offline-first capture and a more useful handoff back to operations."
                ),
                "tech_stack": "Mobile strategy · Service design · Delivery",
                "technologies": "React Native, Node.js, PostgreSQL, Offline sync",
                "github_link": "https://github.example/adeel-m/field-notes",
                "live_link": "https://portfolioforge.example/field-notes",
                "project_url": "https://portfolioforge.example/field-notes",
            },
        ]
        experience = [
            {
                "company": "Northstar Digital",
                "job_title": "Director of Product & Technology",
                "role": "Director of Product & Technology",
                "title": "Director of Product & Technology",
                "start_date": "2022",
                "end_date": "Present",
                "duration": "2022 — Present",
                "description": (
                    "Leading product strategy, platform delivery, and cross-functional teams "
                    "to turn complex commercial needs into durable digital products."
                ),
            },
            {
                "company": "Meridian Systems",
                "job_title": "Senior Product Manager",
                "role": "Senior Product Manager",
                "title": "Senior Product Manager",
                "start_date": "2019",
                "end_date": "2022",
                "duration": "2019 — 2022",
                "description": (
                    "Shaped product roadmaps, established research and measurement practices, "
                    "and helped launch tools used by distributed operations teams."
                ),
            },
            {
                "company": "Studio North",
                "job_title": "Product Designer & Developer",
                "role": "Product Designer & Developer",
                "title": "Product Designer & Developer",
                "start_date": "2016",
                "end_date": "2019",
                "duration": "2016 — 2019",
                "description": (
                    "Designed and built end-to-end digital experiences for early-stage ventures, "
                    "from customer discovery through production launch."
                ),
            },
            {
                "company": "Independent Practice",
                "job_title": "Digital Consultant",
                "role": "Digital Consultant",
                "title": "Digital Consultant",
                "start_date": "2014",
                "end_date": "2016",
                "duration": "2014 — 2016",
                "description": (
                    "Partnered with founders and small teams on digital strategy, brand systems, "
                    "web products, and the practical decisions needed to ship them well."
                ),
            },
        ]
        education = [
            {
                "institution": "National University of Sciences & Technology",
                "school": "National University of Sciences & Technology",
                "degree": "Bachelor of Science in Computer Science",
                "field": "Human-centred systems and software engineering",
                "year": "2014",
                "start_date": "2010",
                "end_date": "2014",
            },
            {
                "institution": "Interaction Design Foundation",
                "school": "Interaction Design Foundation",
                "degree": "Professional Certificate in UX Management",
                "field": "Product strategy, research, and service design",
                "year": "2021",
                "start_date": "2021",
                "end_date": "2021",
            },
        ]
        portfolio = SimpleNamespace(
            full_name="Adeel M.",
            title="Product & Technology Strategist",
            bio=(
                "A product-minded technology leader who turns ambiguous business goals into "
                "clear, scalable digital experiences. I work across strategy, design systems, "
                "and engineering to make complex things feel understandable."
            ),
            email="adeel@example.com",
            phone="+92 300 555 0100",
            location="Karachi, Pakistan",
            linkedin="https://linkedin.example/adeel-m",
            github="https://github.example/adeel-m",
            portfolio_website="https://portfolio.example/adeel-m",
            twitter="https://x.example/adeel-m",
            profile_image=profile_image,
            processed_profile_image=profile_image,
            template=template,
            skills=[
                "Product strategy", "Digital transformation", "System design", "Django",
                "Python", "React", "Design systems", "User research", "API design",
                "Team leadership", "Analytics", "Technical writing",
            ],
            projects=projects,
            experience=experience,
            education=education,
        )
        return {
            "portfolio": portfolio,
            "template": template,
            "template_color": template.color_scheme,
            "full_name": portfolio.full_name,
            "title": portfolio.title,
            "bio": portfolio.bio,
            "email": portfolio.email,
            "phone": portfolio.phone,
            "location": portfolio.location,
            "linkedin": portfolio.linkedin,
            "github": portfolio.github,
            "portfolio_website": portfolio.portfolio_website,
            "twitter": portfolio.twitter,
            "linkedin_url": portfolio.linkedin,
            "github_url": portfolio.github,
            "website_url": portfolio.portfolio_website,
            "twitter_url": portfolio.twitter,
            "website": portfolio.portfolio_website,
            "profile_image": profile_image_base64,
            "profile_image_url": profile_image_base64,
            "profile_image_base64": profile_image_base64,
            "skills": portfolio.skills,
            "projects": projects,
            "experience": experience,
            "education": education,
        }

    @staticmethod
    def _index_html(pages, profile_copy_name):
        cards = "\n".join(
            f"""
            <a class=\"template-card\" href=\"portfolios/{html.escape(page['filename'])}\">
                <span class=\"template-card__number\">{page['position']:02d}</span>
                <span class=\"template-card__category\">{html.escape(page['category'])}</span>
                <strong>{html.escape(page['name'])}</strong>
                <p>{html.escape(page['description'])}</p>
                <span class=\"template-card__open\">Open complete preview <span>↗</span></span>
            </a>"""
            for page in pages
        )
        return f"""<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>PortfolioForge · Local portfolio preview pack</title>
    <style>
        :root {{ color-scheme: dark; }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            min-width: 320px;
            background: #0a0a10;
            color: #f3f3ee;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.55;
        }}
        body::before {{
            position: fixed;
            inset: 0;
            z-index: -1;
            background: radial-gradient(ellipse 70% 48% at 77% -7%, rgba(164, 160, 255, .17), transparent 65%);
            content: '';
        }}
        main {{ max-width: 1320px; margin: 0 auto; padding: clamp(2rem, 5vw, 5.5rem) clamp(1.1rem, 3vw, 3rem) 4rem; }}
        .eyebrow {{ display: inline-flex; align-items: center; gap: .58rem; color: #b9b9c8; font-size: .68rem; font-weight: 800; letter-spacing: .15em; text-transform: uppercase; }}
        .eyebrow::before {{ width: .5rem; height: .5rem; border-radius: 50%; background: #d9ff7f; box-shadow: 0 0 0 5px rgba(217, 255, 127, .08); content: ''; }}
        header {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(260px, .38fr); gap: 3rem; align-items: end; padding-bottom: 3rem; border-bottom: 1px solid rgba(255,255,255,.11); }}
        h1 {{ max-width: 760px; margin: 1rem 0 0; font-size: clamp(2.8rem, 5.7vw, 5.8rem); font-weight: 620; letter-spacing: -.08em; line-height: .93; }}
        h1 em {{ color: #aaa7ff; font-family: Georgia, serif; font-weight: 400; }}
        .intro {{ max-width: 650px; margin: 1.25rem 0 0; color: #9898ac; font-size: 1rem; }}
        .profile-note {{ display: flex; align-items: center; gap: 1rem; padding: 1rem 0 1rem 1.3rem; border-left: 1px solid rgba(255,255,255,.18); }}
        .profile-note img {{ width: 3.25rem; height: 3.25rem; border: 1px solid rgba(255,255,255,.18); border-radius: .75rem; object-fit: cover; object-position: center top; }}
        .profile-note strong {{ display: block; font-size: .85rem; }}
        .profile-note span {{ display: block; margin-top: .18rem; color: #7d7d91; font-size: .73rem; }}
        .summary {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1.25rem 0 1.45rem; color: #858599; font-size: .78rem; }}
        .summary strong {{ color: #ecece8; font-size: .84rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }}
        .template-card {{ position: relative; min-height: 235px; overflow: hidden; padding: 1.25rem; border: 1px solid rgba(255,255,255,.11); border-radius: .9rem; background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.015)); color: inherit; text-decoration: none; transition: border-color .18s ease, background .18s ease, transform .18s ease; }}
        .template-card::before {{ position: absolute; width: 11rem; height: 11rem; right: -5rem; top: -6rem; border-radius: 50%; background: #aaa7ff; content: ''; filter: blur(18px); opacity: .13; }}
        .template-card:hover {{ border-color: rgba(196,194,255,.62); background: linear-gradient(145deg, rgba(170,167,255,.12), rgba(255,255,255,.025)); transform: translateY(-3px); }}
        .template-card__number {{ display: block; color: #9290db; font-size: .67rem; font-weight: 800; letter-spacing: .1em; }}
        .template-card__category {{ display: block; margin-top: 1.5rem; color: #bdbdcc; font-size: .65rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }}
        .template-card strong {{ display: block; margin-top: .45rem; font-size: 1.13rem; letter-spacing: -.04em; }}
        .template-card p {{ display: -webkit-box; margin: .45rem 0 0; overflow: hidden; color: #87879a; font-size: .75rem; line-height: 1.55; -webkit-box-orient: vertical; -webkit-line-clamp: 2; }}
        .template-card__open {{ position: absolute; right: 1.25rem; bottom: 1.1rem; left: 1.25rem; display: flex; align-items: center; justify-content: space-between; color: #ececeb; font-size: .72rem; font-weight: 800; }}
        .template-card__open span {{ color: #d9ff7f; font-size: 1rem; }}
        footer {{ display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem; padding-top: 1.1rem; border-top: 1px solid rgba(255,255,255,.09); color: #6f6f83; font-size: .73rem; }}
        @media (max-width: 900px) {{ header {{ grid-template-columns: 1fr; gap: 1.5rem; }} .profile-note {{ max-width: 320px; }} .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
        @media (max-width: 560px) {{ .grid {{ grid-template-columns: 1fr; }} footer {{ flex-direction: column; }} }}
    </style>
</head>
<body>
    <main>
        <header>
            <div>
                <span class=\"eyebrow\">PortfolioForge local preview pack</span>
                <h1>Every direction, filled with <em>real depth.</em></h1>
                <p class=\"intro\">This local pack contains a complete, self-contained preview for every active template. Each page uses the supplied portrait and the same rich demo portfolio data, so the visual differences are easy to compare.</p>
            </div>
            <div class=\"profile-note\"><img src=\"{html.escape(profile_copy_name)}\" alt=\"Profile photo used in every preview\"><div><strong>Profile photo included</strong><span>Embedded in all portfolio pages for offline viewing.</span></div></div>
        </header>
        <div class=\"summary\"><strong>{len(pages)} complete portfolio previews</strong><span>Open any card to view the template locally.</span></div>
        <section class=\"grid\" aria-label=\"Generated portfolio templates\">{cards}</section>
        <footer><span>PortfolioForge local preview pack</span><span>Demo content is fictional and intended for visual review.</span></footer>
    </main>
</body>
</html>"""

    @staticmethod
    def _ensure_profile_image(rendered_html, profile_image_base64):
        """Add a quiet profile marker only when a template has no native image slot."""
        if profile_image_base64 in rendered_html:
            return rendered_html

        profile_badge = f"""
<style id="portfolioforge-preview-profile-style">
    .portfolioforge-preview-profile {{
        position: fixed;
        right: 18px;
        bottom: 18px;
        z-index: 2147483647;
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 8px 11px 8px 8px;
        border: 1px solid rgba(255, 255, 255, .22);
        border-radius: 999px;
        background: rgba(16, 17, 22, .92);
        box-shadow: 0 10px 30px rgba(0, 0, 0, .28);
        color: #f8f8f3;
        font-family: Inter, Arial, sans-serif;
        font-size: 11px;
        font-weight: 700;
        line-height: 1;
        backdrop-filter: blur(12px);
    }}
    .portfolioforge-preview-profile img {{
        width: 28px;
        height: 28px;
        border: 1px solid rgba(255, 255, 255, .28);
        border-radius: 50%;
        object-fit: cover;
        object-position: center top;
    }}
    .portfolioforge-preview-profile span {{ color: #d9ff7f; }}
    @media print {{ .portfolioforge-preview-profile {{ display: none; }} }}
</style>
<aside class="portfolioforge-preview-profile" aria-label="Demo profile image included">
    <img src="{profile_image_base64}" alt="Adeel M. profile photo">
    <span>Profile included</span>
</aside>"""
        if "</body>" in rendered_html:
            return rendered_html.replace("</body>", f"{profile_badge}\n</body>")
        return f"{rendered_html}\n{profile_badge}"

    @staticmethod
    def _readme_text(page_count, profile_copy_name):
        return (
            "PORTFOLIOFORGE LOCAL PREVIEW PACK\n"
            "=================================\n\n"
            f"This folder contains {page_count} standalone portfolio previews and an index.html file.\n"
            "Open index.html in your browser to compare all templates.\n\n"
            f"The supplied profile image was copied here as {profile_copy_name} and embedded into every portfolio page.\n"
            "All names, project details, contact values, and URLs are rich demo content for visual review only.\n"
        )
