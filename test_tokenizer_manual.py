from app.search.tokenizer import tokenize


examples = [
    "authentication_token",
    "validateToken",
    "DatabaseConnection",
    "AUTHENTICATION",
    "get_user_by_id",
]

for example in examples:
    print(example, "->", tokenize(example))