"""
Agentic Campaign Optimization Engine - Main Streamlit App
A workshop demonstration of how AI agents can autonomously optimize marketing campaigns.
"""

import streamlit as st
from pages.campaign_dashboard import render_dashboard
from pages.anomaly_detection import render_anomaly_detection
from pages.creative_optimization import render_creative_optimization
from pages.budget_reallocation import render_budget_reallocation


# Page configuration
st.set_page_config(
    page_title="Agentic Campaign Optimizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 🤖 Agentic Campaign Optimizer")
    st.markdown("**AI-Powered Marketing Optimization Engine**")
    st.divider()
    
    # Navigation
    page = st.radio(
        "Select Page:",
        [
            "📊 Campaign Dashboard",
            "🚨 Anomaly Detection",
            "✏️ Creative Optimization",
            "💰 Budget Reallocation"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Educational sidebar
    st.markdown("""
    ### About This Workshop
    
    This app demonstrates how **AI Agents** can autonomously:
    - 📊 Analyze marketing performance
    - 🚨 Identify underperformers
    - ✏️ Optimize ad creative
    - 💰 Reallocate budgets
    
    **Key Concepts:**
    - **CPA:** Cost Per Acquisition (lower = better)
    - **CTR:** Click-Through Rate (higher = better)
    - **ROAS:** Return on Ad Spend (higher = better)
    
    ### Data
    This workshop uses simulated marketing data with intentional underperformers:
    - "Soccer Moms 35-45"
    - "Retirees 55-65"
    
    These segments have been given poor performance metrics to demonstrate 
    how the Agent identifies and fixes problems.
    """)
    
    st.divider()
    
    st.markdown("""
    **Built with:**
    - Streamlit
    - Pandas
    - Plotly
    """)

# Main content
if page == "📊 Campaign Dashboard":
    render_dashboard()

elif page == "🚨 Anomaly Detection":
    render_anomaly_detection()

elif page == "✏️ Creative Optimization":
    # Initialize session state for creative optimization
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    
    render_creative_optimization()

elif page == "💰 Budget Reallocation":
    render_budget_reallocation()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #888;'>
    <p>🚀 Agentic Campaign Optimization Engine v1.0</p>
    <p>Built for workshop demonstration | 2026</p>
</div>
""", unsafe_allow_html=True)
