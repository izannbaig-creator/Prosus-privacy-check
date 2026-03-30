
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

# Brighter, more cheerful CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #fafafa;
    }
    .stApp {
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        height: 3.5rem;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #45a049, #4CAF50);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        transform: translateY(-2px);
    }
    .success-box {
        padding: 25px;
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-left: 5px solid #28a745;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .warning-box {
        padding: 25px;
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border-left: 5px solid #ffc107;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .template-box {
        padding: 20px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #dee2e6;
        border-radius: 10px;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.95em;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .step-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
    }
    .question-box {
        background: linear-gradient(135deg, #ffffff, #f1f3f4);
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #e8f0fe;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for step tracking
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Header
st.title("🔒 Privacy Compliance Check")
st.markdown("<div style='text-align: center; color: #666; font-size: 1.1em; margin-bottom: 30px;'>Quick 5-question check before launching your campaign</div>", unsafe_allow_html=True)

# Simplified Sidebar
with st.sidebar:
    st.markdown("### 🚀 Quick Guide")
    st.info("""
    **When to use this:**
    
    🎪 **Events & Webinars**
    🗞️ **Email Campaigns** 
    📝 **Registration Forms**
    🤝 **Partner Events**
    
    **Takes 2 minutes** → Get instant templates!
    """)
    
    st.markdown("---")
    st.markdown("### 📧 Need Help?")
    st.markdown("**Email:** privacy@prosus.com")
    
    st.markdown("---")
    st.markdown("### 💡 Pro Tip")
    st.success("Get your copy-paste consent text based on your specific use case!")

# Step-by-step form logic
def reset_to_step(step_num):
    st.session_state.step = step_num

# Progress indicator
progress = min(st.session_state.step / 5, 1.0)
st.progress(progress)
st.markdown(f"<div style='text-align: center; color: #666; margin-bottom: 20px;'>Step {st.session_state.step} of 5</div>", unsafe_allow_html=True)

# STEP 1: Event Type
if st.session_state.step == 1:
    st.markdown('<div class="step-header">📋 What are you planning to do?</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    event_type = st.radio(
        "Select your campaign type:",
        [
            "🎪 Event (conference, workshop, networking)",
            "💻 Webinar or online session", 
            "📧 Email newsletter or marketing campaign",
            "📝 Contact/signup form on website",
            "🤝 Partner or sponsor collaboration"
        ],
        key="event_type"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Next →", key="step1_next"):
        st.session_state.answers['event_type'] = event_type
        st.session_state.step = 2
        st.rerun()

# STEP 2: Data Collection
elif st.session_state.step == 2:
    st.markdown('<div class="step-header">💾 What information are you collecting?</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        collect_email = st.checkbox("📧 Email addresses", key="email")
        collect_names = st.checkbox("👤 Names", key="names") 
        collect_company = st.checkbox("🏢 Company/job details", key="company")
    
    with col2:
        collect_dietary = st.checkbox("🍽️ Dietary requirements", key="dietary")
        collect_photos = st.checkbox("📸 Photos/videos of people", key="photos")
        collect_other = st.checkbox("📋 Other information", key="other")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                'other': collect_other
            }
            st.session_state.step = 3
            st.rerun()

# STEP 3: Data Usage Intent
elif st.session_state.step == 3:
    st.markdown('<div class="step-header">🎯 What will you do with this information?</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Will you:**")
        send_marketing = st.radio("Send marketing emails later?", ["No", "Yes"], key="marketing")
        share_sponsors = st.radio("Share data with event sponsors?", ["No", "Yes"], key="sponsors")
    
    with col2:
        st.markdown("**Does your form:**")
        preticked_boxes = st.radio("Have any pre-checked boxes?", ["No", "Yes"], key="preticked")
        privacy_link = st.radio("Show privacy policy link?", ["Yes", "No"], key="privacy")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("← Back", key="step3_back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next →", key="step3_next"):
            st.session_state.answers['usage'] = {
                'marketing': send_marketing,
                'sponsors': share_sponsors,
                'preticked': preticked_boxes,
                'privacy': privacy_link
            }
            st.session_state.step = 4
            st.rerun()

# STEP 4: Quick Compliance Check
elif st.session_state.step == 4:
    st.markdown('<div class="step-header">⚡ Quick compliance questions</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    
    platform = st.selectbox(
        "🛠️ What platform are you using?",
        ["Eventbrite", "Luma", "Mailchimp", "Google Forms", "Typeform", "Other"],
        key="platform"
    )
    
    if st.session_state.answers.get('data_collection', {}).get('photos', False):
        photo_consent = st.radio("Do people know they'll be photographed?", ["Yes", "No"], key="photo_consent")
    else:
        photo_consent = "N/A"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("← Back", key="step4_back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Get My Templates! 🎉", key="step4_next"):
            st.session_state.answers['compliance'] = {
                'platform': platform,
                'photo_consent': photo_consent
            }
            st.session_state.step = 5
            st.rerun()

# STEP 5: Results & Templates
elif st.session_state.step == 5:
    
    # Analyze answers for compliance
    answers = st.session_state.answers
    data_collection = answers.get('data_collection', {})
    usage = answers.get('usage', {})
    compliance = answers.get('compliance', {})
    
    # Risk assessment
    risk_issues = []
    
    if usage.get('preticked') == "Yes":
        risk_issues.append("Pre-checked boxes are not allowed")
    if usage.get('privacy') == "No":
        risk_issues.append("Privacy policy link is required")
    if usage.get('sponsors') == "Yes":
        risk_issues.append("Sharing with sponsors needs special consent")
    if data_collection.get('photos') and compliance.get('photo_consent') == "No":
        risk_issues.append("Photo consent is required")
    
    # Show results
    if risk_issues:
        st.markdown('<div class="warning-box"><h3>⚠️ Heads up! Fix these first:</h3>', unsafe_allow_html=True)
        for issue in risk_issues:
            st.markdown(f"• {issue}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box"><h3>✅ Looking good! Here are your templates:</h3></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📝 Your Copy-Paste Templates")
    
    # Generate relevant templates based on answers
    templates_shown = []
    
    # 1. ALWAYS show privacy policy template
    st.markdown("### 1️⃣ Privacy Policy Acceptance (REQUIRED)")
    st.info("⚠️ This checkbox is mandatory and must NOT be pre-checked")
    
    if "🎪 Event" in answers.get('event_type', '') or "💻 Webinar" in answers.get('event_type', ''):
        template_privacy = "☐ I agree that by registering for this event, my personal data will be processed in accordance with the Prosus Privacy Policy."
    else:
        template_privacy = "☐ I agree that by submitting this form, my personal data will be processed in accordance with the Prosus Privacy Policy."
    
    st.code(template_privacy, language=None)
    templates_shown.append("Privacy Policy")
    
    # 2. Marketing email consent (if they said yes to marketing)
    if usage.get('marketing') == "Yes":
        st.markdown("### 2️⃣ Marketing Email Consent (OPTIONAL)")
        st.success("✅ This checkbox is optional and must NOT be pre-checked")
        
        template_marketing = "☐ I would like to receive information about future Prosus events and opportunities. You can unsubscribe at any time."
        st.code(template_marketing, language=None)
        templates_shown.append("Marketing")
    
    # 3. Dietary requirements (if they collect dietary info)
    if data_collection.get('dietary'):
        st.markdown("### 3️⃣ Dietary Requirements Consent")
        st.warning("🚨 Required when collecting dietary information")
        
        template_dietary = "☐ I consent to Prosus processing my dietary requirements for catering purposes. This information will be deleted within 30 days after the event."
        st.code(template_dietary, language=None)
        templates_shown.append("Dietary")
    
    # 4. Photo/video consent (if they collect photos)
    if data_collection.get('photos'):
        st.markdown("### 4️⃣ Photography Consent")
        st.warning("🚨 Required when taking photos/videos")
        
        template_photo = "☐ I consent to being photographed/filmed during this event and to Prosus using these images in promotional materials and social media."
        st.code(template_photo, language=None)
        templates_shown.append("Photography")
    
    # 5. Sponsor data sharing (if they share with sponsors)
    if usage.get('sponsors') == "Yes":
        st.markdown("### 5️⃣ Sponsor Data Sharing Consent")
        st.error("🚨 REQUIRED when sharing data with sponsors")
        
        template_sponsor = "☐ I consent to my contact information (name, email, company) being shared with event sponsors and partners for follow-up communications about their products and services."
        st.code(template_sponsor, language=None)
        templates_shown.append("Sponsor Sharing")
    
    # COMPLETE FORM EXAMPLE
    st.markdown("---")
    st.markdown("## 📋 Complete Form Example")
    st.info("Copy this entire example and customize for your event:")
    
    # Build complete form based on what they're doing
    event_name = "Your Event Name Here"
    if "🎪 Event" in answers.get('event_type', ''):
        event_name = "Prosus Tech Conference 2024"
    elif "💻 Webinar" in answers.get('event_type', ''):
        event_name = "Prosus AI Webinar"
    elif "📧 Email" in answers.get('event_type', ''):
        event_name = "Prosus Newsletter"
    
    complete_form = f"""Registration Form - {event_name}

Please complete the following:"""
    
    if data_collection.get('names'):
        complete_form += "\n- Name: _______________"
    if data_collection.get('email'):
        complete_form += "\n- Email: _______________"
    if data_collection.get('company'):
        complete_form += "\n- Company: _______________\n- Job Title: _______________"
    if data_collection.get('dietary'):
        complete_form += "\n- Dietary Requirements (optional): _______________"
    
    complete_form += f"""

REQUIRED CONSENT:
{template_privacy}"""
    
    if data_collection.get('dietary'):
        complete_form += f"""

DIETARY CONSENT (if dietary requirements provided):
{template_dietary}"""
    
    if data_collection.get('photos'):
        complete_form += f"""

PHOTOGRAPHY CONSENT:
{template_photo}"""
    
    if usage.get('sponsors') == "Yes":
        complete_form += f"""

SPONSOR DATA SHARING (OPTIONAL):
{template_sponsor}"""
    
    if usage.get('marketing') == "Yes":
        complete_form += f"""

OPTIONAL MARKETING:
{template_marketing}"""
    
    complete_form += """

[Submit Registration]"""
    
    st.code(complete_form, language=None)
    
    # Key reminders
    st.markdown("---")
    st.markdown("## ✅ Key Reminders")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **DO:**
        • Place privacy policy link BEFORE data collection
        • Keep all checkboxes unchecked by default
        • Make privacy acceptance mandatory
        • Make marketing opt-ins optional
        • Include unsubscribe links in all emails
        """)
    
    with col2:
        st.error("""
        **DON'T:**
        • Pre-check any boxes
        • Hide privacy policy in small text
        • Make registration require marketing consent
        • Collect data without showing consent first
        • Send marketing emails to people who didn't opt in
        """)
    
    # Save submission for admin tracking
    submission = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Event Type": answers.get('event_type', ''),
        "Data Collected": ', '.join([k for k, v in data_collection.items() if v]),
        "Will Send Marketing": usage.get('marketing', 'No'),
        "Shares with Sponsors": usage.get('sponsors', 'No'),
        "Has Pre-ticked Boxes": usage.get('preticked', 'No'),
        "Shows Privacy Link": usage.get('privacy', 'Yes'),
        "Platform": compliance.get('platform', ''),
        "Templates Provided": ', '.join(templates_shown),
        "Risk Issues": len(risk_issues)
    }
    
    # Save to CSV
    df = pd.DataFrame([submission])
    file_exists = os.path.isfile("submissions.csv")
    df.to_csv("submissions.csv", mode='a', header=not file_exists, index=False)
    
    # Reset button
    if st.button("🔄 Start Over", key="reset"):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Privacy Compliance Tool v3.0</strong> | Simple ✨ Fast ⚡ Effective 🎯</p>
    <p>📧 Questions? Contact: privacy@prosus.com</p>
</div>
""", unsafe_allow_html=True)
