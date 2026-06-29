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

st.set_page_config(page_title="Dashboard", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    .metric-card {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        text-align: center;
        transition: all 0.3s;
    }
    .metric-card:hover { border-color: #4a6cf7; transform: translateY(-3px); }
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a6cf7, #6a4cf7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-number-red {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
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
    .metric-delta { font-size: 0.8rem; margin-top: 0.25rem; }
    .delta-positive { color: #2ecc71; }
    .delta-negative { color: #ff6b6b; }
    hr { border: none; height: 2px; background: linear-gradient(to right, #4a6cf7, #6a4cf7, transparent); margin: 2rem 0; }
    .chart-container {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        margin: 0.5rem 0;
    }
    .footer { text-align: center; color: #8892b0; padding: 1rem; border-top: 1px solid #1a1a2e; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Churn Analytics Dashboard")
st.markdown("### Overview of customer churn metrics and insights")

df = load_data()

total_customers = len(df)
churned = df[df['Churn'] == 'Yes'].shape[0]
churn_rate = (churned / total_customers) * 100
avg_tenure = df['tenure'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{total_customers:,}</div>
        <div class="metric-label">👥 Total Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number-red">{churned:,}</div>
        <div class="metric-label">⚠️ Churned Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number-red">{churn_rate:.1f}%</div>
        <div class="metric-label">📈 Churn Rate</div>
        <div class="metric-delta delta-negative">↓ -0.5%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number-green">{(100 - churn_rate):.1f}%</div>
        <div class="metric-label">✅ Retention Rate</div>
        <div class="metric-delta delta-positive">↑ +0.5%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    churn_counts = df['Churn'].value_counts()
    fig = px.pie(values=churn_counts.values, names=churn_counts.index, title="Churn Distribution",
                 color_discrete_sequence=['#2ecc71', '#e74c3c'])
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    contract_churn = df.groupby('Contract', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    fig = px.bar(x=contract_churn.index, y=contract_churn.values,
                 title="Churn by Contract Type", labels={'x': 'Contract', 'y': 'Churn Rate (%)'},
                 color=contract_churn.values, color_continuous_scale='Reds')
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    internet_churn = df.groupby('InternetService', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    fig = px.bar(x=internet_churn.index, y=internet_churn.values,
                 title="Churn by Internet Service", labels={'x': 'Internet Service', 'y': 'Churn Rate (%)'},
                 color=internet_churn.values, color_continuous_scale='Oranges')
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    payment_churn = df.groupby('PaymentMethod', observed=False)['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    fig = px.bar(x=payment_churn.index, y=payment_churn.values,
                 title="Churn by Payment Method", labels={'x': 'Payment Method', 'y': 'Churn Rate (%)'},
                 color=payment_churn.values, color_continuous_scale='Purples')
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = px.box(df, x='Churn', y='tenure', title="Tenure by Churn",
                 color='Churn', color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'})
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="footer">Built with ❤️ using Streamlit, Plotly & Python</div>', unsafe_allow_html=True)
