# 📘 SpendSmart AI — Complete Setup & Deployment Guide

---

## 📁 Project Structure

```
expense-app/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── .gitignore
├── .streamlit/
│   ├── config.toml                 # Streamlit theme config
│   └── secrets.toml.template       # Secrets template (copy & fill)
├── utils/
│   ├── __init__.py
│   ├── theme.py                    # Global CSS injection
│   ├── session.py                  # Session state helpers
│   ├── supabase_client.py          # All DB + Auth operations
│   ├── ai_advisor.py               # Claude AI integration
│   └── categories.py               # Category constants & icons
└── pages_modules/
    ├── __init__.py
    ├── auth_page.py                # Login / Sign Up
    ├── dashboard_page.py           # Dashboard with charts
    ├── add_expense_page.py         # Add expense form
    ├── expenses_page.py            # List, edit, delete, export
    └── ai_advisor_page.py          # AI insights page
```

---

## 🗄️ STEP 1 — Supabase Setup

### 1.1 Create a Supabase Project

1. Go to https://supabase.com and sign up (free)
2. Click **"New Project"**
3. Fill in:
   - **Name**: `spendsmart-ai`
   - **Database Password**: Choose a strong password (save it!)
   - **Region**: Choose closest to your users (e.g., `ap-south-1` for India)
4. Click **"Create new project"** — wait ~2 minutes for provisioning

### 1.2 Create the Expenses Table

Go to **Table Editor → New Table** or use the **SQL Editor** (recommended):

**SQL Editor → New Query → paste and run:**

```sql
-- Create the expenses table
CREATE TABLE expenses (
  id          BIGSERIAL PRIMARY KEY,
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  amount      NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
  category    TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for fast per-user queries
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
CREATE INDEX idx_expenses_created_at ON expenses(user_id, created_at DESC);
```

### 1.3 Enable Row Level Security (RLS)

**Run this in SQL Editor:**

```sql
-- Enable RLS on the expenses table
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only SELECT their own rows
CREATE POLICY "Users can view own expenses"
  ON expenses FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Users can only INSERT with their own user_id
CREATE POLICY "Users can insert own expenses"
  ON expenses FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only UPDATE their own rows
CREATE POLICY "Users can update own expenses"
  ON expenses FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only DELETE their own rows
CREATE POLICY "Users can delete own expenses"
  ON expenses FOR DELETE
  USING (auth.uid() = user_id);
```

### 1.4 Configure Auth Settings

1. Go to **Authentication → Settings**
2. Under **Email**, ensure **"Enable Email Signup"** is ON
3. Optional: Turn OFF **"Confirm email"** for faster dev/testing
   - (In production, keep it ON for security)

### 1.5 Get Your API Keys

1. Go to **Settings → API**
2. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon / public key** → `SUPABASE_ANON_KEY`

---

## 🤖 STEP 2 — Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up / Log in
3. Go to **API Keys → Create Key**
4. Copy the key → `ANTHROPIC_API_KEY`

> **Note**: The AI advisor degrades gracefully to a rule-based fallback if no API key is provided, so the app still works without it.

---

## 💻 STEP 3 — Local Development Setup

### 3.1 Clone / Download the project

```bash
# If using git
git init expense-app
cd expense-app
# Copy all files into this directory
```

### 3.2 Create a virtual environment

```bash
python -m venv venv

# Activate:
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3.3 Install dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Configure secrets

```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

Now edit `.streamlit/secrets.toml`:

```toml
SUPABASE_URL      = "https://abcdefgh.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGci..."
ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### 3.5 Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser. ✅

---

## 🚀 STEP 4 — Deploy on Streamlit Cloud

### 4.1 Push code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: SpendSmart AI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/spendsmart-ai.git
git push -u origin main
```

> ⚠️ Make sure `.streamlit/secrets.toml` is in `.gitignore` — NEVER push secrets!

### 4.2 Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository**: `YOUR_USERNAME/spendsmart-ai`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Advanced settings"** → **Secrets** tab
6. Paste your secrets:
   ```toml
   SUPABASE_URL      = "https://..."
   SUPABASE_ANON_KEY = "eyJ..."
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
7. Click **"Deploy!"** 🚀

Your app will be live at:
`https://YOUR_USERNAME-spendsmart-ai-app-XXXX.streamlit.app`

---

## 🔐 Security Checklist

| Item | Status |
|------|--------|
| RLS enabled on `expenses` table | ✅ Required |
| All 4 RLS policies created (SELECT/INSERT/UPDATE/DELETE) | ✅ Required |
| Secrets in `.streamlit/secrets.toml` (not hardcoded) | ✅ Required |
| `.streamlit/secrets.toml` in `.gitignore` | ✅ Required |
| Email confirmation enabled (production) | ✅ Recommended |
| ANON key used (not service_role key) | ✅ Required |

---

## 🧪 Testing the App

### Test flow:
1. **Sign Up** with a test email
2. **Add 5–10 expenses** across different categories
3. **Dashboard** — verify totals and chart appear
4. **My Expenses** — test edit and delete
5. **AI Advisor** — click "Analyze My Spending" and verify insights

### Test the RLS isolation:
1. Sign up with a second email
2. Verify you see **zero expenses** (not the first user's data)
3. Add expenses — verify they're completely separate

---

## 🛣️ Future Improvements Roadmap

### Phase 2 — Enhanced Analytics
- [ ] Monthly trend line chart
- [ ] Week-over-week comparison
- [ ] Budget limits per category with progress bars
- [ ] Spending calendar heatmap

### Phase 3 — Smart Features
- [ ] Recurring expense detection
- [ ] Bill reminders / due dates
- [ ] Receipt photo scanning (OCR via Claude Vision)
- [ ] WhatsApp bot integration for quick entry

### Phase 4 — Social & Goals
- [ ] Savings goals tracker
- [ ] Split expenses with friends
- [ ] Monthly PDF report generation
- [ ] Email digest (weekly summary)

### Phase 5 — Mobile & Voice
- [ ] Progressive Web App (PWA) manifest
- [ ] Voice expense entry via Web Speech API
- [ ] Push notifications for budget alerts
- [ ] Offline mode with sync

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `SUPABASE_URL not found` | Check `.streamlit/secrets.toml` exists and has correct keys |
| `Invalid login credentials` | Verify email + password; check if email confirmation is required |
| `RLS policy violation` | Ensure all 4 RLS policies are created in Supabase SQL Editor |
| `AI insights not loading` | Check `ANTHROPIC_API_KEY` — app falls back gracefully if missing |
| `App crashes on start` | Run `pip install -r requirements.txt` to ensure all packages installed |
| `Plotly charts not showing` | Ensure `plotly>=5.22.0` is installed |

---

## 📞 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.35 | UI framework |
| `supabase` | ≥2.4 | Auth + Database client |
| `anthropic` | ≥0.25 | Claude AI API |
| `plotly` | ≥5.22 | Interactive charts |
| `pandas` | ≥2.2 | Data manipulation + CSV export |

---

*Built with ❤️ using Streamlit + Supabase + Claude AI*
