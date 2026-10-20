# 🛡️ PhishGuard — Phishing Detection System

A real-time, rule-based phishing detection web application that analyses URLs and email body text for known phishing indicators. Built with Python and Streamlit — no ML, no API keys, fully offline.

---

## Features

- **URL Scanner** — analyses any URL across 14 detection rules (IP abuse, suspicious TLDs, URL shorteners, punycode, subdomain spoofing, and more)
- **Email Scanner** — analyses email body text across 13 detection rules (urgency language, credential requests, lottery scams, misspelled brands, crypto requests, and more)
- **Risk Scoring** — additive weighted scoring system; every triggered rule contributes points toward a final risk score
- **3-Tier Risk Classification** — Low / Medium / High verdicts with colour-coded meters and alert banners
- **Explainable Results** — every flagged indicator includes a plain-English explanation of *why* it's suspicious
- **Safety Recommendations** — tier-specific action guidance for each scan result
- **Dashboard Stats** — live KPI cards tracking total scans, threats detected, high-risk counts, and safe results
- **Sample Data Table** — 20 pre-labelled scan records with an interactive Plotly risk distribution chart
- **Dark Theme UI** — custom CSS with a midnight-blue, professional cybersecurity aesthetic

---

## Tech Stack

| Component        | Library / Tool              |
|------------------|-----------------------------|
| Web UI           | [Streamlit](https://streamlit.io) |
| Detection Engine | Python stdlib (`re`, `urllib.parse`) |
| Data Table       | Pandas + `st.dataframe`     |
| Charts           | Plotly Express              |
| Styling          | Inline CSS via `st.markdown` |

---

## Installation

**Requirements:** Python 3.10 or later

1. Clone or download the repository:
   ```bash
   git clone <your-repo-url>
   cd phishguard
   ```

2. Install dependencies:
   ```bash
   pip install streamlit pandas plotly
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and go to `http://localhost:8501`

---

## Usage

### Scanning a URL
1. Click **URL Scanner** on the main dashboard
2. Paste or type any URL into the input field (e.g. `http://paypal-secure-login.xyz/verify`)
3. Click **🔍 Scan URL**
4. Review the risk score meter, detected indicators, URL breakdown table, and safety recommendations

### Scanning an Email
1. Click **Email Scanner** on the main dashboard
2. Paste the full email subject + body text into the text area
3. Click **🔍 Scan Email**
4. Review the risk score, flagged indicators (with HIGH / MED severity pills), and recommendations

### Viewing Sample Data
- Click **📊 Generate Sample Data** to load a table of 20 pre-scored records and a risk distribution bar chart

---

## Detection Rules

### URL Rules (14 rules · max 245 pts)

| # | Rule | Weight |
|---|------|--------|
| 1 | Raw IP address in URL | 25 pts |
| 2 | Suspicious TLD (`.xyz`, `.tk`, `.ml`, `.cf` …) | 20 pts |
| 3 | Excessive subdomain depth (4+ levels) | 15 pts |
| 4 | `@` symbol in URL | 20 pts |
| 5 | Hyphenated login/secure/account keyword | 20 pts |
| 6 | URL length > 75 characters | 10 pts |
| 7 | URL shortener (bit.ly, tinyurl, t.co …) | 20 pts |
| 8 | HTTP instead of HTTPS | 15 pts |
| 9 | Double slashes in path | 10 pts |
| 10 | Non-standard port (`:8080`, `:3000` …) | 15 pts |
| 11 | Punycode / IDN homograph (`xn--`) | 25 pts |
| 12 | Sensitive keyword in path/query | 15 pts |
| 13 | Heavy percent-encoding (3+ sequences) | 10 pts |
| 14 | Brand name as subdomain of different TLD | 25 pts |

### Email Rules (13 rules · max 245 pts)

| # | Rule | Weight |
|---|------|--------|
| 1 | Urgency / threat language | 20 pts |
| 2 | Explicit credential request | 25 pts |
| 3 | Vague call-to-action anchor text | 15 pts |
| 4 | Lottery / prize scam language | 25 pts |
| 5 | Misspelled brand name | 20 pts |
| 6 | Generic impersonal greeting | 10 pts |
| 7 | Account closure / suspension threat | 20 pts |
| 8 | Instruction to open/download attachment | 20 pts |
| 9 | Money transfer / cryptocurrency request | 25 pts |
| 10 | Fake security alert language | 15 pts |
| 11 | Excessive ALL-CAPS or exclamation marks | 10 pts |
| 12 | Request to reply with sensitive information | 25 pts |
| 13 | Financial bait language | 15 pts |

---

## Risk Tiers

| Tier | Score % | Action |
|------|---------|--------|
| 🟢 **Low** | < 15% | No significant indicators; general hygiene reminders |
| 🟡 **Medium** | 15 – 35% | Treat with caution; do not enter credentials |
| 🔴 **High** | > 35% | Do NOT proceed; delete message; change passwords if visited |

---

## Project Structure

```
phishguard/
└── app.py          # Single-file application (UI + detection engine)
└── README.md       # This file
```

---

## Author

**Sreevidya Sojan**
