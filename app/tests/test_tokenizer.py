from app.search.tokenizer import tokenize


def test_tokenizer():
    result = tokenize(
        "def validate_access_token(user_id):"
    )

    assert result == [
        "def",
        "validate_access_token",
        "user_id",
    ]


def test_empty_text():
    assert tokenize("") == []