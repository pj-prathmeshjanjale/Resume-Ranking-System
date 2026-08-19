"""
update_app_css.py — Rewrites CSS in app.py for enterprise-grade Light & Dark mode support.
"""

new_css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ════════════════════════════════════════
   THEME VARIABLES (DARK DEFAULT)
   ════════════════════════════════════════ */
:root {
    --bg-base:          #07090f;
    --bg-surface:       #0d1117;
    --bg-elevated:      #161b22;
    --bg-overlay:       rgba(255,255,255,0.03);

    --border-subtle:    rgba(255,255,255,0.08);
    --border-default:   rgba(255,255,255,0.14);
    --border-accent:    rgba(124,58,237,0.5);

    --text-primary:     #f8fafc;
    --text-secondary:   #cbd5e1;
    --text-muted:       #64748b;
    --text-faint:       #334155;

    --brand-primary:    #6366f1;
    --brand-secondary:  #8b5cf6;

    --badge-high-bg:    rgba(16,185,129,0.14);
    --badge-high-border:rgba(16,185,129,0.35);
    --badge-high-text:  #34d399;

    --badge-mid-bg:     rgba(245,158,11,0.14);
    --badge-mid-border: rgba(245,158,11,0.35);
    --badge-mid-text:   #fbbf24;

    --badge-low-bg:     rgba(239,68,68,0.12);
    --badge-low-border: rgba(239,68,68,0.30);
    --badge-low-text:   #f87171;

    --tag-match-bg:     rgba(16,185,129,0.12);
    --tag-match-border: rgba(16,185,129,0.28);
    --tag-match-text:   #6ee7b7;

    --tag-miss-bg:      rgba(239,68,68,0.10);
    --tag-miss-border:  rgba(239,68,68,0.24);
    --tag-miss-text:    #fca5a5;

    --tag-extra-bg:     rgba(99,102,241,0.12);
    --tag-extra-border: rgba(99,102,241,0.28);
    --tag-extra-text:   #a5b4fc;

    --tag-jd-bg:        rgba(139,92,246,0.14);
    --tag-jd-border:    rgba(139,92,246,0.32);
    --tag-jd-text:      #c4b5fd;

    --input-bg:         rgba(13,17,23,0.9);
    --shadow-card:      0 4px 16px rgba(0,0,0,0.4);
    --sidebar-bg:       #05070e;
    --dot-color:        rgba(148,163,184,0.07);
}

/* ════════════════════════════════════════
   LIGHT MODE OVERRIDES
   ════════════════════════════════════════ */
@media (prefers-color-scheme: light) {
    :root {
        --bg-base:          #f8fafc;
        --bg-surface:       #ffffff;
        --bg-elevated:      #f1f5f9;
        --bg-overlay:       rgba(0,0,0,0.02);

        --border-subtle:    #e2e8f0;
        --border-default:   #cbd5e1;
        --border-accent:    #818cf8;

        --text-primary:     #0f172a;
        --text-secondary:   #334155;
        --text-muted:       #64748b;
        --text-faint:       #94a3b8;

        --brand-primary:    #4f46e5;
        --brand-secondary:  #7c3aed;

        --badge-high-bg:    #dcfce7;
        --badge-high-border:#86efac;
        --badge-high-text:  #15803d;

        --badge-mid-bg:     #fef3c7;
        --badge-mid-border:#fde047;
        --badge-mid-text:   #b45309;

        --badge-low-bg:     #fee2e2;
        --badge-low-border:#fca5a5;
        --badge-low-text:   #b91c1c;

        --tag-match-bg:     #f0fdf4;
        --tag-match-border:#bbf7d0;
        --tag-match-text:   #166534;

        --tag-miss-bg:      #fef2f2;
        --tag-miss-border:  #fecaca;
        --tag-miss-text:    #991b1b;

        --tag-extra-bg:     #eef2ff;
        --tag-extra-border: #c7d2fe;
        --tag-extra-text:   #3730a3;

        --tag-jd-bg:        #f5f3ff;
        --tag-jd-border:    #ddd6fe;
        --tag-jd-text:      #5b21b6;

        --input-bg:         #ffffff;
        --shadow-card:      0 1px 3px rgba(0,0,0,0.05), 0 10px 25px -5px rgba(0,0,0,0.03);
        --sidebar-bg:       #f1f5f9;
        --dot-color:        rgba(100,116,139,0.12);
    }
}

[data-theme="light"] {
    --bg-base:          #f8fafc !important;
    --bg-surface:       #ffffff !important;
    --bg-elevated:      #f1f5f9 !important;
    --bg-overlay:       rgba(0,0,0,0.02) !important;

    --border-subtle:    #e2e8f0 !important;
    --border-default:   #cbd5e1 !important;
    --border-accent:    #818cf8 !important;

    --text-primary:     #0f172a !important;
    --text-secondary:   #334155 !important;
    --text-muted:       #64748b !important;

    --badge-high-bg:    #dcfce7 !important;
    --badge-high-border:#86efac !important;
    --badge-high-text:  #15803d !important;

    --badge-mid-bg:     #fef3c7 !important;
    --badge-mid-border:#fde047 !important;
    --badge-mid-text:   #b45309 !important;

    --badge-low-bg:     #fee2e2 !important;
    --badge-low-border:#fca5a5 !important;
    --badge-low-text:   #b91c1c !important;

    --tag-match-bg:     #f0fdf4 !important;
    --tag-match-border:#bbf7d0 !important;
    --tag-match-text:   #166534 !important;

    --tag-miss-bg:      #fef2f2 !important;
    --tag-miss-border:  #fecaca !important;
    --tag-miss-text:    #991b1b !important;

    --tag-extra-bg:     #eef2ff !important;
    --tag-extra-border: #c7d2fe !important;
    --tag-extra-text:   #3730a3 !important;

    --tag-jd-bg:        #f5f3ff !important;
    --tag-jd-border:    #ddd6fe !important;
    --tag-jd-text:      #5b21b6 !important;

    --input-bg:         #ffffff !important;
    --shadow-card:      0 1px 3px rgba(0,0,0,0.05), 0 10px 25px -5px rgba(0,0,0,0.03) !important;
    --sidebar-bg:       #f1f5f9 !important;
    --dot-color:        rgba(100,116,139,0.12) !important;
}

/* ════════════════════════════════════════
   APP CONTAINER
   ════════════════════════════════════════ */
.stApp {
    background-color: var(--bg-base);
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, var(--dot-color) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
    z-index: 0;
}

.main .block-container {
    padding: 1.5rem 1.5rem 4rem !important;
    max-width: 1320px !important;
    position: relative;
    z-index: 1;
}

/* Topbar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 1.4rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    margin-bottom: 1.8rem;
    box-shadow: var(--shadow-card);
}

.brand-name {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
}

.brand-tag {
    font-size: 0.62rem;
    font-weight: 700;
    color: var(--brand-primary);
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.topbar-meta {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    font-size: 0.75rem;
    color: var(--text-muted);
}

.section-header-text {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.section-divider {
    flex: 1;
    height: 1px;
    background: var(--border-subtle);
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.6rem;
}

.kpi-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.1rem 1.1rem 0.9rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-card);
    transition: border-color 0.2s ease;
}

.kpi-card:hover {
    border-color: var(--border-hover);
}

.kpi-card:nth-child(1)::before { background: linear-gradient(90deg,#6366f1,#8b5cf6); }
.kpi-card:nth-child(2)::before { background: linear-gradient(90deg,#8b5cf6,#ec4899); }
.kpi-card:nth-child(3)::before { background: linear-gradient(90deg,#10b981,#6366f1); }
.kpi-card:nth-child(4)::before { background: linear-gradient(90deg,#f59e0b,#ec4899); }

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2.5px;
}

.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    gap: 5px;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 900;
    color: var(--text-primary);
    letter-spacing: -0.04em;
    line-height: 1;
}

.kpi-sub {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
}

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}

.badge-high { background: var(--badge-high-bg); border: 1px solid var(--badge-high-border); color: var(--badge-high-text); }
.badge-mid  { background: var(--badge-mid-bg);  border: 1px solid var(--badge-mid-border);  color: var(--badge-mid-text); }
.badge-low  { background: var(--badge-low-bg);  border: 1px solid var(--badge-low-border);  color: var(--badge-low-text); }

/* Tags */
.tag {
    display: inline-flex;
    align-items: center;
    padding: 2px 9px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 500;
    margin: 2px;
    font-family: 'JetBrains Mono', monospace;
}

.tag-match { background: var(--tag-match-bg); border: 1px solid var(--tag-match-border); color: var(--tag-match-text); }
.tag-miss  { background: var(--tag-miss-bg);  border: 1px solid var(--tag-miss-border);  color: var(--tag-miss-text); }
.tag-extra { background: var(--tag-extra-bg); border: 1px solid var(--tag-extra-border); color: var(--tag-extra-text); }
.tag-jd    { background: var(--tag-jd-bg);    border: 1px solid var(--tag-jd-border);    color: var(--tag-jd-text); }

/* Score bar */
.score-bar-track {
    height: 5px;
    background: var(--border-subtle);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 6px;
}

.score-bar-fill {
    height: 100%;
    border-radius: 3px;
}

/* Feature card */
.feat-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 1.6rem 1.4rem;
    height: 100%;
    box-shadow: var(--shadow-card);
    transition: all 0.25s ease;
}

.feat-card:hover {
    border-color: var(--border-hover);
    transform: translateY(-2px);
}

.feat-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.feat-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.7;
}

/* Streamlit Overrides */
.stTextArea textarea {
    background: var(--input-bg) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 0.86rem !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.7 !important;
}

.stTextArea textarea:focus {
    border-color: var(--border-accent) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

.stSelectbox > div > div {
    background: var(--input-bg) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 0.86rem !important;
}

.stNumberInput input {
    background: var(--input-bg) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

div[data-testid="stDataFrame"] {
    background: var(--bg-surface) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border-subtle) !important;
}

.streamlit-expanderHeader {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 0.84rem !important;
}

.stButton > button {
    background: var(--brand-gradient) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1.6rem !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.35) !important;
}

.stDownloadButton > button {
    background: var(--tag-match-bg) !important;
    color: var(--tag-match-text) !important;
    border: 1px solid var(--tag-match-border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

/* ════════════════════════════════════════
   MOBILE RESPONSIVENESS
   ════════════════════════════════════════ */
html, body, .stApp {
    overflow-x: hidden !important;
    max-width: 100vw !important;
}

div[data-testid="stDataFrame"] {
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
}

.streamlit-expanderHeader {
    white-space: normal !important;
    word-break: break-word !important;
    overflow-wrap: anywhere !important;
    line-height: 1.4 !important;
}

.streamlit-expanderHeader p {
    white-space: normal !important;
    word-break: break-word !important;
    overflow-wrap: anywhere !important;
}

@media (max-width: 768px) {
    .main .block-container {
        padding: 0.75rem 0.5rem 2.5rem !important;
        max-width: 100% !important;
    }

    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 1rem !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
    }

    .kpi-card {
        padding: 0.75rem 0.65rem !important;
    }

    .kpi-value {
        font-size: 1.4rem !important;
    }

    .kpi-label {
        font-size: 0.62rem !important;
    }

    .kpi-sub {
        display: none !important;
    }

    .topbar {
        padding: 0.65rem 0.85rem !important;
        margin-bottom: 1rem !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 0.5rem !important;
    }

    .topbar-meta {
        display: none !important;
    }

    .brand-name {
        font-size: 0.95rem !important;
    }

    .tag {
        font-size: 0.65rem !important;
        padding: 2px 6px !important;
        margin: 1px !important;
    }

    .feat-card {
        padding: 1.1rem 0.9rem !important;
    }

    .feat-title {
        font-size: 0.88rem !important;
    }

    .feat-desc {
        font-size: 0.78rem !important;
    }

    .stRadio > div {
        flex-direction: column !important;
    }

    .stRadio > div > label {
        width: 100% !important;
        text-align: center !important;
    }
}

@media (max-width: 480px) {
    .kpi-grid {
        grid-template-columns: 1fr 1fr !important;
        gap: 6px !important;
    }

    .kpi-value {
        font-size: 1.25rem !important;
    }

    .section-header-text {
        font-size: 0.68rem !important;
    }

    .section-divider {
        display: none !important;
    }
}
</style>"""

import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace <style> ... </style> block
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
content = style_pattern.sub(new_css, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated app.py with dual Light & Dark theme CSS system')
