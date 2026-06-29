import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data import load_data
from src.recommendations import get_interventions

st.set_page_config(page_title="Retention Strategies", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; font-weight: 600 !important; }
    .chart-container {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        margin: 0.5rem 0;
    }
    .strategy-card {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .strategy-card:hover { transform: translateY(-3px); border-color: #4a6cf7; }
    .strategy-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .strategy-title { font-size: 1.1rem; font-weight: 600; color: #ffffff; }
    .strategy-desc { font-size: 0.9rem; color: #8892b0; margin-top: 0.5rem; }
    .strategy-impact {
        margin-top: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .impact-high { background: rgba(255,107,107,0.2); color: #ff6b6b; border: 1px solid rgba(255,107,107,0.3); }
    .impact-medium { background: rgba(255,159,67,0.2); color: #ff9f43; border: 1px solid rgba(255,159,67,0.3); }
    .impact-low { background: rgba(74,108,247,0.2); color: #4a6cf7; border: 1px solid rgba(74,108,247,0.3); }
    .risk-card {
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 4px solid;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .risk-card:hover { transform: translateX(5px); }
    .risk-high { background: linear-gradient(145deg, #1a0a0a, #2a0a0a); border-left-color: #ff6b6b; }
    .risk-medium { background: linear-gradient(145deg, #1a150a, #2a1a0a); border-left-color: #ff9f43; }
    .risk-low { background: linear-gradient(145deg, #0a1a0a, #0a2a0a); border-left-color: #4a6cf7; }
    hr { border: none; height: 2px; background: linear-gradient(to right, #4a6cf7, #6a4cf7, transparent); margin: 2rem 0; }
    .metric-container {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        text-align: center;
        transition: all 0.3s;
    }
    .metric-container:hover { border-color: #4a6cf7; transform: translateY(-3px); }
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
    .metric-label { font-size: 0.85rem; color: #8892b0; margin-top: 0.25rem; }
    .footer { text-align: center; color: #8892b0; padding: 1rem; border-top: 1px solid #1a1a2e; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Retention Strategies & Recommendations")
st.markdown("### Data-driven recommendations to reduce customer churn")

df = load_data()

total_customers = len(df)
churned = df[df['Churn'] == 'Yes'].shape[0]
churn_rate = (churned / total_customers) * 100
avg_tenure = df['tenure'].mean()

USD_TO_INR = 83
avg_monthly_value = 75 * USD_TO_INR
clv = 1800 * USD_TO_INR
savings_per_customer = 400 * USD_TO_INR
annual_savings = 180000 * USD_TO_INR
per_customer_increase = 450 * USD_TO_INR

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
st.subheader("🔍 Top Churn Drivers")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    contract_churn = df.groupby('Contract', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    fig = go.Figure(data=[go.Bar(
        x=contract_churn.index,
        y=contract_churn.values,
        marker=dict(color=contract_churn.values, colorscale='Reds', line=dict(color='#0a0a0a', width=2)),
        text=contract_churn.values.round(1),
        textposition='outside',
        textfont=dict(color='#ffffff')
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
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72], labels=['0-12', '13-24', '25-48', '49-72'])
    tenure_churn = df.groupby('tenure_group', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    fig = go.Figure(data=[go.Bar(
        x=tenure_churn.index,
        y=tenure_churn.values,
        marker=dict(color=tenure_churn.values, colorscale='Oranges', line=dict(color='#0a0a0a', width=2)),
        text=tenure_churn.values.round(1),
        textposition='outside',
        textfont=dict(color='#ffffff')
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
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("💡 Actionable Strategies by Customer Segment")

high_risk_profile = {'Contract': 'Month-to-month', 'tenure': 6, 'MonthlyCharges': 95, 'OnlineSecurity': 'No', 'PaymentMethod': 'Electronic check', 'InternetService': 'Fiber optic', 'Partner': 'No', 'Dependents': 'No'}
medium_risk_profile = {'Contract': 'One year', 'tenure': 18, 'MonthlyCharges': 70, 'OnlineSecurity': 'No', 'PaymentMethod': 'Electronic check', 'InternetService': 'DSL', 'Partner': 'Yes', 'Dependents': 'No'}
low_risk_profile = {'Contract': 'Two year', 'tenure': 48, 'MonthlyCharges': 45, 'OnlineSecurity': 'Yes', 'PaymentMethod': 'Credit card', 'InternetService': 'DSL', 'Partner': 'Yes', 'Dependents': 'Yes'}

high_recs = get_interventions(high_risk_profile, 0.8)
medium_recs = get_interventions(medium_risk_profile, 0.55)
low_recs = get_interventions(low_risk_profile, 0.2)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="risk-card risk-high">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="font-size:1.5rem;">🔴</span>
            <span style="font-size:1.1rem; font-weight:600; color:#ff6b6b;">High Risk</span>
            <span style="margin-left:auto; background:rgba(255,107,107,0.2); padding:0.2rem 0.6rem; border-radius:1rem; font-size:0.75rem; color:#ff6b6b;">>70%</span>
        </div>
        <div style="margin-top:0.75rem; color:#8892b0; font-size:0.9rem;">
            <strong style="color:#ffffff;">Profile:</strong><br>
            • Month-to-month contract<br>• Tenure < 12 months<br>• Monthly charges > <br>• No online security
        </div>
        <div style="margin-top:0.75rem;">
            <div style="color:#ffffff; font-weight:600; font-size:0.9rem;">📋 Actions:</div>
            <div style="margin-top:0.5rem; font-size:0.9rem;">
    """, unsafe_allow_html=True)
    for rec in high_recs[:4]:
        st.markdown(f"""
        <div class="strategy-impact impact-high">✅ {rec['action']}</div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="risk-card risk-medium">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="font-size:1.5rem;">🟡</span>
            <span style="font-size:1.1rem; font-weight:600; color:#ff9f43;">Medium Risk</span>
            <span style="margin-left:auto; background:rgba(255,159,67,0.2); padding:0.2rem 0.6rem; border-radius:1rem; font-size:0.75rem; color:#ff9f43;">40-70%</span>
        </div>
        <div style="margin-top:0.75rem; color:#8892b0; font-size:0.9rem;">
            <strong style="color:#ffffff;">Profile:</strong><br>
            • One-year contract<br>• Tenure 12-24 months<br>• Missing add-on services<br>• Electronic check payment
        </div>
        <div style="margin-top:0.75rem;">
            <div style="color:#ffffff; font-weight:600; font-size:0.9rem;">📋 Actions:</div>
            <div style="margin-top:0.5rem; font-size:0.9rem;">
    """, unsafe_allow_html=True)
    for rec in medium_recs[:4]:
        st.markdown(f"""
        <div class="strategy-impact impact-medium">✅ {rec['action']}</div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="risk-card risk-low">
        <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="font-size:1.5rem;">🟢</span>
            <span style="font-size:1.1rem; font-weight:600; color:#4a6cf7;">Low Risk</span>
            <span style="margin-left:auto; background:rgba(74,108,247,0.2); padding:0.2rem 0.6rem; border-radius:1rem; font-size:0.75rem; color:#4a6cf7;"><40%</span>
        </div>
        <div style="margin-top:0.75rem; color:#8892b0; font-size:0.9rem;">
            <strong style="color:#ffffff;">Profile:</strong><br>
            • Two-year contract<br>• Tenure > 24 months<br>• Multiple services<br>• Auto-payment enabled
        </div>
        <div style="margin-top:0.75rem;">
            <div style="color:#ffffff; font-weight:600; font-size:0.9rem;">📋 Actions:</div>
            <div style="margin-top:0.5rem; font-size:0.9rem;">
    """, unsafe_allow_html=True)
    for rec in low_recs[:4]:
        st.markdown(f"""
        <div class="strategy-impact impact-low">✅ {rec['action']}</div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Business Impact & ROI")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div style="font-size:2.5rem; margin-bottom:0.5rem;">💵</div>
        <div class="metric-number">₹{avg_monthly_value:,.0f}</div>
        <div class="metric-label">Average Monthly Customer Value</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div style="font-size:2.5rem; margin-bottom:0.5rem;">💰</div>
        <div class="metric-number" style="background:linear-gradient(135deg,#4a6cf7,#6a4cf7); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">₹{clv:,.0f}</div>
        <div class="metric-label">Customer Lifetime Value (CLV)</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-container">
        <div style="font-size:2.5rem; margin-bottom:0.5rem;">📈</div>
        <div class="metric-number-green">₹{savings_per_customer:,.0f}</div>
        <div class="metric-label">Savings per Retained Customer</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("🎯 Retention Goals & Targets")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="strategy-card">
        <div class="strategy-icon">🎯</div>
        <div class="strategy-title">Reduce Churn by 10%</div>
        <div class="strategy-desc">Implement targeted retention campaigns for high-risk customers</div>
        <div style="margin-top:0.5rem;"><span class="strategy-impact impact-high">Annual Savings: ₹{annual_savings:,.0f}</span></div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="strategy-card">
        <div class="strategy-icon">⏱️</div>
        <div class="strategy-title">Increase Tenure by 6 Months</div>
        <div class="strategy-desc">Focus on early-stage customers with loyalty programs</div>
        <div style="margin-top:0.5rem;"><span class="strategy-impact impact-high">+₹{per_customer_increase:,} per customer</span></div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="strategy-card">
        <div class="strategy-icon">📅</div>
        <div class="strategy-title">Convert to 1-Year Contracts</div>
        <div class="strategy-desc">Incentivize month-to-month customers to switch</div>
        <div style="margin-top:0.5rem;"><span class="strategy-impact impact-high">-20% Churn Rate</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("💰 ROI Calculation")

col1, col2 = st.columns(2)
with col1:
    total_revenue = total_customers * (75 * 12) * USD_TO_INR
    revenue_lost = churned * (75 * 12) * USD_TO_INR
    potential_savings = revenue_lost * 0.10
    st.markdown(f"""
    <div class="strategy-card">
        <div class="strategy-title">📊 Annual Revenue Impact</div>
        <div style="margin-top:0.75rem;">
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #1a1a2e;">
                <span style="color:#8892b0;">Total Annual Revenue</span>
                <span style="color:#4a6cf7; font-weight:600;">₹{total_revenue:,.0f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #1a1a2e;">
                <span style="color:#8892b0;">Revenue Lost to Churn</span>
                <span style="color:#ff6b6b; font-weight:600;">₹{revenue_lost:,.0f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0;">
                <span style="color:#8892b0;">Potential Savings (10% churn reduction)</span>
                <span style="color:#2ecc71; font-weight:600;">₹{potential_savings:,.0f}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="strategy-card">
        <div class="strategy-title">📈 ROI Calculator</div>
        <div style="margin-top:0.75rem;">
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #1a1a2e;">
                <span style="color:#8892b0;">Customer Acquisition Cost</span>
                <span style="color:#ff9f43; font-weight:600;">₹41,500</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #1a1a2e;">
                <span style="color:#8892b0;">Retention Program Cost</span>
                <span style="color:#4a6cf7; font-weight:600;">₹8,300</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0;">
                <span style="color:#8892b0;">ROI per Customer</span>
                <span style="color:#2ecc71; font-weight:600;">₹33,200</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-top:2px solid #2a2a4a;">
                <span style="color:#8892b0; font-weight:600;">ROI Multiple</span>
                <span style="color:#f1c40f; font-size:1.2rem; font-weight:700;">5x</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div class="footer">
    🚀 Data-driven retention strategies | Powered by Machine Learning | 💰 All values in Indian Rupees (₹)
</div>
""", unsafe_allow_html=True)
