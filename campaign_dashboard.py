"""
Page 1: Campaign Dashboard
Shows overall campaign performance with interactive Plotly charts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.analysis import load_marketing_data, get_segment_performance, get_platform_performance


def render_dashboard():
    """Render the Campaign Dashboard page."""
    
    st.header("📊 Campaign Dashboard")
    
    # Educational context
    st.markdown("""
    ### What's Happening Here?
    The Agentic Campaign Optimizer starts by analyzing your complete marketing dataset. This dashboard displays 
    real-time performance metrics across all campaigns, platforms, and audience segments. 
    
    **The Agent's Job:** Continuously scan this data to identify trends, spot anomalies, and flag underperformers 
    that need immediate attention.
    """)
    
    st.divider()
    
    # Load data
    df = load_marketing_data()
    if df is None:
        st.error("❌ No data found. Please run `python data/generate_data.py` first.")
        return
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spend = df['Spend_USD'].sum()
        st.metric("💰 Total Spend", f"${total_spend:,.0f}")
    
    with col2:
        total_conversions = df['Conversions'].sum()
        st.metric("✅ Total Conversions", f"{int(total_conversions):,}")
    
    with col3:
        avg_cpa = df['CPA_USD'].mean()
        st.metric("📈 Avg CPA", f"${avg_cpa:.2f}")
    
    with col4:
        avg_roas = df['ROAS'].mean()
        st.metric("💵 Avg ROAS", f"{avg_roas:.2f}x")
    
    st.divider()
    
    # Chart 1: Spend vs Conversions by Platform
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💸 Spend vs Conversions by Platform")
        platform_perf = get_platform_performance(df)
        
        fig_platform = px.scatter(
            platform_perf,
            x='Spend_USD',
            y='Conversions',
            size='Num_Campaigns',
            color='Platform',
            hover_data=['Avg_CPA_USD', 'Avg_ROAS'],
            labels={'Spend_USD': 'Total Spend ($)', 'Conversions': 'Total Conversions'},
            title='Platform Performance Overview'
        )
        fig_platform.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig_platform, use_container_width=True)
    
    with col2:
        st.subheader("📊 CPA by Platform")
        fig_cpa = px.bar(
            platform_perf,
            x='Platform',
            y='Avg_CPA_USD',
            color='Avg_ROAS',
            labels={'Avg_CPA_USD': 'Average CPA ($)', 'Avg_ROAS': 'ROAS'},
            title='Cost Per Acquisition by Platform',
            color_continuous_scale='RdYlGn_r'
        )
        fig_cpa.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig_cpa, use_container_width=True)
    
    st.divider()
    
    # Chart 2: Segment Performance
    st.subheader("👥 Audience Segment Performance")
    segment_perf = get_segment_performance(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_segment_spend = px.bar(
            segment_perf,
            x='Audience_Segment',
            y='Spend_USD',
            color='Avg_ROAS',
            labels={'Spend_USD': 'Total Spend ($)', 'Avg_ROAS': 'ROAS'},
            title='Spend by Audience Segment',
            color_continuous_scale='Viridis'
        )
        fig_segment_spend.update_xaxes(tickangle=-45)
        fig_segment_spend.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig_segment_spend, use_container_width=True)
    
    with col2:
        fig_segment_ctr = px.bar(
            segment_perf,
            x='Audience_Segment',
            y='Avg_CTR_Percent',
            color='Avg_CTR_Percent',
            labels={'Avg_CTR_Percent': 'CTR (%)'},
            title='Click-Through Rate by Segment',
            color_continuous_scale='Blues'
        )
        fig_segment_ctr.update_xaxes(tickangle=-45)
        fig_segment_ctr.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig_segment_ctr, use_container_width=True)
    
    st.divider()
    
    # Data table
    st.subheader("📋 Detailed Performance Table")
    
    display_df = df[['Campaign_ID', 'Date', 'Platform', 'Audience_Segment', 'Spend_USD', 
                     'Impressions', 'Clicks', 'Conversions', 'CTR_Percent', 'CPA_USD', 'ROAS']].copy()
    display_df = display_df.sort_values('Date', ascending=False)
    
    # Format for display
    display_df['Spend_USD'] = display_df['Spend_USD'].apply(lambda x: f"${x:,.2f}")
    display_df['CPA_USD'] = display_df['CPA_USD'].apply(lambda x: f"${x:,.2f}")
    display_df['CTR_Percent'] = display_df['CTR_Percent'].apply(lambda x: f"{x:.2f}%")
    display_df['ROAS'] = display_df['ROAS'].apply(lambda x: f"{x:.2f}x")
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    st.info("✨ **Next Step:** Navigate to 'Anomaly Detection' to see which segments the Agent has flagged as underperformers.")
