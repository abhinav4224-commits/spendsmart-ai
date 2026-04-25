import streamlit as st
from utils.session import get_user_id
from utils.supabase_client import get_expenses, get_spending_summary
from utils.ai_advisor import generate_insight
from utils.budget import get_budget


def render():
    user_id = get_user_id()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">AI Financial Advisor</div>
        <div class="page-subtitle">Smart insights to improve your spending</div>
    </div>
    """, unsafe_allow_html=True)

    # ── LOAD DATA ─────────────────────────────────────────
    with st.spinner("Analyzing your finances..."):
        expenses = get_expenses(user_id)
        summary = get_spending_summary(expenses)
        budget = get_budget(user_id)

    # ── EMPTY STATE ───────────────────────────────────────
    if not expenses:
        st.markdown("""
        <div style="text-align:center; padding:60px; background:var(--bg-card);
                    border-radius:var(--radius-lg); border:1px solid var(--border);">
            <div style="font-size:40px;">🤖</div>
            <div style="font-size:20px; font-weight:600;">No data to analyze</div>
            <div style="color:var(--text-secondary); font-size:14px;">
                Add some expenses to get AI insights
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── GENERATE AI INSIGHTS ──────────────────────────────
    insights = generate_insight(summary, budget)

    # ── MAIN AI CARD ──────────────────────────────────────
    st.markdown("""
    <div style="background:var(--bg-card); padding:20px;
                border-radius:var(--radius-lg); border:1px solid var(--border);">
        <div style="font-size:18px; font-weight:600; margin-bottom:10px;">
            🤖 AI Insights for You
        </div>
    """, unsafe_allow_html=True)

    # ── DISPLAY INSIGHTS ──────────────────────────────────
    for insight in insights:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);
                    padding:12px 16px;
                    border-radius:10px;
                    margin-bottom:10px;
                    border:1px solid rgba(255,255,255,0.05);">
            {insight}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── EXTRA SUMMARY (OPTIONAL BUT GOOD UX) ──────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:var(--bg-card); padding:16px;
                border-radius:var(--radius-lg); border:1px solid var(--border);">
        <div style="font-size:16px; font-weight:600; margin-bottom:8px;">
            📊 Quick Summary
        </div>
        <div>Total Spent: ₹{summary['total']:,.0f}</div>
        <div>Transactions: {summary['count']}</div>
        <div>Top Category: {summary.get('top_category', '—')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── BUTTON FOR REFRESHING INSIGHTS ────────────────────
    if st.button("🔄 Generate New Insights"):
        st.rerun()
