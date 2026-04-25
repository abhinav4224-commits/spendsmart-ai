from supabase import create_client
import streamlit as st

# ── LOAD ENV VARIABLES ───────────────────────────────
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY")

# ── VALIDATION (IMPORTANT) ───────────────────────────
if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials are missing in Streamlit secrets.")

# ── CREATE CLIENT (THIS FIXES YOUR ERROR) ────────────
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ── EXPENSE FUNCTIONS ────────────────────────────────
def get_expenses(user_id):
    res = supabase.table("expenses").select("*").eq("user_id", user_id).execute()
    return res.data if res.data else []


def get_spending_summary(expenses):
    if not expenses:
        return {
            "total": 0,
            "count": 0,
            "top_category": None,
            "by_category": {},
            "avg_transaction": 0,
            "top_category_amount": 0
        }

    total = sum(e["amount"] for e in expenses)
    count = len(expenses)

    by_category = {}
    for e in expenses:
        cat = e["category"]
        by_category[cat] = by_category.get(cat, 0) + e["amount"]

    top_category = max(by_category, key=by_category.get)
    top_amount = by_category[top_category]

    avg = total / count if count > 0 else 0

    return {
        "total": total,
        "count": count,
        "top_category": top_category,
        "by_category": by_category,
        "avg_transaction": avg,
        "top_category_amount": top_amount
    }
