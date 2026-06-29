import sys
import os

# Absolute path to your project root (works every time)
project_root = r"C:\Users\subrato dutta\Desktop\All_data_science_projects\Customer_churn_prediction"
sys.path.insert(0, project_root)

# Now import Streamlit and other libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data import load_data   

# ... rest of your code
st.set_page_config(page_title="Dashboard", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #4a6cf7;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(135deg, #4a6cf7, #6a4cf7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8892b0;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
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
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #0d0d1a !important;
    }
    
    /* Text */
    .stMarkdown {
        color: #ccd6f6 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #4a6cf7, #6a4cf7, transparent);
        margin: 2rem 0;
    }
    
    /* KPI grid */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 768px) {
        .kpi-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Churn Analytics Dashboard")
st.markdown("### 📊 Overview of customer churn metrics and insights")

# Load data
from src.data import load_data

df = load_data()

# KPI Cards
st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_customers = len(df)
churned = df[df['Churn'] == 'Yes'].shape[0]
churn_rate = (churned / total_customers) * 100
avg_tenure = df['tenure'].mean()

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👥 Total Customers</div>
        <div class="metric-value">{total_customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚠️ Churned Customers</div>
        <div class="metric-value" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{churned:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📈 Churn Rate</div>
        <div class="metric-value" style="background: linear-gradient(135deg, #ff9f43, #ee5a24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{churn_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⏱️ Avg Tenure</div>
        <div class="metric-value" style="background: linear-gradient(135deg, #4a6cf7, #6a4cf7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{avg_tenure:.1f} mo</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Churn Distribution")
    
    churn_counts = df['Churn'].value_counts()
    colors = ['#4a6cf7', '#ff6b6b']
    
    fig = go.Figure(data=[go.Pie(
        labels=churn_counts.index,
        values=churn_counts.values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color='#0a0a0a', width=2)),
        textinfo='label+percent',
        textfont=dict(color='#ffffff', size=14),
        hoverinfo='label+value+percent'
    )])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Churn by Contract Type")
    
    contract_churn = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    colors_contract = ['#ff6b6b', '#ff9f43', '#4a6cf7']
    
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
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(title='Contract Type', color='#8892b0'),
        yaxis=dict(title='Churn Rate (%)', color='#8892b0', range=[0, 80]),
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Bottom row - 3 charts
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🌐 Churn by Internet Service")
    
    internet_churn = df.groupby('InternetService')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    
    fig = go.Figure(data=[go.Bar(
        x=internet_churn.index,
        y=internet_churn.values,
        marker=dict(
            color=internet_churn.values,
            colorscale='Oranges',
            line=dict(color='#0a0a0a', width=2)
        ),
        text=internet_churn.values.round(1),
        textposition='outside',
        textfont=dict(color='#ffffff', size=12)
    )])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(title='Internet Service', color='#8892b0'),
        yaxis=dict(title='Churn Rate (%)', color='#8892b0', range=[0, 60]),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💳 Churn by Payment Method")
    
    payment_churn = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
    
    fig = go.Figure(data=[go.Bar(
        x=payment_churn.index,
        y=payment_churn.values,
        marker=dict(
            color=payment_churn.values,
            colorscale='Purples',
            line=dict(color='#0a0a0a', width=2)
        ),
        text=payment_churn.values.round(1),
        textposition='outside',
        textfont=dict(color='#ffffff', size=12)
    )])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(title='Payment Method', color='#8892b0'),
        yaxis=dict(title='Churn Rate (%)', color='#8892b0', range=[0, 50]),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Tenure by Churn")
    
    fig = go.Figure()
    
    # Add traces for No Churn and Churn
    fig.add_trace(go.Box(
        y=df[df['Churn'] == 'No']['tenure'],
        name='No Churn',
        marker_color='#4a6cf7',
        boxmean='sd'
    ))
    
    fig.add_trace(go.Box(
        y=df[df['Churn'] == 'Yes']['tenure'],
        name='Churn',
        marker_color='#ff6b6b',
        boxmean='sd'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(title='Churn Status', color='#8892b0'),
        yaxis=dict(title='Tenure (months)', color='#8892b0'),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8892b0; padding: 1rem;'>
    Built with ❤️ using Streamlit, Plotly & Python | Data-driven insights for customer retention
</div>
""", unsafe_allow_html=True)