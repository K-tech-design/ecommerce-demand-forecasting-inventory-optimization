from flask import Flask, request, jsonify
import pandas as pd

from src.ecommerce_forecasting.pipeline.prediction_pipeline import Predictpipline

app = Flask(__name__)


@app.route("/")
def home():
    return "Demand Forecasting API Running"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    input_df = pd.DataFrame([data])

    pipeline = Predictpipline()

    prediction, safety_stock, reorder_point = pipeline.predict(input_df)

    return jsonify({
        "predicted_demand": float(prediction),
        "safety_stock": float(safety_stock),
        "reorder_point": float(reorder_point)
    })


if __name__ == "__main__":
    app.run(debug=True)