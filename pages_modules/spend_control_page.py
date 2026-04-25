import streamlit as st
from utils.session import get_user_id
from utils.budget import get_budget, save_budget
from utils.supabase_client import get_expenses

def render():
    user_id = get_user_id()
    st.title("💸 Spend Control")

    budget = get_budget(user_id)

    income = st.number_input("Monthly Income", value=budget["monthly_income"] if budget else 0)
    limit = st.number_input("Budget Limit", value=budget["budget_limit"] if budget else 0)

    if st.button("Save Budget"):
        save_budget(user_id, income, limit)
        st.success("Budget saved!")

    # Progress bar
    expenses = get_expenses(user_id)
    total_spent = sum([e["amount"] for e in expenses])

    if limit > 0:
        percent = total_spent / limit

        if percent < 0.6:
            color = "green"
        elif percent < 0.85:
            color = "orange"
        else:
            color = "red"

        st.markdown(f"""
        <div style="background:#222; border-radius:10px; padding:10px;">
            <div style="width:{percent*100}%; background:{color};
                        height:20px; border-radius:10px;">
            </div>
        </div>
        <p style="color:{color}; font-weight:bold;">
            ₹{total_spent} / ₹{limit}
        </p>
        """, unsafe_allow_html=True)