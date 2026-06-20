import streamlit as st

st.set_page_config(
    page_title="Customer Churn Prediction System",
    page_icon="🚨",
    layout="wide"
)

# ============== FORCE DARK THEME ==============
st.markdown("""
<style>
    /* Force dark background on everything */
    .stApp, .main, .block-container, .css-1d391kg, [data-testid="stAppViewContainer"],
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    /* Main content area */
    .st-emotion-cache-1r6slb0, .st-emotion-cache-1y4p8pa {
        background-color: #0a0a0a !important;
    }
    
    /* All text */
    body, p, div, span, li, label, .stMarkdown, .stText, .stInfo, .stSuccess {
        color: #ffffff !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"], .css-1d391kg, .st-emotion-cache-1d391kg {
        background-color: #0d0d1a !important;
        border-right: 1px solid #2a2a4a !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4a6cf7, #6a4cf7) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
    }
    
    /* Cards */
    .hero-card {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e) !important;
        padding: 2rem !important;
        border-radius: 1.5rem !important;
        border: 1px solid #2a2a4a !important;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e) !important;
        padding: 1.5rem !important;
        border-radius: 1rem !important;
        border: 1px solid #2a2a4a !important;
        text-align: center !important;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e) !important;
        padding: 1.5rem !important;
        border-radius: 1rem !important;
        border: 1px solid #2a2a4a !important;
        text-align: center !important;
    }
    
    .metric-number {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #4a6cf7, #6a4cf7) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .metric-number-red {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .metric-number-green {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .metric-label {
        font-size: 0.85rem !important;
        color: #8892b0 !important;
        margin-top: 0.25rem !important;
    }
    
    .metric-delta {
        font-size: 0.8rem !important;
        margin-top: 0.25rem !important;
    }
    
    .delta-positive {
        color: #2ecc71 !important;
    }
    
    .delta-negative {
        color: #ff6b6b !important;
    }
    
    .footer {
        text-align: center !important;
        color: #8892b0 !important;
        padding: 1rem !important;
        border-top: 1px solid #1a1a2e !important;
        margin-top: 2rem !important;
    }
    
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(to right, #4a6cf7, #6a4cf7, transparent) !important;
        margin: 2rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============== CONTENT ==============

st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0; color: #ffffff;">🚨 Customer Churn Prediction System</h1>
    <p style="color: #8892b0; font-size: 1.2rem;">End-to-End Machine Learning Solution for Customer Retention</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="hero-card">
        <h2 style="color: #ffffff;">📊 Predict, Analyze, and Act</h2>
        <p style="color: #8892b0; font-size: 1.05rem; line-height: 1.6;">
            This system helps you identify customers at risk of churning and provides actionable 
            recommendations to retain them.
        </p>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
            <span style="background: rgba(74,108,247,0.15); padding: 0.3rem 1rem; border-radius: 2rem; border: 1px solid rgba(74,108,247,0.3); color: #4a6cf7; font-size: 0.85rem;">🔮 Predict churn</span>
            <span style="background: rgba(46,204,113,0.15); padding: 0.3rem 1rem; border-radius: 2rem; border: 1px solid rgba(46,204,113,0.3); color: #2ecc71; font-size: 0.85rem;">📊 Analyze metrics</span>
            <span style="background: rgba(255,159,67,0.15); padding: 0.3rem 1rem; border-radius: 2rem; border: 1px solid rgba(255,159,67,0.3); color: #ff9f43; font-size: 0.85rem;">💡 Get recommendations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="hero-card" style="text-align: center;">
        <h3 style="color: #ffffff;">🚀 Quick Links</h3>
        <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1rem;">
            <div style="color: #4a6cf7; background: rgba(74,108,247,0.1); padding: 0.5rem; border-radius: 0.5rem; border: 1px solid rgba(74,108,247,0.2);">📊 Dashboard</div>
            <div style="color: #4a6cf7; background: rgba(74,108,247,0.1); padding: 0.5rem; border-radius: 0.5rem; border: 1px solid rgba(74,108,247,0.2);">🔮 Predict</div>
            <div style="color: #4a6cf7; background: rgba(74,108,247,0.1); padding: 0.5rem; border-radius: 0.5rem; border: 1px solid rgba(74,108,247,0.2);">📈 Recommendations</div>
        </div>
        <p style="color: #8892b0; font-size: 0.8rem; margin-top: 0.75rem;">Use the sidebar to navigate</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader("📊 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">7,043</div>
        <div class="metric-label">👥 Total Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number-red">26.5%</div>
        <div class="metric-label">📈 Churn Rate</div>
        <div class="metric-delta delta-negative">↓ -0.5%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number-red">1,869</div>
        <div class="metric-label">⚠️ Churned Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number-green">73.5%</div>
        <div class="metric-label">✅ Retention Rate</div>
        <div class="metric-delta delta-positive">↑ +0.5%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader("⚙️ How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📝</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">1️⃣ Input Customer Data</div>
        <div style="font-size: 0.9rem; color: #8892b0; margin-top: 0.5rem;">Enter customer details through the sidebar form in the Predict page.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">2️⃣ Get Prediction</div>
        <div style="font-size: 0.9rem; color: #8892b0; margin-top: 0.5rem;">The ML model predicts churn probability and risk level instantly.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💡</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #ffffff;">3️⃣ Take Action</div>
        <div style="font-size: 0.9rem; color: #8892b0; margin-top: 0.5rem;">Receive personalized retention recommendations based on risk level.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit, Scikit-learn, and Plotly<br>
    <span style="font-size: 0.8rem; color: #64748b;">💰 All prices in Indian Rupees (₹)</span>
</div>
""", unsafe_allow_html=True)