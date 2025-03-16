def individual_user(llm):
    return {
        "id": str(llm["id"]),
        "title": llm["title"],
        "first_name": llm["first_name"],
    }


def all_users(llm):
    return [individual_user(llm) for llm in llm]
