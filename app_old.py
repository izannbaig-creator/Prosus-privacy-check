
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
    h1 {
        color: #1f1f1f;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🔒 Privacy Compliance Check")
st.markdown("**Required before launching any event, campaign, or registration form**")
st.markdown("---")

# Sidebar info
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/4CAF50/FFFFFF?text=PROSUS", width=150)
    st.markdown("### About This Tool")
    st.info("This tool helps ensure your campaigns comply with data protection regulations (GDPR, etc.)")
    st.markdown("### When to Use")
    st.markdown("""
    - ✅ Before event registration
    - ✅ Before email campaigns
    - ✅ Before collecting personal data
    - ✅ Before sharing data with partners
    """)
    st.markdown("### Need Help?")
    st.markdown("Contact: privacy@prosus.com")

# Main Form
with st.form("privacy_check_form"):
    st.subheader("📋 Campaign Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name *", placeholder="John Doe")
        event_name = st.text_input("Campaign/Event Name *", placeholder="AI Summit 2024")
        launch_date = st.date_input("Launch Date *")
    
    with col2:
        platform = st.selectbox(
            "Platform You're Using *",
            ["Select...", "Luma", "Eventbrite", "Mailchimp", "Lever", "Other"]
        )
        collection_point = st.selectbox(
            "Where Are You Collecting Data? *",
            ["Select...", "Website", "Event Registration", "Email Signup", "Other"]
        )
        data_type = st.selectbox(
            "What Data Are You Collecting? *",
            ["Select...", 
             "Email only", 
             "Email + Name", 
             "Email + Name + Job Title/Company",
             "Sensitive data (dietary, health, photos/video)"]
        )
    
    st.markdown("---")
    st.subheader("🔍 Compliance Questions")
    
    col3, col4 = st.columns(2)
    
    with col3:
        privacy_link = st.radio(
            "Is there a visible link to Prosus Privacy Policy? *",
            ["Yes", "No", "Not sure"]
        )
        
        consent_checkboxes = st.multiselect(
            "Which consent checkboxes do you have? (Select all that apply) *",
            [
                "Privacy Policy acceptance (mandatory, NOT pre-ticked)",
                "Marketing emails opt-in (optional, NOT pre-ticked)",
                "Event photo/recording consent",
                "None of these",
                "Not sure"
            ]
        )
        
        preticked = st.radio(
            "Does your form have any PRE-TICKED checkboxes? *",
            ["No", "Yes", "Not sure"]
        )
    
    with col4:
        share_sponsors = st.radio(
            "Will you share data with sponsors/partners? *",
            ["No", "Yes", "Not sure"]
        )
        
        marketing_emails = st.radio(
            "Will you send marketing emails later? *",
            ["No", "Yes", "Maybe"]
        )
    
    st.markdown("---")
    
    # Submit button
    submitted = st.form_submit_button("🚀 Run Compliance Check")

# Process form submission
if submitted:
    # Validation
    if not name or not event_name or platform == "Select..." or collection_point == "Select..." or data_type == "Select...":
        st.error("⚠️ Please fill in all required fields marked with *")
    else:
        # Risk Assessment Logic
        risk_level = "GREEN"
        issues = []
        critical_issues = []
        
        # RED FLAGS
        if share_sponsors in ["Yes", "Not sure"]:
            risk_level = "RED"
            critical_issues.append("Sharing data with sponsors/partners requires explicit opt-in consent")
        
        if "Sensitive data" in data_type:
            risk_level = "RED"
            critical_issues.append("Sensitive data collection requires special consent language")
        
        if preticked == "Yes":
            risk_level = "RED"
            critical_issues.append("Pre-ticked consent boxes violate GDPR")
        
        if privacy_link in ["No", "Not sure"]:
            risk_level = "RED"
            critical_issues.append("Missing Privacy Policy link is a compliance violation")
        
        if platform == "Other":
            risk_level = "RED"
            critical_issues.append("Unapproved platform - may not have Data Processing Agreement")
        
        # YELLOW FLAGS
        if risk_level != "RED":
            if "Job Title/Company" in data_type:
                risk_level = "YELLOW"
                issues.append("Collecting job title/company data - ensure it's necessary")
            
            if marketing_emails in ["Yes", "Maybe"]:
                risk_level = "YELLOW"
                issues.append("Marketing emails require separate opt-in checkbox")
            
            if "None of these" in consent_checkboxes or "Not sure" in consent_checkboxes:
                risk_level = "YELLOW"
                issues.append("Missing required consent checkboxes")
        
        # Save submission
        submission = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Event": event_name,
            "Launch Date": launch_date.strftime("%Y-%m-%d"),
            "Platform": platform,
            "Data Type": data_type,
            "Privacy Link": privacy_link,
            "Share Sponsors": share_sponsors,
            "Pre-ticked": preticked,
            "Marketing Emails": marketing_emails,
            "Risk Level": risk_level
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
            
            st.success("""
            **📋 Final Reminders:**
            
            ☐ Every email must include an unsubscribe link
            
            ☐ Honor opt-outs within 48 hours
            
            ☐ Delete event data after 6 months unless people opted in for future contact
            
            ☐ Only email people who explicitly opted in
            """)
            
            st.balloons()
        
        elif risk_level == "YELLOW":
            st.markdown("""
            <div class="warning-box">
                <h2 style="color: #856404; margin-top: 0;">⚠️ ACTION REQUIRED BEFORE LAUNCH</h2>
                <p style="font-size: 18px;">Fix these issues first, then you can launch</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("""
            **🔧 Required Fixes:**
            
            ☐ Add this MANDATORY checkbox (NOT pre-ticked):
               *"I agree that by registering for this event, my personal data will be processed in accordance with the Prosus Privacy Policy"*
            
            ☐ Add visible link to Prosus Privacy Portal on your form
            
            ☐ If sending marketing emails later, add separate OPTIONAL checkbox (NOT pre-ticked):
               *"I would like to receive information about future events from Prosus"*
            
            ☐ Every email must have an unsubscribe link
            """)
            
            with st.expander("📎 Resources"):
                st.markdown("""
                - [Privacy Portal](https://www.prosus.com/privacy) (Add your real link)
                - [Form Templates](https://drive.google.com) (Add your real link)
                - [Email Templates](https://drive.google.com) (Add your real link)
                """)
        
        else:  # RED
            st.markdown("""
            <div class="danger-box">
                <h2 style="color: #721c24; margin-top: 0;">🛑 STOP - DO NOT LAUNCH</h2>
                <p style="font-size: 18px; font-weight: bold;">You MUST contact the privacy team before proceeding</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.error("**🚨 Critical Issues Detected:**")
            for issue in critical_issues:
                st.markdown(f"- ❌ {issue}")
            
            st.error("""
            **📞 NEXT STEPS:**
            
            1. ❌ Do NOT launch this campaign yet
            2. 📧 Contact privacy team at: privacy@prosus.com
            3. 💬 Or post in #ask-privacy Slack channel
            4. 🔖 Reference this check: {event_name} - {launch_date}
            5. ⏳ Wait for privacy team approval
            
            The privacy team will help you fix this quickly (usually within 24 hours).
            """.format(event_name=event_name, launch_date=launch_date.strftime("%Y-%m-%d")))
        
        # Show submission summary
        with st.expander("📄 Your Submission Summary"):
            st.json(submission)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Privacy Compliance Tool v1.0 | Built for External Communications Team</p>
    <p>Questions? Contact: privacy@prosus.com | #ask-privacy on Slack</p>
</div>
""", unsafe_allow_html=True)
