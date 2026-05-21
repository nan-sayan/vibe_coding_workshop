"""
Page 2: Anomaly Detection
Identify and highlight underperforming segments with visual indicators.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.analysis import load_marketing_data, identify_underperformers, get_segment_performance


def render_anomaly_detection():
    """Render the Anomaly Detection page."""
    
    st.header("🚨 Anomaly Detection: Underperformer Identification")
    
    # Educational context
    st.markdown("""
    ### How the Agent Identifies Underperformers
    The Agent automatically scans all audience segments and flags those with:
    - **High CPA (Cost Per Acquisition):** Spending too much per conversion
    - **Low CTR (Click-Through Rate):** Ads not resonating with the audience
    
    These segments represent wasted budget that could be reallocated to high performers. 
    The Agent's next task is to understand *why* they're failing and generate fixes.
    """)
    
    st.divider()
    
    # Load data
    df = load_marketing_data()
    if df is None:
        st.error("❌ No data found.")
        return
    
    # Get underperformers
    underperformers = identify_underperformers(df)
    
    if len(underperformers) == 0:
        st.success("✅ No underperformers detected! All segments are performing well.")
        return
    
    # Summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🚩 Flagged Segments", len(underperformers))
    
    with col2:
        total_underperformer_spend = underperformers['Spend_USD'].sum()
        st.metric("💸 At-Risk Budget", f"${total_underperformer_spend:,.0f}")
    
    with col3:
        pct_of_total = (total_underperformer_spend / df['Spend_USD'].sum() * 100)
        st.metric("📊 % of Total Spend", f"{pct_of_total:.1f}%")
    
    st.divider()
    
    # Severity visualization
    st.subheader("⚠️ Underperformer Severity Ranking")
    
    severity_df = underperformers[['Audience_Segment', 'Spend_USD', 'Avg_CPA_USD', 
                                    'Avg_CTR_Percent', 'Avg_ROAS', 'Severity_Score']].copy()
    
    # Color code by severity
    fig_severity = px.bar(
        severity_df,
        x='Severity_Score',
        y='Audience_Segment',
        orientation='h',
        color='Severity_Score',
        color_continuous_scale='Reds',
        labels={'Severity_Score': 'Severity Score', 'Audience_Segment': 'Audience Segment'},
        title='Segment Severity Rankings (Higher = Worse)'
    )
    fig_severity.update_layout(height=300, template='plotly_white')
    st.plotly_chart(fig_severity, use_container_width=True)
    
    st.divider()
    
    # Detailed analysis
    st.subheader("📊 Detailed Underperformer Analysis")
    
    for idx, (_, row) in enumerate(underperformers.iterrows()):
        with st.expander(f"🔴 {row['Audience_Segment']} (Severity: {row['Severity_Score']:.2f})", 
                        expanded=(idx == 0)):
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Total Spend", f"${row['Spend_USD']:,.0f}")
            
            with col2:
                st.metric("📈 CPA", f"${row['Avg_CPA_USD']:.2f}", 
                         delta=f"{row['Avg_CPA_USD'] - df['CPA_USD'].mean():.2f} (vs avg)")
            
            with col3:
                st.metric("🖱️ CTR", f"{row['Avg_CTR_Percent']:.2f}%",
                         delta=f"{row['Avg_CTR_Percent'] - df['CTR_Percent'].mean():.2f}% (vs avg)")
            
            with col4:
                st.metric("💵 ROAS", f"{row['Avg_ROAS']:.2f}x")
            
            # Reason for underperformance
            st.markdown(f"""
            **Why This Segment Underperforms:**
            - Very high cost per acquisition (${row['Avg_CPA_USD']:.2f})
            - Low click-through rate ({row['Avg_CTR_Percent']:.2f}% vs industry avg ~2-5%)
            - Poor return on ad spend ({row['Avg_ROAS']:.2f}x)
            - Likely issues: Ad creative doesn't resonate with audience, messaging misaligned with segment values
            """)
            
            # Recommended action
            st.warning(f"✋ **Immediate Action:** This segment wastes ~${row['Spend_USD'] * 0.2:,.0f} per period. "
                      f"The Agent will now analyze and generate optimized creative variants.")
    
    st.divider()
    
    # Comparison chart
    st.subheader("📉 Underperformers vs Average Performance")
    
    all_segments = get_segment_performance(df)
    all_segments['Status'] = all_segments['Audience_Segment'].apply(
        lambda x: 'Underperformer' if x in underperformers['Audience_Segment'].values else 'Healthy'
    )
    
    fig_comparison = px.scatter(
        all_segments,
        x='Avg_CTR_Percent',
        y='Avg_CPA_USD',
        color='Status',
        size='Spend_USD',
        hover_data=['Avg_ROAS', 'Conversions'],
        labels={'Avg_CTR_Percent': 'CTR (%)', 'Avg_CPA_USD': 'CPA ($)'},
        title='Segment Performance Matrix (CTR vs CPA)',
        color_discrete_map={'Underperformer': '#FF6B6B', 'Healthy': '#51CF66'}
    )
    
    # Add threshold lines
    cpa_threshold = 50
    ctr_threshold = 0.5
    fig_comparison.add_hline(y=cpa_threshold, line_dash="dash", line_color="red", 
                            annotation_text=f"CPA Threshold (${cpa_threshold})")
    fig_comparison.add_vline(x=ctr_threshold, line_dash="dash", line_color="red",
                            annotation_text=f"CTR Threshold ({ctr_threshold}%)")
    
    fig_comparison.update_layout(height=450, template='plotly_white')
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    st.divider()
    
    st.info("✨ **Next Step:** Go to 'Creative Optimization' to have the Agent analyze and rewrite ad copy for underperformers.")
