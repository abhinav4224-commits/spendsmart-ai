from supabase import create_client
import streamlit as st

# ── CLIENT SETUP ──────────────────────────────────────
@st.cache_resource
def get_supabase_client():
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_ANON_KEY")

    if not url or not key:
        st.error("Missing Supabase credentials")
        st.stop()

    return create_client(url, key)


def get_authed_client():
    client = get_supabase_client()

    token = st.session_state.get("access_token")

    if token:
        client.auth.set_session(
            access_token=token,
            refresh_token=st.session_state.get("refresh_token", "")
        )

    return client


# ── AUTH FUNCTIONS (FIXED) ────────────────────────────
def sign_up(email: str, password: str):
    client = get_supabase_client()

    try:
        res = client.auth.sign_up({
            "email": email,
            "password": password
        })

        return {
            "user": res.user if res.user else None,
            "access_token": res.session.access_token if res.session else None,
            "refresh_token": res.session.refresh_token if res.session else None,
            "error": None
        }

    except Exception as e:
        return {
            "user": None,
            "access_token": None,
            "refresh_token": None,
            "error": str(e)
        }


def sign_in(email: str, password: str):
    client = get_supabase_client()

    try:
        res = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        return {
            "user": {
                "id": res.user.id,
                "email": res.user.email
            },
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "error": None
        }

    except Exception as e:
        return {
            "user": None,
            "access_token": None,
            "refresh_token": None,
            "error": str(e)
        }


# ── EXPENSE FUNCTIONS ─────────────────────────────────
def get_expenses(user_id):
    client = get_authed_client()

    res = (
        client.table("expenses")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return res.data or []


def add_expense(user_id, amount, category, description):
    client = get_authed_client()

    res = client.table("expenses").insert({
        "user_id": user_id,
        "amount": float(amount),
        "category": category,
        "description": description
    }).execute()

    return {"data": res.data, "error": None}


def update_expense(expense_id, user_id, amount, category, description):
    client = get_authed_client()

    res = client.table("expenses").update({
        "amount": float(amount),
        "category": category,
        "description": description
    }).eq("id", expense_id).eq("user_id", user_id).execute()

    return {"data": res.data, "error": None}


def delete_expense(expense_id, user_id):
    client = get_authed_client()

    client.table("expenses").delete().eq("id", expense_id).eq("user_id", user_id).execute()

    return {"error": None}
