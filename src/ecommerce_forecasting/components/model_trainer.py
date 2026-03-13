import os
import sys
import pandas as pd
import pickle 
import numpy as np


from dataclasses import dataclass
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


from src.ecommerce_forecasting.utils.logger import logging
from src.ecommerce_forecasting.utils.exception import CustomException


@dataclass
class ModelTrainerConfig:
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")
    model_path = os.path.join("artifacts","model.pkl")
    feature_path = os.path.join("artifacts","model_feature.pkl")
class ModelTrainer:

    def __init__(self):
        self.config = ModelTrainerConfig()
    
    def intiate_model_trainer(self):

        try:
            train_df = pd.read_csv(self.config.train_data_path)
            test_df = pd.read_csv(self.config.test_data_path)
            
            X_train = train_df.drop(columns=["units_sold"])
            y_train = train_df["units_sold"]

            X_test = test_df.drop(columns=["units_sold"])
            y_test = test_df["units_sold"]

            model = XGBRegressor(
                n_estimators = 300,
                learning_rate = 0.05,
                max_depth = 6,
                random_state = 42
            )

            model.fit(X_train,y_train)

            y_pred = model.predict(X_test)

            mae = mean_absolute_error(y_test,y_pred)
            rsme = np.sqrt(mean_squared_error(y_test,y_pred))
            r2 = r2_score(y_test,y_pred)

            with open(self.config.model_path,"wb") as f:
                pickle.dump(model,f)

            #save feature names for api prediction
            with open(self.config.feature_path, "wb") as f:
                pickle.dump(X_train.columns.tolist(), f)
        
        except Exception as e:
            raise CustomException(e,sys)
