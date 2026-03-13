import streamlit as st
import pandas as pd
import pickle
import numpy as np

# -----------------------------
# Load Model and Feature List
# -----------------------------

model = pickle.load(open("artifacts/model.pkl", "rb"))
features = pickle.load(open("artifacts/model_feature.pkl", "rb"))

# -----------------------------
# Load Dataset
# -----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("artifacts/final_feature_dataset.csv")

df = load_data()

# -----------------------------
# App Title
# -----------------------------

st.title("Demand Forecasting & Inventory Optimization")

# -----------------------------
# Select Product
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

    input_data = latest_row.drop(
        ["units_sold", "date", "sku_id", "sku_name"],
        errors="ignore"
    )

    input_df = pd.DataFrame([input_data])

    input_df = input_df.reindex(columns=features, fill_value=0)

    predicted_demand = model.predict(input_df)[0]

    # Inventory calculation
    lead_time = 7
    z = 1.65
    demand_std = 2

    safety_stock = z * demand_std * np.sqrt(lead_time)

    reorder_point = predicted_demand + safety_stock

    # -----------------------------
    # Display Results
    # -----------------------------

    st.subheader("Prediction Result")

    st.write("Product:", sku)

    col1, col2, col3 = st.columns(3)

    col1.metric("Predicted Demand", round(predicted_demand,2))
    col2.metric("Safety Stock", round(safety_stock,2))
    col3.metric("Reorder Point", round(reorder_point,2))

    # -----------------------------
    # Reorder Decision
    # -----------------------------

    if current_stock < reorder_point:
        st.error("⚠ Reorder Product Immediately")
    else:
        st.success("Inventory Level is Safe")