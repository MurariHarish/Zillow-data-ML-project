import os,sys,pickle
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from sklearn.metrics import mean_squared_error
import tensorflow as tf
import keras
import numpy as np

class ModelEvaluate:

    def __init__(self):
        pass
    
    def evaluate_model(self, model, X_test, y_test):
        try:
        # Make predictions on the test set
            y_pred = model.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, y_pred)
            logger.info(f'Mean Squared Error: {mse}')
            return mse

        except Exception as e:
            raise CustomException(e, sys)