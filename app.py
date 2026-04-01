import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Privacy Compliance Check",
    page_icon="🔒",
    layout="wide"
)

# Prosus-inspired colors with visible text
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #e8f4f8 0%, #f0f8ff 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #e8f4f8 0%, #f0f8ff 100%);
    }
    
    /* FORCE ALL TEXT TO BE DARK AND VISIBLE */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #1a1a1a !important;
    }
    
    /* Form elements - dark text */
    .stRadio > label {
        color: #1a1a1a !important;
        font-weight: 600;
        font-size: 1.1em;
    }
    .stRadio div[role="radiogroup"] label {
        color: #1a1a1a !important;
        font-size: 1.05em;
    }
    .stRadio div[role="radiogroup"] label span {
        color: #1a1a1a !important;
    }
    
    .stCheckbox > label {
        color: #1a1a1a !important;
        font-weight: 600;
        font-size: 1.05em;
    }
    .stCheckbox label span {
        color: #1a1a1a !important;
    }
    
    .stTextArea > label {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    .stTextArea textarea {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* Code blocks - white text on dark background */
    .stCodeBlock, .stCodeBlock pre, .stCodeBlock code,
    div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code,
    div[data-testid="stCodeBlock"] * {
        color: #ffffff !important;
        background-color: #2d2d2d !important;
    }
    pre {
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #ffffff !important;
        background-color: #2d2d2d !important;
    }
    pre * {
        color: #ffffff !important;
    }
    code {
        color: #ffffff !important;
        background-color: #2d2d2d !important;
    }
    
    /* Buttons - Prosus blue/teal */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #0891b2, #06b6d4);
        color: white !important;
        height: 3.5rem;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(8, 145, 178, 0.3);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #0e7490, #0891b2);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(8, 145, 178, 0.4);
    }
    
    h1 {
        color: #0e7490 !important;
        text-align: center;
        font-weight: 700;
    }
    
    .template-header {
        background: linear-gradient(45deg, #0891b2, #06b6d4);
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0 10px 0;
        font-size: 1.2em;
        font-weight: bold;
    }
    
    .example-box {
        padding: 20px;
        background-color: #fffbeb;
        border: 2px solid #fbbf24;
        border-radius: 10px;
        margin: 15px 0;
    }
    .example-box * {
        color: #1a1a1a !important;
    }
    
    /* Info/warning/success boxes */
    .stAlert {
        color: #1a1a1a !important;
    }
    .stAlert * {
        color: #1a1a1a !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #0891b2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Header
st.title("🔒 Privacy Compliance Tool")
st.markdown("<div style='text-align: center; color: #1a1a1a; font-size: 1.2em; margin-bottom: 30px;'>Super simple - just 3 quick questions!</div>", unsafe_allow_html=True)

# Progress bar
progress = min(st.session_state.step / 3, 1.0)
st.progress(progress)
st.markdown(f"<div style='text-align: center; color: #1a1a1a; margin-bottom: 30px; font-size: 1.1em; font-weight: bold;'>Step {st.session_state.step} of 3</div>", unsafe_allow_html=True)

# STEP 1: What are you doing?
if st.session_state.step == 1:
    st.markdown("## Step 1: What are you doing?")
    st.markdown("### Pick one:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎪 Hosting/Co-hosting an Event", key="event_btn", use_container_width=True):
            st.session_state.answers['activity'] = "Event"
            st.session_state.step = 2
            st.rerun()
    
    with col2:
        if st.button("📧 Creating/Enhancing a Mailing List", key="mailing_btn", use_container_width=True):
            st.session_state.answers['activity'] = "Mailing List"
            st.session_state.step = 2
            st.rerun()

# STEP 2: What data are you collecting?
elif st.session_state.step == 2:
    st.markdown("## Step 2: What data are you collecting?")
    st.markdown("### Check all that apply:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        collect_email = st.checkbox("📧 Email addresses", key="email", value=True)
        collect_names = st.checkbox("👤 Names", key="names", value=True)
        collect_company = st.checkbox("🏢 Company/Job title", key="company")
    
    with col2:
        collect_dietary = st.checkbox("🍽️ Dietary requirements", key="dietary")
        collect_photos = st.checkbox("📸 Photos/videos", key="photos")
    
    st.markdown("---")
    st.markdown("### I'm also collecting:")
    other_data = st.text_area(
        "Type any other information you're collecting (optional):",
        placeholder="e.g., phone numbers, addresses, t-shirt sizes, etc.",
        height=100,
        key="other_data"
    )
    
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("← Back", key="step2_back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next →", key="step2_next"):
            st.session_state.answers['data_collection'] = {
                'email': collect_email,
                'names': collect_names,
                'company': collect_company,
                'dietary': collect_dietary,
                'photos': collect_photos,
                'other': other_data
            }
            st.session_state.step = 3
            st.rerun()

# STEP 3: Will you contact them later?
elif st.session_state.step == 3:
    st.markdown("## Step 3: Will you contact attendees after the event?")
    st.markdown("### (Add them to your mailing list for future emails)")
    
    contact_later = st.radio(
        "Will you send them emails about future events/updates?",
        ["No", "Yes"],
        key="contact_later"
    )
    
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("← Back", key="step3_back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Get My Templates! 🎉", key="step3_next"):
            st.session_state.answers['contact_later'] = contact_later
            st.session_state.step = 4
            st.rerun()

# STEP 4: Show Templates
elif st.session_state.step == 4:
    answers = st.session_state.answers
    data_collection = answers.get('data_collection', {})
    contact_later = answers.get('contact_later', 'No')
    
    st.markdown("# ✅ Here's What You Need!")
    st.success("Copy and paste these into your registration form:")
    
    st.markdown("---")
    
    # Template 1: Mandatory Privacy Checkbox (FIRST)
    st.markdown('<div class="template-header">✅ Required: Privacy Acceptance Checkbox</div>', unsafe_allow_html=True)
    st.markdown("**This checkbox MUST be on your form (and NOT pre-checked):**")
    
    template_privacy = "☐ I agree that by submitting this form, my personal data will be processed in accordance with the Prosus Privacy Policy."
    st.code(template_privacy, language=None)
    
    # Template 2: Privacy Policy Link (SECOND - below checkbox)
    st.markdown('<div class="template-header">📋 Required: Privacy Policy Link</div>', unsafe_allow_html=True)
    st.markdown("**Put this link below the checkbox above:**")
    
    privacy_link_text = "Privacy Policy: https://www.prosus.com/~/media/Files/P/prosus-corp-v2/privacy/prosus-privacy-statement.pdf"
    st.code(privacy_link_text, language=None)
    
    # Template 3: Mailing List Acceptance Checkbox (NEW)
    st.markdown('<div class="template-header">📬 Mailing List Acceptance Checkbox</div>', unsafe_allow_html=True)
    st.markdown("**If you're adding people to a mailing list, add this checkbox:**")
    
    template_mailing_list = "☐ I agree to be added to the Prosus mailing list and understand I can unsubscribe at any time."
    st.code(template_mailing_list, language=None)
    
    # Template 4: Optional Marketing Checkbox (if they said yes to contact later)
    if contact_later == "Yes":
        st.markdown('<div class="template-header">📧 Optional: Future Marketing Emails Checkbox</div>', unsafe_allow_html=True)
        st.markdown("**Add this SEPARATE checkbox for future marketing emails (NOT pre-checked):**")
        
        template_marketing = "☐ I would like to receive emails about future Prosus events and updates. I can unsubscribe anytime."
        st.code(template_marketing, language=None)
        
        st.warning("⚠️ **IMPORTANT:** This checkbox must be OPTIONAL and SEPARATE from the privacy acceptance!")
    
    # Additional templates based on data collection
    if data_collection.get('dietary'):
        st.markdown('<div class="template-header">🍽️ Dietary Information Checkbox</div>', unsafe_allow_html=True)
        st.markdown("**If collecting dietary info, add this checkbox:**")
        
        template_dietary = "☐ I consent to Prosus processing my dietary requirements for catering. This will be deleted 30 days after the event."
        st.code(template_dietary, language=None)
    
    if data_collection.get('photos'):
        st.markdown('<div class="template-header">📸 Photo/Video Consent Checkbox</div>', unsafe_allow_html=True)
        st.markdown("**If taking photos/videos, add this checkbox:**")
        
        template_photo = "☐ I consent to being photographed/filmed and to Prosus using these images in promotional materials."
        st.code(template_photo, language=None)
    
    # EXAMPLE OF HOW IT SHOULD LOOK
    st.markdown("---")
    st.markdown("# 📝 Example: How Your Form Should Look")
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("### Sample Registration Form")
    
    # Build example text properly
    example_parts = []
    example_parts.append("**Event Registration**")
    example_parts.append("")
    example_parts.append("Please fill out:")
    example_parts.append("- Name: _______________")
    example_parts.append("- Email: _______________")
    
    if data_collection.get('company'):
        example_parts.append("- Company/Job Title: _______________")
    if data_collection.get('dietary'):
        example_parts.append("- Dietary Requirements (optional): _______________")
    
    example_parts.append("")
    example_parts.append("**REQUIRED CONSENT:**")
    example_parts.append(template_privacy)
    example_parts.append("")
    example_parts.append(privacy_link_text)
    
    example_parts.append("")
    example_parts.append("**MAILING LIST:**")
    example_parts.append(template_mailing_list)
    
    if data_collection.get('dietary'):
        example_parts.append("")
        example_parts.append("**DIETARY CONSENT (if you filled dietary field):**")
        example_parts.append(template_dietary)
    
    if data_collection.get('photos'):
        example_parts.append("")
        example_parts.append("**PHOTO CONSENT:**")
        example_parts.append(template_photo)
    
    if contact_later == "Yes":
        example_parts.append("")
        example_parts.append("**OPTIONAL (for future marketing emails):**")
        example_parts.append(template_marketing)
    
    example_parts.append("")
    example_parts.append("[Submit Registration Button]")
    
    example_text = "\n".join(example_parts)
    
    st.code(example_text, language=None)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Reminders
    st.markdown("---")
    st.markdown("## ⚠️ Super Important Reminders:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **DO:**
        ✅ Show privacy policy link AFTER the checkbox
        ✅ Keep ALL checkboxes unchecked by default
        ✅ Make privacy acceptance mandatory
        ✅ Make marketing checkbox optional (if you have one)
        """)
    
    with col2:
        st.error("""
        **DON'T:**
        ❌ Pre-check ANY boxes
        ❌ Hide the privacy policy link
        ❌ Make people agree to marketing to register
        ❌ Send marketing emails to people who didn't check the box
        """)
    
    # Save submission
    other_text = data_collection.get('other', '').strip()
    data_collected_list = [k for k, v in data_collection.items() if v and k != 'other']
    if other_text:
        data_collected_list.append(f"Other: {other_text}")
    
    submission = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Activity": answers.get('activity', ''),
        "Data Collected": ', '.join(data_collected_list),
        "Contact Later": contact_later,
    }
    
    # Save to CSV
    df = pd.DataFrame([submission])
    file_exists = os.path.isfile("submissions.csv")
    df.to_csv("submissions.csv", mode='a', header=not file_exists, index=False)
    
    # Show notification
    st.markdown("---")
    st.info(f"""
    ✅ **Submission saved!** 
    
    Timestamp: {submission['Timestamp']}
    
    This response has been logged and saved to submissions.csv
    """)
    
    # Reset button
    if st.button("🔄 Start Over (New Form)", key="reset"):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #1a1a1a; padding: 20px;">
    <p><strong>Privacy Compliance Tool </strong> </p>
    <p>📧 Questions? Contact: privacy@prosus.com</p>
</div>
""", unsafe_allow_html=True)
