import os
import streamlit as st
import pandas as pd
import pickle
import numpy as np

# -----------------------------
# File Paths (Cloud-friendly)
# -----------------------------

MODEL_PATH = "artifacts/model.pkl"
FEATURE_PATH = "artifacts/model_feature.pkl"
DATA_PATH = "artifacts/final_feature_dataset.csv"

# -----------------------------
# Helper Function: Load Pickle Safely
# -----------------------------

def load_pickle(path, description="file"):
    if not os.path.exists(path):
        st.error(f"{description} not found at: {path}")
        st.stop()
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Failed to load {description}: {e}")
        st.stop()

# -----------------------------
# Load Model and Feature List
# -----------------------------

model = load_pickle(MODEL_PATH, "Model")
features = load_pickle(FEATURE_PATH, "Feature list")

# -----------------------------
# Load Dataset
# -----------------------------

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Dataset not found at: {DATA_PATH}")
        st.stop()
    return pd.read_csv(DATA_PATH)

df = load_data()

# -----------------------------
# App Title
# -----------------------------

st.title("Demand Forecasting & Inventory Optimization")

# -----------------------------
# Select Product (SKU)
# -----------------------------

sku = st.selectbox(
    "Select Product (SKU)",
    df["sku_name"].unique()
)

# -----------------------------
# Get Latest Product Data
# -----------------------------

product_data = df[df["sku_name"] == sku]
latest_row = product_data.iloc[-1]

# -----------------------------
# User Input
# -----------------------------

current_stock = st.number_input("Current Inventory Level", min_value=0)

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Demand"):

    # Prepare input data
    input_data = latest_row.drop(
        ["units_sold", "date", "sku_id", "sku_name"],
        errors="ignore"
    )
    input_df = pd.DataFrame([input_data])
    input_df = input_df.reindex(columns=features, fill_value=0)

    # Make prediction
    try:
        predicted_demand = model.predict(input_df)[0]
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

    # Inventory calculations
    lead_time = 7  # days
    z = 1.65       # 95% service level
    demand_std = 2

    safety_stock = z * demand_std * np.sqrt(lead_time)
    reorder_point = predicted_demand + safety_stock

    # -----------------------------
    # Display Results
    # -----------------------------

    st.subheader("Prediction Result")
    st.write("Product:", sku)

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted Demand", round(predicted_demand, 2))
    col2.metric("Safety Stock", round(safety_stock, 2))
    col3.metric("Reorder Point", round(reorder_point, 2))

    # -----------------------------
    # Reorder Decision
    # -----------------------------

    if current_stock < reorder_point:
        st.error("⚠ Reorder Product Immediately")
    else:
        st.success("Inventory Level is Safe")