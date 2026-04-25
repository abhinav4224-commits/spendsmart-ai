import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
        :root {
            --bg-card: #111827;
            --border: #1f2937;
            --text-primary: #f9fafb;
            --text-secondary: #9ca3af;
            --radius-lg: 12px;
        }

        body {
            background-color: #0f172a;
            color: var(--text-primary);
        }

        .page-header {
            margin-bottom: 20px;
        }

        .page-title {
            font-size: 28px;
            font-weight: 700;
        }

        .page-subtitle {
            font-size: 14px;
            color: var(--text-secondary);
        }

        .stat-card {
            background: var(--bg-card);
            padding: 16px;
            border-radius: var(--radius-lg);
            border: 1px solid var(--border);
        }
    </style>
    """, unsafe_allow_html=True)
