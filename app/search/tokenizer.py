import re


IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def tokenize(text: str) -> list[str]:
    if not text:
        return []

    return [
        token.lower()
        for token in IDENTIFIER_PATTERN.findall(text)
    ]