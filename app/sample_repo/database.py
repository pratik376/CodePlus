USERS = {
    1: {
        "id": 1,
        "name": "Pratik",
    }
}


def find_user(user_id: int):
    return USERS.get(user_id)