import streamlit as st
import re
from urllib.parse import urlparse
import pandas as pd

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhishGuard – Phishing Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ═══════════════════════════════════════════
   BASE
═══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: #060b18 !important;
    color: #cbd5e1;
    font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
}
[data-testid="stHeader"]          { background: transparent !important; }
[data-testid="stSidebar"]         { background-color: #080e1f !important; }
[data-testid="stDecoration"]      { display: none; }
[data-testid="stToolbar"]         { display: none; }

/* remove default streamlit top padding */
.block-container {
    max-width: 100% !important;
    padding: 0 clamp(1rem, 4vw, 3.5rem) 3rem !important;
}

/* ═══════════════════════════════════════════
   HEADER BAR
═══════════════════════════════════════════ */
.pg-header {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1.35rem clamp(1.25rem, 3vw, 2.5rem);
    background: linear-gradient(115deg, #08142f 0%, #102653 48%, #0a1734 100%);
    border-bottom: 1px solid rgba(59, 130, 246, .55);
    box-shadow: 0 10px 32px rgba(2, 8, 23, .22);
    margin-bottom: 1.5rem;
    margin-left: calc(-1 * clamp(1rem, 4vw, 3.5rem));
    margin-right: calc(-1 * clamp(1rem, 4vw, 3.5rem));
    overflow: hidden;
}
.pg-header::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
    background: linear-gradient(180deg, #60a5fa, #2563eb, #34d399);
}
.pg-header::after {
    content: "";
    position: absolute;
    width: 260px;
    height: 160px;
    right: 12%;
    top: -100px;
    border-radius: 50%;
    background: rgba(59, 130, 246, .10);
    filter: blur(35px);
    pointer-events: none;
}
.pg-logo {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 1rem;
    min-width: 0;
}
.pg-logo-icon {
    flex: 0 0 54px;
    width: 54px;
    height: 54px;
    background: linear-gradient(145deg, #60a5fa 0%, #2563eb 48%, #1d4ed8 100%);
    border: 1px solid rgba(191, 219, 254, .35);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.7rem;
    box-shadow: 0 8px 24px rgba(37, 99, 235, .32), inset 0 1px 0 rgba(255,255,255,.2);
}
.pg-logo-text {
    line-height: 1.1 !important;
}
.pg-logo-text h1,
.pg-logo-text div {
    display: block !important;
    font-family: 'Inter', Arial, sans-serif !important;
    font-size: 64px !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    text-transform: uppercase !important;
    letter-spacing: -1.8px !important;
    line-height: 1.02 !important;
    margin: 0 !important;
    padding: 0 !important;
    height: auto !important;
    max-height: none !important;
    text-shadow:
    0 0 8px rgba(96, 165, 250, 0.30),
    0 0 22px rgba(59, 130, 246, 0.25),
    0 0 38px rgba(37, 99, 235, 0.15) !important;
}
.pg-logo-text span {
    display: block;
    margin-top: .45rem;
    font-size: .72rem !important;
    font-weight: 600;
    color: #9bb2d8 !important;
    letter-spacing: .16em;
    text-transform: uppercase;
}
.pg-status {
    position: relative;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    gap: .6rem;
    background: linear-gradient(135deg, rgba(6, 78, 59, .34), rgba(6, 95, 70, .16));
    border: 1px solid rgba(52, 211, 153, .35);
    border-radius: 999px;
    padding: .65rem 1rem;
    font-size: .82rem;
    font-weight: 700;
    color: #6ee7b7;
    letter-spacing: .01em;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
    white-space: nowrap;
}
.pg-status-dot {
    width: 9px;
    height: 9px;
    flex: 0 0 9px;
    background: #34d399;
    border-radius: 50%;
    box-shadow: 0 0 0 4px rgba(52, 211, 153, .10), 0 0 12px rgba(52, 211, 153, .65);
    animation: pulse 2s infinite;
}
@media (max-width: 600px) {
    .pg-header { padding: 1.1rem 1.25rem; }
    .pg-logo { gap: .75rem; }
    .pg-logo-icon { flex-basis: 44px; width: 44px; height: 44px; border-radius: 13px; font-size: 1.4rem; }
    .pg-logo-text h1, .pg-logo-text div { font-size: clamp(2rem, 9vw, 3rem) !important; letter-spacing: -1px !important; }
    .pg-logo-text span { font-size: .62rem !important; letter-spacing: .1em; }
    .pg-status { padding: .5rem .8rem; }
}
@keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50%      { opacity: .5; transform: scale(1.4); }
}

/* ═══════════════════════════════════════════
   STAT CARDS
═══════════════════════════════════════════ */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
@media (max-width: 900px) { .stat-grid { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 500px) { .stat-grid { grid-template-columns: 1fr; } }

.stat-card {
    background: #0c1428;
    border: 1px solid #1e2d52;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    position: relative;
    overflow: hidden;
    transition: border-color .2s, transform .2s;
}
.stat-card:hover { border-color: #2d4fa8; transform: translateY(-2px); }
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, #3b82f6);
    border-radius: 14px 14px 0 0;
}
.stat-card .sc-icon {
    font-size: 1.4rem; margin-bottom: .5rem;
    filter: drop-shadow(0 0 6px var(--accent, #3b82f6));
}
.stat-card .sc-label {
    font-size: .7rem; text-transform: uppercase;
    letter-spacing: .08em; color: #475569; font-weight: 600;
    margin-bottom: .25rem;
}
.stat-card .sc-value {
    font-size: 1.9rem; font-weight: 800; color: #e2e8f0;
    line-height: 1;
}
.stat-card .sc-sub {
    font-size: .72rem; color: #475569; margin-top: .3rem;
}

/* ═══════════════════════════════════════════
   SCANNER PANELS
═══════════════════════════════════════════ */
.scanner-panel {
    background: #0c1428;
    border: 1px solid #1e2d52;
    border-radius: 16px;
    overflow: hidden;
    height: 100%;
}
.scanner-panel-head {
    padding: 1.1rem 1.4rem .9rem;
    border-bottom: 1px solid #1a2745;
    background: linear-gradient(135deg, #0d1d4a 0%, #0e1f50 100%);
    display: flex; align-items: center; gap: .6rem;
}
.scanner-panel-head .sph-icon {
    width: 32px; height: 32px;
    background: rgba(59,130,246,.15);
    border: 1px solid rgba(59,130,246,.3);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.scanner-panel-head h2 {
    font-size: .95rem; font-weight: 700; color: #93c5fd; margin: 0 0 .1rem;
}
.scanner-panel-head p  {
    font-size: .75rem; color: #475569; margin: 0;
}
.scanner-panel-body { padding: 1.1rem 1.4rem 1.4rem; }

/* ═══════════════════════════════════════════
   INPUTS
═══════════════════════════════════════════ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #070d1e !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e3060 !important;
    border-radius: 10px !important;
    font-size: .88rem !important;
    transition: border-color .2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important;
}

/* ═══════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════ */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: .88rem !important;
    padding: .6rem 1.5rem !important;
    width: 100% !important;
    letter-spacing: .02em;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 4px 14px rgba(37,99,235,.35) !important;
}
[data-testid="stButton"] > button:hover {
    opacity: .9 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* secondary / ghost button overrides — applied via key suffix class trick */
.btn-secondary [data-testid="stButton"] > button {
    background: rgba(30,58,138,.35) !important;
    border: 1px solid #1e3a8a !important;
    box-shadow: none !important;
    color: #93c5fd !important;
}

/* ═══════════════════════════════════════════
   RESULT PANEL
═══════════════════════════════════════════ */
.result-panel {
    background: #0c1428;
    border: 1px solid #1e2d52;
    border-radius: 14px;
    overflow: hidden;
    margin-top: 1rem;
    animation: fadeIn .35s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

.result-panel-head {
    padding: .85rem 1.2rem;
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: .6rem;
    border-bottom: 1px solid #1a2745;
}
.rph-left { display: flex; align-items: center; gap: .75rem; }
.rph-verdict {
    font-size: .7rem; text-transform: uppercase; letter-spacing: .1em;
    color: #64748b; font-weight: 600; margin-bottom: .2rem;
}
.rph-title { font-size: 1.05rem; font-weight: 700; color: #e2e8f0; }

.score-strip {
    display: flex; align-items: center; gap: .9rem;
    flex-wrap: wrap;
}
.score-pill {
    background: rgba(59,130,246,.1);
    border: 1px solid rgba(59,130,246,.25);
    border-radius: 8px;
    padding: .3rem .75rem;
    font-size: .8rem; color: #93c5fd; font-weight: 600;
    white-space: nowrap;
}
.score-bar-wrap { flex: 1 1 120px; min-width: 80px; }
.score-bar-track {
    background: #131f3a;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    border: 1px solid #1e3a8a;
}
.score-bar-fill { height: 100%; border-radius: 999px; transition: width .5s ease; }

/* badges */
.badge {
    display: inline-flex; align-items: center; gap: .3rem;
    padding: .28rem .9rem;
    border-radius: 20px;
    font-weight: 700; font-size: .78rem;
    letter-spacing: .06em; text-transform: uppercase;
    white-space: nowrap;
}
.badge::before { content:''; width:6px; height:6px; border-radius:50%; background:currentColor; opacity:.8; }
.badge-low    { background:#052e20; color:#34d399; border:1px solid #065f46; }
.badge-medium { background:#431407; color:#fb923c; border:1px solid #7c2d12; }
.badge-high   { background:#450a0a; color:#f87171; border:1px solid #7f1d1d; }

/* ═══════════════════════════════════════════
   WARNING & RECOMMENDATION ITEMS
═══════════════════════════════════════════ */
.warn-item {
    display: flex; align-items: flex-start; gap: .6rem;
    background: #160d0d;
    border: 1px solid #3f1313;
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: .55rem .85rem;
    margin-bottom: .4rem;
    color: #fca5a5;
    font-size: .82rem; line-height: 1.45;
}
.rec-item {
    display: flex; align-items: flex-start; gap: .6rem;
    background: #061512;
    border: 1px solid #0d3b2e;
    border-left: 3px solid #10b981;
    border-radius: 8px;
    padding: .55rem .85rem;
    margin-bottom: .4rem;
    color: #6ee7b7;
    font-size: .82rem; line-height: 1.45;
}

.section-label {
    font-size: .7rem; text-transform: uppercase; letter-spacing: .1em;
    color: #475569; font-weight: 700;
    margin: 1rem 0 .5rem; padding: 0 1.2rem;
}

.result-body { padding: 0 1.2rem 1.2rem; }

.breakdown-table {
    width: 100%; border-collapse: collapse; font-size: .82rem; margin-top: .2rem;
}
.breakdown-table td {
    padding: .35rem .5rem;
    border-bottom: 1px solid #131f3a;
}
.breakdown-table tr:last-child td { border-bottom: none; }
.breakdown-table td:first-child { color: #64748b; width: 38%; }
.breakdown-table td:last-child  { color: #e2e8f0; font-weight: 500; }

/* ═══════════════════════════════════════════
   SCAN HISTORY TABLE
═══════════════════════════════════════════ */
.history-wrap {
    background: #0c1428;
    border: 1px solid #1e2d52;
    border-radius: 16px;
    /* do NOT clip — let the dataframe scroll inside */
    overflow: visible;
    margin-top: 1rem;
    width: 100%;
}
.history-head {
    padding: .9rem 1.4rem;
    border-bottom: 1px solid #1a2745;
    border-radius: 16px 16px 0 0;
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: .5rem;
}
.history-head h3 { margin: 0; font-size: .95rem; font-weight: 700; color: #93c5fd; }
.history-head span { font-size: .75rem; color: #475569; }

/* ── dataframe container: full-width, tall, scrollable ── */
[data-testid="stDataFrame"] {
    border: none !important;
    width: 100% !important;
    min-width: 0 !important;
}
/* the inner glide-data-grid iframe / canvas wrapper */
[data-testid="stDataFrame"] > div {
    border-radius: 0 0 16px 16px !important;
    border: none !important;
    width: 100% !important;
    /* allow horizontal scroll on small screens without page overflow */
    overflow-x: auto !important;
    overflow-y: auto !important;
}
/* make every column cell wrap long text instead of truncating */
[data-testid="stDataFrame"] [role="gridcell"],
[data-testid="stDataFrame"] [role="columnheader"] {
    white-space: normal !important;
    word-break: break-word !important;
}

/* ═══════════════════════════════════════════
   DIVIDERS
═══════════════════════════════════════════ */
.result-divider {
    border: none; border-top: 1px solid #131f3a; margin: 1rem 0;
}

/* ═══════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════ */
.footer {
    text-align: center; color: #2d3f5e;
    font-size: .75rem; margin-top: 3rem;
    border-top: 1px solid #0f1a30; padding-top: 1.2rem;
    letter-spacing: .03em;
}

/* ═══════════════════════════════════════════
   MISC STREAMLIT OVERRIDES
═══════════════════════════════════════════ */
[data-testid="stMarkdownContainer"] h4 {
    font-size: .82rem; text-transform: uppercase;
    letter-spacing: .08em; color: #475569;
    font-weight: 700; margin: .9rem 0 .4rem;
}
/* hide expand button on dataframe */
[data-testid="StyledFullScreenButton"] { display: none !important; }
/* hide streamlit hamburger & footer */
#MainMenu, footer { visibility: hidden; }

/* Scanner buttons — larger, clearer text */
.st-key-select_url_scanner button,
.st-key-select_email_scanner button {
    min-height: 100px !important;
    white-space: pre-line !important;
    text-align: center !important;
    padding: 1.1rem 1.4rem !important;
    border-radius: 16px !important;
    border: 1px solid #2563eb !important;
    background: linear-gradient(135deg, #0d1d4a 0%, #0e1f50 100%) !important;
    color: #93c5fd !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
}

.st-key-select_url_scanner button p,
.st-key-select_email_scanner button p {
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    line-height: 1.5 !important;
}

.st-key-select_url_scanner button:hover,
.st-key-select_email_scanner button:hover {
    border-color: #60a5fa !important;
    box-shadow: 0 0 18px rgba(37, 99, 235, 0.25) !important;
}

/* Your existing CSS stays here */

/* Subtle glow for scanner buttons */
.st-key-select_url_scanner button,
.st-key-select_email_scanner button {
    transition: all 180ms ease-in-out !important;
}

.st-key-select_url_scanner button:hover,
.st-key-select_email_scanner button:hover {
    box-shadow: 0 0 18px rgba(37, 99, 235, 0.25) !important;
    border-color: #60a5fa !important;
}

/* ═══════════════════════════════════════════
   RISK SCORE METER
   Displays a large 0-100 normalised score above the progress bar.
   The meter ring colour is driven by --meter-color, set inline per scan.
═══════════════════════════════════════════ */
.risk-meter-wrap {
    display: flex;
    align-items: center;
    gap: 1.4rem;
    padding: 1rem 1.2rem 0.8rem;
    border-bottom: 1px solid #131f3a;
}

/* Circular SVG-backed score ring */
.risk-meter-ring {
    flex: 0 0 84px;
    width: 84px;
    height: 84px;
    position: relative;
}
.risk-meter-ring svg {
    transform: rotate(-90deg);   /* start arc at 12 o'clock */
    width: 84px;
    height: 84px;
}
.risk-meter-ring .ring-bg {
    fill: none;
    stroke: #1a2745;
    stroke-width: 8;
}
.risk-meter-ring .ring-fill {
    fill: none;
    stroke-width: 8;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.6s ease;
}
.risk-meter-num {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    line-height: 1;
    /* NOT rotated — keep the number upright */
}
.risk-meter-num .rmn-val {
    font-size: 1.4rem;
    color: var(--meter-color, #3b82f6);
}
.risk-meter-num .rmn-lbl {
    font-size: .52rem;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: #475569;
    margin-top: .15rem;
}

/* Right-side text block next to the ring */
.risk-meter-text {
    flex: 1 1 auto;
    min-width: 0;
}
.risk-meter-text .rmt-title {
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #475569;
    font-weight: 600;
    margin-bottom: .3rem;
}
.risk-meter-text .rmt-level {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--meter-color, #3b82f6);
    margin-bottom: .4rem;
}
.risk-meter-text .rmt-bar-track {
    background: #131f3a;
    border-radius: 999px;
    height: 7px;
    overflow: hidden;
    border: 1px solid #1e3a8a;
    margin-bottom: .3rem;
}
.risk-meter-text .rmt-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: var(--meter-color, #3b82f6);
    transition: width .6s ease;
}
.risk-meter-text .rmt-caption {
    font-size: .7rem;
    color: #475569;
}

/* ═══════════════════════════════════════════
   SECURITY ALERT BANNERS
   Shown above the warnings list:
     • High  → bright red "THREAT DETECTED" banner
     • Medium→ amber "SUSPICIOUS CONTENT" banner
     • Low   → green  "NO THREATS FOUND"  banner
═══════════════════════════════════════════ */
.alert-banner {
    display: flex;
    align-items: flex-start;
    gap: .75rem;
    border-radius: 10px;
    padding: .85rem 1.1rem;
    margin: .8rem 1.2rem .2rem;
    font-size: .86rem;
    line-height: 1.5;
    border: 1px solid transparent;
}
.alert-banner .ab-icon {
    font-size: 1.35rem;
    flex: 0 0 auto;
    line-height: 1;
    margin-top: .05rem;
}
.alert-banner .ab-body strong {
    display: block;
    font-size: .92rem;
    font-weight: 700;
    margin-bottom: .15rem;
}

/* High-risk: deep red */
.alert-high {
    background: #1c0808;
    border-color: #7f1d1d;
    color: #fca5a5;
}
.alert-high .ab-body strong { color: #f87171; }

/* Medium-risk: amber */
.alert-medium {
    background: #1c1008;
    border-color: #78350f;
    color: #fcd34d;
}
.alert-medium .ab-body strong { color: #fbbf24; }

/* Low-risk / safe: green */
.alert-low {
    background: #061512;
    border-color: #065f46;
    color: #6ee7b7;
}
.alert-low .ab-body strong { color: #34d399; }

/* ═══════════════════════════════════════════
   WARNING ITEM SEVERITY ICONS
   Each triggered rule now shows a coloured
   dot whose intensity reflects the rule weight:
     high-weight  (>= 20 pts) → red    🔴
     medium-weight(>= 10 pts) → amber  🟡
   The colour class is set inline via data attr.
═══════════════════════════════════════════ */
.warn-item-high {
    border-left-color: #ef4444 !important;
    background: #1a0808 !important;
}
.warn-item-medium {
    border-left-color: #f59e0b !important;
    background: #1a1208 !important;
    color: #fcd34d !important;
}
.warn-sev {
    flex: 0 0 auto;
    font-size: .75rem;
    font-weight: 800;
    letter-spacing: .05em;
    text-transform: uppercase;
    padding: .1rem .45rem;
    border-radius: 4px;
    white-space: nowrap;
    align-self: flex-start;
    margin-top: .05rem;
}
.warn-sev-high   { background:#450a0a; color:#f87171; border:1px solid #7f1d1d; }
.warn-sev-medium { background:#431407; color:#fb923c; border:1px solid #7c2d12; }

/* End of CSS */
</style>
""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════════════
#  DETECTION LOGIC — pure if-statement rules, no ML or external APIs
#
#  Each rule is a standalone if block so the logic is easy to read and extend.
#  Every triggered rule appends a human-readable message that explains WHY the
#  item was flagged, not just WHAT matched.
#  Points are additive; risk level is derived from the final score percentage.
# ══════════════════════════════════════════════════════════════════════════════

# Maximum possible URL score — sum of all 14 rule weights below (used for % calc)
# 25+20+15+20+20+10+20+15+10+15+25+15+10+25 = 245
MAX_URL_SCORE = 245

# Maximum possible email score — sum of all 13 rule weights below
# 20+25+15+25+20+10+20+20+25+15+10+25+15 = 245
MAX_EMAIL_SCORE = 245


def _score_url(url: str) -> tuple[int, list[str], list[int]]:
    """
    Analyse a URL with explicit if-statement rules.
    Returns (total_score, list_of_warning_messages, list_of_rule_weights).
    The weights list mirrors warnings 1-to-1 so callers can show severity.
    Each warning message explains why the URL is suspicious.
    """
    warnings: list[str] = []
    weights:  list[int] = []   # tracks the point value of each fired rule
    score = 0
    url_lower = url.lower()

    # ── Rule 1: Raw IP address instead of a domain name (+25 pts) ─────────────
    # Legitimate websites almost never use bare IP addresses in their links.
    # Phishing pages frequently host on cheap VPS IPs to avoid registering
    # a traceable domain name.
    if re.search(r"https?://\d{1,3}(\.\d{1,3}){3}", url_lower):
        warnings.append(
            "IP address used instead of a domain name — legitimate sites use "
            "named domains (e.g. example.com), not raw IPs like 192.168.1.1."
        )
        weights.append(25); score += 25

    # ── Rule 2: Suspicious top-level domain (+20 pts) ──────────────────────────
    # Free or very cheap TLDs (.xyz, .top, .tk, .ml, .cf, .ga, .gq, .pw,
    # .click, .loan) are disproportionately abused for phishing because they
    # cost little or nothing and are easy to discard after a campaign.
    if re.search(r"\.(xyz|top|tk|ml|cf|ga|gq|pw|click|loan)(\/|$)", url_lower):
        warnings.append(
            "Suspicious top-level domain detected (.xyz / .top / .tk / .ml etc.) "
            "— these free or ultra-cheap TLDs are heavily abused by phishing campaigns."
        )
        weights.append(20); score += 20

    # ── Rule 3: Excessive subdomain depth (+15 pts) ────────────────────────────
    # Four or more dot-separated labels before the TLD (e.g.
    # secure.login.paypal.attacker.com) is a classic trick to make the real
    # malicious domain (attacker.com) visually less prominent.
    if re.search(r"(([a-zA-Z0-9\-]+\.){4,}[a-zA-Z]{2,})", url_lower):
        warnings.append(
            "Excessive subdomain depth (4+ levels) — attackers nest many subdomains "
            "to hide the actual controlling domain at the end of the chain."
        )
        weights.append(15); score += 15

    # ── Rule 4: '@' symbol in the URL (+20 pts) ────────────────────────────────
    # Browsers ignore everything before '@' in a URL
    # (e.g. http://trusted.com@evil.com/). Placing a well-known brand before
    # the '@' tricks users into thinking they are visiting the trusted site.
    if "@" in url_lower:
        warnings.append(
            "URL contains an '@' symbol — browsers treat everything before '@' as "
            "credentials and silently redirect to the domain after it, making "
            "http://paypal.com@evil.com appear safe while loading evil.com."
        )
        weights.append(20); score += 20

    # ── Rule 5: Hyphenated login/secure/account keyword (+20 pts) ─────────────
    # Patterns like 'paypal-login', 'secure-account', 'bank-signin' mimic
    # trusted brand names while sitting on a different domain.
    if re.search(r"[a-z]+-[a-z]+(login|secure|account|bank)", url_lower):
        warnings.append(
            "Hyphenated brand-style keyword (e.g. 'paypal-login', 'secure-account') "
            "— phishers use hyphens to impersonate trusted brands without owning "
            "their actual domain."
        )
        weights.append(20); score += 20

    # ── Rule 6: URL length exceeds 75 characters (+10 pts) ────────────────────
    # Excessively long URLs are used to hide the real destination by burying
    # suspicious portions deep in the query string where users won't look.
    if len(url) > 75:
        warnings.append(
            f"URL is unusually long ({len(url)} characters) — attackers pad URLs "
            "to obscure the real domain or bury malicious parameters beyond the "
            "visible portion of the address bar."
        )
        weights.append(10); score += 10

    # ── Rule 7: URL shortener service (+20 pts) ────────────────────────────────
    # Services like bit.ly, tinyurl.com, or t.co completely hide the final
    # destination. Phishers use them so the malicious URL never appears in
    # the email or message.
    if re.search(
        r"(bit\.ly|tinyurl|goo\.gl|t\.co|ow\.ly|is\.gd|buff\.ly|cutt\.ly)",
        url_lower,
    ):
        warnings.append(
            "URL shortener detected (bit.ly / tinyurl / t.co etc.) — shortened "
            "links completely mask the real destination, a common phishing tactic "
            "to prevent previewing where you will actually land."
        )
        weights.append(20); score += 20

    # ── Rule 8: HTTP instead of HTTPS (+15 pts) ────────────────────────────────
    # All modern legitimate sites use HTTPS. An HTTP link means the connection
    # is unencrypted and, more importantly, that no certificate authority has
    # validated the domain owner's identity.
    if url_lower.startswith("http://"):
        warnings.append(
            "Plain HTTP used instead of HTTPS — the connection is unencrypted and "
            "the site has no valid SSL certificate proving ownership, which is "
            "extremely rare for legitimate sites in 2024."
        )
        weights.append(15); score += 15

    # ── Rule 9: Double slashes in the path (+10 pts) ───────────────────────────
    # Double slashes after the host (e.g. https://legit.com//evil) can be used
    # to confuse URL parsers or to redirect to a different path entirely.
    if re.search(r"https?://[^/]+/.*//", url_lower):
        warnings.append(
            "Double slashes found in the URL path — this can confuse browser "
            "parsers and is occasionally used to bypass URL-filtering systems."
        )
        weights.append(10); score += 10

    # ── Rule 10: Non-standard port number (+15 pts) ────────────────────────────
    # Ports like :8080, :3000, or :4443 indicate a non-standard web server.
    # Legitimate public-facing sites almost always serve on port 80/443.
    # Phishing kits are often deployed on cheap hosts that use random ports.
    if re.search(r":\d{2,5}(/|$)", url_lower):
        warnings.append(
            "Non-standard port number in URL (e.g. :8080, :3000) — legitimate "
            "public websites serve on port 80 or 443; other ports suggest a "
            "hastily deployed phishing kit."
        )
        weights.append(15); score += 15

    # ── Rule 11: Punycode / IDN homograph attack (+25 pts) ─────────────────────
    # 'xn--' is the ACE prefix for internationalised domain names. Attackers
    # register domains with visually similar Unicode characters
    # (e.g. xn--pple-43d.com looks like apple.com) to fool users.
    if "xn--" in url_lower:
        warnings.append(
            "Punycode / IDN homograph encoding detected (xn--) — this encoding "
            "allows attackers to register domains that look identical to trusted "
            "brands using visually similar Unicode characters (e.g. apple vs apple)."
        )
        weights.append(25); score += 25

    # ── Rule 12: Sensitive keyword in path or query (+15 pts) ─────────────────
    # Words like 'login', 'verify', 'update', 'password', 'confirm' in the
    # URL path signal a credential-harvesting page. Combined with a suspicious
    # domain, this is a strong phishing indicator.
    if re.search(
        r"(login|signin|verify|account|update|secure|banking|paypal|amazon|"
        r"microsoft|apple|google|support|password|confirm)",
        url_lower,
    ):
        warnings.append(
            "Sensitive keyword found in URL path/query (login / verify / password "
            "/ account etc.) — phishing pages deliberately include these words to "
            "appear as official authentication or account-management pages."
        )
        weights.append(15); score += 15

    # ── Rule 13: Heavy percent-encoding (+10 pts) ──────────────────────────────
    # Three or more percent-encoded sequences (%20, %3A, etc.) in a URL often
    # indicate an attempt to obfuscate the real path or bypass keyword filters.
    if re.search(r"(%[0-9a-fA-F]{2}.*){3,}", url_lower):
        warnings.append(
            "Heavy URL percent-encoding detected (3+ encoded characters like %20) "
            "— excessive encoding is used to obfuscate the true destination path "
            "and to evade text-based URL scanners."
        )
        weights.append(10); score += 10

    # ── Rule 14: Brand name in subdomain pointing to a different TLD (+25 pts) ─
    # e.g. paypal.attacker.com — the brand 'paypal' appears before the dot
    # but the actual domain registered is 'attacker.com', not 'paypal.com'.
    if re.search(
        r"(paypal|amazon|apple|google|microsoft|netflix)\.[^com]", url_lower
    ):
        warnings.append(
            "Trusted brand name appears as a subdomain of a different domain "
            "(e.g. paypal.evil.com) — this is a subdomain spoofing trick designed "
            "to make the URL look legitimate at a quick glance."
        )
        weights.append(25); score += 25

    return score, warnings, weights


def _score_email(text: str) -> tuple[int, list[str], list[int]]:
    """
    Analyse email body text with explicit if-statement rules.
    Returns (total_score, list_of_warning_messages, list_of_rule_weights).
    The weights list mirrors warnings 1-to-1 so callers can show severity.
    Each warning message explains why the email is suspicious.
    """
    warnings: list[str] = []
    weights:  list[int] = []   # tracks the point value of each fired rule
    score = 0
    text_lower = text.lower()

    # ── Rule 1: Urgency / threat language (+20 pts) ────────────────────────────
    # Creating a sense of time pressure ("Act now!", "Within 24 hours",
    # "Account will be suspended") is the most common phishing technique.
    # It bypasses rational thinking and pushes the target to act immediately.
    if re.search(
        r"\b(urgent|immediately|act now|your account (will be|has been)|"
        r"suspended|limited|within 24|expire|alert|warning|critical)\b",
        text_lower,
    ):
        warnings.append(
            "Urgency or threat language detected ('urgent', 'act now', 'suspended', "
            "'within 24 hours' etc.) — phishers manufacture false time pressure to "
            "stop you thinking critically before clicking a malicious link."
        )
        weights.append(20); score += 20

    # ── Rule 2: Request for credentials (+25 pts) ──────────────────────────────
    # Legitimate companies never ask you to 'enter your password' or
    # 'verify your account' via email. This is a definitive phishing signal.
    if re.search(
        r"\b(enter your (password|username|pin|ssn|social security)|"
        r"verify your (account|identity|email|password)|confirm your details)\b",
        text_lower,
    ):
        warnings.append(
            "Explicit request for credentials or personal details ('enter your "
            "password', 'verify your identity' etc.) — no legitimate service ever "
            "asks for passwords or PINs over email."
        )
        weights.append(25); score += 25

    # ── Rule 3: Suspicious call-to-action anchor text (+15 pts) ───────────────
    # Phrases like 'Click here', 'Tap here', or 'Follow this link' without
    # showing the actual URL are used to get victims to follow a link without
    # seeing where it really goes.
    if re.search(
        r"click (here|now|below|this link)|tap here|follow this link",
        text_lower,
    ):
        warnings.append(
            "Vague call-to-action link text found ('click here', 'tap here', "
            "'follow this link') — hiding the destination URL behind generic anchor "
            "text prevents recipients from previewing where the link leads."
        )
        weights.append(15); score += 15

    # ── Rule 4: Lottery / prize scam language (+25 pts) ───────────────────────
    # 'You have won', 'Congratulations, claim your prize' are hallmarks of
    # advance-fee fraud and credential-harvesting prize scams.
    if re.search(
        r"\b(you (have |'ve )?(won|been selected)|congratulations.*prize|"
        r"claim your (reward|prize|gift|winnings))\b",
        text_lower,
    ):
        warnings.append(
            "Lottery or prize scam language found ('you have won', 'claim your "
            "reward', 'congratulations') — these are classic social "
            "engineering hooks used in advance-fee fraud and credential harvesting."
        )
        weights.append(25); score += 25

    # ── Rule 5: Misspelled brand name (+20 pts) ────────────────────────────────
    # Swapping letters for visually similar characters (paypa1, amaz0n, g00gle,
    # app1e) is used to slip past simple keyword filters while still looking
    # convincing to a casual reader.
    if re.search(
        r"\b(paypa[^l]|amaz[o0]n|g[o0]{2}gle|micros[o0]ft|app1e|"
        r"faceb[o0]{2}k|netfl[i1]x)\b",
        text_lower,
    ):
        warnings.append(
            "Misspelled brand name detected (e.g. 'paypa1', 'amaz0n', 'g00gle') "
            "— replacing letters with similar-looking numbers or characters is used "
            "to evade keyword filters while still appearing as a trusted brand."
        )
        weights.append(20); score += 20

    # ── Rule 6: Generic greeting (+10 pts) ────────────────────────────────────
    # 'Dear Customer', 'Dear Account Holder', 'Dear User' indicate a mass
    # phishing campaign where the attacker does not know the recipient's name.
    # Legitimate services personalise their emails.
    if re.search(
        r"\b(dear (customer|user|account holder|member|sir|madam|friend))\b",
        text_lower,
    ):
        warnings.append(
            "Generic, impersonal greeting ('Dear Customer', 'Dear User' etc.) — "
            "legitimate organisations address you by name; phishing emails use "
            "generic salutations because they are sent to thousands of strangers."
        )
        weights.append(10); score += 10

    # ── Rule 7: Threat of account closure (+20 pts) ────────────────────────────
    # 'Your account will be closed/suspended/deactivated' is paired with a
    # fraudulent link to 'verify' the account, harvesting credentials.
    if re.search(
        r"\b(account (will be |has been )?(closed|suspended|terminated|"
        r"deactivated|disabled))\b",
        text_lower,
    ):
        warnings.append(
            "Account closure or suspension threat detected — phishers claim your "
            "account will be shut down to force a panicked click on a fake "
            "'verify now' link that steals your login credentials."
        )
        weights.append(20); score += 20

    # ── Rule 8: Instruction to open an attachment (+20 pts) ────────────────────
    # Malicious attachments (PDF, Word, ZIP) are a primary malware delivery
    # vector. Phrases like 'open the attached invoice' prime the victim to
    # execute a malicious file without thinking.
    if re.search(
        r"\b(open|download|view) (the |this )?"
        r"(attached|attachment|file|document|invoice|receipt)\b",
        text_lower,
    ):
        warnings.append(
            "Instruction to open or download an attachment found ('open the attached "
            "invoice', 'view this document') — malicious attachments are a leading "
            "malware delivery method; do not open files from unexpected emails."
        )
        weights.append(20); score += 20

    # ── Rule 9: Money transfer or crypto request (+25 pts) ─────────────────────
    # Wire transfer, Western Union, MoneyGram, or crypto requests are
    # irreversible payment methods preferred by scammers (BEC fraud, romance
    # scams, ransomware) because funds cannot be recalled.
    if re.search(
        r"\b(wire transfer|send money|bank transfer|western union|"
        r"moneygram|bitcoin|crypto wallet)\b",
        text_lower,
    ):
        warnings.append(
            "Money transfer or cryptocurrency request detected (wire transfer, "
            "Western Union, Bitcoin etc.) — these irreversible payment methods are "
            "exclusively used by scammers; legitimate businesses never request them "
            "via cold email."
        )
        weights.append(25); score += 25

    # ── Rule 10: Fake security alert language (+15 pts) ────────────────────────
    # 'Unusual sign-in detected', 'security breach', 'unauthorized access' are
    # used to create fear and make victims click a fake remediation link.
    if re.search(
        r"\b(unusual (sign-?in|activity|login)|security (breach|alert|notification)|"
        r"unauthorized (access|login))\b",
        text_lower,
    ):
        warnings.append(
            "Fake security alert language found ('unusual sign-in', 'security "
            "breach', 'unauthorized access') — fabricating a security incident is "
            "a classic social-engineering tactic designed to provoke a fearful, "
            "unthinking response."
        )
        weights.append(15); score += 15

    # ── Rule 11: Excessive ALL-CAPS words or exclamation marks (+10 pts) ───────
    # Three or more all-caps words (e.g. FREE, URGENT, ACT) or three or more
    # exclamation marks are strong visual indicators of spam / scam content
    # and are rarely found in professional correspondence.
    caps_words = re.findall(r"\b[A-Z]{4,}\b", text)   # find words with 4+ capitals
    exclamation_count = text.count("!")
    if len(caps_words) >= 3 or exclamation_count >= 3:
        warnings.append(
            f"Excessive capitalisation ({len(caps_words)} all-caps word(s)) or "
            f"exclamation marks ({exclamation_count}) — aggressive formatting is a "
            "hallmark of spam and scam emails, used to manufacture excitement or "
            "alarm that overrides careful reading."
        )
        weights.append(10); score += 10

    # ── Rule 12: Request to reply with sensitive information (+25 pts) ─────────
    # 'Reply with your password', 'respond with your SSN' — legitimate services
    # never collect credentials through plain email replies.
    if re.search(
        r"\b(reply (with|to this)|respond (with|to this)).{0,40}"
        r"(password|ssn|number|details|info)\b",
        text_lower,
    ):
        warnings.append(
            "Request to reply to the email with sensitive information (password, "
            "SSN, account details) — legitimate companies never collect credentials "
            "via email replies; this is a direct social-engineering extraction attempt."
        )
        weights.append(25); score += 25

    # ── Rule 13: Free money / financial bait language (+15 pts) ───────────────
    # 'Free gift card', 'pre-approved for a loan', 'no cost no fee' are used
    # in financial bait scams to lure victims into providing personal data or
    # making upfront payments to claim a fictitious reward.
    if re.search(
        r"\b(free (money|gift card|iphone|laptop)|"
        r"you (are|have been) (pre-?approved|selected)|"
        r"no (cost|fee|obligation))\b",
        text_lower,
    ):
        warnings.append(
            "Financial bait language found ('free gift card', 'pre-approved', "
            "'no fee no obligation') — unsolicited financial offers are used to "
            "entice victims into handing over personal data or making upfront "
            "'processing' payments."
        )
        weights.append(15); score += 15

    return score, warnings, weights


def _risk_level(score: int, max_score: int) -> tuple[str, str, str]:
    """
    Convert a raw score to a risk tier based on percentage of maximum.

    Thresholds are calibrated against the fixed max scores (245 pts each).
    In practice, a heavily flagged URL/email will score roughly 80-140 pts
    (33-57%), so the tiers are spread to produce meaningful Low/Medium/High
    classifications across real-world inputs:

      < 15%  -> Low    (0-36 pts)  -- few or no indicators, likely safe
      15-35% -> Medium (37-85 pts) -- several indicators, treat with caution
      > 35%  -> High   (86+ pts)   -- many serious indicators, do not proceed

    Returns (level_label, css_badge_class, bar_colour_hex).
    """
    pct = score / max_score if max_score else 0
    if pct < 0.15:
        return "Low",    "badge-low",    "#10b981"
    elif pct < 0.35:
        return "Medium", "badge-medium", "#f59e0b"
    else:
        return "High",   "badge-high",   "#ef4444"


URL_RECOMMENDATIONS = {
    "Low": [
        "✅ This URL appears safe, but always verify the domain carefully.",
        "🔒 Ensure the site uses HTTPS before entering any information.",
        "🧠 Keep your browser and antivirus software up to date.",
    ],
    "Medium": [
        "⚠️ Proceed with caution — do not enter passwords or payment details.",
        "🔍 Manually type the official website address in your browser instead.",
        "📋 Check the full URL in your address bar for unexpected characters.",
        "📞 Contact the organisation directly if you're unsure about this link.",
    ],
    "High": [
        "🚫 Do NOT click, visit, or share this URL.",
        "🗑️ Delete the message containing this link immediately.",
        "🔑 If you already visited it, change your passwords right away.",
        "🛡️ Report it to your IT team or at reportphishing.antiphishing.org.",
        "🔔 Enable multi-factor authentication on all important accounts.",
    ],
}

EMAIL_RECOMMENDATIONS = {
    "Low": [
        "✅ This email appears legitimate, but stay alert.",
        "🔗 Hover over links before clicking to preview the destination.",
        "📎 Be cautious with unexpected attachments.",
    ],
    "Medium": [
        "⚠️ Treat this email with suspicion — verify the sender independently.",
        "❌ Do not click links or download attachments from this email.",
        "📞 If it claims to be from a known company, call them directly.",
        "🔍 Check the sender's full email address for misspellings.",
    ],
    "High": [
        "🚫 This email shows strong signs of phishing — do NOT respond.",
        "🗑️ Delete this email immediately without clicking anything.",
        "🔑 If you replied with credentials, change your passwords now.",
        "📣 Report it as phishing in your email client (e.g. Gmail → Report Phishing).",
        "🏦 If financial info was shared, contact your bank immediately.",
        "🛡️ Run a malware scan on your device as a precaution.",
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
#  SAMPLE DATA
# ══════════════════════════════════════════════════════════════════════════════
SAMPLE_RECORDS = [
    {"ID": 1,  "URL / Email": "http://paypal-secure-login.xyz/verify",          "Type": "URL",   "Risk Level": "High",   "Risk Score": 185, "Scan Status": "⛔ Blocked"},
    {"ID": 2,  "URL / Email": "support@micros0ft-helpdesk.com",                  "Type": "Email", "Risk Level": "High",   "Risk Score": 170, "Scan Status": "⛔ Blocked"},
    {"ID": 3,  "URL / Email": "https://192.168.4.22/account/reset",              "Type": "URL",   "Risk Level": "High",   "Risk Score": 160, "Scan Status": "⛔ Blocked"},
    {"ID": 4,  "URL / Email": "Click here to claim your FREE iPhone NOW!!!",     "Type": "Email", "Risk Level": "High",   "Risk Score": 155, "Scan Status": "⛔ Blocked"},
    {"ID": 5,  "URL / Email": "http://bit.ly/amaz0n-prize-claim",                "Type": "URL",   "Risk Level": "High",   "Risk Score": 150, "Scan Status": "⛔ Blocked"},
    {"ID": 6,  "URL / Email": "Dear Customer, your account will be suspended",   "Type": "Email", "Risk Level": "High",   "Risk Score": 140, "Scan Status": "⛔ Blocked"},
    {"ID": 7,  "URL / Email": "https://secure-banklogin.top/signin?ref=user",    "Type": "URL",   "Risk Level": "High",   "Risk Score": 135, "Scan Status": "⛔ Blocked"},
    {"ID": 8,  "URL / Email": "Wire transfer $500 to confirm your identity",     "Type": "Email", "Risk Level": "High",   "Risk Score": 130, "Scan Status": "⛔ Blocked"},
    {"ID": 9,  "URL / Email": "http://apple-verify.tk/update-payment",           "Type": "URL",   "Risk Level": "Medium", "Risk Score": 95,  "Scan Status": "⚠️ Flagged"},
    {"ID": 10, "URL / Email": "Unusual sign-in detected. Verify now.",           "Type": "Email", "Risk Level": "Medium", "Risk Score": 90,  "Scan Status": "⚠️ Flagged"},
    {"ID": 11, "URL / Email": "https://login-google.support/password-reset",     "Type": "URL",   "Risk Level": "Medium", "Risk Score": 85,  "Scan Status": "⚠️ Flagged"},
    {"ID": 12, "URL / Email": "You have been pre-approved for a $10,000 loan",   "Type": "Email", "Risk Level": "Medium", "Risk Score": 80,  "Scan Status": "⚠️ Flagged"},
    {"ID": 13, "URL / Email": "http://tinyurl.com/nf7x2k9p",                     "Type": "URL",   "Risk Level": "Medium", "Risk Score": 75,  "Scan Status": "⚠️ Flagged"},
    {"ID": 14, "URL / Email": "Dear user, please confirm your account details",  "Type": "Email", "Risk Level": "Medium", "Risk Score": 65,  "Scan Status": "⚠️ Flagged"},
    {"ID": 15, "URL / Email": "https://netflix.com/login/verify-account",        "Type": "URL",   "Risk Level": "Low",    "Risk Score": 30,  "Scan Status": "✅ Clean"},
    {"ID": 16, "URL / Email": "Your monthly invoice is attached. Thank you.",    "Type": "Email", "Risk Level": "Low",    "Risk Score": 25,  "Scan Status": "✅ Clean"},
    {"ID": 17, "URL / Email": "https://www.github.com/features/security",        "Type": "URL",   "Risk Level": "Low",    "Risk Score": 10,  "Scan Status": "✅ Clean"},
    {"ID": 18, "URL / Email": "Hi John, your order has shipped! Track here.",    "Type": "Email", "Risk Level": "Low",    "Risk Score": 10,  "Scan Status": "✅ Clean"},
    {"ID": 19, "URL / Email": "https://docs.python.org/3/library/re.html",       "Type": "URL",   "Risk Level": "Low",    "Risk Score": 5,   "Scan Status": "✅ Clean"},
    {"ID": 20, "URL / Email": "Newsletter: Weekly cybersecurity digest – Vol 12","Type": "Email", "Risk Level": "Low",    "Risk Score": 0,   "Scan Status": "✅ Clean"},
]


# ══════════════════════════════════════════════════════════════════════════════
#  RENDER HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def render_results(
    score: int,
    max_score: int,
    warnings: list[str],
    recs: dict,
    breakdown_html: str = "",
    weights: list[int] | None = None,
) -> None:
    """
    Render the unified result panel, including:
      1. Risk Score Meter  — 0-100 normalised score ring + labelled progress bar
      2. Security Alert    — prominent banner that changes colour with risk level
      3. Threat Warnings   — each indicator tagged with a severity pill
      4. URL/Email Breakdown table (optional)
      5. Safety Recommendations
    """
    if weights is None:
        # Fallback: treat every warning as medium-weight when no data given
        weights = [15] * len(warnings)

    level, badge_cls, bar_color = _risk_level(score, max_score)

    # ── 1. Normalise score to 0-100 for the meter display ─────────────────────
    # We map the raw score against max_score, then clamp to [0, 100].
    # This gives a consistent 0-100 scale regardless of scan type.
    meter_pct = min(round((score / max_score) * 100), 100) if max_score else 0

    # SVG ring math: circumference of a circle with r=34 is 2*pi*34 ≈ 213.6
    # stroke-dashoffset = circumference * (1 - fill_fraction)
    circ = 213.6
    dash_offset = round(circ * (1 - meter_pct / 100), 1)

    # ── 2. Build the alert banner text based on risk level ────────────────────
    # Each tier gets a distinct icon, title, and supporting sentence so users
    # understand immediately what action they should take.
    if level == "High":
        alert_cls  = "alert-high"
        alert_icon = "🚨"
        alert_title = "THREAT DETECTED — Do Not Proceed"
        alert_body  = (
            f"This scan returned a risk score of {meter_pct}/100. "
            f"{len(warnings)} suspicious indicator(s) were found. "
            "Avoid clicking links, entering credentials, or opening attachments."
        )
    elif level == "Medium":
        alert_cls  = "alert-medium"
        alert_icon = "⚠️"
        alert_title = "Suspicious Content — Proceed with Caution"
        alert_body  = (
            f"This scan returned a risk score of {meter_pct}/100. "
            f"{len(warnings)} indicator(s) suggest potentially unsafe content. "
            "Verify the source independently before taking any action."
        )
    else:  # Low
        alert_cls  = "alert-low"
        alert_icon = "✅"
        alert_title = "No Threats Found — Appears Safe"
        alert_body  = (
            f"This scan returned a risk score of {meter_pct}/100. "
            "No significant phishing indicators were detected. "
            "Stay cautious — always verify unexpected messages."
        )

    # ── 3. Open the result panel and render the existing header strip ─────────
    verdict_icon = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}[level]

    st.markdown(f"""
    <div class="result-panel">
        <div class="result-panel-head">
            <div class="rph-left">
                <div style="font-size:1.6rem">{verdict_icon}</div>
                <div>
                    <div class="rph-verdict">Scan Verdict</div>
                    <div class="rph-title">
                        <span class="badge {badge_cls}">{level} Risk</span>
                    </div>
                </div>
            </div>
            <div class="score-strip">
                <div class="score-pill">Score: {score} / {max_score}</div>
                <div class="score-pill">Indicators: {len(warnings)}</div>
                <div class="score-bar-wrap">
                    <div class="score-bar-track">
                        <div class="score-bar-fill"
                             style="width:{meter_pct}%;background:{bar_color};"></div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── 4. Risk Score Meter ────────────────────────────────────────────────────
    # Shows a circular SVG arc (filled proportionally to 0-100 score) alongside
    # a labelled linear progress bar. The --meter-color CSS variable controls
    # both ring and bar colour without extra class logic.
    caption_text = (
        f"{len(warnings)} indicator(s) triggered"
        if warnings else "No suspicious indicators detected"
    )
    st.markdown(f"""
    <div class="risk-meter-wrap" style="--meter-color:{bar_color}">
        <!-- Circular arc ring: fill fraction = meter_pct/100 -->
        <div class="risk-meter-ring">
            <svg viewBox="0 0 84 84">
                <!-- Background track ring -->
                <circle class="ring-bg" cx="42" cy="42" r="34"/>
                <!-- Coloured fill arc: stroke-dashoffset drives the arc length -->
                <circle class="ring-fill"
                        cx="42" cy="42" r="34"
                        stroke="{bar_color}"
                        stroke-dasharray="{circ}"
                        stroke-dashoffset="{dash_offset}"/>
            </svg>
            <!-- Centred numeric label over the ring (not rotated by CSS) -->
            <div class="risk-meter-num">
                <span class="rmn-val">{meter_pct}</span>
                <span class="rmn-lbl">/ 100</span>
            </div>
        </div>
        <!-- Right-side text: tier label + linear progress bar -->
        <div class="risk-meter-text">
            <div class="rmt-title">Risk Score Meter</div>
            <div class="rmt-level">{level} Risk</div>
            <div class="rmt-bar-track">
                <div class="rmt-bar-fill" style="width:{meter_pct}%"></div>
            </div>
            <div class="rmt-caption">{caption_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 5. Security Alert Banner ───────────────────────────────────────────────
    # One clearly visible banner appears directly below the meter so users see
    # the verdict at a glance before reading the detailed indicators.
    st.markdown(f"""
    <div class="alert-banner {alert_cls}">
        <div class="ab-icon">{alert_icon}</div>
        <div class="ab-body">
            <strong>{alert_title}</strong>
            {alert_body}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 6. Detected Indicators (with severity pills) ──────────────────────────
    # Each fired rule is shown in a card. Rules worth >= 20 pts are tagged HIGH
    # severity (red pill), rules worth 10-19 pts are tagged MEDIUM (amber pill).
    # This helps users understand which findings are most serious.
    if warnings:
        st.markdown(
            '<div class="section-label">⚠️ Detected Indicators</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="result-body">', unsafe_allow_html=True)
        for w, wt in zip(warnings, weights):
            # Determine severity tier based on rule weight
            if wt >= 20:
                # High-weight rule: strong red indicator
                sev_cls  = "warn-sev-high"
                sev_lbl  = "HIGH"
                card_cls = "warn-item warn-item-high"
            else:
                # Medium-weight rule: amber indicator
                sev_cls  = "warn-sev-medium"
                sev_lbl  = "MED"
                card_cls = "warn-item warn-item-medium"
            st.markdown(
                f'<div class="{card_cls}">'
                f'<span class="warn-sev {sev_cls}">{sev_lbl}</span>'
                f'&nbsp;{w}'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 7. URL / Email Breakdown table ────────────────────────────────────────
    if breakdown_html:
        st.markdown(
            '<div class="section-label">🔎 URL Breakdown</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="result-body">{breakdown_html}</div>',
            unsafe_allow_html=True,
        )

    # ── 8. Safety Recommendations ─────────────────────────────────────────────
    st.markdown(
        '<div class="section-label">💡 Safety Recommendations</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="result-body">', unsafe_allow_html=True)
    for rec in recs[level]:
        st.markdown(f'<div class="rec-item">{rec}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close result-panel


def render_sample_table() -> None:
    """Render the 20 sample records using st.dataframe."""
    df = pd.DataFrame(SAMPLE_RECORDS).rename(columns={"Type": "Detection Type"})
    st.markdown(
        '<div class="history-wrap">'
        '<div class="history-head">'
        '<h3>📋 Scan History</h3>'
        '<span>20 sample records · sorted by risk</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    # height: 38px header + 20 rows × 38px row height + 2px border
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=798,
        column_config={
            "ID":             st.column_config.NumberColumn("ID",             width="small"),
            "URL / Email":    st.column_config.TextColumn("URL / Email",      width="large"),
            "Detection Type": st.column_config.TextColumn("Type",            width="medium"),
            "Risk Level":     st.column_config.TextColumn("Risk Level",       width="medium"),
            "Risk Score":     st.column_config.NumberColumn("Score",          width="small",
                                                            format="%d pts"),
            "Scan Status":    st.column_config.TextColumn("Status",          width="medium"),
        },
    )
        # Redesigned risk analysis graph
    import plotly.express as px

    risk_counts = (
        pd.DataFrame(SAMPLE_RECORDS)["Risk Level"]
        .value_counts()
        .reindex(["High", "Low", "Medium"], fill_value=0)
    )

    chart_data = pd.DataFrame({
        "Risk Level": risk_counts.index,
        "Number of Records": risk_counts.values,
    })

    colors = {
        "High": "#FF5B64",
        "Low": "#35D0B0",
        "Medium": "#FFC247",
    }

    fig = px.bar(
        chart_data,
        x="Risk Level",
        y="Number of Records",
        color="Risk Level",
        color_discrete_map=colors,
        text="Number of Records",
        title="📊 Sample Records Risk Analysis",
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        paper_bgcolor="#07152F",
        plot_bgcolor="#07152F",
        font=dict(color="#E5EEFF", family="Arial"),
        showlegend=False,
        xaxis_title="Risk Level",
        yaxis_title="Number of Records",
        yaxis=dict(
            rangemode="tozero",
            gridcolor="#19365D",
        ),
        xaxis=dict(showgrid=False),
        margin=dict(l=25, r=25, t=80, b=25),
        height=430,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD STATS  — computed once from session_state on every render pass
#
#  Why this avoids double-counting:
#  Streamlit re-runs the entire script on every interaction. Rather than
#  incrementing a counter each run (which would inflate numbers), we derive
#  stats purely from what is stored in session_state. Each scanner key
#  ('url_result', 'email_result') is set exactly once per user scan and
#  overwritten if the user scans again, so the count is always 0, 1, or 2 —
#  never accumulates across reruns.
# ══════════════════════════════════════════════════════════════════════════════

# Initial demo metrics
if "base_stats" not in st.session_state:
    st.session_state["base_stats"] = {
        "total": 248,
        "threats": 67,
        "high": 23,
        "safe": 181,
    }

def _compute_stats() -> tuple[int, int, int, int]:
    base = st.session_state["base_stats"]

    total_scans = base["total"]
    threats_found = base["threats"]
    high_risk = base["high"]
    safe_count = base["safe"]

    # Count each scanner's latest result once
    for key in ("url_result", "email_result"):
        result = st.session_state.get(key)

        if result:
            total_scans += 1
            level, _, _ = _risk_level(result["score"], result["max"])

            if level == "High":
                threats_found += 1
                high_risk += 1
            elif level == "Medium":
                threats_found += 1
            else:
                safe_count += 1

    return total_scans, threats_found, high_risk, safe_count


# Calculate dashboard metrics
total_scans, threats_found, high_risk, safe_count = _compute_stats()


# ══════════════════════════════════════════════════════════════════════════════
#  LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pg-header">
    <div class="pg-logo">
        <div class="pg-logo-icon">🛡️</div>
        <div class="pg-logo-text">
            <div>PHISHGUARD</div>
            <span>Phishing Detection System</span>
        </div>
    </div>
    <div class="pg-status">
        <div class="pg-status-dot"></div>
        System Active
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card" style="--accent:#3b82f6">
        <div class="sc-icon">🔍</div>
        <div class="sc-label">Total Scans</div>
        <div class="sc-value">{total_scans}</div>
        <div class="sc-sub">This session</div>
    </div>
    <div class="stat-card" style="--accent:#f59e0b">
        <div class="sc-icon">⚠️</div>
        <div class="sc-label">Threats Detected</div>
        <div class="sc-value">{threats_found}</div>
        <div class="sc-sub">Medium + High risk</div>
    </div>
    <div class="stat-card" style="--accent:#ef4444">
        <div class="sc-icon">🚨</div>
        <div class="sc-label">High-Risk Threats</div>
        <div class="sc-value">{high_risk}</div>
        <div class="sc-sub">Immediate action needed</div>
    </div>
    <div class="stat-card" style="--accent:#10b981">
        <div class="sc-icon">✅</div>
        <div class="sc-label">Safe Results</div>
        <div class="sc-value">{safe_count}</div>
        <div class="sc-sub">Low risk verified</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Scanner selector buttons ──────────────────────────────────────────────────
if "active_scanner" not in st.session_state:
    st.session_state["active_scanner"] = None

col_url, col_email = st.columns(2, gap="large")
with col_url:
    if st.button("🔗  URL Scanner:\nAnalyse any URL for phishing indicators", key="select_url_scanner", use_container_width=True):
        st.session_state["active_scanner"] = "url"
        st.rerun()
with col_email:
    if st.button("📧  Email Scanner:\nDetect phishing patterns in email text", key="select_email_scanner", use_container_width=True):
        st.session_state["active_scanner"] = "email"
        st.rerun()

# ── Active scanner ────────────────────────────────────────────────────────────
if st.session_state["active_scanner"] is None:
    st.info("Select URL Scanner or Email Scanner to get started.")

elif st.session_state["active_scanner"] == "url":
    url_input = st.text_input(
        "URL input",
        placeholder="https://example.com/login",
        label_visibility="collapsed",
        key="url_input_field",
    )
    url_scan_btn = st.button("🔍  Scan URL", key="scan_url", use_container_width=True)

    if url_scan_btn:
        raw = url_input.strip()
        if not raw:
            st.warning("Please enter a URL before scanning.")
        else:
            # Prepend https:// if the user omitted a scheme
            if not raw.startswith(("http://", "https://")):
                raw = "https://" + raw
            score, warnings, weights = _score_url(raw)
            parsed = urlparse(raw)
            # Store result in session_state — overwrites any previous URL scan.
            # _compute_stats() reads this key on every rerun so the dashboard
            # updates automatically without an extra counter variable.
            st.session_state["url_result"] = {
                "score": score, "max": MAX_URL_SCORE,
                "warnings": warnings, "weights": weights,
                "parsed": parsed, "raw": raw,
            }
            st.rerun()

    if st.session_state.get("url_result"):
        r = st.session_state["url_result"]
        p = r["parsed"]
        bd = f"""
        <table class="breakdown-table">
            <tr><td>Scheme</td>     <td>{p.scheme or "—"}</td></tr>
            <tr><td>Domain</td>     <td>{p.netloc or "—"}</td></tr>
            <tr><td>Path</td>       <td>{p.path or "/"}</td></tr>
            <tr><td>Query</td>      <td>{p.query or "—"}</td></tr>
            <tr><td>Length</td>     <td>{len(r["raw"])} chars</td></tr>
        </table>
        """
        render_results(r["score"], r["max"], r["warnings"], URL_RECOMMENDATIONS, bd,
                       weights=r.get("weights"))

elif st.session_state["active_scanner"] == "email":
    email_input = st.text_area(
        "Email content",
        height=195,
        placeholder="Paste the full email here (subject + body)…",
        label_visibility="collapsed",
        key="email_input_field",
    )
    email_scan_btn = st.button("🔍  Scan Email", key="scan_email", use_container_width=True)

    if email_scan_btn:
        raw_email = email_input.strip()
        if not raw_email:
            st.warning("Please paste email content before scanning.")
        elif len(raw_email) < 20:
            st.warning("Email text is too short — please paste the full email body.")
        else:
            score, warnings, weights = _score_email(raw_email)
            # Store result in session_state — overwrites any previous email scan.
            # _compute_stats() reads this key on every rerun so the dashboard
            # updates automatically without an extra counter variable.
            st.session_state["email_result"] = {
                "score": score, "max": MAX_EMAIL_SCORE,
                "warnings": warnings, "weights": weights, "raw": raw_email,
            }
            st.rerun()

    if st.session_state.get("email_result"):
        r = st.session_state["email_result"]
        word_count = len(r["raw"].split())
        link_count = len(re.findall(r'https?://', r["raw"], re.I))
        email_addrs = len(re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', r["raw"]))
        stats_html = f"""
        <table class="breakdown-table">
            <tr><td>Word Count</td>      <td>{word_count}</td></tr>
            <tr><td>URLs Found</td>      <td>{link_count}</td></tr>
            <tr><td>Email Addresses</td> <td>{email_addrs}</td></tr>
            <tr><td>Characters</td>      <td>{len(r["raw"])}</td></tr>
        </table>
        """
        render_results(r["score"], r["max"], r["warnings"], EMAIL_RECOMMENDATIONS, stats_html,
                       weights=r.get("weights"))


# ── Full-width Sample Data Table ──────────────────────────────────────────────

st.markdown('<div style="margin-top:1rem;"></div>', unsafe_allow_html=True)

gen_col, _ = st.columns([1, 3])

with gen_col:
    gen_btn = st.button(
        "📊 Generate Sample Data",
        key="gen_sample",
        use_container_width=True
    )

if gen_btn:
    st.session_state["sample_shown"] = True

if st.session_state.get("sample_shown"):
    render_sample_table()



# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">'
    'PhishGuard v2.0 &nbsp;·&nbsp; Built with Python &amp; Streamlit'
    ' &nbsp;·&nbsp; Rule-based heuristic analysis &nbsp;·&nbsp; For educational use only'
    '</div>',
    unsafe_allow_html=True,
)
