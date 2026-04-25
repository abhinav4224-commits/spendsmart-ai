import streamlit as st
import utils.supabase_client as supabase_client
from utils.session import get_user_id
import utils.categories as categories


def render():
    user_id = get_user_id()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">My Expenses</div>
        <div class="page-subtitle">Manage your transactions</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FETCH DATA ─────────────────────────────────────
    expenses = supabase_client.get_expenses(user_id)

    if not expenses:
        st.info("No expenses found.")
        return

    # ── DISPLAY EXPENSES ───────────────────────────────
    for e in expenses:
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"""
                <div style="font-weight:600;">
                    {categories.get_icon(e['category'])} {e['description']}
                </div>
                <div style="font-size:12px; color:gray;">
                    {e['category']}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"₹{e['amount']:,.2f}")

            with col3:
                if st.button("✏️", key=f"edit_{e['id']}"):
                    st.session_state["edit_id"] = e["id"]

                if st.button("🗑️", key=f"delete_{e['id']}"):
                    res = supabase_client.delete_expense(e["id"], user_id)
                    if res["error"]:
                        st.error(res["error"])
                    else:
                        st.success("Deleted")
                        st.rerun()

    # ── EDIT MODE ─────────────────────────────────────
    edit_id = st.session_state.get("edit_id")

    if edit_id:
        st.markdown("### ✏️ Edit Expense")

        exp = next((x for x in expenses if x["id"] == edit_id), None)

        if exp:
            amount = st.number_input("Amount", value=float(exp["amount"]))
            category = st.selectbox(
                "Category",
                categories.get_categories(),
                index=categories.get_categories().index(exp["category"])
            )
            description = st.text_input("Description", value=exp["description"])

            if st.button("Update Expense"):
                res = supabase_client.update_expense(
                    edit_id,
                    user_id,
                    amount,
                    category,
                    description
                )

                if res["error"]:
                    st.error(res["error"])
                else:
                    st.success("Updated successfully")
                    st.session_state.pop("edit_id")
                    st.rerun()
