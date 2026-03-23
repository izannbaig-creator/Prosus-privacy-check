
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

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3rem;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 20px 0;
    }
    .warning-box {
        padding: 20px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 20px 0;
    }
    .danger-box {
        padding: 20px;
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        margin: 20px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        border-radius: 5px;
        margin: 15px 0;
    }
    .template-box {
        padding: 15px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        margin: 10px 0;
        font-family: monospace;
        font-size: 0.9em;
    }
    h1 {
        color: #1f1f1f;
        font-weight: 700;
    }
    .sidebar-icon {
        font-size: 1.2em;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🔒 Privacy Compliance Check")
st.markdown("**Required before launching any event, campaign, or registration form**")
st.markdown("---")

# Enhanced Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x60/4CAF50/FFFFFF?text=PROSUS", width=200)
    
    st.markdown("### 📖 About This Tool")
    st.info("This automated tool helps ensure your campaigns comply with GDPR and data protection regulations before launch.")
    
    st.markdown("---")
    st.markdown("### ✅ When to Use This Tool")
    st.markdown("""
    **Always run this check before:**
    
    🎫 **Event Registrations**
    - Conferences & summits
    - Webinars & workshops
    - Networking events
    - Hackathons
    
    📧 **Email Campaigns**
    - Newsletter signups
    - Marketing campaigns
    - Event follow-ups
    - Lead generation
    
    📝 **Data Collection Forms**
    - Contact forms
    - Survey forms
    - Application forms
    - Feedback forms
    
    🤝 **Partner Collaborations**
    - Co-hosted events
    - Sponsor activations
    - Third-party integrations
    - Data sharing agreements
    
    📸 **Events with Media**
    - Photographed events
    - Recorded sessions
    - Live streams
    - Video content
    
    🌍 **Cross-border Activities**
    - International events
    - Global campaigns
    - Multi-region data collection
    
    👥 **Special Audiences**
    - Children/minors (<16)
    - Sensitive data collection
    - Health-related events
    """)
    
    st.markdown("---")
    st.markdown("### 🆘 Need Help?")
    st.markdown("📧 **Email:** privacy@prosus.com")
    st.markdown("💬 **Slack:** #ask-privacy")
    st.markdown("📚 **[Privacy Portal](https://www.prosus.com/privacy)**")
    
    st.markdown("---")
    st.markdown("### 🚨 Common Red Flags")
    st.error("""
    **Immediate escalation needed:**
    - ❌ Pre-ticked consent boxes
    - ❌ No privacy policy link
    - ❌ Sharing with sponsors (no consent)
    - ❌ Bundled consent
    - ❌ No unsubscribe option
    """)

# Main Form
st.markdown("## 📋 Campaign Assessment")

# Add Copy-Paste Templates Section at the top
with st.expander("📝 COPY-PASTE CONSENT TEMPLATES (Click to expand)", expanded=False):
    st.markdown("### Ready-to-Use Consent Text for Your Forms")
    st.info("⚡ **Quick Tip:** Click the copy icon on the right side of each text box to copy instantly!")
    
    st.markdown("---")
    
    # 1. MANDATORY PRIVACY POLICY ACCEPTANCE
    st.markdown("#### 1️⃣ Privacy Policy Acceptance Checkbox (MANDATORY)")
    st.warning("⚠️ This checkbox is REQUIRED and must NOT be pre-ticked")
    
    st.markdown("**Option A - Standard Event Registration:**")
    template_1a = """☐ I agree that by registering for this event, my personal data will be processed in accordance with the Prosus Privacy Policy."""
    st.code(template_1a, language=None)
    
    st.markdown("**Option B - General Form/Signup:**")
    template_1b = """☐ I agree that by submitting this form, my personal data will be processed in accordance with the Prosus Privacy Policy."""
    st.code(template_1b, language=None)
    
    st.markdown("**Option C - With Link Included:**")
    template_1c = """☐ I have read and agree to the Prosus Privacy Policy (https://www.prosus.com/privacy) and consent to the processing of my personal data as described therein."""
    st.code(template_1c, language=None)
    
    st.markdown("---")
    
    # 2. MARKETING OPT-IN
    st.markdown("#### 2️⃣ Marketing Communications Opt-In (OPTIONAL)")
    st.success("✅ This checkbox is OPTIONAL and must NOT be pre-ticked")
    
    st.markdown("**Option A - Future Events:**")
    template_2a = """☐ I would like to receive information about future Prosus events and opportunities."""
    st.code(template_2a, language=None)
    
    st.markdown("**Option B - Marketing Communications:**")
    template_2b = """☐ I consent to receiving marketing communications from Prosus, including newsletters, event invitations, and promotional materials. I understand I can unsubscribe at any time."""
    st.code(template_2b, language=None)
    
    st.markdown("**Option C - Specific Event Series:**")
    template_2c = """☐ I would like to receive updates about similar Prosus events and programs. You can unsubscribe at any time using the link in our emails."""
    st.code(template_2c, language=None)
    
    st.markdown("---")
    
    # 3. SENSITIVE DATA CONSENT
    st.markdown("#### 3️⃣ Sensitive Data Processing (DIETARY/ACCESSIBILITY)")
    st.error("🚨 Required when collecting health/dietary information")
    
    st.markdown("**Option A - Dietary Requirements:**")
    template_3a = """☐ I consent to Prosus processing my dietary requirements/restrictions for the purpose of providing appropriate catering at this event. This information will be deleted within 30 days after the event."""
    st.code(template_3a, language=None)
    
    st.markdown("**Option B - Accessibility Needs:**")
    template_3b = """☐ I consent to Prosus processing information about my accessibility needs to ensure appropriate accommodations are provided. This information will be handled confidentially and deleted after the event."""
    st.code(template_3b, language=None)
    
    st.markdown("**Option C - Combined Dietary & Accessibility:**")
    template_3c = """☐ I consent to Prosus processing my dietary requirements and/or accessibility needs for the sole purpose of ensuring appropriate arrangements at this event. This sensitive information will be kept confidential and deleted within 30 days after the event."""
    st.code(template_3c, language=None)
    
    st.markdown("---")
    
    # 4. PHOTO/VIDEO CONSENT
    st.markdown("#### 4️⃣ Photography & Video Recording Consent")
    st.error("🚨 Required for photographed/recorded events")
    
    st.markdown("**Option A - Event Photography (Opt-In):**")
    template_4a = """☐ I consent to being photographed/filmed during this event and to Prosus using these images in promotional materials, social media, and marketing communications."""
    st.code(template_4a, language=None)
    
    st.markdown("**Option B - Event Photography (Opt-Out):**")
    template_4b = """☐ I do NOT wish to be photographed or filmed during this event. I understand I can request a special badge/lanyard to indicate this preference."""
    st.code(template_4b, language=None)
    
    st.markdown("**Option C - Virtual Event Recording:**")
    template_4c = """☐ I understand this virtual event will be recorded and consent to my participation (including video, audio, and chat messages) being recorded. The recording may be shared with registered attendees and used for Prosus marketing purposes."""
    st.code(template_4c, language=None)
    
    st.markdown("---")
    
    # 5. SPONSOR/PARTNER DATA SHARING
    st.markdown("#### 5️⃣ Sponsor/Partner Data Sharing Consent")
    st.error("🚨 EXPLICIT opt-in required before sharing with sponsors")
    
    st.markdown("**Option A - Event Sponsors:**")
    template_5a = """☐ I consent to my contact information (name, email, company, job title) being shared with event sponsors and partners for follow-up communications about their products and services."""
    st.code(template_5a, language=None)
    
    st.markdown("**Option B - Specific Sponsor List:**")
    template_5b = """☐ I consent to my contact information being shared with the following event sponsors: [SPONSOR NAME 1], [SPONSOR NAME 2], [SPONSOR NAME 3]. I understand they may contact me about their offerings."""
    st.code(template_5b, language=None)
    
    st.markdown("**Option C - Exhibition/Networking:**")
    template_5c = """☐ I consent to event exhibitors and sponsors scanning my badge/collecting my contact information during the event for follow-up communications."""
    st.code(template_5c, language=None)
    
    st.markdown("---")
    
    # 6. CHILDREN'S DATA / PARENTAL CONSENT
    st.markdown("#### 6️⃣ Parental Consent (for participants under 16)")
    st.error("🚨 Required when collecting data from minors")
    
    st.markdown("**Option A - Parental Consent Statement:**")
    template_6a = """☐ I am the parent/legal guardian of the participant and consent to Prosus collecting and processing their personal data for this event in accordance with the Prosus Privacy Policy."""
    st.code(template_6a, language=None)
    
    st.markdown("**Option B - Age Verification + Parent Contact:**")
    template_6b = """☐ I confirm I am 16 years or older, OR my parent/guardian has reviewed and agreed to the Prosus Privacy Policy on my behalf. Parent/Guardian Email: _______________"""
    st.code(template_6b, language=None)
    
    st.markdown("---")
    
    # 7. COMPLETE FORM EXAMPLES
    st.markdown("#### 📦 Complete Form Examples (All Checkboxes Together)")
    
    st.markdown("**Scenario 1: Standard Event (No Sensitive Data)**")
    complete_1 = """Registration Form - Prosus AI Summit 2024

Please complete the following:
- Name: _______________
- Email: _______________
- Company: _______________
- Job Title: _______________

REQUIRED CONSENT:
☐ I agree that by registering for this event, my personal data will be processed in accordance with the Prosus Privacy Policy (https://www.prosus.com/privacy).

OPTIONAL:
☐ I would like to receive information about future Prosus events and opportunities. You can unsubscribe at any time.

[Submit Registration]"""
    st.code(complete_1, language=None)
    
    st.markdown("**Scenario 2: Event with Catering + Photos**")
    complete_2 = """Registration Form - Prosus Tech Workshop 2024

Please complete the following:
- Name: _______________
- Email: _______________
- Dietary Requirements (optional): _______________

REQUIRED CONSENT:
☐ I agree that by registering for this event, my personal data will be processed in accordance with the Prosus Privacy Policy (https://www.prosus.com/privacy).

SENSITIVE DATA CONSENT (if dietary requirements provided):
☐ I consent to Prosus processing my dietary requirements for catering purposes. This information will be deleted within 30 days after the event.

PHOTOGRAPHY CONSENT:
☐ I consent to being photographed during this event and to Prosus using these images in promotional materials.
   OR
☐ I do NOT wish to be photographed. I will receive a special badge indicating this preference.

OPTIONAL MARKETING:
☐ I would like to receive information about future Prosus events.

[Submit Registration]"""
    st.code(complete_2, language=None)
    
    st.markdown("**Scenario 3: Event with Sponsors**")
    complete_3 = """Registration Form - Prosus Innovation Conference 2024

Please complete the following:
- Name: _______________
- Email: _______________
- Company: _______________

REQUIRED CONSENT:
☐ I agree that by registering for this event, my personal data will be processed in accordance with the Prosus Privacy Policy (https://www.prosus.com/privacy).

SPONSOR DATA SHARING (OPTIONAL):
☐ I consent to my contact information being shared with event sponsors for follow-up communications about their products and services.

   Event Sponsors: [Company A], [Company B], [Company C]

OPTIONAL MARKETING:
☐ I would like to receive information about future Prosus events.

[Submit Registration]"""
    st.code(complete_3, language=None)
    
    st.markdown("---")
    
    # IMPORTANT REMINDERS
    st.markdown("### ⚠️ IMPORTANT REMINDERS")
    st.error("""
    **DO:**
    - ✅ Place privacy policy link BEFORE data collection
    - ✅ Keep checkboxes UNCHECKED by default
    - ✅ Make privacy acceptance MANDATORY
    - ✅ Make marketing opt-ins OPTIONAL
    - ✅ Use clear, simple language
    - ✅ Allow easy opt-out from marketing
    
    **DON'T:**
    - ❌ Pre-tick any checkboxes
    - ❌ Bundle privacy acceptance with marketing consent
    - ❌ Hide privacy policy in fine print
    - ❌ Make registration conditional on marketing opt-in
    - ❌ Use vague language like "we may use your data"
    - ❌ Collect data before showing consent options
    """)
    
    st.success("""
    💡 **Pro Tip:** After copying text, adjust:
    - Event name
    - Your actual privacy policy URL
    - Specific sponsor names
    - Data retention periods
    """)

# Continue with the rest of the form (same as before)
with st.form("privacy_check_form"):
    
    # Section 1: Basic Information
    st.markdown("### 👤 Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("📛 Your Name *", placeholder="John Doe")
        event_name = st.text_input("🎯 Campaign/Event Name *", placeholder="AI Summit 2024")
    
    with col2:
        launch_date = st.date_input("📅 Launch Date *")
        event_type = st.selectbox(
            "🎪 Event Type *",
            ["Select...", "Conference/Summit", "Webinar/Workshop", "Networking Event", 
             "Marketing Campaign", "Email Newsletter", "Partner Event", "Recruitment/Careers", "Other"]
        )
    
    st.markdown("---")
    
    # Section 2: Data Collection
    st.markdown("### 📊 Data Collection Details")
    
    col3, col4 = st.columns(2)
    
    with col3:
        collection_point = st.selectbox(
            "📍 Where Are You Collecting Data? *",
            ["Select...", "Website Form", "Event Registration Page", "Email Signup", 
             "Landing Page", "Social Media", "Third-party Platform", "Other"]
        )
        
        platform = st.selectbox(
            "🛠️ Platform You're Using *",
            ["Select...", "Luma", "Eventbrite", "Mailchimp", "Lever", "Google Forms", 
             "Typeform", "HubSpot", "Zoom", "Other"]
        )
    
    with col4:
        data_type = st.selectbox(
            "💾 What Data Are You Collecting? *",
            ["Select...", 
             "Email only", 
             "Email + Name", 
             "Email + Name + Job Title/Company",
             "Sensitive data (see below for options)"]
        )
        
        is_virtual = st.radio(
            "💻 Is this a virtual/online event?",
            ["No", "Yes"]
        )
    
    # Conditional: Sensitive Data Details
    sensitive_data_types = []
    explicit_consent_sensitive = None
    if data_type == "Sensitive data (see below for options)":
        st.markdown("#### 🔐 Sensitive Data Specifications")
        st.info("⚠️ Sensitive data requires explicit consent and special handling. See templates above ⬆️")
        
        sensitive_data_types = st.multiselect(
            "Select all types of sensitive data you're collecting:",
            [
                "🍽️ Dietary requirements/restrictions",
                "🏥 Health information/accessibility needs",
                "📸 Photos/videos of attendees",
                "👶 Children's data (under 16)",
                "🏛️ Government ID/passport information",
                "💳 Financial/payment information",
                "🎓 Educational records",
                "Other sensitive personal data"
            ]
        )
        
        explicit_consent_sensitive = st.radio(
            "Do you have EXPLICIT consent language specifically for this sensitive data?",
            ["Not sure", "No", "Yes, we have specific consent text"],
            help="Check the templates above for examples. Generic privacy policy acceptance is NOT sufficient."
        )
    
    st.markdown("---")
    
    # Section 3: Privacy Compliance Elements
    st.markdown("### 🔍 Privacy Compliance Elements")
    
    col5, col6 = st.columns(2)
    
    with col5:
        privacy_link = st.radio(
            "🔗 Is there a visible link to Prosus Privacy Policy on your form/page? *",
            ["Yes, clearly visible", "Yes, but in footer/small text", "No", "Not sure"],
            help="Privacy policy must be visible BEFORE data collection"
        )
        
        consent_checkboxes = st.multiselect(
            "✅ Which consent checkboxes do you have? (Select all that apply) *",
            [
                "✓ Privacy Policy acceptance (mandatory, NOT pre-ticked)",
                "✓ Marketing emails opt-in (optional, NOT pre-ticked)",
                "✓ Event photo/recording consent",
                "✓ Third-party sharing consent (sponsors/partners)",
                "✓ Sensitive data processing consent",
                "None of these",
                "Not sure"
            ],
            help="See templates section above for exact wording"
        )
    
    with col6:
        preticked = st.radio(
            "⚠️ Does your form have any PRE-TICKED checkboxes? *",
            ["No, all boxes are unchecked by default", "Yes, some boxes are pre-ticked", "Not sure"],
            help="Pre-ticked consent boxes violate GDPR"
        )
        
        bundled_consent = st.radio(
            "🔀 Is consent bundled? (Registration requires agreeing to marketing)",
            ["No, consents are separate", "Yes, must agree to everything to register", "Not sure"],
            help="Consent must be freely given, not a condition of registration"
        )
    
    st.markdown("---")
    
    # Section 4: Data Sharing & Partners
    st.markdown("### 🤝 Data Sharing & Third Parties")
    
    col7, col8 = st.columns(2)
    
    with col7:
        share_sponsors = st.radio(
            "🎁 Will you share attendee data with sponsors or partners? *",
            ["No", "Yes", "Not sure"],
            help="See Template 5 above for sponsor consent wording"
        )
    
    with col8:
        cookies_tracking = st.radio(
            "🍪 Are you using cookies or tracking pixels?",
            ["No", "Yes, analytics only", "Yes, marketing/tracking", "Not sure"]
        )
    
    # Conditional: Sponsor/Partner Sharing Details
    sponsor_dpa = None
    sponsor_count = None
    sponsor_consent = None
    if share_sponsors == "Yes":
        st.markdown("#### 🚨 Sponsor Data Sharing Details")
        st.error("⚠️ Sharing data with sponsors requires EXPLICIT opt-in consent (see Template 5 above)")
        
        col9, col10 = st.columns(2)
        with col9:
            sponsor_count = st.number_input(
                "How many sponsors/partners will receive data?",
                min_value=1,
                max_value=50,
                value=1
            )
            
            sponsor_consent = st.radio(
                "Do attendees have EXPLICIT opt-in for sponsor data sharing?",
                ["No/Not sure", "Yes, separate checkbox for sponsor sharing"],
                help="Generic consent is not sufficient - must be explicit opt-in"
            )
        
        with col10:
            sponsor_dpa = st.radio(
                "Is there a signed Data Processing Agreement (DPA) with sponsors?",
                ["No/Not sure", "Yes, DPA signed", "We are independent controllers"],
                help="Required for GDPR compliance"
            )
    
    # Conditional: Cookie Consent
    cookie_banner = None
    if cookies_tracking in ["Yes, analytics only", "Yes, marketing/tracking"]:
        st.markdown("#### 🍪 Cookie Compliance")
        col11, col12 = st.columns(2)
        
        with col11:
            cookie_banner = st.radio(
                "Do you have a cookie consent banner?",
                ["No", "Yes, with accept/reject options", "Yes, but only 'Accept'"],
                help="Marketing cookies require explicit consent"
            )
        
        with col12:
            cookie_categories = st.multiselect(
                "What cookie categories do you use?",
                ["Strictly necessary (always allowed)",
                 "Analytics/Performance (requires consent)",
                 "Marketing/Tracking/Targeting (requires consent)"]
            )
    
    st.markdown("---")
    
    # Section 5: Virtual Event Specific
    recording_notice = None
    recording_consent = None
    chat_logs = None
    if is_virtual == "Yes":
        st.markdown("### 🎥 Virtual Event Specific Questions")
        st.info("💡 See Template 4C above for virtual event recording consent")
        
        col13, col14 = st.columns(2)
        
        with col13:
            recording_notice = st.radio(
                "Will the event be recorded?",
                ["No", "Yes, with clear notice to participants", "Yes, but no notice"],
                help="Participants must be informed if recording (see Template 4C)"
            )
            
            chat_logs = st.radio(
                "Will chat logs/Q&A be saved?",
                ["No", "Yes", "Not sure"]
            )
        
        with col14:
            if recording_notice in ["Yes, with clear notice to participants", "Yes, but no notice"]:
                recording_consent = st.radio(
                    "Do participants consent to being recorded?",
                    ["No explicit consent", "Yes, consent obtained at registration", 
                     "Yes, consent given at event start"],
                    help="Recording consent should be obtained (see Template 4C)"
                )
    
    st.markdown("---")
    
    # Section 6: Platform & Cross-border
    st.markdown("### 🌍 Platform & Data Location")
    
    col15, col16 = st.columns(2)
    
    with col15:
        platform_dpa = None
        if platform == "Other":
            other_platform_name = st.text_input(
                "🔧 Specify platform name:",
                placeholder="e.g., Custom CRM, Internal tool"
            )
            
            platform_dpa = st.radio(
                "Is there a signed Data Processing Agreement with this platform?",
                ["No/Not sure", "Yes, DPA signed", "Not applicable (internal tool)"]
            )
        
        data_location = st.selectbox(
            "📍 Where are the platform servers located?",
            ["Not sure", "European Union", "United States", "United Kingdom", 
             "Other country", "Multiple locations"]
        )
    
    with col16:
        marketing_emails = st.radio(
            "📧 Will you send marketing emails to attendees later? *",
            ["No", "Yes, to those who opted in", "Yes, to all attendees", "Maybe/Not sure"],
            help="See Template 2 above for marketing opt-in wording"
        )
        
        unsubscribe_link = None
        if marketing_emails in ["Yes, to those who opted in", "Yes, to all attendees", "Maybe/Not sure"]:
            unsubscribe_link = st.radio(
                "Will emails include an unsubscribe link?",
                ["Yes, in every email", "No/Not sure"],
                help="Required by GDPR and CAN-SPAM"
            )
    
    st.markdown("---")
    
    # Section 7: Special Cases
    with st.expander("🔬 Advanced / Special Cases (Optional)"):
        st.markdown("Only fill this section if applicable to your campaign")
        
        col17, col18 = st.columns(2)
        
        with col17:
            children_data = st.radio(
                "👶 Are you collecting data from children (<16 years old)?",
                ["No", "Yes", "Not sure"],
                help="See Template 6 above for parental consent wording"
            )
            
            parental_consent = None
            if children_data == "Yes":
                parental_consent = st.radio(
                    "Do you have parental consent mechanism?",
                    ["No", "Yes", "Age verification only"],
                    help="Required for children's data (see Template 6)"
                )
            
            retention_period = st.selectbox(
                "📅 How long will you retain this data?",
                ["Not determined yet", "Until event ends", "6 months", "1 year", 
                 "2+ years", "Indefinitely"]
            )
        
        with col18:
            automated_decisions = st.radio(
                "🤖 Are you using automated decisions/profiling?",
                ["No", "Yes (e.g., targeting algorithms, scoring)", "Not sure"],
                help="Automated individual decision-making has special requirements"
            )
            
            data_breach_plan = st.radio(
                "🚨 Do you have a data breach response plan?",
                ["No/Not sure", "Yes", "Not applicable"]
            )
    
    st.markdown("---")
    
    # Submit button
    submitted = st.form_submit_button("🚀 Run Compliance Check")

# Process form submission (same logic as before but mentioning templates)
if submitted:
    # Validation
    if not name or not event_name or event_type == "Select..." or collection_point == "Select..." or platform == "Select..." or data_type == "Select...":
        st.error("⚠️ Please fill in all required fields marked with *")
    else:
        # Risk Assessment Logic
        risk_level = "GREEN"
        issues = []
        critical_issues = []
        warnings = []
        
        # CRITICAL RED FLAGS
        if share_sponsors == "Yes":
            if sponsor_consent == "No/Not sure":
                risk_level = "RED"
                critical_issues.append("🚨 Sharing data with sponsors WITHOUT explicit opt-in consent violates GDPR. Use Template 5 above for proper consent wording.")
            if sponsor_dpa == "No/Not sure":
                risk_level = "RED"
                critical_issues.append("🚨 No Data Processing Agreement with sponsors - required for GDPR compliance")
        
        if data_type == "Sensitive data (see below for options)":
            risk_level = "RED"
            if not sensitive_data_types:
                critical_issues.append("🚨 Sensitive data collection requires specification of data types")
            if explicit_consent_sensitive in ["Not sure", "No"]:
                critical_issues.append("🚨 Sensitive data requires EXPLICIT consent with specific language. See Templates 3, 4, or 6 above.")
            if "👶 Children's data (under 16)" in sensitive_data_types:
                critical_issues.append("🚨 Children's data requires parental consent mechanism (see Template 6)")
        
        if preticked == "Yes, some boxes are pre-ticked":
            risk_level = "RED"
            critical_issues.append("🚨 Pre-ticked consent boxes violate GDPR Article 4(11) - consent must be active opt-in. ALL checkboxes must be unchecked by default.")
        
        if privacy_link in ["No", "Not sure"]:
            risk_level = "RED"
            critical_issues.append("🚨 Privacy Policy must be visible and accessible BEFORE data collection. Add link prominently on your form.")
        
        if bundled_consent == "Yes, must agree to everything to register":
            risk_level = "RED"
            critical_issues.append("🚨 Bundled consent violates GDPR - consent must be freely given, not a condition of service. Use separate checkboxes (see templates above).")
        
        if platform == "Other" and platform_dpa == "No/Not sure":
            risk_level = "RED"
            critical_issues.append("🚨 Unapproved platform without DPA - high compliance risk")
        
        if marketing_emails == "Yes, to all attendees":
            risk_level = "RED"
            critical_issues.append("🚨 Cannot email all attendees for marketing - only those who explicitly opted in. Use Template 2 for proper opt-in.")
        
        if is_virtual == "Yes" and recording_notice == "Yes, but no notice":
            risk_level = "RED"
            critical_issues.append("🚨 Recording without notice violates privacy rights. Use Template 4C for virtual event consent.")
        
        if cookies_tracking == "Yes, marketing/tracking" and cookie_banner in ["No", "Yes, but only 'Accept'"]:
            risk_level = "RED"
            critical_issues.append("🚨 Marketing cookies require explicit consent with accept/reject options")
        
        if data_location in ["United States", "Other country"] and risk_level != "RED":
            risk_level = "YELLOW"
            warnings.append("⚠️ Cross-border data transfer requires appropriate safeguards (SCCs, adequacy decision, etc.)")
        
        # YELLOW FLAGS (if not already RED)
        if risk_level != "RED":
            if data_type == "Email + Name + Job Title/Company":
                warnings.append("⚠️ Collecting job title/company - ensure it's necessary for the event purpose")
            
            if privacy_link == "Yes, but in footer/small text":
                warnings.append("⚠️ Privacy policy should be prominently visible, not just in footer")
            
            if "None of these" in consent_checkboxes or "Not sure" in consent_checkboxes:
                risk_level = "YELLOW"
                warnings.append("⚠️ Missing required consent checkboxes. Check templates above for what you need.")
            
            if marketing_emails == "Maybe/Not sure":
                warnings.append("⚠️ If sending marketing emails, you need explicit opt-in checkbox (Template 2)")
            
            if share_sponsors == "Not sure":
                warnings.append("⚠️ Clarify if data will be shared with third parties")
            
            if retention_period == "Indefinitely":
                warnings.append("⚠️ Indefinite retention may violate data minimization principles")
            
            if is_virtual == "Yes" and chat_logs == "Yes":
                warnings.append("⚠️ Inform participants that chat logs will be saved")
            
            if len(warnings) >= 3:
                risk_level = "YELLOW"
        
        # Save submission
        submission = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Event": event_name,
            "Event Type": event_type,
            "Launch Date": launch_date.strftime("%Y-%m-%d"),
            "Platform": platform,
            "Data Type": data_type,
            "Privacy Link": privacy_link,
            "Share Sponsors": share_sponsors,
            "Pre-ticked": preticked,
            "Marketing Emails": marketing_emails,
            "Risk Level": risk_level,
            "Critical Issues": len(critical_issues),
            "Warnings": len(warnings)
        }
        
        # Save to CSV
        df = pd.DataFrame([submission])
        file_exists = os.path.isfile("submissions.csv")
        df.to_csv("submissions.csv", mode='a', header=not file_exists, index=False)
        
        # Display Results
        st.markdown("---")
        st.markdown("## 📊 Compliance Assessment Results")
        
        if risk_level == "GREEN":
            st.markdown("""
            <div class="success-box">
                <h2 style="color: #28a745; margin-top: 0;">✅ COMPLIANCE CHECK PASSED</h2>
                <p style="font-size: 18px;">Your campaign looks good to launch!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(f"""
            **📋 Final Reminders for {event_name}:**
            
            ✓ Every email must include an unsubscribe link
            
            ✓ Honor opt-outs within 48 hours
            
            ✓ Delete event data after 6 months unless people opted in for future contact
            
            ✓ Only email people who explicitly opted in
            
            ✓ Keep records of consent (who opted in, when, for what)
            """)
            
            st.balloons()
        
        elif risk_level == "YELLOW":
            st.markdown("""
            <div class="warning-box">
                <h2 style="color: #856404; margin-top: 0;">⚠️ ACTION REQUIRED BEFORE LAUNCH</h2>
                <p style="font-size: 18px;">Fix these issues first, then you can launch</p>
            </div>
            """, unsafe_allow_html=True)
            
            if warnings:
                st.warning("**🔧 Issues to Address:**")
                for warning in warnings:
                    st.markdown(f"- {warning}")
            
            st.info("""
            
            **💡 Quick Fix:** Use the copy-paste templates at the top of this page!
            
            **✅ Required Actions:**
            
            ☐ Add mandatory Privacy Policy acceptance checkbox (see Template 1)
            
            ☐ Add visible Privacy Portal link on your form
            
            ☐ If sending marketing emails, add optional opt-in checkbox (see Template 2)
            
            ☐ Every email must have a working unsubscribe link
            
            ☐ Address the specific warnings listed above
            """)
            
            with st.expander("📎 Helpful Resources"):
                st.markdown("""
                - 📋 [Privacy Portal](https://www.prosus.com/privacy)
                - 📝 Templates are at the top of this page ⬆️
                - 📖 [GDPR Compliance Guide](https://drive.google.com)
                - 📧 Contact: privacy@prosus.com
                """)
        
        else:  # RED
            st.markdown("""
            <div class="danger-box">
                <h2 style="color: #721c24; margin-top: 0;">🛑 STOP - DO NOT LAUNCH</h2>
                <p style="font-size: 18px; font-weight: bold;">You MUST contact the privacy team before proceeding</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.error("**🚨 Critical Compliance Violations Detected:**")
            for issue in critical_issues:
                st.markdown(f"- {issue}")
            
            if warnings:
                st.warning("**⚠️ Additional Concerns:**")
                for warning in warnings:
                    st.markdown(f"- {warning}")
            
            st.error(f"""
            
            **📞 IMMEDIATE NEXT STEPS:**
            
            1. ❌ **Do NOT launch "{event_name}" yet**
            
            2. 📝 **Check the consent templates at the top of this page** - they show the correct wording
            
            3. 📧 **Contact privacy team IMMEDIATELY:**
               - Email: privacy@prosus.com
               - Slack: Post in #ask-privacy channel
               - Tag: @privacy-team
            
            4. 🔖 **Reference this check:**
               - Event: {event_name}
               - Date: {launch_date.strftime("%Y-%m-%d")}
               - Submitted by: {name}
               - Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            5. ⏳ **Wait for privacy team approval** before proceeding
            
            6. 📋 **Provide them with:**
               - Your registration form/landing page
               - Current consent checkbox wording
               - List of sponsors/partners (if applicable)
               - Platform details
            
            ⚡ **The privacy team will help you fix these issues quickly (usually within 24 hours).**
            
            🎯 **Why this matters:** Launching with these violations could result in GDPR fines up to €20M or 4% of annual revenue, plus reputational damage.
            """)
        
        # Show submission summary
        with st.expander("📄 Your Submission Summary (for your records)"):
            st.json(submission)
            
            if sensitive_data_types:
                st.markdown(f"**Sensitive Data Types:** {', '.join(sensitive_data_types)}")
            if sponsor_count:
                st.markdown(f"**Number of Sponsors:** {sponsor_count}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Privacy Compliance Tool v2.1</strong> | Built for External Communications Team</p>
    <p>📧 Questions? Contact: privacy@prosus.com | 💬 #ask-privacy on Slack</p>
    <p style="font-size: 0.9em; margin-top: 10px;">
        🔒 This tool helps prevent GDPR violations | All submissions are logged for audit purposes
    </p>
    <p style="font-size: 0.85em; margin-top: 5px;">
        💡 <strong>Tip:</strong> Use the copy-paste consent templates at the top to save time!
    </p>
</div>
""", unsafe_allow_html=True)
