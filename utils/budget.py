import utils.supabase_client as supabase_client


def get_budget(user_id):
    client = supabase_client.get_authed_client()

    res = (
        client.table("user_budget")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return res.data[0] if res.data else None


def save_budget(user_id, income, limit):
    client = supabase_client.get_authed_client()

    existing = get_budget(user_id)

    if existing:
        client.table("user_budget").update({
            "monthly_income": income,
            "budget_limit": limit
        }).eq("user_id", user_id).execute()
    else:
        client.table("user_budget").insert({
            "user_id": user_id,
            "monthly_income": income,
            "budget_limit": limit
        }).execute()
