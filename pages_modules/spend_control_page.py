import streamlit as st
from utils.session import get_user_id
import utils.budget as budget
import utils.supabase_client as supabase_client


def render():
    user_id = get_user_id()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">Spend Control</div>
        <div class="page-subtitle">Manage your budget effectively</div>
    </div>
    """, unsafe_allow_html=True)

    # ── GET EXISTING BUDGET ─────────────────────────────
    budget_data = budget.get_budget(user_id)

    income = st.number_input(
        "Monthly Income",
        value=budget_data["monthly_income"] if budget_data else 0
    )

    limit = st.number_input(
        "Budget Limit",
        value=budget_data["budget_limit"] if budget_data else 0
    )

    if st.button("Save Budget"):
        budget.save_budget(user_id, income, limit)
        st.success("Budget saved successfully!")

    # ── CALCULATE SPENDING ──────────────────────────────
    expenses = supabase_client.get_expenses(user_id)
    total_spent = sum([e["amount"] for e in expenses])

    # ── PROGRESS BAR ────────────────────────────────────
    if limit > 0:
        percent = total_spent / limit

        if percent < 0.6:
            color = "green"
        elif percent < 0.85:
            color = "orange"
        else:
            color = "red"

        st.markdown(f"""
        <div style="background:#1e1e1e; border-radius:10px; padding:10px;">
            <div style="
                width:{min(percent*100, 100)}%;
                background:{color};
                height:20px;
                border-radius:10px;
                transition:0.3s;">
            </div>
        </div>
        <p style="color:{color}; font-weight:bold;">
            ₹{total_spent:.0f} / ₹{limit:.0f}
        </p>
        """, unsafe_allow_html=True)
