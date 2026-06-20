"""
Model Validation Tests - Customer Churn Prediction
Tests the churn prediction model with different risk scenarios
"""

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_model_and_scaler():
    """Load the trained model and scaler."""
    # Try different paths
    possible_paths = [
        '../models/churn_pipeline.pkl',
        'models/churn_pipeline.pkl',
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'churn_pipeline.pkl')
    ]
    
    for model_path in possible_paths:
        scaler_path = model_path.replace('churn_pipeline.pkl', 'scaler.pkl')
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            print(f"✅ Found model at: {model_path}")
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler
    
    print("❌ Model not found! Please train the model first.")
    print("Checked paths:")
    for path in possible_paths:
        print(f"  - {path}")
    return None, None

def test_scenario(scenario_name, customer_data, model, scaler):
    """Test a scenario and return the prediction details."""
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
    
    # Risk level
    if probability >= 0.7:
        risk = "🔴 HIGH RISK"
        risk_color = "RED"
    elif probability >= 0.4:
        risk = "🟡 MEDIUM RISK"
        risk_color = "YELLOW"
    else:
        risk = "🟢 LOW RISK"
        risk_color = "GREEN"
    
    return {
        'scenario': scenario_name,
        'probability': probability,
        'prediction': 'Will Churn' if prediction == 1 else 'Will Stay',
        'risk_level': risk,
        'risk_color': risk_color,
        'churn_prediction': int(prediction)
    }

def test_high_risk_scenario(model, scaler):
    """Test High Risk scenario."""
    high_risk = {
        'gender': 'Male',
        'SeniorCitizen': 0,
        'Partner': 'No',
        'Dependents': 'No',
        'tenure': 6,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'No',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 95.0,
        'TotalCharges': 570.0
    }
    return test_scenario("🔴 HIGH RISK", high_risk, model, scaler)

def test_medium_risk_scenario(model, scaler):
    """Test Medium Risk scenario."""
    medium_risk = {
        'gender': 'Male',
        'SeniorCitizen': 0,
        'Partner': 'No',
        'Dependents': 'No',
        'tenure': 18,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'One year',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 70.0,
        'TotalCharges': 1260.0
    }
    return test_scenario("🟡 MEDIUM RISK", medium_risk, model, scaler)

def test_low_risk_scenario(model, scaler):
    """Test Low Risk scenario."""
    low_risk = {
        'gender': 'Male',
        'SeniorCitizen': 0,
        'Partner': 'No',
        'Dependents': 'No',
        'tenure': 48,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'TechSupport': 'Yes',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'No',
        'Contract': 'Two year',
        'PaperlessBilling': 'No',
        'PaymentMethod': 'Credit card',
        'MonthlyCharges': 45.0,
        'TotalCharges': 2160.0
    }
    return test_scenario("🟢 LOW RISK", low_risk, model, scaler)

def test_default_scenario(model, scaler):
    """Test Default scenario (what you see in the app)."""
    default = {
        'gender': 'Male',
        'SeniorCitizen': 0,
        'Partner': 'No',
        'Dependents': 'No',
        'tenure': 36,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'TechSupport': 'Yes',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'No',
        'Contract': 'Two year',
        'PaperlessBilling': 'No',
        'PaymentMethod': 'Credit card',
        'MonthlyCharges': 50.0,
        'TotalCharges': 1800.0
    }
    return test_scenario("📊 DEFAULT (App)", default, model, scaler)

def run_all_tests():
    """Run all test scenarios."""
    print("="*70)
    print("🧪 CUSTOMER CHURN MODEL VALIDATION TESTS")
    print("="*70)
    
    # Load model
    model, scaler = load_model_and_scaler()
    if model is None:
        print("\n💡 Please train the model first by running:")
        print("   python src/train.py")
        return
    
    print("\n📊 Running Test Scenarios:")
    print("-"*70)
    
    # Run all tests
    results = []
    results.append(test_high_risk_scenario(model, scaler))
    results.append(test_medium_risk_scenario(model, scaler))
    results.append(test_low_risk_scenario(model, scaler))
    results.append(test_default_scenario(model, scaler))
    
    # Print results
    print("\n📈 TEST RESULTS:")
    print("-"*70)
    
    for result in results:
        print(f"\n{result['scenario']}:")
        print(f"  Churn Probability: {result['probability']:.2%}")
        print(f"  Prediction: {result['prediction']}")
        print(f"  Risk Level: {result['risk_level']}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY:")
    print("-"*70)
    
    high_risk_count = sum(1 for r in results if 'HIGH RISK' in r['risk_level'])
    medium_risk_count = sum(1 for r in results if 'MEDIUM RISK' in r['risk_level'])
    low_risk_count = sum(1 for r in results if 'LOW RISK' in r['risk_level'])
    
    print(f"  High Risk Scenarios: {high_risk_count}")
    print(f"  Medium Risk Scenarios: {medium_risk_count}")
    print(f"  Low Risk Scenarios: {low_risk_count}")
    print(f"  Total Tests Run: {len(results)}")
    
    # Validation
    print("\n✅ VALIDATION RESULTS:")
    print("-"*70)
    
    passed = 0
    total = 3
    
    if high_risk_count >= 1:
        print("  ✅ Model correctly identifies HIGH RISK (probability > 70%)")
        passed += 1
    else:
        print("  ⚠️ Model struggling with HIGH RISK detection")
    
    if medium_risk_count >= 1:
        print("  ✅ Model correctly identifies MEDIUM RISK (probability 40-70%)")
        passed += 1
    else:
        print("  ⚠️ Model struggling with MEDIUM RISK detection")
    
    if low_risk_count >= 1:
        print("  ✅ Model correctly identifies LOW RISK (probability < 40%)")
        passed += 1
    else:
        print("  ⚠️ Model struggling with LOW RISK detection")
    
    print("\n" + "-"*70)
    print(f"  Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("  🎉 ALL TESTS PASSED! Model is working correctly.")
    else:
        print("  ⚠️ Some tests failed. Model may need tuning.")
    
    print("\n" + "="*70)
    print("🏁 Tests Complete!")
    print("="*70)

if __name__ == "__main__":
    run_all_tests()