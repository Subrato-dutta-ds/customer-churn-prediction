import joblib
import pickle
import pandas as pd

def load_model_and_encoders():
    """Load model, scaler, and fitted encoders."""
    model = joblib.load('models/churn_pipeline.pkl')
    scaler = joblib.load('models/scaler.pkl')
    with open('models/encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    return model, scaler, encoders

def predict_churn(customer_data):
    """
    Predict churn probability for a single customer.
    
    Args:
        customer_data (dict): Feature values for a customer.
    
    Returns:
        dict: Prediction details.
    """
    model, scaler, encoders = load_model_and_encoders()
    df = pd.DataFrame([customer_data])
    
    # Use saved encoders (transform only)
    categorical_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                       'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                       'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                       'PaperlessBilling', 'PaymentMethod']
    
    for col in categorical_cols:
        df[col] = encoders[col].transform(df[col])
    
    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    
    probability = model.predict_proba(df)[0][1]
    prediction = model.predict(df)[0]
    
    # Risk level
    if probability >= 0.7:
        risk = 'High Risk 🚨'
    elif probability >= 0.4:
        risk = 'Medium Risk ⚠️'
    else:
        risk = 'Low Risk ✅'
    
    return {
        'churn_prediction': int(prediction),
        'churn_probability': float(probability),
        'risk_level': risk
    }