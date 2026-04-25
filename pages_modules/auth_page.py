import streamlit as st
import utils.supabase_client as supabase_client
from utils.session import set_session


def render():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Welcome to SpendSmart AI</div>
        <div class="page-subtitle">Track your expenses smartly</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ── LOGIN ─────────────────────────────────────────
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if not email or not password:
                st.error("Please enter email and password")
                return

            res = supabase_client.sign_in(email, password)

            if res["error"]:
                st.error(res["error"])
            else:
                set_session(
                    res["user"]["id"],
                    res["user"]["email"],
                    res["access_token"],
                    res["refresh_token"]
                )
                st.success("Login successful!")
                st.rerun()

    # ── SIGN UP ───────────────────────────────────────
    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Create Account"):
            if not email or not password:
                st.error("Please enter email and password")
                return

            res = supabase_client.sign_up(email, password)

            if res["error"]:
                st.error(res["error"])
            else:
                st.success("Account created! Please login.")
