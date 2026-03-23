import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Admin Dashboard - Privacy Compliance",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Privacy Compliance - Admin Dashboard")
st.markdown("**Monitor all submissions and identify high-risk campaigns**")
st.markdown("---")

# Load data
if os.path.isfile("submissions.csv"):
    df = pd.read_csv("submissions.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(df)
        st.metric("Total Submissions", total)
    
    with col2:
        red_count = len(df[df['Risk Level'] == 'RED'])
        st.metric("🔴 High Risk", red_count, delta=f"{(red_count/total*100):.1f}%" if total > 0 else "0%")
    
    with col3:
        yellow_count = len(df[df['Risk Level'] == 'YELLOW'])
        st.metric("🟡 Medium Risk", yellow_count, delta=f"{(yellow_count/total*100):.1f}%" if total > 0 else "0%")
    
    with col4:
        green_count = len(df[df['Risk Level'] == 'GREEN'])
        st.metric("🟢 Low Risk", green_count, delta=f"{(green_count/total*100):.1f}%" if total > 0 else "0%")
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            ["RED", "YELLOW", "GREEN"],
            default=["RED", "YELLOW", "GREEN"]
        )
    
    with col2:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
    
    with col3:
        platform_filter = st.multiselect(
            "Filter by Platform",
            df['Platform'].unique(),
            default=df['Platform'].unique()
        )
    
    # Apply filters
    filtered_df = df[
        (df['Risk Level'].isin(risk_filter)) &
        (df['Platform'].isin(platform_filter))
    ]
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Timestamp'].dt.date >= date_range[0]) &
            (filtered_df['Timestamp'].dt.date <= date_range[1])
        ]
    
    st.markdown(f"### 📋 Showing {len(filtered_df)} submissions")
    
    # Risk level color coding
    def color_risk(val):
        if val == 'RED':
            return 'background-color: #f8d7da; color: #721c24; font-weight: bold'
        elif val == 'YELLOW':
            return 'background-color: #fff3cd; color: #856404; font-weight: bold'
        else:
            return 'background-color: #d4edda; color: #155724; font-weight: bold'
    
    # Display table
    styled_df = filtered_df.style.applymap(color_risk, subset=['Risk Level'])
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name=f"privacy_checks_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # High-risk alerts
    st.markdown("---")
    st.subheader("🚨 High-Risk Submissions Requiring Attention")
    
    high_risk = filtered_df[filtered_df['Risk Level'] == 'RED'].sort_values('Timestamp', ascending=False)
    
    if len(high_risk) > 0:
        for idx, row in high_risk.head(5).iterrows():
            with st.expander(f"🔴 {row['Event']} - {row['Name']} ({row['Timestamp'].strftime('%Y-%m-%d')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Event:** {row['Event']}")
                    st.markdown(f"**Launch Date:** {row['Launch Date']}")
                    st.markdown(f"**Platform:** {row['Platform']}")
                    st.markdown(f"**Data Type:** {row['Data Type']}")
                
                with col2:
                    st.markdown(f"**Privacy Link Visible:** {row['Privacy Link']}")
                    st.markdown(f"**Sharing with Sponsors:** {row['Share Sponsors']}")
                    st.markdown(f"**Pre-ticked Boxes:** {row['Pre-ticked']}")
                    st.markdown(f"**Marketing Emails:** {row['Marketing Emails']}")
                
                st.warning(f"⚠️ Contact {row['Name']} immediately to prevent non-compliant launch")
    else:
        st.success("✅ No high-risk submissions in selected timeframe")
    
    # Analytics
    st.markdown("---")
    st.subheader("📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Risk Distribution**")
        risk_counts = filtered_df['Risk Level'].value_counts()
        st.bar_chart(risk_counts)
    
    with col2:
        st.markdown("**Platform Usage**")
        platform_counts = filtered_df['Platform'].value_counts()
        st.bar_chart(platform_counts)

else:
    st.info("📭 No submissions yet. Share the privacy check tool with your team!")
    st.markdown("""
    **To get started:**
    1. Share the main app link with external communications team
    2. Submissions will appear here automatically
    3. You'll be able to filter and monitor all checks
    """)

# Footer
st.markdown("---")
st.caption("Admin Dashboard | For Privacy Team Use Only")
