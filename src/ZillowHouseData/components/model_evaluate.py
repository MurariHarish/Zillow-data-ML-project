import os,sys,pickle, keras, mlflow, mlflow.keras
import numpy as np
import tensorflow as tf
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.utils.common import load_pickle_object
from src.ZillowHouseData.entity.config_entity import ModelEvaluationConfig


class ModelEvaluate:

    def __init__(self, config: ModelEvaluationConfig):
        
        self.config = config
        self.mlflow_uri = self.config.mlflow_uri
    
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info(">>>>>> model details for me to see inside evaluate_model : <<<<<<\n\nx==========x")
            model_details = model.summary()
            logger.info(">>>>>> Model Summary <<<<<<\n\nx==========x")
            logger.info(model_details)

        # Make predictions on the test set
            y_pred = model.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, y_pred)
            logger.info(f'Mean Squared Error: {mse}')

            mlflow_uri = "https://dagshub.com/MurariHarish/Zillow-data-ML-project.mlflow"
            mlflow.set_registry_uri(self.mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            params = load_pickle_object("models", "params.pkl")

            with mlflow.start_run():
                mlflow.log_params(params)
            # mlflow.start_run(run_id=run_id)
                mlflow.log_metric('mse', mse)
                # mlflow.xgboost.log_model(model, "model")

                if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.keras.log_model(model, "model", registered_model_name="FeedForwardModel")
                else:
                    mlflow.keras.log_model(model, "model")

            return mse

        except Exception as e:
            raise CustomException(e, sys)

# --------------------XXXXXXXXXXXX------------------XGB Below-------------------

# import mlflow, sys
# from src.ZillowHouseData.logger import logger
# from src.ZillowHouseData.exception import CustomException
# from sklearn.metrics import mean_squared_error
# from urllib.parse import urlparse
# from src.ZillowHouseData.utils.common import load_pickle_object
# from src.ZillowHouseData.entity.config_entity import ModelEvaluationConfig


# class ModelEvaluate:

#     def __init__(self, config: ModelEvaluationConfig):
        
#         self.config = config
#         self.mlflow_uri = self.config.mlflow_uri
    
#     def evaluate_model(self, model, X_test, y_test):
#         try:
#         # Make predictions on the test set
#             y_pred = model.predict(X_test)

#             # Evaluate the model
#             mse = mean_squared_error(y_test, y_pred)
#             logger.info(f'Mean Squared Error: {mse}')

#             # mlflow_uri = "https://dagshub.com/MurariHarish/Zillow-data-ML-project.mlflow"
#             mlflow.set_registry_uri(self.mlflow_uri)
#             tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

#             params = load_pickle_object("models", "params.pkl")

#             with mlflow.start_run():
#                 mlflow.log_params(params)
#             # mlflow.start_run(run_id=run_id)
#                 mlflow.log_metric('mse', mse)
#                 # mlflow.xgboost.log_model(model, "model")

#                 if tracking_url_type_store != "file":

#                     # Register the model
#                     # There are other ways to use the Model Registry, which depends on the use case,
#                     # please refer to the doc for more information:
#                     # https://mlflow.org/docs/latest/model-registry.html#api-workflow
#                     mlflow.xgboost.log_model(model, "model", registered_model_name="XGModel")
#                 else:
#                     mlflow.keras.log_model(model, "model")

#             return mse

#         except Exception as e:
#             raise CustomException(e, sys)
        
        