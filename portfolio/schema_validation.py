"""Validation and defaulting for structured portfolio content."""

from copy import deepcopy

from .schema_registry import get_schema, iter_fields


class StructuredContentValidationError(ValueError):
    """Raised when explicitly submitted structured content is invalid."""

    def __init__(self, errors):
        self.errors = errors
        super().__init__("Structured portfolio content is invalid.")


def _default_for_field(field):
    if "default" in field:
        return deepcopy(field["default"])
    if field.get("type") == "repeatable":
        return []
    if field.get("type") == "checkbox":
        return False
    return ""


def apply_safe_defaults(schema, content):
    """Apply declared defaults without deleting unknown user-provided keys."""
    normalized = deepcopy(content) if isinstance(content, dict) else {}
    for field in iter_fields(schema):
        field_id = field["id"]
        if field_id not in normalized or normalized[field_id] is None:
            normalized[field_id] = _default_for_field(field)
        elif field.get("type") == "repeatable" and not isinstance(normalized[field_id], list):
            normalized[field_id] = []
    return normalized
def validate_structured_content(template, content, *, strict=False):
    """Return normalized content, validating known fields and preserving extras.

    ``strict=False`` is used while reading legacy records so missing structured
    fields receive defaults instead of invalidating old portfolios.  New API
    writes can opt into strict required-field validation.
    """
    if content in (None, ""):
        content = {}
    if not isinstance(content, dict):
        raise StructuredContentValidationError({"structured_content": "Expected an object."})

    schema = get_schema(template)
    normalized = apply_safe_defaults(schema, content)
    if not strict:
        return normalized

    errors = {}
    for field in iter_fields(schema):
        if not field.get("required"):
            continue
        value = normalized.get(field["id"])
        if value in (None, "", []):
            errors[field["id"]] = "This field is required."

    if errors:
        raise StructuredContentValidationError(errors)
    return normalized
# End of schema validation helpers.
