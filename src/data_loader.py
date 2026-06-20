import pandas as pd
import numpy as np

def load_data(filepath):
    """Load the Telco Customer Churn dataset."""
    return pd.read_csv(filepath)

def clean_data(df):
    """Clean and preprocess the dataset."""
    df_clean = df.copy()
    df_clean = df_clean.drop('customerID', axis=1)
    df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'], errors='coerce')
    df_clean['TotalCharges'].fillna(df_clean['TotalCharges'].median(), inplace=True)
    df_clean['Churn'] = df_clean['Churn'].map({'Yes': 1, 'No': 0})
    return df_clean