import streamlit as st


# ── SET SESSION ───────────────────────────────────────
def set_session(user_id, email, access_token, refresh_token):
    st.session_state["user_id"] = user_id
    st.session_state["email"] = email
    st.session_state["access_token"] = access_token
    st.session_state["refresh_token"] = refresh_token


# ── GET USER ──────────────────────────────────────────
def get_user_id():
    return st.session_state.get("user_id")


def is_logged_in():
    return "user_id" in st.session_state


# ── LOGOUT ────────────────────────────────────────────
def logout():
    keys = ["user_id", "email", "access_token", "refresh_token"]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]
