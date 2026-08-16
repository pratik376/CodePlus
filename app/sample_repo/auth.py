from database import find_user


def validate_token(token: str):
    return token == "valid-token"


def authenticate_user(
    token: str,
    user_id: int,
):
    if not validate_token(token):
        return None

    return find_user(user_id)