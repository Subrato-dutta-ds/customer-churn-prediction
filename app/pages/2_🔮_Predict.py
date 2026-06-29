import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from src.data import load_data

st.set_page_config(page_title="Churn Predictor", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #0d0d1a !important;
        border-right: 1px solid #1a1a2e;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Input labels */
    .stSelectbox label, .stSlider label, .stNumberInput label {
        color: #ccd6f6 !important;
        font-weight: 500 !important;
    }
    
    /* Input fields */
    .stSelectbox > div > div, .stNumberInput > div > div > input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #2a2a4a !important;
        border-radius: 0.5rem !important;
    }
    
    .stSelectbox > div > div:hover, .stNumberInput > div > div > input:hover {
        border-color: #4a6cf7 !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #2a2a4a !important;
    }
    .stSlider > div > div > div > div {
        background-color: #4a6cf7 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4a6cf7, #6a4cf7) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(74, 108, 247, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(74, 108, 247, 0.5) !important;
    }
    
    /* Prediction result container */
    .result-container {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 2rem;
        border-radius: 1.5rem;
        border: 1px solid #2a2a4a;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-top: 1rem;
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #2a2a4a;
        text-align: center;
        transition: all 0.3s;
    }
    .prediction-card:hover {
        transform: translateY(-5px);
        border-color: #4a6cf7;
    }
    
    .prediction-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .prediction-label {
        font-size: 0.9rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .risk-high {
        color: #ff6b6b;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .risk-medium {
        color: #ff9f43;
        background: linear-gradient(135deg, #ff9f43, #f0932b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .risk-low {
        color: #4a6cf7;
        background: linear-gradient(135deg, #4a6cf7, #6a4cf7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .recommendation-item {
        background: linear-gradient(145deg, #0d0d1a, #1a1a2e);
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #4a6cf7;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .recommendation-item:hover {
        border-left-color: #6a4cf7;
        background: linear-gradient(145deg, #1a1a2e, #16213e);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #4a6cf7, #6a4cf7, transparent);
        margin: 2rem 0;
    }
    
    /* Risk indicator cards */
    .risk-indicator {
        padding: 1rem;
        border-radius: 0.75rem;
        text-align: center;
        margin: 0.25rem 0;
        transition: all 0.3s;
    }
    .risk-indicator:hover {
        transform: scale(1.02);
    }
    .risk-indicator-high {
        background: rgba(255, 107, 107, 0.15);
        border: 1px solid rgba(255, 107, 107, 0.3);
    }
    .risk-indicator-medium {
        background: rgba(255, 159, 67, 0.15);
        border: 1px solid rgba(255, 159, 67, 0.3);
    }
    .risk-indicator-low {
        background: rgba(74, 108, 247, 0.15);
        border: 1px solid rgba(74, 108, 247, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("🔮 Customer Churn Predictor")
st.markdown("### Enter customer details to predict churn probability")

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('models/churn_pipeline.pkl')
        scaler = joblib.load('models/scaler.pkl')
        return model, scaler
    except:
        return None, None

model, scaler = load_model()

if model is None:
    st.error("⚠️ Model not found! Please train the model first.")
    st.stop()

# Create columns for layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📝 Customer Details")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["👤 Personal", "📱 Services", "💳 Billing"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"], index=0)
            senior_citizen = st.selectbox("Senior Citizen", [0, 1], index=0)
            partner = st.selectbox("Partner", ["Yes", "No"], index=1)
        with col2:
            dependents = st.selectbox("Dependents", ["Yes", "No"], index=1)
            tenure = st.slider("Tenure (months)", 0, 72, 36, help="Longer tenure = Lower risk")
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], index=2, 
                                   help="Two year = Lowest risk, Month-to-month = Highest risk")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            phone_service = st.selectbox("Phone Service", ["Yes", "No"], index=0)
            multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"], index=1)
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], index=0)
        with col2:
            online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"], index=0,
                                          help="Having Online Security = Lower risk")
            online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"], index=0)
            device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"], index=0)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"], index=1)
            payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], index=3,
                                         help="Credit card = Lower risk, Electronic check = Higher risk")
        with col2:
            monthly_charges = st.number_input("Monthly Charges ($)", 20.0, 150.0, 50.0, step=5.0,
                                             help="Lower charges = Lower risk")
            tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"], index=0)
            streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"], index=0)

with col_right:
    st.markdown("### 🎯 Actions")
    
    # Build customer data
    customer_data = {
        'gender': gender,
        'SeniorCitizen': senior_citizen,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone_service,
        'MultipleLines': multiple_lines,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'TechSupport': tech_support,
        'StreamingTV': streaming_tv,
        'StreamingMovies': 'No',
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': monthly_charges * tenure if tenure > 0 else 50
    }
    
    predict_btn = st.button("🚀 Predict Churn Risk", use_container_width=True)
    
    # Risk Level Guide
    st.markdown("---")
    st.markdown("### 📊 Risk Level Guide")
    st.markdown("""
    <div class="risk-indicator risk-indicator-high">
        <span style="font-size: 1.2rem;">🔴</span>
        <strong style="color: #ff6b6b;">High Risk</strong>
        <div style="font-size: 0.8rem; color: #8892b0;">Probability > 70%</div>
        <div style="font-size: 0.75rem; color: #8892b0; margin-top: 0.25rem;">
            Month-to-month • Tenure &lt; 12 • Charges &gt; $80
        </div>
    </div>
    <div class="risk-indicator risk-indicator-medium">
        <span style="font-size: 1.2rem;">🟡</span>
        <strong style="color: #ff9f43;">Medium Risk</strong>
        <div style="font-size: 0.8rem; color: #8892b0;">Probability 40-70%</div>
        <div style="font-size: 0.75rem; color: #8892b0; margin-top: 0.25rem;">
            One year • Tenure 12-24 • Charges $60-80
        </div>
    </div>
    <div class="risk-indicator risk-indicator-low">
        <span style="font-size: 1.2rem;">🟢</span>
        <strong style="color: #4a6cf7;">Low Risk</strong>
        <div style="font-size: 0.8rem; color: #8892b0;">Probability &lt; 40%</div>
        <div style="font-size: 0.75rem; color: #8892b0; margin-top: 0.25rem;">
            Two year • Tenure &gt; 24 • Charges &lt; $60
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Quick Scenarios")
    
    # Quick scenario buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔴 High Risk", use_container_width=True):
            # Set High Risk scenario
            tenure = 6
            contract = "Month-to-month"
            monthly_charges = 95
            online_security = "No"
            payment_method = "Electronic check"
            st.rerun()
    
    with col2:
        if st.button("🟡 Medium Risk", use_container_width=True):
            # Set Medium Risk scenario
            tenure = 18
            contract = "One year"
            monthly_charges = 70
            online_security = "No"
            payment_method = "Electronic check"
            st.rerun()
    
    with col3:
        if st.button("🟢 Low Risk", use_container_width=True):
            # Set Low Risk scenario
            tenure = 48
            contract = "Two year"
            monthly_charges = 45
            online_security = "Yes"
            payment_method = "Credit card"
            st.rerun()

# Prediction results
if predict_btn:
    try:
        # Convert to DataFrame
        df = pd.DataFrame([customer_data])
        
        # Encode categorical variables
        categorical_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                           'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                           'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                           'PaperlessBilling', 'PaymentMethod']
        
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
        
        # Scale numerical features
        numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
        df[numerical_cols] = scaler.transform(df[numerical_cols])
        
        # Predict
        probability = model.predict_proba(df)[0][1]
        prediction = model.predict(df)[0]
        
        # Determine risk level
        if probability >= 0.7:
            risk_class = "risk-high"
            risk_emoji = "🔴"
            risk_text = "High Risk"
            risk_color = "#ff6b6b"
            bg_color = "linear-gradient(135deg, #1a0a0a, #2a0a0a)"
            border_color = "#ff6b6b"
            risk_description = "Customer is very likely to churn. Immediate action required!"
        elif probability >= 0.4:
            risk_class = "risk-medium"
            risk_emoji = "🟡"
            risk_text = "Medium Risk"
            risk_color = "#ff9f43"
            bg_color = "linear-gradient(135deg, #1a150a, #2a1a0a)"
            border_color = "#ff9f43"
            risk_description = "Customer shows signs of potential churn. Proactive engagement needed."
        else:
            risk_class = "risk-low"
            risk_emoji = "🟢"
            risk_text = "Low Risk"
            risk_color = "#4a6cf7"
            bg_color = "linear-gradient(135deg, #0a1a0a, #0a2a0a)"
            border_color = "#4a6cf7"
            risk_description = "Customer is loyal and unlikely to churn. Maintain good relationship."
        
        # Display results
        st.markdown("---")
        st.markdown("## 📊 Prediction Results")
        
        # Risk Summary Card
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1.5rem; border-radius: 1rem; border: 2px solid {border_color}; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                <div>
                    <div style="font-size: 0.9rem; color: #8892b0;">Risk Assessment</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: {risk_color};">
                        {risk_emoji} {risk_text}
                    </div>
                    <div style="font-size: 0.9rem; color: #8892b0; margin-top: 0.25rem;">{risk_description}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; color: #8892b0;">Churn Probability</div>
                    <div style="font-size: 3rem; font-weight: 700; color: {risk_color};">{probability:.1%}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.9rem; color: #8892b0;">Prediction</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: {'#ff6b6b' if prediction == 1 else '#4a6cf7'};">
                        {risk_emoji} {'Will Churn' if prediction == 1 else 'Will Stay'}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Three columns for detailed metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="prediction-card" style="background: {bg_color}; border-color: {border_color};">
                <div class="prediction-label">📊 Prediction</div>
                <div class="prediction-value" style="color: {'#ff6b6b' if prediction == 1 else '#4a6cf7'};">
                    {risk_emoji} {'⚠️ Churn' if prediction == 1 else '✅ No Churn'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="prediction-card" style="background: {bg_color}; border-color: {border_color};">
                <div class="prediction-label">📈 Probability</div>
                <div class="prediction-value {risk_class}">
                    {probability:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="prediction-card" style="background: {bg_color}; border-color: {border_color};">
                <div class="prediction-label">🎯 Risk Level</div>
                <div class="prediction-value {risk_class}">
                    {risk_emoji} {risk_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("---")
        st.markdown("### 💡 Retention Recommendations")
        
        recommendations = []
        if contract == "Month-to-month":
            recommendations.append("📅 Offer 10% discount to switch to 1-year contract")
        if tenure < 12:
            recommendations.append("🎁 Send welcome rewards or loyalty bonus")
        if monthly_charges > 80:
            recommendations.append("💰 Offer $10/month discount for 6 months")
        if online_security == "No":
            recommendations.append("🔒 Offer free Online Security for 3 months")
        if payment_method == "Electronic check":
            recommendations.append("💳 Offer $5 credit to switch to auto-pay")
        if probability > 0.7:
            recommendations.append("📞 Priority support call within 24 hours")
        if internet_service == "Fiber optic" and online_security == "No":
            recommendations.append("🔐 Free fiber internet upgrade for 1 month")
        if partner == "No" and dependents == "No":
            recommendations.append("👥 Offer family plan or referral bonus")
        
        if recommendations:
            for rec in recommendations:
                st.markdown(f"""
                <div class="recommendation-item">
                    {rec}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No immediate interventions needed. Customer is low risk.")
        
        # Risk Factors Analysis
        st.markdown("---")
        st.markdown("### 🔍 Risk Factors Analysis")
        
        risk_factors = []
        if contract == "Month-to-month":
            risk_factors.append("⚠️ Month-to-month contract (increases risk)")
        elif contract == "One year":
            risk_factors.append("ℹ️ One year contract (moderate risk)")
        else:
            risk_factors.append("✅ Two year contract (low risk)")
        
        if tenure < 12:
            risk_factors.append("⚠️ Short tenure (< 12 months) - high risk")
        elif tenure < 24:
            risk_factors.append("ℹ️ Moderate tenure (12-24 months) - medium risk")
        else:
            risk_factors.append("✅ Long tenure (> 24 months) - low risk")
        
        if monthly_charges > 80:
            risk_factors.append("⚠️ High monthly charges (> $80) - increases risk")
        elif monthly_charges > 60:
            risk_factors.append("ℹ️ Moderate charges ($60-80) - medium risk")
        else:
            risk_factors.append("✅ Low monthly charges (< $60) - low risk")
        
        if online_security == "No":
            risk_factors.append("⚠️ No Online Security - missing protection")
        else:
            risk_factors.append("✅ Online Security enabled - good")
        
        if payment_method == "Electronic check":
            risk_factors.append("⚠️ Electronic check payment - high risk")
        elif payment_method == "Credit card":
            risk_factors.append("✅ Credit card payment - low risk")
        
        for factor in risk_factors:
            st.markdown(f"""
            <div class="recommendation-item">
                {factor}
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error making prediction: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8892b0; padding: 1rem;'>
    🚀 Powered by Machine Learning | Click scenario buttons to test different risk levels
</div>
""", unsafe_allow_html=True)