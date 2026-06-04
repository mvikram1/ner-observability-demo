import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Wells Fargo NER Observability Demo", layout="wide")

# Title
st.title("Wells Fargo NER Customer Segmentation: Observability Demo")
st.markdown("**Scenario:** Holiday surge breaks entity recognition for LOCATION matching")

# Generate mock time series data (14 days, with holiday surge starting day 7)
def generate_data():
    dates = pd.date_range(start=datetime.now() - timedelta(days=14), periods=14, freq='D')
    
    # Model accuracy for LOCATION entity matching (declines after day 7)
    accuracy = np.concatenate([
        np.linspace(92, 91.5, 7),  # Days 1-7: stable
        np.linspace(91.5, 87, 7)   # Days 8-14: decline (holiday surge)
    ])
    
    # API availability (slight dip during surge)
    availability = np.concatenate([
        np.full(7, 99.8),           # Days 1-7: stable
        np.linspace(99.8, 98.5, 7)  # Days 8-14: slight dip
    ])
    
    # API error rate (increases during surge)
    error_rate = np.concatenate([
        np.full(7, 0.2),            # Days 1-7: baseline
        np.linspace(0.2, 1.2, 7)    # Days 8-14: increase
    ])
    
    # Data quality: null rate in input text (spikes during surge)
    null_rate = np.concatenate([
        np.full(7, 0.1),            # Days 1-7: baseline
        np.linspace(0.1, 2.3, 7)    # Days 8-14: spike
    ])
    
    # Data quality: encoding issues (international surge)
    encoding_issues = np.concatenate([
        np.full(7, 0.05),           # Days 1-7: baseline
        np.linspace(0.05, 3.2, 7)   # Days 8-14: spike
    ])
    
    # Infrastructure latency (slight increase)
    latency = np.concatenate([
        np.full(7, 45),             # Days 1-7: baseline
        np.linspace(45, 120, 7)     # Days 8-14: increase
    ])
    
    return pd.DataFrame({
        'date': dates,
        'accuracy': accuracy,
        'availability': availability,
        'error_rate': error_rate,
        'null_rate': null_rate,
        'encoding_issues': encoding_issues,
        'latency': latency
    })

data = generate_data()

# Sidebar controls
st.sidebar.markdown("### Demo Controls")
st.sidebar.markdown("Use the timeline slider to see how metrics changed over 14 days.")

# Timeline slider
day_selected = st.sidebar.slider(
    "Select Day to Inspect",
    min_value=1,
    max_value=14,
    value=14,
    step=1,
    help="Day 1-7: Normal. Day 7+: Holiday surge begins."
)

current_data = data.iloc[:day_selected]

st.sidebar.markdown("---")
st.sidebar.markdown("**Timeline Context:**")
st.sidebar.markdown("- **Days 1-7:** Normal traffic pattern")
st.sidebar.markdown("- **Day 7:** Holiday surge begins (international customers)")
st.sidebar.markdown("- **Days 8-14:** High volume of non-standard text formats")

# Main metrics display
col1, col2, col3, col4 = st.columns(4)

with col1:
    current_accuracy = current_data['accuracy'].iloc[-1]
    st.metric(
        "LOCATION Accuracy",
        f"{current_accuracy:.1f}%",
        delta=f"{current_accuracy - 92:.1f}%",
        delta_color="inverse"
    )

with col2:
    current_availability = current_data['availability'].iloc[-1]
    st.metric(
        "API Availability",
        f"{current_availability:.2f}%",
        delta=f"{current_availability - 99.8:.2f}%",
        delta_color="inverse"
    )

with col3:
    current_error_rate = current_data['error_rate'].iloc[-1]
    st.metric(
        "API Error Rate",
        f"{current_error_rate:.2f}%",
        delta=f"{current_error_rate - 0.2:.2f}%"
    )

with col4:
    current_latency = current_data['latency'].iloc[-1]
    st.metric(
        "API Latency",
        f"{current_latency:.0f}ms",
        delta=f"{current_latency - 45:.0f}ms"
    )

st.markdown("---")

# Visualizations
tab1, tab2, tab3 = st.tabs(["📊 All Metrics", "🔍 Correlation Analysis", "💡 Root Cause Analysis"])

with tab1:
    st.markdown("### Metric Trends Over Time")
    
    # Create subplots
    fig = go.Figure()
    
    # Model accuracy
    fig.add_trace(go.Scatter(
        x=current_data['date'],
        y=current_data['accuracy'],
        name='LOCATION Accuracy (%)',
        yaxis='y1',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # API error rate
    fig.add_trace(go.Scatter(
        x=current_data['date'],
        y=current_data['error_rate'],
        name='API Error Rate (%)',
        yaxis='y2',
        line=dict(color='#ff7f0e', width=2)
    ))
    
    # Data quality - null rate
    fig.add_trace(go.Scatter(
        x=current_data['date'],
        y=current_data['null_rate'],
        name='Null Rate in Input (%)',
        yaxis='y3',
        line=dict(color='#d62728', width=2)
    ))
    
    # Data quality - encoding issues
    fig.add_trace(go.Scatter(
        x=current_data['date'],
        y=current_data['encoding_issues'],
        name='Encoding Issues (%)',
        yaxis='y4',
        line=dict(color='#2ca02c', width=2, dash='dash')
    ))
    
    # Update layout with multiple y-axes
    fig.update_layout(
        title='Model, Infrastructure, and Data Quality Signals',
        xaxis=dict(title='Date'),
        yaxis=dict(
            title='Model Accuracy (%)',
            titlefont=dict(color='#1f77b4'),
            tickfont=dict(color='#1f77b4'),
            side='left'
        ),
        yaxis2=dict(
            title='API Error Rate (%)',
            titlefont=dict(color='#ff7f0e'),
            tickfont=dict(color='#ff7f0e'),
            overlaying='y',
            side='right'
        ),
        yaxis3=dict(
            title='Null Rate (%)',
            titlefont=dict(color='#d62728'),
            tickfont=dict(color='#d62728'),
            overlaying='y',
            side='left',
            anchor='free',
            position=0.15
        ),
        yaxis4=dict(
            title='Encoding Issues (%)',
            titlefont=dict(color='#2ca02c'),
            tickfont=dict(color='#2ca02c'),
            overlaying='y',
            side='right',
            anchor='free',
            position=0.85
        ),
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(x=0.01, y=0.99)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Correlation Analysis")
    
    # Calculate correlations
    if day_selected >= 7:
        accuracy_change = current_data['accuracy'].iloc[-1] - 92
        error_rate_change = current_data['error_rate'].iloc[-1] - 0.2
        null_rate_change = current_data['null_rate'].iloc[-1] - 0.1
        encoding_issues_change = current_data['encoding_issues'].iloc[-1] - 0.05
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Correlation Strength:**")
            
            # Accuracy vs error rate
            corr_accuracy_error = np.corrcoef(
                current_data['accuracy'],
                current_data['error_rate']
            )[0, 1]
            
            # Accuracy vs null rate
            corr_accuracy_null = np.corrcoef(
                current_data['accuracy'],
                current_data['null_rate']
            )[0, 1]
            
            # Accuracy vs encoding
            corr_accuracy_encoding = np.corrcoef(
                current_data['accuracy'],
                current_data['encoding_issues']
            )[0, 1]
            
            st.write(f"**Accuracy ↔ API Error Rate:** {corr_accuracy_error:.2f}")
            st.write(f"**Accuracy ↔ Null Rate:** {corr_accuracy_null:.2f} ⭐")
            st.write(f"**Accuracy ↔ Encoding Issues:** {corr_accuracy_encoding:.2f} ⭐")
        
        with col2:
            st.markdown("**What This Means:**")
            st.info(
                "🔴 **Strong correlation:** When null rate and encoding issues spike, "
                "accuracy drops simultaneously.\n\n"
                "🟢 **Weak correlation:** API error rate is stable (infrastructure is fine).\n\n"
                "→ **Conclusion:** Problem is DATA, not infrastructure or model."
            )
    else:
        st.info("📌 Select Day 8+ to see correlation analysis (surge begins on Day 7)")

with tab3:
    st.markdown("### Root Cause Analysis")
    
    if day_selected >= 7:
        accuracy_drop = 92 - current_data['accuracy'].iloc[-1]
        null_rate_spike = current_data['null_rate'].iloc[-1] - 0.1
        encoding_spike = current_data['encoding_issues'].iloc[-1] - 0.05
        
        st.markdown("#### **Root Cause: Data Quality Issue**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Evidence:**")
            st.markdown(f"- Accuracy dropped: **{accuracy_drop:.1f}%**")
            st.markdown(f"- Null rate increased: **{null_rate_spike:.2f}%** (23x baseline)")
            st.markdown(f"- Encoding issues: **{encoding_spike:.2f}%** (64x baseline)")
            st.markdown("- API infrastructure: **Stable** (slight latency from load, not errors)")
            st.markdown("- Model itself: **No code changes**")
        
        with col2:
            st.markdown("**What Happened:**")
            st.markdown(
                "Holiday surge brought international customers with:\n"
                "- Different text encodings (UTF-8 variants, non-ASCII)\n"
                "- Unexpected entity formats (international names, addresses)\n"
                "- Missing fields (some customer records incomplete)\n\n"
                "Model was trained on 'normal' text patterns. Holiday surge = out-of-distribution data."
            )
        
        st.markdown("---")
        st.markdown("#### **What Each Observability Path Would Do:**")
        
        path_comparison = pd.DataFrame({
            'Path': ['Path 1: Custom On-Prem', 'Path 2: Hybrid (Braintrust + InsightFinder)', 'Path 3: Pure InsightFinder Cloud'],
            'Detection Time': ['8-12 hours', '30 minutes', '30 minutes'],
            'Root Cause Found': ['Manual archaeology', 'Automated (causal inference)', 'Automated (causal inference)'],
            'GDPR Compliant': ['✓ Yes', '✓ Yes', '✗ No (data to cloud)'],
            'Who Figures It Out': ['Data eng + SRE team manually correlating', "InsightFinder's engine", "InsightFinder's engine"]
        })
        
        st.dataframe(path_comparison, use_container_width=True)
        
        st.markdown("---")
        st.markdown("#### **Recommendation Action:**")
        st.success(
            "**Path 2 (Hybrid)** is ideal here because:\n"
            "1. Detects root cause in 30 minutes (not 8+ hours)\n"
            "2. GDPR compliant (data stays on-prem)\n"
            "3. Automated correlation (no manual detective work)\n"
            "4. Engineering team can act immediately on fix (retrain with international data patterns)"
        )
    else:
        st.info("📌 Select Day 8+ to see root cause analysis (surge begins on Day 7)")

st.markdown("---")

# Scenario explanation
with st.expander("ℹ️ About This Scenario", expanded=False):
    st.markdown("""
    **The Holiday Surge Scenario:**
    
    Wells Fargo's NER model for customer segmentation was trained on 6 months of customer data.
    It learned to recognize LOCATION entities (cities, countries, addresses) very well: 92% accuracy.
    
    During holiday season, traffic surges. More international customers, more account opening requests.
    The new customer data has:
    - Different text encodings (UTF-8 variants from international systems)
    - Entity formats the model hasn't seen (international names, postal codes)
    - Missing fields in some records (incomplete holiday signup forms)
    
    **The Problem:**
    - Day 1-7: System runs smoothly
    - Day 8: Surge starts, accuracy begins dropping
    - Day 14: Accuracy is 87%, 5% below SLA
    
    **Traditional Monitoring:**
    - Datadog shows API latency up 2.5x (not an error, just load)
    - Custom model dashboard shows accuracy down 5%
    - Data quality team notices null rates up
    - ServiceNow gets three tickets from different teams
    - SRE team spends 8+ hours correlating: "Is it the model? Infrastructure? Data?"
    
    **With Path 2 (Hybrid Observability):**
    - InsightFinder's causal inference engine immediately shows: null rates + encoding issues = model accuracy drop
    - Correlation is automatic, not manual
    - Root cause identified in 30 minutes
    - Data team can retrain on international patterns
    - GDPR compliance maintained (raw data stayed on-prem)
    """)

st.markdown("---")
st.markdown("**Built for InsightFinder Interview Demo** | Wells Fargo NER Observability Scenario")
