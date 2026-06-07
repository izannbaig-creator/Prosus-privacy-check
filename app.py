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
    
    /* Font rules safely avoiding global icon breaks */
    h1, h2, h3, h4, h5, h6, p, label, li {
        font-family: 'Aptos', 'Inter', 'Segoe UI', sans-serif !important;
        color: #14141f !important;
    }
    h1 { color: #00427F !important; font-weight: 800; }
    
    /* Global Form Button Settings */
    .stButton>button {
        width: 100%; background: #00427F; color: #ffffff !important;
        height: 3.2rem; font-size: 16px; font-weight: 700; border-radius: 12px;
        border: none; box-shadow: 0 4px 15px rgba(0, 66, 127, .25); transition: all .25s;
    }
    .stButton>button:hover { background: #003666; transform: translateY(-1px); }
    
    /* ---- FIXED: Input Fields & Controlled Output Textareas ---- */
    .stTextArea textarea, .stTextInput input { 
        background-color: #f5f7fb !important; 
        color: #14141f !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 14.5px !important;
    }
    
    /* Keep disabled read-only textareas completely opaque and clear */
    .stTextArea textarea:disabled {
        -webkit-text-fill-color: #14141f !important;
        color: #14141f !important;
        opacity: 1 !important;
        background-color: #f5f7fb !important;
        border: 1px solid #d8dce7 !important;
    }
    
    /* Style labels on output code text fields so they stand out clearly */
    .stTextArea label p {
        font-size: 0.85em !important;
        font-weight: 700 !important;
        color: #2f4b78 !important;
        margin-top: 6px !important;
    }
    
    /* ---- FIXED: Dropdown Menu Overlay Interventions ---- */
    .stSelectbox div[role="combobox"], 
    .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #14141f !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #ffffff !important;
        color: #14141f !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] li * {
        background-color: #ffffff !important;
        color: #14141f !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li:hover * {
        background-color: #eef4fb !important;
        color: #00427F !important;
    }
    select, option { background-color: #ffffff !important; color: #14141f !important; }
    
    /* Header Banners inside Output blocks */
    .stProgress > div > div { background-color: #00427F !important; }
    .block-head {
        background: #00427F; color: #fff !important; padding: 10px 16px;
        border-radius: 10px; margin: 24px 0 10px 0; font-weight: 700;
        font-family: 'Aptos', 'Inter', sans-serif;
    }
    .block-head.opt { background: #2f4b78; }

    .stAlert, .stAlert * { color: #14141f !important; }
</style>
""", unsafe_allow_html=True)

# session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "sheets_ok" not in st.session_state:
    st.session_state.sheets_ok = None

st.title("🔒 Prosus Event Data & Consent Tool")
st.markdown(
    "<div style='text-align:center;font-size:1.05em;margin-bottom:24px;'>"
    "For HR, Talent Acquisition &amp; Comms — tell us about your event and we'll "
    "generate the consent wording you need.</div>",
    unsafe_allow_html=True,
)

if st.session_state.step <= 3:
    st.progress(min(st.session_state.step / 3, 1.0))
    st.markdown(
        f"<div style='text-align:center;font-weight:700;margin-bottom:18px;'>Step {st.session_state.step} of 3</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# STEP 1 — Event basics
# ---------------------------------------------------------------------------
if st.session_state.step == 1:
    st.markdown("## Step 1: About your event")

    team = st.radio(
        "Which team is running this?",
        ["Human Resources", "Talent Acquisition", "Communications"],
        index=0, key="team",
    )
    event_name = st.text_input("Event name", placeholder="e.g. Prosus Tech Careers Day 2026", key="event_name")
    col1, col2 = st.columns(2)
    with col1:
        event_type = st.selectbox(
            "Event type",
            ["Recruitment / careers event", "Conference", "Internal / culture event", "Networking / social"],
            key="event_type",
        )
    with col2:
        event_format = st.selectbox("Format", ["In person", "Virtual", "Hybrid"], key="event_format")

    if st.button("Continue →", key="s1_next"):
        st.session_state.answers.update({
            "team": team, "event_name": event_name,
            "event_type": event_type, "event_format": event_format,
        })
        st.session_state.step = 2
        st.rerun()

# ---------------------------------------------------------------------------
# STEP 2 — What data are you collecting?
# ---------------------------------------------------------------------------
elif st.session_state.step == 2:
    st.markdown("## Step 2: What data are you collecting?")
    st.markdown("##### Tick everything your registration form will ask for.")

    sel = {}
    st.markdown("**Standard personal data**")
    c1, c2 = st.columns(2)
    for i, (key, label, default) in enumerate(STANDARD):
        with (c1 if i % 2 == 0 else c2):
            sel[key] = st.checkbox(label, value=default, key=f"std_{key}")

    st.markdown("**Special category / sensitive data — needs explicit consent**")
    c3, c4 = st.columns(2)
    for i, (key, label) in enumerate(SENSITIVE):
        with (c3 if i % 2 == 0 else c4):
            sel[key] = st.checkbox(label, key=f"sens_{key}")

    st.markdown("**Photography / recording**")
    c5, c6 = st.columns(2)
    with c5:
        sel["photos"] = st.checkbox("Photographs / video of attendees", key="media_photos")
    with c6:
        sel["audio"] = st.checkbox("Audio recording of attendees", key="media_audio")

    st.markdown("**Marketing & sharing**")
    c7, c8 = st.columns(2)
    with c7:
        sel["marketing"] = st.checkbox("Contact attendees later / marketing", key="opt_marketing")
    with c8:
        sel["thirdparty"] = st.checkbox("Share data with third parties", key="opt_thirdparty")

    # live, plain-language compliance signal
    tmp = assess({"data": sel})
    if tmp["explicit_required"]:
        st.warning(
            f"⚠️ **Explicit consent required.** You're collecting special category data "
            f"({human_list(tmp['sensitive'])}). GDPR needs a separate, required, opt-in checkbox."
        )
    else:
        st.info("✓ No special category data selected. A standard privacy notice + consent checkbox will be enough.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="s2_back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Continue →", key="s2_next"):
            st.session_state.answers["data"] = sel
            st.session_state.step = 3
            st.rerun()

# ---------------------------------------------------------------------------
# STEP 3 — Configure + (audit) generate
# ---------------------------------------------------------------------------
elif st.session_state.step == 3:
    st.markdown("## Step 3: Configure the notice")
    answers = st.session_state.answers
    default_purpose = PURPOSE_SUGGEST.get(answers.get("event_type", ""), "")

    purpose = st.text_area("Why are you collecting this data? (the purpose)", value=default_purpose, key="purpose")
    col1, col2 = st.columns(2)
    with col1:
        retention = st.selectbox("How long will you keep it?", RETENTION_OPTIONS, key="retention")
    with col2:
        contact = st.text_input("Privacy contact (for questions / withdrawal)", placeholder="e.g. privacy@prosus.com", key="contact")

    if assess(answers)["explicit_required"]:
        st.warning("Because you're collecting sensitive data, the explicit-consent checkbox must be unticked by default and kept separate from the general agreement.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="s3_back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Generate form →", key="s3_next"):
            answers.update({"purpose": purpose, "retention": retention, "contact": contact})
            d = assess(answers)
            # --- AUDIT: log this use once, at generation time ---
            row = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Team": answers.get("team", ""),
                "Event Name": answers.get("event_name", "") or "(unnamed)",
                "Event Type": answers.get("event_type", ""),
                "Format": answers.get("event_format", ""),
                "Standard Data": ", ".join(d["standard"]),
                "Sensitive Data": ", ".join(d["sensitive"]) or "—",
                "Explicit Consent Required": "YES" if d["explicit_required"] else "NO",
                "Photography": "YES" if d["photography"] else "NO",
                "Marketing": "YES" if d["marketing"] else "NO",
                "Third-Party Sharing": "YES" if d["thirdparty"] else "NO",
                "Purpose": (purpose or "").strip(),
                "Retention": retention,
                "Privacy Contact": (contact or "").strip(),
                "Needs Review": "YES" if (d["explicit_required"] or d["thirdparty"]) else "NO",
            }
            st.session_state.sheets_ok = log_submission(row)
            st.session_state.step = 4
            st.rerun()

# ---------------------------------------------------------------------------
# STEP 4 — Generated form / templates
# ---------------------------------------------------------------------------
elif st.session_state.step == 4:
    answers = st.session_state.answers
    d = assess(answers)
    purpose = (answers.get("purpose") or PURPOSE_SUGGEST.get(answers.get("event_type", ""), "[purpose]")).strip() or "[purpose]"
    retention = answers.get("retention", RETENTION_OPTIONS[0])
    contact = (answers.get("contact") or "").strip() or "[privacy contact email]"
    event_name = (answers.get("event_name") or "").strip() or "[event name]"

    st.markdown("# ✅ Your consent wording")
    if d["explicit_required"]:
        st.warning(
            f"This event collects special category data ({human_list(d['sensitive'])}). "
            "Use the explicit-consent checkbox below as-is: required, unticked by default, separate from the general agreement."
        )
    else:
        st.success("Copy the privacy notice and consent checkbox below into your registration form.")

    def block(title, body_text, html_snippet=None, optional=False):
        cls = "block-head opt" if optional else "block-head"
        st.markdown(f'<div class="{cls}">{title}</div>', unsafe_allow_html=True)
        
        # Plain Copy-Paste Box
        st.text_area("Plain text variant:", value=body_text, height=90, disabled=True, key=f"txt_{hash(body_text)}")
        
        # HTML Copy-Paste Box inside same container, utilizing layout clean labels
        if html_snippet:
            st.text_area("HTML code variant:", value=html_snippet, height=110, disabled=True, key=f"html_{hash(html_snippet)}")

    # 1. Privacy notice (always)
    block(
        "📋 Privacy notice (required)",
        f"Prosus collects this information to {purpose}. Prosus is the data controller and keeps your data "
        f"{retention}. You can access, correct or delete it at any time — see the Prosus Privacy Policy: {PRIVACY_URL}",
        html_snippet=f'<p>Prosus collects this information to {purpose}. Prosus is the data controller and keeps your '
                     f'data {retention}. You can access, correct or delete it at any time — see the '
                     f'<a href="{PRIVACY_URL}" target="_blank" rel="noopener">Prosus Privacy Policy</a>.</p>',
    )

    # 2. Standard consent checkbox (always)
    block(
        "✅ Consent checkbox (required)",
        "☐ I agree that by submitting this form, my personal data will be processed in accordance with the "
        "Prosus Privacy Policy.",
        html_snippet='<label>\n  <input type="checkbox" name="consent_privacy" required>\n'
                     f'  I agree that by submitting this form, my personal data will be processed in accordance with '
                     f'the <a href="{PRIVACY_URL}" target="_blank" rel="noopener">Prosus Privacy Policy</a>.\n</label>',
    )

    # 3. Explicit consent (only if sensitive)
    if d["explicit_required"]:
        block(
            "🔐 Explicit consent — sensitive data (required)",
            f"☐ I explicitly consent to Prosus processing the sensitive information I provide "
            f"({human_list(d['sensitive'])}) for this event. Providing it is voluntary and I can withdraw my consent "
            f"at any time by contacting {contact}.",
            html_snippet=f'<label>\n  <input type="checkbox" name="consent_sensitive" required>\n'
                         f'  I explicitly consent to Prosus processing the sensitive information I provide '
                         f'({human_list(d["sensitive"])}) for this event. Providing it is voluntary and I can '
                         f'withdraw my consent at any time by contacting {contact}.\n</label>',
        )
        st.caption("Keep this checkbox unticked by default and separate from the agreement above.")

    # 4. Photography / recording (opt-out, not required)
    if d["photography"]:
        if len(d["media_keys"]) == 2:
            medium = "photographed and/or recorded"
        elif "photos" in d["media_keys"]:
            medium = "photographed and/or filmed"
        else:
            medium = "audio recorded"
        block(
            "📸 Photography / recording (recommended)",
            f"This event may be {medium} by Prosus, and the material may be used in Prosus communications.\n\n"
            f"☐ I prefer not to be {medium}.",
            html_snippet=f'<p>This event may be {medium} by Prosus, and the material may be used in Prosus '
                         f'communications.</p>\n<label>\n  <input type="checkbox" name="photo_optout">\n'
                         f'  I prefer not to be {medium}.\n</label>',
            optional=True,
        )
        if d["marketing"]:
            st.caption("For external marketing use, collect a separate explicit opt-in rather than relying on this opt-out.")

    # 5. Marketing opt-in (optional)
    if d["marketing"]:
        block(
            "📬 Marketing consent (optional)",
            "☐ I'd like to hear from Prosus about future events and opportunities. (Optional — you can unsubscribe at any time.)",
            html_snippet='<label>\n  <input type="checkbox" name="marketing_optin">\n'
                         "  I'd like to hear from Prosus about future events and opportunities. (Optional — you can "
                         "unsubscribe at any time.)\n</label>",
            optional=True,
        )

    # 6. Third-party sharing (notice)
    if d["thirdparty"]:
        block(
            "🤝 Third-party sharing notice (required)",
            "Some of your data may be shared with partners who help run this event (for example [name the recipients]). "
            f"They may only use it for this event. See the Prosus Privacy Policy: {PRIVACY_URL}",
            html_snippet="<p>Some of your data may be shared with partners who help run this event (for example "
                         "[name the recipients]). They may only use it for this event. See the "
                         f'<a href="{PRIVACY_URL}" target="_blank" rel="noopener">Prosus Privacy Policy</a>.</p>',
        )

    # reminders
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.success("**DO**\n\n✅ Keep all consent boxes unticked by default\n\n✅ Make the privacy consent mandatory\n\n✅ Keep marketing & photography opt-outs optional\n\n✅ Show the Privacy Policy link by the checkbox")
    with c2:
        st.error("**DON'T**\n\n❌ Pre-tick any box\n\n❌ Force marketing consent to register\n\n❌ Bundle sensitive-data consent with the general agreement\n\n❌ Rely only on the browser — re-check consent server-side")

    st.caption("⚖️ Starting template, not legal advice. Have the Prosus privacy / legal team review before publishing.")

    if st.button("🔄 Start a new form", key="reset"):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.session_state.sheets_ok = None
        st.rerun()

# ---------------------------------------------------------------------------
# Sidebar — audit access (restrict this in deployment)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Audit log")
    if st.session_state.get("sheets_ok"):
        st.caption("✅ Last submission saved to Google Sheets + CSV")
    elif st.session_state.get("sheets_ok") is False:
        st.caption("💾 Last submission saved to local CSV")
    with st.sidebar.expander("View / download log"):
        if os.path.isfile(AUDIT_FILE):
            log_df = pd.read_csv(AUDIT_FILE)
            st.caption(f"{len(log_df)} submissions logged")
            st.dataframe(log_df.tail(15), use_container_width=True)
            st.download_button(
                "Download audit_log.csv",
                log_df.to_csv(index=False).encode("utf-8"),
                file_name="audit_log.csv",
                mime="text/csv",
            )
        else:
            st.caption("No submissions logged yet.")
    st.caption("Restrict sidebar/log access to admins before deploying.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    f"<div style='text-align:center;padding:16px;'>"
    f"<strong>Prosus Event Data &amp; Consent Tool</strong><br>"
    f"Prosus is the data controller · <a href='{PRIVACY_URL}' target='_blank'>Privacy Policy</a></div>",
    unsafe_allow_html=True,
)
