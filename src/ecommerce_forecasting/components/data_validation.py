import os
import sys
import pandas as pd
import json
from dataclasses import dataclass

from src.ecommerce_forecasting.utils.logger import logging
from src.ecommerce_forecasting.utils.exception import CustomException


@dataclass
class DataValidationConfig:

    raw_data_path = os.path.join("artifacts","raw_data")

    sales_data_file = os.path.join("artifacts","raw_data","sales_fact.csv")
    products_data_file = os.path.join("artifacts","raw_data","products_master.csv")
    suppliers_data_file = os.path.join("artifacts","raw_data","suppliers_master.csv")
    inventory_data_file = os.path.join("artifacts","raw_data","inventory_snapshot.csv")

    report_file_path =os.path.join("artifacts","data_validation_report.json")

class DataValidation:
    
    def __init__(self):
        self.validation_config = DataValidationConfig()

    def validate_data(self):
        try:
            logging.info("Starting data validation")

            sales_df = pd.read_csv(self.validation_config.sales_data_file)
            product_df = pd.read_csv(self.validation_config.products_data_file)

            report = {}

            report["missing_values"] = int(sales_df.isnull().sum().sum())

            report["duplicate_values"] = int(sales_df.duplicated().sum())

            try:
                pd.to_datetime(sales_df["date"], format="%Y-%m-%d")
                report ["invalid_dates"] = 0

            except:
                report["invalid_dates"] = 1

            report["Negative_units_sold"] = int((sales_df["units_sold"] < 0).sum())

            missing_skus = set(sales_df["sku_id"]) - set(product_df["sku_id"])
            report["foreign_key_errors"] = len(missing_skus)

            with open(self.validation_config.report_file_path,"w") as f:
                json.dump(report,f,indent= 4)

            logging.info("Data Validation Completed")

            return report
        except Exception as e:
            raise CustomException(e,sys)
