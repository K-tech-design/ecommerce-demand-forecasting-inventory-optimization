import os 
import sys
import pandas as pd

from src.ecommerce_forecasting.utils.logger import logging
from src.ecommerce_forecasting.utils.exception import CustomException
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join("artifacts","raw_data")

    sales_data_file = "data/raw/sales_fact.csv"
    products_data_file = "data/raw/products_master.csv"
    suppliers_data_file = "data/raw/suppliers_master.csv"
    inventory_data_file = "data/raw/inventory_snapshot.csv"

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion (self):
        try:
            os.makedirs(self.ingestion_config.raw_data_path,exist_ok= True)

            sales_df = pd.read_csv(self.ingestion_config.sales_data_file)
            products_df = pd.read_csv(self.ingestion_config.products_data_file)
            suppliers_df = pd.read_csv(self.ingestion_config.suppliers_data_file)
            inventory_df = pd.read_csv(self.ingestion_config.inventory_data_file)

            sales_df.to_csv("artifacts/raw_data/sales_fact.csv", index=False)
            products_df.to_csv("artifacts/raw_data/products_master.csv", index=False)
            suppliers_df.to_csv("artifacts/raw_data/suppliers_master.csv", index=False)
            inventory_df.to_csv("artifacts/raw_data/inventory_snapshot.csv", index=False)

            return (
                "artifacts/raw_data/sales_fact.csv",
                "artifacts/raw_data/products_master.csv",
                "artifacts/raw_data/suppliers_master.csv",
                "artifacts/raw_data/inventory_snapshot.csv"
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        