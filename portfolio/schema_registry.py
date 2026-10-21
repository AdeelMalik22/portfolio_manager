"""Versioned, composable schemas for portfolio content.

The registry is intentionally independent from the builder UI.  It provides a
stable contract for validation and future schema-driven forms while existing
templates continue to consume the legacy context keys.
"""

from copy import deepcopy


CURRENT_SCHEMA_KEY = "portfolio"
CURRENT_SCHEMA_VERSION = 1


def _field(field_id, field_type="text", *, required=False, default=None, **metadata):
    field = {
        "id": field_id,
        "type": field_type,
        "required": required,
        "default": default,
    }
    field.update(metadata)
    return field


SHARED_SCHEMA = {
    "sections": [
        {
            "id": "profile",
            "label": "Profile",
            "fields": [
                _field("full_name", required=True, default=""),
                _field("title", required=True, default=""),
                _field("bio", "textarea", required=True, default=""),
                _field("email", "email", required=True, default=""),
                _field("phone", default=""),
                _field("location", default=""),
                _field("profile_image", "image", default=None),
            ],
        },
        {
            "id": "links",
            "label": "Links",
            "fields": [
                _field("linkedin", "url", default=""),
                _field("github", "url", default=""),
                _field("portfolio_website", "url", default=""),
                _field("twitter", "url", default=""),
            ],
        },
        {
            "id": "work",
            "label": "Work",
            "fields": [
                _field("skills", "repeatable", default=[], item_type="text"),
                _field("stats", "repeatable", default=[], item_type="stat"),
                _field("projects", "repeatable", default=[], item_type="project"),
            ],
        },
        {
            "id": "record",
            "label": "Experience and education",
            "fields": [
                _field("experience", "repeatable", default=[], item_type="experience"),
                _field("education", "repeatable", default=[], item_type="education"),
            ],
        },
    ],
    "defaults": {
        "skills": [],
        "stats": [],
        "projects": [],
        "experience": [],
        "education": [],
    },
}


CATEGORY_SCHEMAS = {
    "developer": {
        "sections": [
            {
                "id": "developer_context",
                "label": "Developer context",
                "fields": [
                    _field("primary_stack", default=""),
                    _field("availability", default=""),
                ],
            }
        ]
    },
    "creative": {
        "sections": [
            {
                "id": "creative_context",
                "label": "Creative context",
                "fields": [
                    _field("practice", default=""),
                    _field("services", "repeatable", default=[], item_type="text"),
                ],
            }
        ]
    },
    "corporate": {
        "sections": [
            {
                "id": "professional_context",
                "label": "Professional context",
                "fields": [
                    _field("industry", default=""),
                    _field("consulting_focus", default=""),
                ],
            }
        ]
    },
    "minimalist": {
        "sections": [
            {
                "id": "minimal_context",
                "label": "Minimal context",
                "fields": [
                    _field("descriptor", default=""),
                ],
            }
        ]
    },
}


TEMPLATE_OVERRIDES = {
    "architect_portfolio": {
        "sections": [
            {
                "id": "architect_context",
                "label": "Architect context",
                "fields": [
                    _field("architectural_thesis", "textarea", default=""),
                ],
            }
        ]
    },
}


# A schema key owns versions.  Category and template definitions are composed
# into the returned schema; they are not separate forms.
SCHEMA_REGISTRY = {
    CURRENT_SCHEMA_KEY: {
        CURRENT_SCHEMA_VERSION: {
            "base": SHARED_SCHEMA,
            "categories": CATEGORY_SCHEMAS,
            "templates": TEMPLATE_OVERRIDES,
        }
    }
}


def _merge_schema(base, extension):
    """Merge sections and fields by stable IDs while preserving unknown data."""
    result = deepcopy(base)
    extension = extension or {}
    sections = {section["id"]: section for section in result.get("sections", [])}

    for section in extension.get("sections", []):
        section_id = section["id"]
        if section_id not in sections:
            result.setdefault("sections", []).append(deepcopy(section))
            sections[section_id] = result["sections"][-1]
            continue

        fields = {field["id"]: field for field in sections[section_id].get("fields", [])}
        for field in section.get("fields", []):
            if field["id"] in fields:
                fields[field["id"]].update(deepcopy(field))
            else:
                sections[section_id].setdefault("fields", []).append(deepcopy(field))

    result.setdefault("defaults", {}).update(deepcopy(extension.get("defaults", {})))
    return result


def get_schema(template=None, *, schema_key=None, schema_version=None):
    """Return a composed schema with safe fallback for unknown metadata."""
    requested_key = schema_key or getattr(template, "schema_key", None) or CURRENT_SCHEMA_KEY
    requested_version = schema_version or getattr(template, "schema_version", None) or CURRENT_SCHEMA_VERSION

    try:
        requested_version = int(requested_version)
    except (TypeError, ValueError):
        requested_version = CURRENT_SCHEMA_VERSION

    registry = SCHEMA_REGISTRY.get(requested_key) or SCHEMA_REGISTRY[CURRENT_SCHEMA_KEY]
    version = requested_version if requested_version in registry else CURRENT_SCHEMA_VERSION
    definition = registry.get(version) or SCHEMA_REGISTRY[CURRENT_SCHEMA_KEY][CURRENT_SCHEMA_VERSION]

    schema = deepcopy(definition["base"])
    category = getattr(template, "category", None)
    slug = getattr(template, "slug", None)
    schema = _merge_schema(schema, definition.get("categories", {}).get(category, {}))
    schema = _merge_schema(schema, definition.get("templates", {}).get(slug, {}))
    schema["schema_key"] = requested_key if requested_key in SCHEMA_REGISTRY else CURRENT_SCHEMA_KEY
    schema["schema_version"] = version
    schema["requested_schema_key"] = requested_key
    schema["requested_schema_version"] = requested_version
    return schema


def iter_fields(schema):
    for section in schema.get("sections", []):
        yield from section.get("fields", [])
