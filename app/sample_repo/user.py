from auth import authenticate_user


def get_user_profile(
    token: str,
    user_id: int,
):
    return authenticate_user(
        token,
        user_id,
    )