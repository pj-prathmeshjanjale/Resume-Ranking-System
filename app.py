"""
app.py — Resume Rank Pro: AI-Based Resume Ranking System
==========================================================
Streamlit application entry point.
Wires the text extraction, NLP preprocessing, skill matching, and TF-IDF
ranking pipeline into an interactive, visually polished recruiter dashboard.

Run with:
    streamlit run app.py
"""

import io
import logging
import sys
import os

import pandas as pd
import streamlit as st

# ── Add project root to path so 'src' package is importable ──────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Project modules ────────────────────────────────────────────────────────────
from src.extractor    import extract_text
from src.preprocessor import preprocess, preprocess_batch, get_nlp
from src.skills       import extract_skills, compute_skill_match
from src.ranker       import compute_composite_scores, results_to_dataframe
from src.sample_data  import SAMPLE_JOB_DESCRIPTIONS, load_sample_resumes, get_dataset_categories

# ── Logging configuration ─────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG & CUSTOM CSS
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="RecruitIQ — AI Resume Screener",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>R</text></svg>",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SVG Icon Helpers ──────────────────────────────────────────────────────────
def svg_icon(path_d, size=16, color="currentColor", viewBox="0 0 24 24"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}"
        viewBox="{viewBox}" fill="none" stroke="{color}" stroke-width="1.8"
        stroke-linecap="round" stroke-linejoin="round"
        style="vertical-align:-3px; display:inline-block; flex-shrink:0;">
        {path_d}
    </svg>"""

ICONS = {
    "logo_mark": """<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>""",
    "spark":     """<path d="M13 10V3L4 14h7v7l9-11h-7z"/>""",
    "brain":     """<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>""",
    "chart":     """<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>""",
    "upload":    """<path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>""",
    "database":  """<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>""",
    "check":     """<polyline points="20 6 9 17 4 12"/>""",
    "x_mark":   """<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>""",
    "plus":      """<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>""",
    "settings":  """<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>""",
    "download":  """<path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>""",
    "search":    """<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>""",
    "user":      """<path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>""",
    "info":      """<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>""",
    "briefcase": """<rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>""",
    "zap":       """<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>""",
    "award":     """<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/>""",
    "filter":    """<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>""",
    "layers":    """<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>""",
    "key":       """<path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 11-7.778 7.778 5.5 5.5 0 017.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>""",
}

# ── Professional CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: #080c14;
    min-height: 100vh;
}

/* Subtle grid background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1280px;
    position: relative;
    z-index: 1;
}

/* ── Topbar / Nav ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.5rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    margin-bottom: 1.8rem;
    backdrop-filter: blur(20px);
}

.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(99,102,241,0.4);
}

.brand-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}

.brand-tag {
    font-size: 0.65rem;
    font-weight: 600;
    color: #6366f1;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.topbar-meta {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    font-size: 0.78rem;
    color: #64748b;
}

.topbar-meta-item {
    display: flex;
    align-items: center;
    gap: 5px;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.75rem;
}

.section-header-text {
    font-size: 0.78rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.section-divider {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ── Input Panels ── */
.input-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.25rem;
    height: 100%;
    transition: border-color 0.2s ease;
}

.input-panel:hover {
    border-color: rgba(99,102,241,0.25);
}

.panel-label {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #cbd5e1;
    margin-bottom: 0.75rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}

.kpi-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.1rem 1rem;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    opacity: 0.7;
}

.kpi-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 5px;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
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
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* ════════════════════════════════════════
   SCORE BADGES
   ════════════════════════════════════════ */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: var(--radius-sm);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    font-variant-numeric: tabular-nums;
}

.badge-high {
    background: rgba(16,185,129,0.14);
    border: 1px solid rgba(16,185,129,0.35);
    color: var(--green-400);
}

.badge-mid {
    background: rgba(245,158,11,0.13);
    border: 1px solid rgba(245,158,11,0.35);
    color: var(--amber-400);
}

.badge-low {
    background: rgba(239,68,68,0.11);
    border: 1px solid rgba(239,68,68,0.28);
    color: var(--red-400);
}

/* ════════════════════════════════════════
   SKILL TAGS
   ════════════════════════════════════════ */
.tag {
    display: inline-flex;
    align-items: center;
    padding: 2px 9px;
    border-radius: var(--radius-sm);
    font-size: 0.72rem;
    font-weight: 500;
    margin: 2px;
    font-family: var(--font-mono);
    letter-spacing: 0.01em;
    transition: filter 0.15s ease;
}

.tag:hover { filter: brightness(1.15); }

.tag-match {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.28);
    color: #6ee7b7;
}

.tag-miss {
    background: rgba(239,68,68,0.09);
    border: 1px solid rgba(239,68,68,0.22);
    color: #fca5a5;
}

.tag-extra {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.28);
    color: #a5b4fc;
}

.tag-jd {
    background: rgba(139,92,246,0.13);
    border: 1px solid rgba(139,92,246,0.32);
    color: #c4b5fd;
}

/* ════════════════════════════════════════
   RANK INDICATORS
   ════════════════════════════════════════ */
.rank-indicator {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: var(--radius-sm);
    font-size: 0.76rem;
    font-weight: 800;
    flex-shrink: 0;
    font-variant-numeric: tabular-nums;
}

.rank-1 { background: rgba(251,191,36,0.18); border: 1px solid rgba(251,191,36,0.4); color: #fbbf24; }
.rank-2 { background: rgba(148,163,184,0.14); border: 1px solid rgba(148,163,184,0.32); color: #94a3b8; }
.rank-3 { background: rgba(180,105,60,0.15); border: 1px solid rgba(180,105,60,0.32); color: #c4956a; }
.rank-n { background: rgba(255,255,255,0.04); border: 1px solid var(--border-subtle); color: var(--text-muted); }

/* ════════════════════════════════════════
   SCORE BARS
   ════════════════════════════════════════ */
.score-bar-track {
    height: 5px;
    background: rgba(255,255,255,0.06);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 6px;
}

.score-bar-fill {
    height: 100%;
    border-radius: 3px;
}

/* ════════════════════════════════════════
   FEATURE CARDS (landing)
   ════════════════════════════════════════ */
.feat-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-xl);
    padding: 1.6rem 1.4rem;
    height: 100%;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}

.feat-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg,rgba(124,58,237,0.04) 0%,transparent 60%);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.feat-card:hover {
    border-color: rgba(124,58,237,0.35);
    box-shadow: 0 0 0 1px rgba(124,58,237,0.1), var(--shadow-md);
    transform: translateY(-2px);
}

.feat-card:hover::before { opacity: 1; }

.feat-icon {
    width: 42px;
    height: 42px;
    background: rgba(124,58,237,0.14);
    border: 1px solid rgba(124,58,237,0.28);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.1rem;
}

.feat-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

.feat-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.7;
}

/* ════════════════════════════════════════
   STREAMLIT ELEMENT OVERRIDES
   ════════════════════════════════════════ */

/* Text area */
.stTextArea textarea {
    background: rgba(13,17,23,0.9) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-size: 0.86rem !important;
    font-family: var(--font-sans) !important;
    line-height: 1.7 !important;
    resize: vertical !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.stTextArea textarea:focus {
    border-color: var(--border-accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
    outline: none !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(13,17,23,0.9) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-size: 0.86rem !important;
    font-family: var(--font-sans) !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--border-accent) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
}

/* Number input */
.stNumberInput input {
    background: rgba(13,17,23,0.9) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-size: 0.86rem !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] {
    padding-top: 0.5rem !important;
}

.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--violet-500) !important;
    border-color: var(--violet-500) !important;
    box-shadow: 0 0 0 4px rgba(139,92,246,0.2) !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    background: var(--bg-surface);
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--border-subtle);
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--indigo-500), var(--violet-500)) !important;
    border-radius: 4px !important;
}

/* Primary button */
.stButton > button {
    background: linear-gradient(135deg, var(--indigo-500) 0%, var(--violet-600) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    font-family: var(--font-sans) !important;
    padding: 0.65rem 1.6rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 10px rgba(124,58,237,0.35), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #6d28d9 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(99,102,241,0.4) !important;
}

.stDownloadButton > button {
    background: rgba(16,185,129,0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

.stDownloadButton > button:hover {
    background: rgba(16,185,129,0.25) !important;
    border-color: rgba(16,185,129,0.5) !important;
}

.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    color: #cbd5e1 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(99,102,241,0.07) !important;
    border-color: rgba(99,102,241,0.2) !important;
}

.stRadio > div { gap: 0.5rem; }
.stRadio > div > label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    padding: 0.4rem 1rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    transition: all 0.15s ease !important;
}

.stRadio > div > label:has(input:checked) {
    background: rgba(99,102,241,0.15) !important;
    border-color: rgba(99,102,241,0.4) !important;
    color: #c7d2fe !important;
}

.stFileUploader > div {
    background: rgba(255,255,255,0.025) !important;
    border: 1.5px dashed rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
}

.stFileUploader > div:hover {
    border-color: rgba(99,102,241,0.4) !important;
    background: rgba(99,102,241,0.05) !important;
}

section[data-testid="stSidebar"] {
    background: #05080f !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── Misc ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.55); }

/* ── Alerts ── */
/* ── Mobile & Responsive Overrides ── */
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
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner="Loading NLP model...")
def load_nlp_model():
    """Load and cache the spaCy model (runs once per session)."""
    return get_nlp()


def score_badge(score: float) -> str:
    if score >= 60:
        cls = "badge-high"
    elif score >= 30:
        cls = "badge-mid"
    else:
        cls = "badge-low"
    return f'<span class="badge {cls}">{score:.1f}%</span>'


def score_bar(score: float) -> str:
    pct = min(score, 100)
    if pct >= 60:
        color = "linear-gradient(90deg,#10b981,#059669)"
    elif pct >= 30:
        color = "linear-gradient(90deg,#f59e0b,#d97706)"
    else:
        color = "linear-gradient(90deg,#ef4444,#dc2626)"
    return f'''<div class="score-bar-track">
        <div class="score-bar-fill" style="width:{pct}%;background:{color};"></div>
    </div>'''


def tags_html(skills: list, css_class: str) -> str:
    if not skills:
        return '<span style="color:#475569;font-size:0.78rem;font-style:italic;">None detected</span>'
    return "".join(f'<span class="tag {css_class}">{s}</span>' for s in skills)


def rank_badge(rank: int) -> str:
    cls = {1: "rank-1", 2: "rank-2", 3: "rank-3"}.get(rank, "rank-n")
    return f'<span class="rank-indicator {cls}">{rank}</span>'


def run_ranking_pipeline(job_description, candidates, tfidf_weight, skill_weight):
    """Full NLP + ranking pipeline orchestration."""
    nlp = load_nlp_model()

    with st.spinner("Preprocessing job description..."):
        jd_processed, jd_doc = preprocess(job_description)

    with st.spinner(f"Processing {len(candidates)} resume(s) through NLP pipeline..."):
        resume_texts    = [c["text"] for c in candidates]
        candidate_names = [c["name"] for c in candidates]
        preprocessed    = preprocess_batch(resume_texts)
        resumes_processed = [p[0] for p in preprocessed]
        resume_docs       = [p[1] for p in preprocessed]

    with st.spinner("Running skill extraction and matching..."):
        jd_skills = extract_skills(jd_doc, nlp)
        skill_results = []
        for doc in resume_docs:
            rs = extract_skills(doc, nlp)
            skill_results.append(compute_skill_match(jd_skills, rs))

    with st.spinner("Computing TF-IDF similarity and composite scores..."):
        results = compute_composite_scores(
            jd_processed=jd_processed,
            resumes_processed=resumes_processed,
            skill_results=skill_results,
            candidate_names=candidate_names,
            candidate_raw_texts=resume_texts,
            tfidf_weight=tfidf_weight,
            skill_weight=skill_weight,
        )

    return results, jd_skills


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Brand mark
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:0.5rem 0 1.2rem;">
        <div style="width:34px;height:34px;background:linear-gradient(135deg,#6366f1,#8b5cf6);
                    border-radius:8px;display:flex;align-items:center;justify-content:center;
                    box-shadow:0 4px 12px rgba(99,102,241,0.35);">
            {svg_icon(ICONS['layers'], size=17, color='white')}
        </div>
        <div>
            <div style="font-size:0.95rem;font-weight:700;color:#f1f5f9;letter-spacing:-0.02em;">RecruitIQ</div>
            <div style="font-size:0.65rem;color:#6366f1;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;">AI Screening</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin-bottom:1.2rem;"></div>', unsafe_allow_html=True)

    # Algorithm Weights
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:0.6rem;">
        {svg_icon(ICONS['settings'], size=14, color='#6366f1')}
        <span style="font-size:0.73rem;font-weight:600;color:#94a3b8;
                     text-transform:uppercase;letter-spacing:0.08em;">Algorithm Weights</span>
    </div>
    """, unsafe_allow_html=True)

    tfidf_weight = st.slider(
        "TF-IDF Semantic Similarity",
        min_value=0.0, max_value=1.0, value=0.70, step=0.05,
        help="Weight of TF-IDF cosine similarity in the final composite score.",
        key="tfidf_slider"
    )
    skill_weight = round(1.0 - tfidf_weight, 2)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.2);
                    border-radius:8px;padding:0.6rem;text-align:center;">
            <div style="font-size:1.3rem;font-weight:800;color:#818cf8;">{tfidf_weight:.0%}</div>
            <div style="font-size:0.65rem;color:#64748b;font-weight:500;margin-top:2px;">TF-IDF</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div style="background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.2);
                    border-radius:8px;padding:0.6rem;text-align:center;">
            <div style="font-size:1.3rem;font-weight:800;color:#a78bfa;">{skill_weight:.0%}</div>
            <div style="font-size:0.65rem;color:#64748b;font-weight:500;margin-top:2px;">Skills</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:1.2rem 0;"></div>', unsafe_allow_html=True)

    # How it works
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:0.8rem;">
        {svg_icon(ICONS['info'], size=14, color='#6366f1')}
        <span style="font-size:0.73rem;font-weight:600;color:#94a3b8;
                     text-transform:uppercase;letter-spacing:0.08em;">Methodology</span>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        (ICONS['upload'],   "Text Extraction",   "PDF · DOCX · TXT via pdfplumber"),
        (ICONS['brain'],    "NLP Pipeline",      "Tokenize → Stopwords → Lemmatize"),
        (ICONS['key'],      "Skill Matching",    "PhraseMatcher · 250+ skill taxonomy"),
        (ICONS['chart'],    "TF-IDF Ranking",    "Cosine similarity · bigram vectors"),
        (ICONS['zap'],      "Composite Score",   "w₁·TF-IDF + w₂·SkillOverlap"),
    ]

    for icon, title, desc in steps:
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:9px;margin-bottom:0.8rem;">
            <div style="width:26px;height:26px;background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.2);
                        border-radius:6px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">
                {svg_icon(icon, size=13, color='#818cf8')}
            </div>
            <div>
                <div style="font-size:0.8rem;font-weight:600;color:#cbd5e1;">{title}</div>
                <div style="font-size:0.72rem;color:#475569;margin-top:1px;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:0.8rem 0 1rem;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem;color:#334155;line-height:1.6;">
        <div style="color:#475569;font-weight:500;margin-bottom:4px;">Project Metadata</div>
        Domain: Human Resources<br>
        AI: NLP · Ranking Algorithms<br>
        Stack: Python · spaCy · Streamlit<br>
        Dataset: Resume Dataset · 26 candidates
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TOP NAV BAR
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">
        <div class="brand-icon">
            {svg_icon(ICONS['layers'], size=18, color='white')}
        </div>
        <span class="brand-name">RecruitIQ</span>
        <span class="brand-tag">Beta</span>
    </div>
    <div class="topbar-meta">
        <div class="topbar-meta-item">
            {svg_icon(ICONS['database'], size=13, color='#475569')}
            <span>26 Sample Candidates</span>
        </div>
        <div class="topbar-meta-item">
            {svg_icon(ICONS['layers'], size=13, color='#475569')}
            <span>250+ Skills Taxonomy</span>
        </div>
        <div class="topbar-meta-item">
            {svg_icon(ICONS['chart'], size=13, color='#475569')}
            <span>TF-IDF · Cosine Similarity</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown(f"""
    <div class="section-header">
        {svg_icon(ICONS['briefcase'], size=14, color='#6366f1')}
        <span class="section-header-text">Job Description</span>
        <div class="section-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    sample_jd_options = ["Select a sample role..."] + list(SAMPLE_JOB_DESCRIPTIONS.keys())
    selected_sample_jd = st.selectbox(
        "Load sample JD",
        options=sample_jd_options,
        key="sample_jd_select",
        label_visibility="collapsed",
    )

    default_jd = (
        SAMPLE_JOB_DESCRIPTIONS[selected_sample_jd].strip()
        if selected_sample_jd != "Select a sample role..."
        else ""
    )

    job_description = st.text_area(
        "Job Description",
        value=default_jd,
        height=310,
        placeholder="Paste the job description here, or select a sample role above.\n\nInclude responsibilities, required skills, and qualifications for best results.",
        key="jd_input",
        label_visibility="collapsed",
    )

    word_count = len(job_description.split()) if job_description.strip() else 0
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;margin-top:4px;">
        <span style="font-size:0.72rem;color:#334155;">{word_count} words</span>
    </div>""", unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
    <div class="section-header">
        {svg_icon(ICONS['user'], size=14, color='#6366f1')}
        <span class="section-header-text">Candidate Resumes</span>
        <div class="section-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    resume_source = st.radio(
        "Source",
        options=["Upload Files", "Sample Dataset"],
        horizontal=True,
        key="resume_source",
        label_visibility="collapsed",
    )

    uploaded_candidates = []

    if resume_source == "Upload Files":
        uploaded_files = st.file_uploader(
            "Upload resumes",
            type=["pdf", "docx", "doc", "txt"],
            accept_multiple_files=True,
            key="resume_upload",
            label_visibility="collapsed",
        )
        if uploaded_files:
            st.markdown(f"""
            <div style="font-size:0.78rem;color:#34d399;display:flex;align-items:center;
                        gap:6px;margin:6px 0;">
                {svg_icon(ICONS['check'], size=13, color='#34d399')}
                {len(uploaded_files)} file(s) ready
            </div>""", unsafe_allow_html=True)
            for f in uploaded_files:
                raw_bytes = f.read()
                text = extract_text(io.BytesIO(raw_bytes), f.name)
                name = os.path.splitext(f.name)[0].replace("_", " ").replace("-", " ").title()
                uploaded_candidates.append({
                    "name": name,
                    "text": text if text.strip() else f"[No text extracted from {f.name}]"
                })
        else:
            st.markdown(f"""
            <div style="font-size:0.8rem;color:#475569;display:flex;align-items:center;
                        gap:6px;margin:8px 0;">
                {svg_icon(ICONS['upload'], size=14, color='#475569')}
                Drag and drop PDF, DOCX, or TXT files above
            </div>""", unsafe_allow_html=True)

    else:
        categories = get_dataset_categories()
        if categories:
            col_cat, col_max = st.columns([3, 2])
            with col_cat:
                selected_cat = st.selectbox(
                    "Category",
                    options=["All Categories"] + categories,
                    key="dataset_category",
                )
            with col_max:
                max_n = st.number_input(
                    "Max candidates",
                    min_value=3, max_value=26, value=15, step=1,
                    key="max_n",
                )

            cat_filter = None if selected_cat == "All Categories" else selected_cat
            df_resumes = load_sample_resumes(category_filter=cat_filter, max_per_category=int(max_n))

            if not df_resumes.empty:
                st.markdown(f"""
                <div style="font-size:0.78rem;color:#34d399;display:flex;align-items:center;
                            gap:6px;margin-bottom:6px;">
                    {svg_icon(ICONS['check'], size=13, color='#34d399')}
                    {len(df_resumes)} candidates loaded
                </div>""", unsafe_allow_html=True)

                st.dataframe(
                    df_resumes[["name", "category"]].rename(columns={"name":"Candidate","category":"Category"}),
                    hide_index=True,
                    use_container_width=True,
                    height=230,
                )
                for _, row in df_resumes.iterrows():
                    uploaded_candidates.append({
                        "name": f"{row['name']}",
                        "text": str(row["resume_text"]),
                    })
            else:
                st.warning("No resumes found for the selected category.")
        else:
            st.error("Dataset not found. Please check data/sample_resumes.csv")


# ══════════════════════════════════════════════════════════════════════════════
# RUN BUTTON
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    rank_button = st.button(
        "Run Screening",
        use_container_width=True,
        key="rank_btn",
        type="primary",
    )


# ══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════════════════════

if rank_button:
    errors = []
    if not job_description.strip():
        errors.append("Job description is required.")
    if not uploaded_candidates:
        errors.append("Please upload resumes or load the sample dataset.")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:1.2rem 0;"></div>', unsafe_allow_html=True)

    # Run pipeline
    try:
        results, jd_skills = run_ranking_pipeline(
            job_description=job_description,
            candidates=uploaded_candidates,
            tfidf_weight=tfidf_weight,
            skill_weight=skill_weight,
        )
    except Exception as e:
        st.error(f"Pipeline error: {str(e)}")
        logger.exception("Pipeline failed")
        st.stop()

    # ── KPI Strip ─────────────────────────────────────────────────────────────
    top_score  = results[0].final_score_pct if results else 0
    avg_score  = sum(r.final_score_pct for r in results) / max(len(results), 1)
    qualified  = sum(1 for r in results if r.final_score_pct >= 50)

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">
                {svg_icon(ICONS['user'], size=12, color='#6366f1')} Candidates
            </div>
            <div class="kpi-value">{len(results)}</div>
            <div class="kpi-sub">screened against JD</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">
                {svg_icon(ICONS['award'], size=12, color='#6366f1')} Top Score
            </div>
            <div class="kpi-value">{top_score:.0f}%</div>
            <div class="kpi-sub">{results[0].name.split('(')[0].strip() if results else '-'}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">
                {svg_icon(ICONS['chart'], size=12, color='#6366f1')} Avg Score
            </div>
            <div class="kpi-value">{avg_score:.0f}%</div>
            <div class="kpi-sub">across all candidates</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">
                {svg_icon(ICONS['filter'], size=12, color='#6366f1')} JD Skills
            </div>
            <div class="kpi-value">{len(jd_skills)}</div>
            <div class="kpi-sub">requirements extracted</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # JD Skills panel
    if jd_skills:
        with st.expander(f"Extracted JD Requirements  —  {len(jd_skills)} skills identified", expanded=False):
            st.markdown(tags_html(sorted(jd_skills), "tag-jd"), unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:1rem 0 1.4rem;"></div>', unsafe_allow_html=True)

    # ── Results Split: Table + Chart ──────────────────────────────────────────
    res_col, chart_col = st.columns([1.1, 0.9], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="section-header" style="margin-bottom:1rem;">
            {svg_icon(ICONS['award'], size=14, color='#6366f1')}
            <span class="section-header-text">Candidate Rankings</span>
            <div class="section-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        results_df = results_to_dataframe(results)
        st.dataframe(
            results_df.style.background_gradient(
                subset=["Match Score (%)"], cmap="RdYlGn", vmin=0, vmax=100
            ).format({
                "Match Score (%)": "{:.1f}",
                "TF-IDF Score":    "{:.1f}",
                "Skill Score (%)": "{:.1f}",
            }),
            use_container_width=True,
            hide_index=True,
            height=min(40 + len(results) * 38, 480),
        )

        csv_buf = io.StringIO()
        results_df.to_csv(csv_buf, index=False)
        st.download_button(
            label="Download CSV Report",
            data=csv_buf.getvalue().encode("utf-8"),
            file_name="recruitiq_ranking_results.csv",
            mime="text/csv",
            key="download_csv",
        )

    with chart_col:
        st.markdown(f"""
        <div class="section-header" style="margin-bottom:1rem;">
            {svg_icon(ICONS['chart'], size=14, color='#6366f1')}
            <span class="section-header-text">Score Visualization</span>
            <div class="section-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import numpy as np

        chart_data = results[:12]
        names  = [r.name.split("(")[0].strip()[:22] for r in chart_data]
        scores = [r.final_score_pct for r in chart_data]

        fig, ax = plt.subplots(figsize=(7, max(4.5, len(names) * 0.48 + 1.2)))
        fig.patch.set_facecolor("#080c14")
        ax.set_facecolor("#0c1120")

        y = np.arange(len(names))
        h = 0.6

        colours = ["#10b981" if s >= 60 else "#f59e0b" if s >= 30 else "#ef4444" for s in scores]
        bars = ax.barh(y, scores, h, color=colours, alpha=0.85, zorder=3,
                       linewidth=0, edgecolor="none")

        # Score labels
        for bar, score in zip(bars, scores):
            w = bar.get_width()
            ax.text(
                max(w - 1.5, 0.5), bar.get_y() + bar.get_height() / 2,
                f"{score:.1f}%",
                va="center", ha="right" if w > 8 else "left",
                fontsize=8.5, fontweight="600",
                color="white" if w > 8 else "#94a3b8",
                fontfamily="DejaVu Sans", zorder=5,
            )

        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=8.5, color="#94a3b8", fontfamily="DejaVu Sans")
        ax.set_xlabel("Match Score (%)", color="#475569", fontsize=8.5)
        ax.set_title("Match Score Distribution", color="#cbd5e1", fontsize=10,
                     fontweight="600", pad=10, fontfamily="DejaVu Sans")
        ax.set_xlim(0, 107)
        ax.tick_params(colors="#475569", labelsize=8)

        for spine in ax.spines.values():
            spine.set_edgecolor("#1e293b")

        ax.xaxis.grid(True, color="#1a2540", linestyle="--", alpha=0.8, zorder=0)
        ax.set_axisbelow(True)

        patches = [
            mpatches.Patch(color="#10b981", label="Strong  ≥60%", alpha=0.85),
            mpatches.Patch(color="#f59e0b", label="Moderate 30–60%", alpha=0.85),
            mpatches.Patch(color="#ef4444", label="Weak  <30%", alpha=0.85),
        ]
        ax.legend(handles=patches, loc="lower right", framealpha=0.15,
                  facecolor="#0c1120", edgecolor="#1e293b",
                  labelcolor="#94a3b8", fontsize=7.5)

        plt.tight_layout(pad=1.2)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:1.4rem 0;"></div>', unsafe_allow_html=True)

    # ── Candidate Breakdown ───────────────────────────────────────────────────
    st.markdown(f"""
    <div class="section-header" style="margin-bottom:1rem;">
        {svg_icon(ICONS['search'], size=14, color='#6366f1')}
        <span class="section-header-text">Candidate Skill Analysis</span>
        <div class="section-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    for rank, r in enumerate(results, start=1):
        score_html = score_badge(r.final_score_pct)
        label = (
            f"#{rank}  {r.name}  ·  "
            f"{r.final_score_pct:.1f}% Match  "
            f"({len(r.matched_skills)} matched, {len(r.missing_skills)} missing)"
        )

        with st.expander(label, expanded=(rank <= 3)):
            # Score bars row
            b1, b2, b3 = st.columns(3)
            with b1:
                st.markdown(f"""
                <div style="margin-bottom:0.3rem;">
                    <div style="font-size:0.72rem;color:#64748b;font-weight:500;
                                text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">
                        Final Score
                    </div>
                    <div style="font-size:1.4rem;font-weight:800;color:#f1f5f9;
                                letter-spacing:-0.03em;">{r.final_score_pct:.1f}%</div>
                    {score_bar(r.final_score_pct)}
                </div>""", unsafe_allow_html=True)
            with b2:
                st.markdown(f"""
                <div style="margin-bottom:0.3rem;">
                    <div style="font-size:0.72rem;color:#64748b;font-weight:500;
                                text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">
                        TF-IDF Similarity
                    </div>
                    <div style="font-size:1.4rem;font-weight:800;color:#818cf8;
                                letter-spacing:-0.03em;">{r.tfidf_score*100:.1f}%</div>
                    {score_bar(r.tfidf_score*100)}
                </div>""", unsafe_allow_html=True)
            with b3:
                st.markdown(f"""
                <div style="margin-bottom:0.3rem;">
                    <div style="font-size:0.72rem;color:#64748b;font-weight:500;
                                text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;">
                        Skill Coverage
                    </div>
                    <div style="font-size:1.4rem;font-weight:800;color:#a78bfa;
                                letter-spacing:-0.03em;">{r.skill_score*100:.1f}%</div>
                    {score_bar(r.skill_score*100)}
                </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:1px;background:rgba(255,255,255,0.05);margin:0.8rem 0;"></div>', unsafe_allow_html=True)

            # Skill columns
            sk1, sk2, sk3 = st.columns(3)
            with sk1:
                st.markdown(f"""
                <div style="font-size:0.72rem;font-weight:600;color:#34d399;
                            text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;
                            display:flex;align-items:center;gap:5px;">
                    {svg_icon(ICONS['check'], size=12, color='#34d399')} Matched
                    <span style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);
                                 color:#34d399;padding:1px 6px;border-radius:10px;font-size:0.68rem;">
                        {len(r.matched_skills)}
                    </span>
                </div>
                {tags_html(r.matched_skills, 'tag-match')}
                """, unsafe_allow_html=True)
            with sk2:
                st.markdown(f"""
                <div style="font-size:0.72rem;font-weight:600;color:#f87171;
                            text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;
                            display:flex;align-items:center;gap:5px;">
                    {svg_icon(ICONS['x_mark'], size=12, color='#f87171')} Missing
                    <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);
                                 color:#f87171;padding:1px 6px;border-radius:10px;font-size:0.68rem;">
                        {len(r.missing_skills)}
                    </span>
                </div>
                {tags_html(r.missing_skills, 'tag-miss')}
                """, unsafe_allow_html=True)
            with sk3:
                st.markdown(f"""
                <div style="font-size:0.72rem;font-weight:600;color:#a5b4fc;
                            text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;
                            display:flex;align-items:center;gap:5px;">
                    {svg_icon(ICONS['plus'], size=12, color='#a5b4fc')} Additional
                    <span style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.25);
                                 color:#a5b4fc;padding:1px 6px;border-radius:10px;font-size:0.68rem;">
                        {len(r.extra_skills)}
                    </span>
                </div>
                {tags_html(r.extra_skills[:15], 'tag-extra')}
                """, unsafe_allow_html=True)

            # Top keywords
            if r.top_tfidf_terms:
                st.markdown('<div style="height:1px;background:rgba(255,255,255,0.05);margin:0.8rem 0 0.6rem;"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="font-size:0.72rem;font-weight:600;color:#94a3b8;
                            text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;
                            display:flex;align-items:center;gap:5px;">
                    {svg_icon(ICONS['key'], size=12, color='#6366f1')} Top TF-IDF Keywords
                </div>
                {tags_html(r.top_tfidf_terms[:8], 'tag-extra')}
                """, unsafe_allow_html=True)

    # Footer
    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:1.5rem 0 0.8rem;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;color:#1e293b;font-size:0.72rem;">
        <span style="color:#334155;font-weight:600;">RecruitIQ — AI-Based Resume Ranking System</span>
        <span style="color:#1e293b;">Python · spaCy · scikit-learn · Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Landing state ─────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    feat_cols = st.columns(3, gap="large")
    features = [
        (ICONS['upload'],   "Multi-Format Parsing",
         "Extracts raw text from PDF, DOCX, and TXT resumes. Uses pdfplumber as primary engine with PyPDF2 as fallback for complex layouts."),
        (ICONS['layers'],   "NLP Preprocessing Pipeline",
         "spaCy-powered: noise removal, tokenization, stopword filtering, and lemmatization — before TF-IDF vectorization."),
        (ICONS['zap'],      "Explainable AI Ranking",
         "Blends TF-IDF cosine similarity with a skill-overlap ratio from a 250+ skill taxonomy for transparent, auditable results."),
    ]

    for col, (icon, title, desc) in zip(feat_cols, features):
        with col:
            st.markdown(f"""
            <div class="feat-card">
                <div class="feat-icon">
                    {svg_icon(icon, size=20, color='#a78bfa')}
                </div>
                <div class="feat-title">{title}</div>
                <div class="feat-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:2.8rem;color:var(--text-muted);font-size:0.84rem;line-height:2;">
        Select a sample job description &nbsp;&rarr;&nbsp; load candidates &nbsp;&rarr;&nbsp; click
        <span style="color:#a78bfa;font-weight:600;background:rgba(139,92,246,0.12);
                     border:1px solid rgba(139,92,246,0.25);padding:2px 12px;border-radius:6px;">
            Run Screening
        </span>
    </div>
    """, unsafe_allow_html=True)

