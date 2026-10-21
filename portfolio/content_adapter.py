"""Compatibility adapter between legacy portfolio fields and structured content."""

from copy import deepcopy

from .schema_validation import apply_safe_defaults
from .schema_registry import get_schema


LEGACY_CONTENT_FIELDS = ("skills", "stats", "projects", "experience", "education")


def _read(source, key, default=None):
    if source is None:
        return default
    if isinstance(source, dict):
        return source.get(key, default)
    return getattr(source, key, default)


def legacy_content_from(source):
    return {
        key: deepcopy(_read(source, key, []))
        for key in LEGACY_CONTENT_FIELDS
    }


def adapt_content(template, structured_content=None, legacy_content=None):
    """Normalize structured content while retaining every legacy/unknown key."""
    schema = get_schema(template)
    raw = deepcopy(structured_content) if isinstance(structured_content, dict) else {}
    legacy = deepcopy(legacy_content or {})
    content = apply_safe_defaults(schema, raw)

    # Legacy values populate missing structured keys only. If a future schema
    # has a new value for a known key, the old value remains in `_legacy`.
    for key, value in legacy.items():
        if key not in raw:
            content[key] = deepcopy(value)

    legacy_snapshot = content.setdefault("_legacy", {})
    if not isinstance(legacy_snapshot, dict):
        legacy_snapshot = {}
        content["_legacy"] = legacy_snapshot
    for key, value in legacy.items():
        legacy_snapshot.setdefault(key, deepcopy(value))

    return content, schema


def add_content_context(context, *, template=None, source=None, structured_content=None):
    """Add new schema context without changing legacy template aliases."""
    template = template or _read(source, "template") or context.get("template")
    source = source or context.get("portfolio")
    structured_content = (
        structured_content
        if structured_content is not None
        else _read(source, "structured_content", context.get("structured_content", {}))
    )

    legacy = legacy_content_from(source)
    for key in LEGACY_CONTENT_FIELDS:
        if not legacy[key] and context.get(key):
            legacy[key] = deepcopy(context[key])

    content, schema = adapt_content(template, structured_content, legacy)
    content_schema_version = _read(
        source,
        "content_schema_version",
        schema["schema_version"],
    )
    try:
        content_schema_version = int(content_schema_version)
    except (TypeError, ValueError):
        content_schema_version = schema["schema_version"]
    context["structured_content"] = content
    context["content_schema_version"] = content_schema_version
    context["portfolio_schema"] = schema
    return context
