from apischema.validator import validate_todo_entry, validate_tags


def test_short_summary_in_todo_entry() -> None:
    data = {
        "summary": "Lo",
        "detail": "",
        "created_at": "2022-09-05T18:07:19.280040+00:00",
    }

    error = validate_todo_entry(raw_data=data)
    assert error.path == "summary"
    assert "maxLength" in error.validation_schema
    assert "minLength" in error.validation_schema
    assert "type" in error.validation_schema


def test_sample_tags() -> None:
    data = {
        "tags": ["doc", "secret"],
    }

    error = validate_tags(raw_data=data)
    assert not error


def test_empty_tags() -> None:
    data = {
        "tags": [],
    }

    error = validate_tags(raw_data=data)
    assert error.path == "tags"
    assert "minItems" in error.validation_schema
