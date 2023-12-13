import os,sys,pickle, keras, mlflow, mlflow.keras
import numpy as np
import tensorflow as tf
from sklearn.metrics import r2_score
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
            # Model summary logging
            model_details = model.summary()
            logger.info(">>>>>> Model Summary <<<<<<\n\nx==========x")
            logger.info(model_details)

            # Make predictions on the test set
            y_pred = model.predict(X_test)

            # Calculate and log metrics
            mse, rmse, r2 = self.calculate_metrics(y_test, y_pred)
            self.log_metrics(mse, rmse, r2, model)

            return mse, rmse, r2

        except Exception as e:
            raise CustomException(e, sys)

    def calculate_metrics(self, y_test, y_pred):
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        return mse, rmse, r2

    def log_metrics(self, mse, rmse, r2, model):
        mlflow.set_registry_uri(self.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        params = load_pickle_object("models", "params.pkl")

        with mlflow.start_run():
            mlflow.log_params(params)
            mlflow.log_metric('MSE', mse)
            mlflow.log_metric('RMSE', rmse)
            mlflow.log_metric('R2', r2)

            if tracking_url_type_store != "file":
                mlflow.keras.log_model(model, "model", registered_model_name="FeedForwardModel")
            else:
                mlflow.keras.log_model(model, "model")
