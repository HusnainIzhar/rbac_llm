def individual_user(user):
    return {
        "id": str(user["_id"]),
        "email": user.get("email", ""),
        "full_name": user.get("full_name", ""),
        "role": user.get("role", "user"),
        "created_at": user.get("created_at", 0)
    }


def all_users(users):
    return [individual_user(user) for user in users]