import os
import sys
import pandas as pd
import numpy as np

from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.ecommerce_forecasting.utils.logger import logging
from src.ecommerce_forecasting.utils.exception import CustomException


@dataclass
class DataTransformationConfig:

    data_path = os.path.join("artifacts","final_feature_dataset.csv")
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")


class DataTransformation:

    def __init__(self):
        self.config = DataTransformationConfig()

    def initiate_data_transformation(self):

        try:

            df = pd.read_csv(self.config.data_path)

            df = df.drop(columns=[
                    "sku_id",
                    "supplier_id_x",
                    "supplier_id_y"], errors="ignore")

            df = pd.get_dummies(df, drop_first= True)

            X = df.drop(columns=["units_sold","date"], errors= "ignore")
            y = df["units_sold"]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            train_df = pd.concat([X_train, y_train], axis=1)
            test_df = pd.concat([X_test, y_test], axis=1)

            train_df.to_csv(self.config.train_data_path, index=False)
            test_df.to_csv(self.config.test_data_path, index=False)

            logging.info("Data Transformation Completed")

        except Exception as e:
            raise CustomException(e,sys)