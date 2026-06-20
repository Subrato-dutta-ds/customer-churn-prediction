import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_model():
    """Load the trained pipeline."""
    return joblib.load('models/churn_pipeline.pkl')

def load_scaler():
    """Load the scaler."""
    return joblib.load('models/scaler.pkl')

def predict_churn(customer_data):
    """Predict churn probability for a single customer."""
    model = load_model()
    scaler = load_scaler()
    
    df = pd.DataFrame([customer_data])
    
    categorical_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                       'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                       'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                       'PaperlessBilling', 'PaymentMethod']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    
    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    
    probability = model.predict_proba(df)[0][1]
    prediction = model.predict(df)[0]
    
    if probability >= 0.7:
        risk_level = 'High Risk 🚨'
    elif probability >= 0.4:
        risk_level = 'Medium Risk ⚠️'
    else:
        risk_level = 'Low Risk ✅'
    
    return {
        'churn_prediction': int(prediction),
        'churn_probability': float(probability),
        'risk_level': risk_level
    }