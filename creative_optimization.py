"""
Page 3: Agentic Creative Optimization
Simulate AI agent analyzing underperformers and generating new ad copy.
"""

import streamlit as st
import time
from utils.analysis import (load_marketing_data, get_underperforming_segments, 
                           simulate_ai_agent_analysis)


def render_creative_optimization():
    """Render the Creative Optimization page."""
    
    st.header("✏️ Agentic Creative Optimization")
    
    # Educational context
    st.markdown("""
    ### The Agent's Creativity Engine
    Once underperformers are identified, the Agent uses AI to:
    1. **Analyze** why the current creative is failing for this specific audience
    2. **Generate** 3 brand new ad copy variants tailored to the segment's values and pain points
    3. **Test** these variants against the current creative to find the winner
    
    This simulates how an LLM (Large Language Model) can act as a real-time marketing strategist, 
    instantly producing multiple creative options without human brainstorming.
    """)
    
    st.divider()
    
    # Load data
    df = load_marketing_data()
    if df is None:
        st.error("❌ No data found.")
        return
    
    # Get underperforming segments
    underperforming_segments = get_underperforming_segments(df)
    
    if len(underperforming_segments) == 0:
        st.success("✅ No underperforming segments to optimize!")
        return
    
    # Segment selector
    st.subheader("🎯 Select Underperforming Segment")
    selected_segment = st.selectbox(
        "Choose a segment for creative optimization:",
        underperforming_segments,
        help="These are the segments the Agent flagged as underperformers"
    )
    
    st.divider()
    
    # Run analysis button
    if st.button("🤖 Run AI Agent Analysis", type="primary", use_container_width=True):
        
        # Simulate thinking with progress bar
        with st.spinner("🧠 Agent is analyzing the segment..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)  # Simulate thinking time
                progress_bar.progress(i + 1)
        
        # Run simulation
        analysis_result = simulate_ai_agent_analysis(selected_segment, df)
        
        # Store in session state for display
        st.session_state.analysis_result = analysis_result
        st.session_state.show_results = True
    
    # Display results if available
    if st.session_state.get('show_results', False):
        analysis = st.session_state.analysis_result
        
        st.divider()
        
        # Current performance metrics
        st.subheader("📊 Current Performance Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        metrics = analysis['current_metrics']
        
        with col1:
            st.metric("💰 Spend", f"${metrics['spend']:,.0f}")
        
        with col2:
            st.metric("✅ Conversions", f"{metrics['conversions']:,}")
        
        with col3:
            st.metric("📈 CPA", f"${metrics['cpa']:.2f}")
        
        with col4:
            st.metric("🖱️ CTR", f"{metrics['ctr']:.2f}%")
        
        with col5:
            st.metric("💵 ROAS", f"{metrics['roas']:.2f}x")
        
        st.divider()
        
        # Agent's analysis
        st.subheader("🔍 Agent's Analysis")
        st.markdown(f"""
        ### Why the Current Creative is Failing
        
        {analysis['analysis']}
        """)
        
        st.divider()
        
        # Recommendations
        st.subheader("💡 Agent's Recommendations")
        for i, rec in enumerate(analysis['recommendations'], 1):
            st.write(f"{i}. {rec}")
        
        st.divider()
        
        # Creative variants
        st.subheader("🎨 AI-Generated Ad Copy Variants")
        st.markdown("""
        The Agent has generated 3 new creative variants optimized for this audience. 
        Each is designed to address the specific pain points and values of this segment.
        """)
        
        # Display each variant in a card-like format
        for i, variant in enumerate(analysis['creative_variants'], 1):
            with st.container(border=True):
                col1, col2 = st.columns([1, 4]

)
                
                with col1:
                    st.markdown(f"## Variant {i}")
                    st.markdown("✨ **AI Generated**")
                
                with col2:
                    st.markdown(f"### 📝 {variant['headline']}")
                    st.markdown(variant['primary_text'])
            
            # Copy button
            copy_text = f"Headline: {variant['headline']}\n\nPrimary Text: {variant['primary_text']}"
            st.code(copy_text, language="text")
        
        st.divider()
        
        # Next steps
        st.markdown("""
        ### 🚀 What Happens Next?
        
        In a real production system, these creative variants would be:
        1. **Deployed** to a small test audience (~10% of usual spend)
        2. **Monitored** for performance over 3-5 days
        3. **Compared** against the current creative baseline
        4. **Scaled** - the winning variant gets 50% of the budget, others get 25% each
        5. **Rotated** - new variants generated weekly if performance plateaus
        
        The Agent would autonomously manage this entire A/B testing cycle.
        """)
        
        st.info("✨ **Next Step:** Go to 'Budget Reallocation' to see how the Agent reallocates budget from underperformers to winners.")
    
    else:
        st.info("👆 Click the 'Run AI Agent Analysis' button above to generate creative variants for this segment.")
