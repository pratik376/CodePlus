from app.search.tokenizer import tokenize


def test_tokenizer():
    result = tokenize(
        "def validate_access_token(user_id):"
    )

    assert result == [
        "def",
        "validate",
        "access",
        "token",
        "user",
        "id",
    ]


def test_camel_case_identifier():
    result = tokenize(
        "validateAccessToken"
    )

    assert result == [
        "validate",
        "access",
        "token",
    ]


def test_pascal_case_identifier():
    result = tokenize(
        "DatabaseConnection"
    )

    assert result == [
        "database",
        "connection",
    ]


def test_empty_text():
    assert tokenize("") == []