import streamlit as st
import utils.supabase_client as supabase_client
import utils.categories as categories
from utils.session import get_user_id


def render():
    user_id = get_user_id()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">Add Expense</div>
        <div class="page-subtitle">Track your spending easily</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FORM ───────────────────────────────────────────
    with st.form("expense_form"):
        amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)

        category = st.selectbox(
            "Category",
            categories.get_categories()
        )

        description = st.text_input("Description")

        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if amount <= 0:
                st.error("Please enter a valid amount")
                return

            if not category:
                st.error("Please select a category")
                return

            res = supabase_client.add_expense(
                user_id,
                amount,
                category,
                description
            )

            if res["error"]:
                st.error(f"Error: {res['error']}")
            else:
                st.success("Expense added successfully!")
                st.rerun()
