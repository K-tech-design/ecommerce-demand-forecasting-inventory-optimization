import sys
from src.ecommerce_forecasting.components.data_ingestion import DataIngestion
from src.ecommerce_forecasting.components.data_validation import DataValidation
from src.ecommerce_forecasting.components.data_transformation import DataTransformation
from src.ecommerce_forecasting.components.model_trainer import ModelTrainer

from src.ecommerce_forecasting.utils.exception import CustomException
from src.ecommerce_forecasting.utils.logger import logging


class TrainingPipeline:

    def __init__(self):
        pass

    def run_pipeline(self):

        try:

            logging.info("Pipeline started")

            # Data Ingestion
            ingestion = DataIngestion()
            ingestion.initiate_data_ingestion()

            # Data Validation
            validation = DataValidation()
            validation.validate_data()

            # Data Transformation
            transformation = DataTransformation()
            transformation.initiate_data_transformation()

            # Model Training
            trainer = ModelTrainer()
            trainer.intiate_model_trainer()

            logging.info("Pipeline completed successfully")

        except Exception as e:
            raise CustomException(e, sys)