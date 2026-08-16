import re


IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

CAMEL_CASE_PATTERN = re.compile(
    r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|[0-9]+"
)


def split_identifier(identifier: str) -> list[str]:
    """
    Split code identifiers into searchable terms.

    Examples:
        authentication_token -> authentication, token
        validateToken        -> validate, token
        DatabaseConnection   -> database, connection
    """

    parts = []

    for section in identifier.split("_"):
        if not section:
            continue

        matches = CAMEL_CASE_PATTERN.findall(section)

        parts.extend(
            match.lower()
            for match in matches
        )

    return parts


def tokenize(text: str) -> list[str]:
    """
    Extract and normalize searchable tokens from source code.
    """

    if not text:
        return []

    tokens = []

    for identifier in IDENTIFIER_PATTERN.findall(text):
        tokens.extend(
            split_identifier(identifier)
        )

    return tokens