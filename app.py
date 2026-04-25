import streamlit as st

# Import pages
from pages_modules import (
    auth_page,
    dashboard_page,
    add_expense_page,
    expenses_page,
    ai_advisor_page,
    spend_control_page
)

from utils.session import is_logged_in, logout

# ── PAGE CONFIG ─────────────────────────────────────────
st.set_page_config(
    page_title="SpendSmart AI",
    layout="wide"
)

# ── CUSTOM THEME ────────────────────────────────────────
from utils.theme import apply_theme
apply_theme()

# ── AUTH CHECK ──────────────────────────────────────────
if not is_logged_in():
    auth_page.render()
    st.stop()

# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 SpendSmart AI")

    st.markdown("---")

    selected = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Expense",
            "My Expenses",
            "Spend Control",   # ✅ NEW FEATURE
            "AI Advisor"
        ]
    )

    st.markdown("---")

    if st.button("🚪 Sign Out"):
        logout()
        st.rerun()

# ── PAGE ROUTING ────────────────────────────────────────
if selected == "Dashboard":
    dashboard_page.render()

elif selected == "Add Expense":
    add_expense_page.render()

elif selected == "My Expenses":
    expenses_page.render()

elif selected == "Spend Control":
    spend_control_page.render()   # ✅ NEW PAGE

elif selected == "AI Advisor":
    ai_advisor_page.render()
