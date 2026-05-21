"""
Page 4: Budget Reallocation Engine
Show budget optimization recommendations and projected impact.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.analysis import load_marketing_data, calculate_budget_reallocation


def render_budget_reallocation():
    """Render the Budget Reallocation page."""
    
    st.header("💰 Budget Reallocation Engine")
    
    # Educational context
    st.markdown("""
    ### Autonomous Budget Optimization
    The Agent doesn't just identify problems—it solves them autonomously by:
    1. **Calculating** the cost of underperformance
    2. **Recommending** budget shifts from low performers to high performers
    3. **Projecting** the revenue impact of reallocation
    4. **Executing** the strategy (in production systems, with approval)
    
    This mimics how a senior marketing director would reallocate budgets, but the Agent 
    does it in real-time using data-driven logic instead of intuition.
    """)
    
    st.divider()
    
    # Load data
    df = load_marketing_data()
    if df is None:
        st.error("❌ No data found.")
        return
    
    # Calculate reallocation
    current_alloc, recommended_alloc, projections = calculate_budget_reallocation(df)
    
    # Summary metrics
    st.subheader("📊 Reallocation Impact Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💸 Current Total Spend",
            f"${projections['current_spend']:,.0f}",
            help="Total budget across all segments"
        )
    
    with col2:
        st.metric(
            "💸 Recommended Total Spend",
            f"${projections['recommended_spend']:,.0f}",
            help="Same total, redistributed optimally"
        )
    
    with col3:
        st.metric(
            "✅ Current Conversions",
            f"{projections['current_conversions']:,}",
            help="Conversions with current allocation"
        )
    
    with col4:
        st.metric(
            "✅ Projected Conversions",
            f"{projections['projected_conversions']:,}",
            delta=f"+{projections['conversion_lift']} ({projections['conversion_lift_pct']:.1f}%)",
            help="Expected conversions after reallocation"
        )
    
    st.divider()
    
    # Main comparison visualization
    st.subheader("🔄 Current vs Recommended Budget Allocation")
    
    # Prepare comparison data
    comparison_data = pd.DataFrame({
        'Audience_Segment': current_alloc['Audience_Segment'],
        'Current Spend': current_alloc['Current_Spend'],
        'Recommended Spend': recommended_alloc['Recommended_Spend'],
        'Change': recommended_alloc['Recommended_Spend'] - current_alloc['Current_Spend']
    })
    
    comparison_data = comparison_data.sort_values('Change', ascending=False)
    
    # Create grouped bar chart
    fig_allocation = px.bar(
        comparison_data,
        x='Audience_Segment',
        y=['Current Spend', 'Recommended Spend'],
        barmode='group',
        labels={'value': 'Spend ($)', 'variable': 'Allocation'},
        title='Current vs Recommended Budget by Segment',
        color_discrete_map={'Current Spend': '#3498db', 'Recommended Spend': '#2ecc71'}
    )
    fig_allocation.update_xaxes(tickangle=-45)
    fig_allocation.update_layout(height=450, template='plotly_white')
    st.plotly_chart(fig_allocation, use_container_width=True)
    
    st.divider()
    
    # Detailed segment analysis
    st.subheader("📋 Segment-by-Segment Reallocation Details")
    
    # Color code changes
    comparison_data_display = comparison_data.copy()
    comparison_data_display['Current Spend'] = comparison_data_display['Current Spend'].apply(lambda x: f"${x:,.0f}")
    comparison_data_display['Recommended Spend'] = comparison_data_display['Recommended Spend'].apply(lambda x: f"${x:,.0f}")
    comparison_data_display['Change'] = comparison_data_display['Change'].apply(lambda x: f"${x:,.0f}")
    
    # Create detailed table with segment analysis
    for idx, row in comparison_data.iterrows():
        segment_name = row['Audience_Segment']
        current_spend = row['Current Spend']
        recommended_spend = row['Recommended Spend']
        change = recommended_spend - current_spend
        
        # Determine color and label
        if change > 0:
            change_label = "🟢 INCREASE"
            change_color = "green"
        elif change < 0:
            change_label = "🔴 DECREASE"
            change_color = "red"
        else:
            change_label = "⚪ NO CHANGE"
            change_color = "gray"
        
        with st.expander(f"{change_label} {segment_name} | {change:+,.0f}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Spend", f"${current_spend:,.0f}")
            
            with col2:
                st.metric("Recommended Spend", f"${recommended_spend:,.0f}")
            
            with col3:
                st.metric("Change", f"${change:+,.0f}")
            
            # Show rationale
            segment_data = recommended_alloc[recommended_alloc['Audience_Segment'] == segment_name].iloc[0]
            
            if change > 0:
                st.success(f"""
                ✅ **Budget Increase Recommended**
                
                This segment is a top performer with:
                - ROAS: {segment_data['Avg_ROAS']:.2f}x
                - CPA: ${segment_data['Avg_CPA_USD']:.2f}
                - CTR: {segment_data['Avg_CTR_Percent']:.2f}%
                
                **Action:** Increase spend to capture more high-quality conversions.
                """)
            elif change < 0:
                st.error(f"""
                ❌ **Budget Decrease Recommended**
                
                This segment underperforms with:
                - ROAS: {segment_data['Avg_ROAS']:.2f}x
                - CPA: ${segment_data['Avg_CPA_USD']:.2f}
                - CTR: {segment_data['Avg_CTR_Percent']:.2f}%
                
                **Action:** Reduce spend and use budget for better performers. 
                Consider new creative strategy (from Creative Optimization).
                """)
            else:
                st.info(f"""
                ⚪ **Budget Hold Recommended**
                
                This segment maintains steady performance. No change needed at this time.
                """)
    
    st.divider()
    
    # ROI Impact visualization
    st.subheader("📈 Projected ROI Impact")
    
    impact_data = pd.DataFrame({
        'Metric': ['Conversions', 'Spend', 'Conv. per $1000 Spent'],
        'Current': [
            projections['current_conversions'],
            projections['current_spend'],
            (projections['current_conversions'] / projections['current_spend'] * 1000)
        ],
        'Recommended': [
            projections['projected_conversions'],
            projections['recommended_spend'],
            (projections['projected_conversions'] / projections['recommended_spend'] * 1000)
        ]
    })
    
    # Create comparison table
    st.metric(
        "📊 Efficiency Gain",
        f"{((projections['projected_conversions'] / projections['recommended_spend']) / (projections['current_conversions'] / projections['current_spend']) - 1) * 100:.1f}%",
        help="Improvement in conversions per dollar spent"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Current Allocation Efficiency
        - **Total Conversions:** {:,}
        - **Total Spend:** ${:,.0f}
        - **Conversions per $1000:** {:.2f}
        """.format(
            projections['current_conversions'],
            projections['current_spend'],
            projections['current_conversions'] / projections['current_spend'] * 1000
        ))
    
    with col2:
        st.markdown("""
        ### Recommended Allocation Efficiency
        - **Total Conversions:** {:,}
        - **Total Spend:** ${:,.0f}
        - **Conversions per $1000:** {:.2f}
        """.format(
            projections['projected_conversions'],
            projections['recommended_spend'],
            projections['projected_conversions'] / projections['recommended_spend'] * 1000
        ))
    
    st.divider()
    
    # Implementation recommendations
    st.subheader("🚀 Implementation Roadmap")
    
    st.markdown(f"""
    ### Suggested 30-Day Action Plan
    
    **Week 1: Validation**
    - Approve recommended budget shifts
    - Test new creative variants (from Creative Optimization) with 10% of budget
    - Monitor performance closely
    
    **Week 2-3: Gradual Rollout**
    - Gradually shift budget ({projections['reallocation_amount']:,.0f} total) from underperformers
    - Scale winning creative variants
    - Set up automated alerts for performance changes
    
    **Week 4: Optimization**
    - Analyze full results from reallocated budget
    - Fine-tune segments based on new data
    - Re-run Agent for next round of optimizations
    
    ### Expected Results
    - **Conversion Lift:** +{projections['conversion_lift']} conversions ({projections['conversion_lift_pct']:.1f}% improvement)
    - **Efficiency Gain:** {((projections['projected_conversions'] / projections['recommended_spend']) / (projections['current_conversions'] / projections['current_spend']) - 1) * 100:.1f}% better ROI
    - **Spend Efficiency:** Same budget, smarter allocation
    """)
    
    st.divider()
    
    st.info("""
    ✨ **The Complete Agentic Loop:**
    
    1. ✅ Analyze campaign data (Dashboard)
    2. ✅ Identify underperformers (Anomaly Detection)
    3. ✅ Generate new creative (Creative Optimization)
    4. ✅ Reallocate budget (You are here)
    5. 🔄 Monitor & repeat autonomously
    
    In a production system, an AI Agent would handle steps 1-4 continuously, 
    improving performance without human intervention.
    """)
