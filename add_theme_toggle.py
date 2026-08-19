"""
add_theme_toggle.py — Adds an explicit 1-click Theme Mode selector to sidebar in app.py
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '    st.markdown(\'<div style="height:1px;background:rgba(255,255,255,0.06);margin-bottom:1.2rem;"></div>\', unsafe_allow_html=True)'

theme_code = '''    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin-bottom:1.2rem;"></div>', unsafe_allow_html=True)

    # ── Explicit Theme Switcher ──
    app_theme = st.selectbox(
        "Theme",
        options=["🌙 Dark Mode", "☀️ Light Mode"],
        key="app_theme_mode",
    )

    if app_theme == "☀️ Light Mode":
        st.markdown("""
        <style>
        :root, body, .stApp, section[data-testid="stSidebar"] {
            --bg-base: #f8fafc !important;
            --bg-surface: #ffffff !important;
            --bg-elevated: #f1f5f9 !important;
            --border-subtle: #e2e8f0 !important;
            --border-default: #cbd5e1 !important;
            --border-accent: #818cf8 !important;
            --text-primary: #0f172a !important;
            --text-secondary: #334155 !important;
            --text-muted: #64748b !important;
            --badge-high-bg: #dcfce7 !important;
            --badge-high-border: #86efac !important;
            --badge-high-text: #15803d !important;
            --badge-mid-bg: #fef3c7 !important;
            --badge-mid-border: #fde047 !important;
            --badge-mid-text: #b45309 !important;
            --badge-low-bg: #fee2e2 !important;
            --badge-low-border: #fca5a5 !important;
            --badge-low-text: #b91c1c !important;
            --tag-match-bg: #f0fdf4 !important;
            --tag-match-border: #bbf7d0 !important;
            --tag-match-text: #166534 !important;
            --tag-miss-bg: #fef2f2 !important;
            --tag-miss-border: #fecaca !important;
            --tag-miss-text: #991b1b !important;
            --tag-extra-bg: #eef2ff !important;
            --tag-extra-border: #a5b4fc !important;
            --tag-extra-text: #3730a3 !important;
            --tag-jd-bg: #f5f3ff !important;
            --tag-jd-border: #ddd6fe !important;
            --tag-jd-text: #5b21b6 !important;
            --input-bg: #ffffff !important;
            --shadow-card: 0 1px 3px rgba(0,0,0,0.05), 0 10px 25px -5px rgba(0,0,0,0.03) !important;
            --sidebar-bg: #f1f5f9 !important;
            --dot-color: rgba(100,116,139,0.12) !important;
        }
        </style>
        """, unsafe_allow_html=True)'''

if target in content:
    content = content.replace(target, theme_code, 1)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Theme switcher added successfully")
else:
    print("Target string not found")
