"""
Prosus — Event Data & Consent Compliance Tool (Streamlit)

For HR, Talent Acquisition & Comms. Walks the user through their event and the
data they collect, flags special-category (GDPR Art. 9) data, and generates
ready-to-paste consent checkboxes for the registration form.

AUDIT: every time a team generates templates, a full row is written to
`audit_log.csv` (and to a Google Sheet if configured) so usage can be reviewed.

Run:
    pip install streamlit pandas
    # optional, for Google Sheets logging:
    pip install gspread oauth2client
    streamlit run app.py
"""

import os
from datetime import datetime

import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PRIVACY_URL = "https://www.prosus.com/site-services/privacy"
AUDIT_FILE = "audit_log.csv"

AUDIT_COLUMNS = [
    "Timestamp", "Team", "Event Name", "Event Type", "Format",
    "Standard Data", "Sensitive Data", "Explicit Consent Required",
    "Photography", "Marketing", "Third-Party Sharing",
    "Purpose", "Retention", "Privacy Contact", "Needs Review",
]

# Google Sheets integration (optional — falls back to CSV if not configured)
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SHEET_NAME = 'Prosus Event Consent Audit'  # name of your Google Sheet


def send_to_google_sheets(row_dict):
    """Append one audit row to Google Sheets. Returns True on success."""
    if not GOOGLE_SHEETS_AVAILABLE:
        return False
    try:
        if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            import json
            info = json.loads(st.secrets["gcp_service_account"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(info, SCOPES)
        else:
            service_account_file = 'service-account.json'
            if not os.path.exists(service_account_file):
                return False
            creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        # write a header row once if the sheet is empty
        if not sheet.get_all_values():
            sheet.append_row(AUDIT_COLUMNS)
        sheet.append_row([str(row_dict.get(c, "")) for c in AUDIT_COLUMNS])
        return True
    except Exception:
        return False  # silently fall back to CSV


def log_submission(row_dict):
    """Write one audit row to Google Sheets (if available) and always to CSV."""
    sheets_ok = send_to_google_sheets(row_dict)
    df = pd.DataFrame([row_dict], columns=AUDIT_COLUMNS)
    df.to_csv(AUDIT_FILE, mode='a', header=not os.path.isfile(AUDIT_FILE), index=False)
    return sheets_ok


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
STANDARD = [
    ("name", "Full name", True),
    ("email", "Email address", True),
    ("phone", "Phone number", False),
    ("job", "Job title & company", False),
    ("profile", "LinkedIn / professional profile", False),
    ("rsvp", "RSVP / attendance", False),
    ("cv", "CV / résumé", False),
]

# special-category (Art. 9) data that triggers explicit consent
SENSITIVE = [
    ("health", "Health / medical information"),
    ("accessibility", "Accessibility requirements"),
    ("dietary", "Dietary requirements / allergies"),
    ("ethnic", "Racial or ethnic origin"),
    ("religion", "Religious beliefs"),
    ("rtw", "Right-to-work / ID documents"),
    ("biometric", "Biometric data"),
    ("other_sensitive", "Other sensitive information"),
]

# media items handled via a photography/recording notice + opt-out
MEDIA = [
    ("photos", "Photographs / video of attendees"),
    ("audio", "Audio recording of attendees"),
]

PURPOSE_SUGGEST = {
    "Recruitment / careers event": "consider you for roles at Prosus and manage your participation in this event",
    "Conference": "manage your registration and participation in this conference",
    "Internal / culture event": "organise your participation in this internal event",
    "Networking / social": "manage your registration and participation in this networking event",
}

RETENTION_OPTIONS = [
    "until shortly after the event",
    "for up to 6 months",
    "for up to 12 months",
    "in line with the Prosus Privacy Policy",
]


def human_list(names):
    names = [n.lower() for n in names]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + " and " + names[-1]


def assess(answers):
    """Derive everything we need for templates + audit from the raw answers."""
    sel = answers.get("data", {})
    std_labels = [lbl for key, lbl, _ in STANDARD if sel.get(key)]
    sens_labels = [lbl for key, lbl in SENSITIVE if sel.get(key)]
    media_keys = [key for key, _ in MEDIA if sel.get(key)]
    return {
        "standard": std_labels,
        "sensitive": sens_labels,
        "media_keys": media_keys,
        "explicit_required": len(sens_labels) > 0,
        "photography": len(media_keys) > 0,
        "marketing": bool(sel.get("marketing")),
        "thirdparty": bool(sel.get("thirdparty")),
    }


# ---------------------------------------------------------------------------
# Page setup + styling (Prosus Congress Blue)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Prosus Event Data & Consent Tool", page_icon="🔒", layout="wide")

st.markdown("""
<style>
    /* Global Base Page Changes */
    .stApp { background: linear-gradient(135deg, #eef4fb 0%, #ffffff 60%); }
    
    /* Font rules safely ignoring font-icon wrappers */
    body, .stApp, h1, h2, h3, h4, h5, h6, p, span:not([class*="icon"]), label, li {
        font-family: 'Aptos', 'Inter', 'Segoe UI', sans-serif !important;
        color: #14141f;
    }
    h1 { color: #00427F !important; font-weight: 800; }
    
    /* Buttons */
    .stButton>button {
        width: 100%; background: #00427F; color: #ffffff !important;
        height: 3.2rem; font-size: 16px; font-weight: 700; border-radius: 12px;
        border: none; box-shadow: 0 4px 15px rgba(0, 66, 127, .25); transition: all .25s;
    }
    .stButton>button:hover { background: #003666; transform: translateY(-1px); }
    .stTextArea textarea, .stTextInput input { background: #fff !important; color: #14141f !important; }
    
    /* ---- FIXED: Dropdown Menu Elements ---- */
    .stSelectbox div[role="combobox"], 
    .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #14141f !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #ffffff !important;
        color: #14141f !important;
    }
    div[data-baseweb="popover"] li {
        background-color: #ffffff !important;
        color: #14141f !important;
        border-bottom: 1px solid rgba(20,20,31,.08) !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #eef4fb !important;
        color: #00427F !important;
    }
    select, option { background-color: #ffffff !important; color: #14141f !important; }
    
    /* Layout Elements */
    .stProgress > div > div { background-color: #00427F !important; }
    .block-head {
        background: #00427F; color: #fff !important; padding: 10px 16px;
        border-radius: 10px; margin: 22px 0 8px 0; font-weight: 700;
    }
    .block-head.opt { background: #
