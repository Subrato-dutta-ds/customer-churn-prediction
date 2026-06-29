import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load and cache the dataset."""
    return pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')