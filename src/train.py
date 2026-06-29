import joblib
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🚀 STARTING MODEL TRAINING...")
print("="*60)

# Load and clean data
df = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df = df.drop('customerID', axis=1)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
print("✅ Data loaded and cleaned")

# Define categorical columns
categorical_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                   'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                   'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                   'PaperlessBilling', 'PaymentMethod']

# Encode categorical and save encoders
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Save encoders
with open('models/encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)
print("✅ Encoders saved to models/encoders.pkl")

# Split data
X = df.drop('Churn', axis=1)
y = df['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"✅ Training set: {len(X_train)} rows, Test set: {len(X_test)} rows")

# Scale numerical features
scaler = StandardScaler()
numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test_scaled[numerical_cols] = scaler.transform(X_test[numerical_cols])

# Apply SMOTE (explicitly)
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
print(f"✅ SMOTE applied: {len(X_train_resampled)} samples (was {len(X_train_scaled)})")

# Train model
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
model.fit(X_train_resampled, y_train_resampled)
print("✅ Model trained")

# Evaluate
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"📊 Accuracy: {accuracy:.3f}")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(model, 'models/churn_pipeline.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("✅ Model saved to models/churn_pipeline.pkl")
print("✅ Scaler saved to models/scaler.pkl")
print("="*60)
print("🎉 TRAINING COMPLETE!")
print("="*60)