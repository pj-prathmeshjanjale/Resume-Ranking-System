"""
fix_light_theme.py — Replaces light mode CSS in app.py with bulletproof high-contrast rules.
"""
import re

light_css_block = '''    if app_theme == "☀️ Light Mode":
        st.markdown("""
        <style>
        /* Base & Background */
        :root, body, .stApp {
            background-color: #f8fafc !important;
            background-image: radial-gradient(circle, rgba(100,116,139,0.1) 1px, transparent 1px) !important;
            color: #0f172a !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #f1f5f9 !important;
            border-right: 1px solid #e2e8f0 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #0f172a !important;
        }

        section[data-testid="stSidebar"] .stSelectbox > div > div {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #0f172a !important;
        }

        /* Topbar & Header */
        .topbar {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }

        .brand-name {
            color: #0f172a !important;
        }

        .brand-tag {
            color: #4338ca !important;
            background: #e0e7ff !important;
            border: 1px solid #a5b4fc !important;
        }

        .topbar-meta, .topbar-meta-item span {
            color: #475569 !important;
        }

        .section-header-text {
            color: #334155 !important;
        }

        .section-divider {
            background: #e2e8f0 !important;
        }

        /* Input Controls */
        .stTextArea textarea {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }

        .stTextArea textarea::placeholder {
            color: #64748b !important;
        }

        .stSelectbox > div > div,
        .stSelectbox [data-baseweb="select"] {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
        }

        .stSelectbox [data-baseweb="select"] * {
            color: #0f172a !important;
        }

        div[data-baseweb="popover"] * {
            background-color: #ffffff !important;
            color: #0f172a !important;
        }

        .stNumberInput input {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }

        /* Radio Buttons */
        .stRadio label, .stRadio label span, .stRadio p {
            color: #0f172a !important;
        }

        .stRadio > div > label {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #0f172a !important;
        }

        .stRadio > div > label:has(input:checked) {
            background-color: #e0e7ff !important;
            border-color: #6366f1 !important;
            color: #3730a3 !important;
        }

        /* Cards & KPIs */
        .kpi-card, .feat-card {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 10px 25px -5px rgba(0,0,0,0.03) !important;
        }

        .kpi-value, .feat-title {
            color: #0f172a !important;
        }

        .kpi-label, .kpi-sub, .feat-desc {
            color: #475569 !important;
        }

        /* Dataframe Table */
        div[data-testid="stDataFrame"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
        }

        div[data-testid="stDataFrame"] * {
            color: #0f172a !important;
            background-color: #ffffff !important;
        }

        /* Skill Tags & Badges */
        .tag-match { background-color: #f0fdf4 !important; border: 1px solid #bbf7d0 !important; color: #166534 !important; }
        .tag-miss  { background-color: #fef2f2 !important; border: 1px solid #fecaca !important; color: #991b1b !important; }
        .tag-extra { background-color: #eef2ff !important; border: 1px solid #c7d2fe !important; color: #3730a3 !important; }
        .tag-jd    { background-color: #f5f3ff !important; border: 1px solid #ddd6fe !important; color: #5b21b6 !important; }

        .badge-high { background-color: #dcfce7 !important; border: 1px solid #86efac !important; color: #15803d !important; }
        .badge-mid  { background-color: #fef3c7 !important; border: 1px solid #fde047 !important; color: #b45309 !important; }
        .badge-low  { background-color: #fee2e2 !important; border: 1px solid #fca5a5 !important; color: #b91c1c !important; }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #0f172a !important;
        }

        .streamlit-expanderHeader * {
            color: #0f172a !important;
        }

        .score-bar-track {
            background-color: #e2e8f0 !important;
        }
        </style>
        """, unsafe_allow_html=True)'''

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace old light mode block
pattern = re.compile(
    r'if app_theme == "☀️ Light Mode":.*?unsafe_allow_html=True\)',
    re.DOTALL
)

content = pattern.sub(light_css_block, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated Light Mode CSS in app.py')
