import sys
import pickle
import pandas as pd
import numpy as np


from src.ecommerce_forecasting.utils.logger import logging
from src.ecommerce_forecasting.utils.exception import CustomException


class Predictpipline:
    def __init__(self):
        pass
    
    
    def predict(self, input_data):

        try:
            model_path = "artifacts/model.pkl"
            feature_path = "artifacts/model_feature.pkl"

            with open(model_path, "rb") as f:
                model = pickle.load(f)
            
            with open(feature_path, "rb") as f:
                model_feature = pickle.load(f)
        # create empty data frame with training features
            input_df = pd.DataFrame(columns= model_feature)

            for col in input_data.columns:
                input_df[col] = input_data[col]

            input_df = input_df.fillna(0)

            predicted_demand = model.predict(input_df)[0]

            lead_time =7 # avg supply delivery time
            z = 1.65  # z= service level factor for 95%->1.65
            demand_std = 2 # standard deviation

            safety_stocks = z * demand_std * np.sqrt(lead_time)
            reorder_point = predicted_demand + safety_stocks

            return predicted_demand, safety_stocks, reorder_point  
        
        except Exception as e:
            raise CustomException(e,sys)