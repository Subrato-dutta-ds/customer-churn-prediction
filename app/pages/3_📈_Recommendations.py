import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Retention Strategies", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Chart containers */
    .chart-container {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin: 0.5rem 0;
    }
    
    /* Strategy cards */
    .strategy-card {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .strategy-card:hover {
        transform: translateY(-3px);
        border-color: #4a6cf7;
        box-shadow: 0 8px 30px rgba(74, 108, 247, 0.1);
    }
    
    .strategy-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .strategy-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
    }
    .strategy-desc {
        font-size: 0.9rem;
        color: #8892b0;
        margin-top: 0.5rem;
    }
    .strategy-impact {
        margin-top: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .impact-high {
        background: rgba(255, 107, 107, 0.2);
        color: #ff6b6b;
        border: 1px solid rgba(255, 107, 107, 0.3);
    }
    .impact-medium {
        background: rgba(255, 159, 67, 0.2);
        color: #ff9f43;
        border: 1px solid rgba(255, 159, 67, 0.3);
    }
    .impact-low {
        background: rgba(74, 108, 247, 0.2);
        color: #4a6cf7;
        border: 1px solid rgba(74, 108, 247, 0.3);
    }
    
    /* Risk cards */
    .risk-card {
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 4px solid;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .risk-card:hover {
        transform: translateX(5px);
    }
    
    .risk-high {
        background: linear-gradient(145deg, #1a0a0a, #2a0a0a);
        border-left-color: #ff6b6b;
    }
    .risk-medium {
        background: linear-gradient(145deg, #1a150a, #2a1a0a);
        border-left-color: #ff9f43;
    }
    .risk-low {
        background: linear-gradient(145deg, #0a1a0a, #0a2a0a);
        border-left-color: #4a6cf7;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #4a6cf7, #6a4cf7, transparent);
        margin: 2rem 0;
    }
    
    /* Metric containers */
    .metric-container {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        text-align: center;
        transition: all 0.3s;
    }
    .metric-container:hover {
        border-color: #4a6cf7;
        transform: translateY(-3px);
    }
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a6cf7, #6a4cf7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-number-green {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-number-gold {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f1c40f, #f39c12);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8892b0;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Retention Strategies & Recommendations")
st.markdown("### Data-driven recommendations to reduce customer churn")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    return df

df = load_data()

# Key metrics
total_customers = len(df)
churned = df[df['Churn'] == 'Yes'].shape[0]
churn_rate = (churned / total_customers) * 100
avg_tenure = df['tenure'].mean()

# Exchange rate (USD to INR)
USD_TO_INR = 83

# Convert values to INR
avg_monthly_value_usd = 75
avg_monthly_value_inr = avg_monthly_value_usd * USD_TO_INR  # ₹6,225

clv_usd = 1800
clv_inr = clv_usd * USD_TO_INR  # ₹149,400

savings_usd = 400
savings_inr = savings_usd * USD_TO_INR  # ₹33,200

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-number">{total_customers:,}</div>
        <div class="metric-label">👥 Total Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-number" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{churned:,}</div>
        <div class="metric-label">⚠️ Churned Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-number" style="background: linear-gradient(135deg, #ff9f43, #f0932b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{churn_rate:.1f}%</div>
        <div class="metric-label">📈 Churn Rate</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-number" style="background: linear-gradient(135deg, #4a6cf7, #6a4cf7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{avg_tenure:.1f} mo</div>
        <div class="metric-label">⏱️ Avg Tenure</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Top churn drivers
st.subheader("🔍 Top Churn Drivers")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Contract type impact
    contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    colors = ['#ff6b6b', '#ff9f43', '#4a6cf7']
    
    fig = go.Figure(data=[go.Bar(
        x=contract_churn.index,
        y=contract_churn.values,
        marker=dict(
            color=contract_churn.values,
            colorscale='Reds',
            line=dict(color='#0a0a0a', width=2)
        ),
        text=contract_churn.values.round(1),
        textposition='outside',
        textfont=dict(color='#ffffff', size=12)
    )])
    
    fig.update_layout(
        title=dict(text="📊 Churn Rate by Contract Type", font=dict(color='#ffffff', size=16)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(title='Contract Type', color='#8892b0'),
        yaxis=dict(title='Churn Rate (%)', color='#8892b0', range=[0, 80]),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # Tenure impact
    df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72], 
                                 labels=['0-12', '13-24', '25-48', '49-72'])
    tenure_churn = df.groupby('tenure_group')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    
    fig = go.Figure(data=[go.Bar(
        x=tenure_churn.index,
        y=tenure_churn.values,
        marker=dict(
            color=tenure_churn.values,
            colorscale='Oranges',
            line=dict(color='#0a0a0a', width=2)
        ),
        text=tenure_churn.values.round(1),
        textposition='outside',
        textfont=dict(color='#ffffff', size=12)
    )])
    
    fig.update_layout(
        title=dict(text="⏱️ Churn Rate by Tenure", font=dict(color='#ffffff', size=16)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(title='Tenure (months)', color='#8892b0'),
        yaxis=dict(title='Churn Rate (%)', color='#8892b0', range=[0, 60]),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Customer segment strategies
st.subheader("💡 Actionable Strategies by Customer Segment")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="risk-card risk-high">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">🔴</span>
            <span style="font-size: 1.1rem; font-weight: 600; color: #ff6b6b;">High Risk</span>
            <span style="margin-left: auto; background: rgba(255,107,107,0.2); padding: 0.2rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; color: #ff6b6b;">>70%</span>
        </div>
        <div style="margin-top: 0.75rem; color: #8892b0; font-size: 0.9rem;">
            <strong style="color: #ffffff;">Profile:</strong><br>
            • Month-to-month contract<br>
            • Tenure < 12 months<br>
            • Monthly charges > $80<br>
            • No online security
        </div>
        <div style="margin-top: 0.75rem;">
            <div style="color: #ffffff; font-weight: 600; font-size: 0.9rem;">📋 Actions:</div>
            <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                <div class="strategy-impact impact-high">🚨 Priority support call</div>
                <div class="strategy-impact impact-high">💰 ₹1,660/month discount (6 months)</div>
                <div class="strategy-impact impact-high">📅 1-year contract with 15% discount</div>
                <div class="strategy-impact impact-medium">🎁 Loyalty bonus or gift card</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="risk-card risk-medium">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">🟡</span>
            <span style="font-size: 1.1rem; font-weight: 600; color: #ff9f43;">Medium Risk</span>
            <span style="margin-left: auto; background: rgba(255,159,67,0.2); padding: 0.2rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; color: #ff9f43;">40-70%</span>
        </div>
        <div style="margin-top: 0.75rem; color: #8892b0; font-size: 0.9rem;">
            <strong style="color: #ffffff;">Profile:</strong><br>
            • Month-to-month contract<br>
            • Tenure 12-24 months<br>
            • Missing add-on services<br>
            • Electronic check payment
        </div>
        <div style="margin-top: 0.75rem;">
            <div style="color: #ffffff; font-weight: 600; font-size: 0.9rem;">📋 Actions:</div>
            <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                <div class="strategy-impact impact-medium">🔒 Free Online Security (3 months)</div>
                <div class="strategy-impact impact-medium">📊 Personalized usage report</div>
                <div class="strategy-impact impact-medium">📱 Automatic payment setup</div>
                <div class="strategy-impact impact-low">💳 ₹830 credit for bill payment</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="risk-card risk-low">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">🟢</span>
            <span style="font-size: 1.1rem; font-weight: 600; color: #4a6cf7;">Low Risk</span>
            <span style="margin-left: auto; background: rgba(74,108,247,0.2); padding: 0.2rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; color: #4a6cf7;"><40%</span>
        </div>
        <div style="margin-top: 0.75rem; color: #8892b0; font-size: 0.9rem;">
            <strong style="color: #ffffff;">Profile:</strong><br>
            • Long-term contract<br>
            • Tenure > 24 months<br>
            • Multiple services<br>
            • Auto-payment enabled
        </div>
        <div style="margin-top: 0.75rem;">
            <div style="color: #ffffff; font-weight: 600; font-size: 0.9rem;">📋 Actions:</div>
            <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                <div class="strategy-impact impact-low">📱 Upsell additional services</div>
                <div class="strategy-impact impact-low">🎯 Send referral offers</div>
                <div class="strategy-impact impact-low">📊 Loyalty program benefits</div>
                <div class="strategy-impact impact-low">⭐ Premium support tier</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Business impact metrics (INR)
st.subheader("📊 Business Impact & ROI")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💵</div>
        <div class="metric-number">₹{avg_monthly_value_inr:,.0f}</div>
        <div class="metric-label">Average Monthly Customer Value</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💰</div>
        <div class="metric-number" style="background: linear-gradient(135deg, #4a6cf7, #6a4cf7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">₹{clv_inr:,.0f}</div>
        <div class="metric-label">Customer Lifetime Value (CLV)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-container">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📈</div>
        <div class="metric-number-green">₹{savings_inr:,.0f}</div>
        <div class="metric-label">Savings per Retained Customer</div>
    </div>
    """, unsafe_allow_html=True)

# Bottom row - Retention goals with INR
st.markdown("---")
st.subheader("🎯 Retention Goals & Targets")

col1, col2, col3 = st.columns(3)

with col1:
    annual_savings = 180000  # USD
    annual_savings_inr = annual_savings * USD_TO_INR
    st.markdown(f"""
    <div class="strategy-card">
        <div class="strategy-icon">🎯</div>
        <div class="strategy-title">Reduce Churn by 10%</div>
        <div class="strategy-desc">Implement targeted retention campaigns for high-risk customers</div>
        <div style="margin-top: 0.5rem;">
            <span class="strategy-impact impact-high">Annual Savings: ₹{annual_savings_inr:,.0f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    per_customer_value = 450  # USD
    per_customer_value_inr = per_customer_value * USD_TO_INR
    st.markdown(f"""
    <div class="strategy-card">
        <div class="strategy-icon">⏱️</div>
        <div class="strategy-title">Increase Tenure by 6 Months</div>
        <div class="strategy-desc">Focus on early-stage customers with loyalty programs</div>
        <div style="margin-top: 0.5rem;">
            <span class="strategy-impact impact-high">+₹{per_customer_value_inr:,} per customer</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="strategy-card">
        <div class="strategy-icon">📅</div>
        <div class="strategy-title">Convert to 1-Year Contracts</div>
        <div class="strategy-desc">Incentivize month-to-month customers to switch</div>
        <div style="margin-top: 0.5rem;">
            <span class="strategy-impact impact-high">-20% Churn Rate</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Additional ROI calculation
st.markdown("---")
st.subheader("💰 ROI Calculation")

col1, col2 = st.columns(2)

with col1:
    # Total annual revenue
    total_revenue_usd = total_customers * avg_monthly_value_usd * 12
    total_revenue_inr = total_revenue_usd * USD_TO_INR
    
    # Revenue lost to churn
    revenue_lost_usd = churned * avg_monthly_value_usd * 12
    revenue_lost_inr = revenue_lost_usd * USD_TO_INR
    
    st.markdown(f"""
    <div class="strategy-card">
        <div class="strategy-title">📊 Annual Revenue Impact</div>
        <div style="margin-top: 0.75rem;">
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #1a1a2e;">
                <span style="color: #8892b0;">Total Annual Revenue</span>
                <span style="color: #4a6cf7; font-weight: 600;">₹{total_revenue_inr:,.0f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #1a1a2e;">
                <span style="color: #8892b0;">Revenue Lost to Churn</span>
                <span style="color: #ff6b6b; font-weight: 600;">₹{revenue_lost_inr:,.0f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span style="color: #8892b0;">Potential Savings (10% churn reduction)</span>
                <span style="color: #2ecc71; font-weight: 600;">₹{(revenue_lost_inr * 0.10):,.0f}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="strategy-card">
        <div class="strategy-title">📈 ROI Calculator</div>
        <div style="margin-top: 0.75rem;">
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #1a1a2e;">
                <span style="color: #8892b0;">Customer Acquisition Cost</span>
                <span style="color: #ff9f43; font-weight: 600;">₹41,500</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #1a1a2e;">
                <span style="color: #8892b0;">Retention Program Cost</span>
                <span style="color: #4a6cf7; font-weight: 600;">₹8,300</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span style="color: #8892b0;">ROI per Customer</span>
                <span style="color: #2ecc71; font-weight: 600;">₹33,200</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-top: 2px solid #2a2a4a;">
                <span style="color: #8892b0; font-weight: 600;">ROI Multiple</span>
                <span style="color: #f1c40f; font-size: 1.2rem; font-weight: 700;">5x</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8892b0; padding: 1rem;'>
    🚀 Data-driven retention strategies | Powered by Machine Learning | 💰 All values in Indian Rupees (₹)
</div>
""", unsafe_allow_html=True)