"""Context builders for safe, no-save portfolio previews."""

from __future__ import annotations

import base64
import json
import mimetypes
from copy import deepcopy
from types import SimpleNamespace


MAX_PREVIEW_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_PREVIEW_IMAGE_TYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
}


class PreviewPayloadError(ValueError):
    """Raised when a browser-only preview payload cannot be rendered safely."""


def _sample_portrait_data_uri() -> str:
    """Return a neutral, embedded illustration for public template examples.

    Gallery previews deliberately use a fictitious, non-user portrait. A real
    visitor's image is only sent to the no-save draft preview after they choose
    it themselves in the builder.
    """
    svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 900" role="img" aria-label="Sample portfolio portrait">
      <rect width="720" height="900" fill="#111827"/>
      <circle cx="550" cy="160" r="170" fill="#b8d7d9" opacity=".75"/>
      <path d="M0 720C145 630 244 604 360 604c136 0 246 45 360 142v154H0z" fill="#234451"/>
      <path d="M165 900c10-185 80-289 195-289s188 104 198 289z" fill="#d8e9e9"/>
      <path d="M211 900c9-161 62-256 149-256s144 95 152 256z" fill="#1b2f3d"/>
      <ellipse cx="360" cy="330" rx="142" ry="176" fill="#d5a37e"/>
      <path d="M216 350c5-167 71-244 149-244 111 0 170 100 143 249-38-44-75-61-148-61-55 0-100 18-144 56z" fill="#18222d"/>
      <path d="M246 519c26 44 67 69 114 69s92-25 116-69c-28 18-64 27-116 27s-88-9-114-27z" fill="#c48b6d"/>
      <circle cx="310" cy="354" r="9" fill="#1e2934"/>
      <circle cx="413" cy="354" r="9" fill="#1e2934"/>
      <path d="M316 444c26 19 62 19 88 0" fill="none" stroke="#8d5446" stroke-width="10" stroke-linecap="round"/>
      <path d="M218 722 360 805 502 722 468 900H252z" fill="#f5f1e9"/>
      <path d="m360 805 38 95h-76z" fill="#8f6555"/>
    </svg>
    """.strip()
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


SAMPLE_PROFILE_IMAGE = _sample_portrait_data_uri()

SAMPLE_SKILLS = [
    "Product strategy",
    "Digital transformation",
    "System design",
    "Django",
    "Python",
    "React",
    "Design systems",
    "User research",
    "API design",
    "Team leadership",
    "Analytics",
    "Technical writing",
]

SAMPLE_PROJECTS = [
    {
        "title": "PortfolioForge Studio",
        "description": (
            "A complete portfolio platform that turns a guided content workflow into "
            "a refined, responsive site owners can publish anywhere."
        ),
        "tech_stack": "Django · Design systems · Product strategy",
        "technologies": "Django, Python, JavaScript, HTML, CSS",
        "github_link": "https://github.example/morgan-lee/portfolioforge-studio",
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
        "github_link": "https://github.example/morgan-lee/atlas-operations",
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
        "github_link": "https://github.example/morgan-lee/signal-commerce",
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
        "github_link": "https://github.example/morgan-lee/ledger-assistant",
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
        "github_link": "https://github.example/morgan-lee/field-notes",
        "live_link": "https://portfolioforge.example/field-notes",
        "project_url": "https://portfolioforge.example/field-notes",
    },
]

SAMPLE_EXPERIENCE = [
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
]

SAMPLE_EDUCATION = [
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

SAMPLE_PROFILE = {
    "full_name": "Morgan Lee",
    "title": "Product & Technology Strategist",
    "bio": (
        "A product-minded technology leader who turns ambiguous business goals into "
        "clear, scalable digital experiences. I work across strategy, design systems, "
        "and engineering to make complex things feel understandable."
    ),
    "email": "morgan@example.com",
    "phone": "+1 415 555 0142",
    "location": "San Francisco, California",
    "linkedin": "https://linkedin.example/morgan-lee",
    "github": "https://github.example/morgan-lee",
    "portfolio_website": "https://portfolio.example/morgan-lee",
    "twitter": "https://x.example/morgan-lee",
}


def _portfolio_context(template, profile, image_data_uri, skills, projects, experience, education):
    """Create the aliases used across the independent template families."""
    portfolio = SimpleNamespace(
        **profile,
        profile_image=SimpleNamespace(url=image_data_uri) if image_data_uri else None,
        processed_profile_image=None,
        skills=skills,
        projects=projects,
        experience=experience,
        education=education,
        template=template,
    )
    return {
        **profile,
        "portfolio": portfolio,
        "website": profile["portfolio_website"],
        "website_url": profile["portfolio_website"],
        "github_url": profile["github"],
        "linkedin_url": profile["linkedin"],
        "twitter_url": profile["twitter"],
        "profile_image": image_data_uri,
        "profile_image_url": image_data_uri,
        "profile_image_base64": image_data_uri,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": education,
        "template_color": template.color_scheme,
    }


def build_sample_preview_context(template, profile_image_base64=None):
    """Return a complete, clearly fictitious example portfolio."""
    return _portfolio_context(
        template=template,
        profile=deepcopy(SAMPLE_PROFILE),
        image_data_uri=profile_image_base64 or SAMPLE_PROFILE_IMAGE,
        skills=deepcopy(SAMPLE_SKILLS),
        projects=deepcopy(SAMPLE_PROJECTS),
        experience=deepcopy(SAMPLE_EXPERIENCE),
        education=deepcopy(SAMPLE_EDUCATION),
    )


def _read_json_list(payload, field_name):
    raw_value = payload.get(field_name, "")
    if not raw_value:
        return []
    try:
        value = json.loads(raw_value)
    except (TypeError, json.JSONDecodeError) as exc:
        raise PreviewPayloadError(f"Invalid {field_name} preview data.") from exc
    if not isinstance(value, list):
        raise PreviewPayloadError(f"Invalid {field_name} preview data.")
    return value


def _normalise_projects(projects):
    normalised = []
    for item in projects:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        if not title:
            continue
        normalised.append({
            "title": title,
            "description": str(item.get("description", "")).strip(),
            "tech_stack": str(item.get("tech_stack", "")).strip(),
            "technologies": str(item.get("technologies", item.get("tech_stack", ""))).strip(),
            "github_link": str(item.get("github_link", "")).strip(),
            "live_link": str(item.get("live_link", "")).strip(),
            "project_url": str(item.get("project_url", item.get("live_link", ""))).strip(),
        })
    return normalised


def _normalise_experience(experience):
    normalised = []
    for item in experience:
        if not isinstance(item, dict):
            continue
        company = str(item.get("company", "")).strip()
        role = str(item.get("role", item.get("title", ""))).strip()
        if not company and not role:
            continue
        normalised.append({
            "company": company,
            "role": role,
            "title": role,
            "job_title": role,
            "duration": str(item.get("duration", "")).strip(),
            "start_date": str(item.get("start_date", "")).strip(),
            "end_date": str(item.get("end_date", "")).strip(),
            "description": str(item.get("description", "")).strip(),
        })
    return normalised


def _normalise_education(education):
    normalised = []
    for item in education:
        if not isinstance(item, dict):
            continue
        school = str(item.get("school", item.get("institution", ""))).strip()
        degree = str(item.get("degree", "")).strip()
        if not school and not degree:
            continue
        normalised.append({
            "school": school,
            "institution": school,
            "degree": degree,
            "field": str(item.get("field", "")).strip(),
            "year": str(item.get("year", "")).strip(),
            "start_date": str(item.get("start_date", "")).strip(),
            "end_date": str(item.get("end_date", "")).strip(),
        })
    return normalised


def _image_data_uri(image_file):
    if not image_file:
        return None
    if image_file.size and image_file.size > MAX_PREVIEW_IMAGE_BYTES:
        raise PreviewPayloadError("Profile images for preview must be 5 MB or smaller.")

    mime_type = image_file.content_type or mimetypes.guess_type(image_file.name)[0]
    if mime_type not in ALLOWED_PREVIEW_IMAGE_TYPES:
        raise PreviewPayloadError("Use a PNG, JPG, GIF, or WebP profile image for preview.")

    image_data = image_file.read()
    if not image_data:
        raise PreviewPayloadError("The selected profile image is empty.")
    if len(image_data) > MAX_PREVIEW_IMAGE_BYTES:
        raise PreviewPayloadError("Profile images for preview must be 5 MB or smaller.")

    encoded = base64.b64encode(image_data).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def build_draft_preview_context(template, payload, image_file=None):
    """Render the unsaved form values without storing them anywhere.

    A blank builder opens as a rich sample. As soon as the visitor adds any
    detail or an image, the preview switches to their exact draft, so sample
    contact information never appears alongside their identity.
    """
    profile_image_base64 = _image_data_uri(image_file)
    skills = [str(skill).strip() for skill in _read_json_list(payload, "skills") if str(skill).strip()]
    projects = _normalise_projects(_read_json_list(payload, "projects"))
    experience = _normalise_experience(_read_json_list(payload, "experience"))
    education = _normalise_education(_read_json_list(payload, "education"))

    profile_fields = (
        "full_name",
        "title",
        "bio",
        "email",
        "phone",
        "location",
        "linkedin",
        "github",
        "portfolio_website",
        "twitter",
    )
    profile = {field: str(payload.get(field, "")).strip() for field in profile_fields}
    has_draft_content = any(profile.values()) or any((skills, projects, experience, education)) or bool(profile_image_base64)
    if not has_draft_content:
        return build_sample_preview_context(template)

    display_profile = {
        "full_name": profile["full_name"] or "Your name",
        "title": profile["title"] or "Your professional title",
        "bio": profile["bio"] or "Add a concise introduction to see how your story will read here.",
        "email": profile["email"],
        "phone": profile["phone"],
        "location": profile["location"],
        "linkedin": profile["linkedin"],
        "github": profile["github"],
        "portfolio_website": profile["portfolio_website"],
        "twitter": profile["twitter"],
    }
    return _portfolio_context(
        template=template,
        profile=display_profile,
        image_data_uri=profile_image_base64,
        skills=skills,
        projects=projects,
        experience=experience,
        education=education,
    )
