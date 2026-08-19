"""
lock_dark_mode.py — Enforces strict 100% Dark Mode across all components in app.py.
"""
import re

dark_css = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ════════════════════════════════════════
   100% DARK THEME SYSTEM (UNCONDITIONAL)
   ════════════════════════════════════════ */
:root, [data-theme="light"], [data-theme="dark"] {
    color-scheme: dark !important;

    --bg-base:          #07090f !important;
    --bg-surface:       #0d1117 !important;
    --bg-elevated:      #161b22 !important;

    --border-subtle:    rgba(255,255,255,0.08) !important;
    --border-default:   rgba(255,255,255,0.14) !important;
    --border-accent:    rgba(124,58,237,0.5) !important;

    --text-primary:     #f8fafc !important;
    --text-secondary:   #cbd5e1 !important;
    --text-muted:       #64748b !important;

    --badge-high-bg:    rgba(16,185,129,0.14) !important;
    --badge-high-border:rgba(16,185,129,0.35) !important;
    --badge-high-text:  #34d399 !important;

    --badge-mid-bg:     rgba(245,158,11,0.14) !important;
    --badge-mid-border: rgba(245,158,11,0.35) !important;
    --badge-mid-text:   #fbbf24 !important;

    --badge-low-bg:     rgba(239,68,68,0.12) !important;
    --badge-low-border: rgba(239,68,68,0.30) !important;
    --badge-low-text:   #f87171 !important;

    --tag-match-bg:     rgba(16,185,129,0.12) !important;
    --tag-match-border: rgba(16,185,129,0.28) !important;
    --tag-match-text:   #6ee7b7 !important;

    --tag-miss-bg:      rgba(239,68,68,0.10) !important;
    --tag-miss-border:  rgba(239,68,68,0.24) !important;
    --tag-miss-text:    #fca5a5 !important;

    --tag-extra-bg:     rgba(99,102,241,0.12) !important;
    --tag-extra-border: rgba(99,102,241,0.28) !important;
    --tag-extra-text:   #a5b4fc !important;

    --tag-jd-bg:        rgba(139,92,246,0.14) !important;
    --tag-jd-border:    rgba(139,92,246,0.32) !important;
    --tag-jd-text:      #c4b5fd !important;
}

/* Base App Background */
.stApp, body {
    background-color: #07090f !important;
    color: #f8fafc !important;
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, rgba(148,163,184,0.07) 1px, transparent 1px);
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

/* Sidebar Dark Locking */
section[data-testid="stSidebar"] {
    background-color: #05070e !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc;
}

/* Topbar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 1.4rem;
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px;
    margin-bottom: 1.8rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

.brand-name {
    font-size: 1.05rem;
    font-weight: 800;
    color: #f8fafc !important;
    letter-spacing: -0.03em;
}

.brand-tag {
    font-size: 0.62rem;
    font-weight: 700;
    color: #818cf8 !important;
    background: rgba(99,102,241,0.12) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
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
    color: #64748b !important;
}

.topbar-meta-item span {
    color: #94a3b8 !important;
}

.section-header-text {
    font-size: 0.72rem;
    font-weight: 700;
    color: #cbd5e1 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.section-divider {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08) !important;
}

/* KPI & Feature Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.6rem;
}

.kpi-card {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px;
    padding: 1.1rem 1.1rem 0.9rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
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
    color: #64748b !important;
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
    color: #f8fafc !important;
    letter-spacing: -0.04em;
    line-height: 1;
}

.kpi-sub {
    font-size: 0.7rem;
    color: #475569 !important;
    margin-top: 0.3rem;
}

/* Badges & Tags */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
}

.badge-high { background: rgba(16,185,129,0.14) !important; border: 1px solid rgba(16,185,129,0.35) !important; color: #34d399 !important; }
.badge-mid  { background: rgba(245,158,11,0.14) !important; border: 1px solid rgba(245,158,11,0.35) !important; color: #fbbf24 !important; }
.badge-low  { background: rgba(239,68,68,0.12) !important; border: 1px solid rgba(239,68,68,0.30) !important; color: #f87171 !important; }

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

.tag-match { background: rgba(16,185,129,0.12) !important; border: 1px solid rgba(16,185,129,0.28) !important; color: #6ee7b7 !important; }
.tag-miss  { background: rgba(239,68,68,0.10) !important; border: 1px solid rgba(239,68,68,0.24) !important; color: #fca5a5 !important; }
.tag-extra { background: rgba(99,102,241,0.12) !important; border: 1px solid rgba(99,102,241,0.28) !important; color: #a5b4fc !important; }
.tag-jd    { background: rgba(139,92,246,0.14) !important; border: 1px solid rgba(139,92,246,0.32) !important; color: #c4b5fd !important; }

.score-bar-track {
    height: 5px;
    background: rgba(255,255,255,0.06) !important;
    border-radius: 3px;
    overflow: hidden;
    margin-top: 6px;
}

.score-bar-fill {
    height: 100%;
    border-radius: 3px;
}

.feat-card {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 18px;
    padding: 1.6rem 1.4rem;
    height: 100%;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

.feat-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc !important;
    margin-bottom: 0.5rem;
}

.feat-desc {
    font-size: 0.82rem;
    color: #64748b !important;
    line-height: 1.7;
}

/* Streamlit Component Overrides */
.stTextArea textarea {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    font-size: 0.86rem !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.7 !important;
}

.stTextArea textarea::placeholder {
    color: #64748b !important;
}

.stSelectbox > div > div {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    font-size: 0.86rem !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #f8fafc !important;
    fill: #f8fafc !important;
}

div[data-baseweb="popover"] * {
    background: #0d1117 !important;
    color: #f8fafc !important;
}

.stNumberInput input {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
}

.stRadio label, .stRadio label span, .stRadio p {
    color: #cbd5e1 !important;
}

.stRadio > div > label {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #cbd5e1 !important;
}

.stRadio > div > label:has(input:checked) {
    background: rgba(99,102,241,0.18) !important;
    border-color: rgba(99,102,241,0.45) !important;
    color: #c7d2fe !important;
}

div[data-testid="stDataFrame"] {
    background: #0d1117 !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

div[data-testid="stDataFrame"] * {
    color: #f8fafc !important;
}

.streamlit-expanderHeader {
    background: #0d1117 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
}

.streamlit-expanderHeader * {
    color: #f8fafc !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1.6rem !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.35) !important;
}

.stDownloadButton > button {
    background: rgba(16,185,129,0.14) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16,185,129,0.35) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

/* Mobile Responsiveness */
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

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace <style> ... </style> block completely
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
content = style_pattern.sub(dark_css, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Enforced strict 100% Dark Mode in app.py")
