schema = {
    "type": "object",
    "required": ["summary", "created_at"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "summary": {"type": "string", "minLength": 3, "maxLength": 26},
        "detail": {"type": "string", "maxLength": 255},
        "tags": {"type": "array", "items": {"type": "string"}},
        "created_at": {"type": "string", "format": "date-time"},
    },
}

schema_tags = {
    "type": "object",
    "required": ["tags"],
    "properties": {
        "tags": {"type": "array", "items": {"type": "string"}, "minItems": 1,"uniqueItems": True},
    },
}