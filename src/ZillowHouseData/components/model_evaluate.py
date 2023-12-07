# import os,sys,pickle
# from src.ZillowHouseData.logger import logger
# from src.ZillowHouseData.exception import CustomException
# from sklearn.metrics import mean_squared_error
# import tensorflow as tf
# import keras
# import numpy as np

# class ModelEvaluate:

#     def __init__(self):
#         pass
    
#     def evaluate_model(self, model, X_test, y_test):
#         try:
#         # Make predictions on the test set
#             y_pred = model.predict(X_test)

#             # Evaluate the model
#             mse = mean_squared_error(y_test, y_pred)
#             logger.info(f'Mean Squared Error: {mse}')
#             return mse

#         except Exception as e:
#             raise CustomException(e, sys)

# --------------------XXXXXXXXXXXX------------------XGB Below-------------------

import mlflow, sys
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from sklearn.metrics import mean_squared_error
from urllib.parse import urlparse
from src.ZillowHouseData.utils.common import load_pickle_object
from src.ZillowHouseData.entity.config_entity import ModelEvaluationConfig


class ModelEvaluate:

    def __init__(self, config: ModelEvaluationConfig):
        
        self.config = config
        self.mlflow_uri = self.config.mlflow_uri
    
    def evaluate_model(self, model, X_test, y_test):
        try:
        # Make predictions on the test set
            y_pred = model.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, y_pred)
            logger.info(f'Mean Squared Error: {mse}')

            # mlflow_uri = "https://dagshub.com/MurariHarish/Zillow-data-ML-project.mlflow"
            mlflow.set_registry_uri(self.mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            params = load_pickle_object("models", "params.pkl")

            with mlflow.start_run():
                mlflow.log_params(params)
            # mlflow.start_run(run_id=run_id)
                mlflow.log_metric('mse', mse)
                mlflow.xgboost.log_model(model, "model")

            return mse

        except Exception as e:
            raise CustomException(e, sys)
        
        