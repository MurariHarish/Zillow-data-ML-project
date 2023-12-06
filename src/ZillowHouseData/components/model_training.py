# #environment Imports
# import os, sys, pickle
# # from src.ZillowHouseData.logger import logger
# from src.ZillowHouseData.exception import CustomException
# # from sklearn.preprocessing import LabelEncoder
# from src.ZillowHouseData.entity.config_entity import ModelTrainingConfig

# #model imports
# # import pandas as pd
# # from sklearn.model_selection import train_test_split
# # from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import mean_squared_error
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, BatchNormalization,Dropout
# from tensorflow.keras.optimizers import Adam

# class DataModeling:
        
#     def __init__(self, config: ModelTrainingConfig):
#         self.config = config
#         self.learning_rate = self.config.learning_rate
#         self.epochs = self.config.epochs
#         self.batch_size = self.config.batch_size
#         self.validation_split = self.config.validation_split
#         self.verbose = self.config.verbose

#     def build_model(self, input_shape):
#         try:
#             model = Sequential()
#             model.add(Dense(128, activation='relu', input_shape=(input_shape,)))
#             model.add(BatchNormalization())
#             model.add(Dropout(0.5))
#             model.add(Dense(64, activation='relu', kernel_regularizer='l2'))
#             model.add(BatchNormalization())
#             model.add(Dropout(0.3))
#             model.add(Dense(32, activation='relu', kernel_regularizer='l2'))
#             model.add(BatchNormalization())
#             model.add(Dropout(0.3))
#             model.add(Dense(1, kernel_regularizer='l2'))

#             # Compile the model
#             model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse')

#             return model

#         except Exception as e:
#             raise CustomException(e, sys)

#     def train_model(self, model, X_train, y_train):
#         try:

#             # Train the model
#             model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_split=self.validation_split, verbose=self.verbose)

#             return model

#         except Exception as e:
#             raise CustomException(e, sys)

# --------------------XXXXXXXXXXXX------------------XGB Below-------------------

import xgboost as xgb
import mlflow, sys
import mlflow.xgboost
from urllib.parse import urlparse
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.entity.config_entity import ModelTrainingConfig


class DataModeling:
        
    def __init__(self, config: ModelTrainingConfig):

        self.config = config
        self.max_depth = self.config.max_depth
        self.learning_rate = self.config.learning_rate
        self.reg_alpha = self.config.reg_alpha
        self.reg_lambda = self.config.reg_lambda
        self.min_child_weight = self.config.min_child_weight
        self.objective = self.config.objective
        self.eval_metric = self.config.eval_metric
        self.n_estimators = self.config.n_estimators
        self.random_state = self.config.random_state
        

    def train_model(self, X_train, y_train):
        try:
            params = {
                'max_depth': self.max_depth,
                'learning_rate': self.learning_rate,
                'reg_alpha': self.reg_alpha,
                'reg_lambda': self.reg_lambda,
                'min_child_weight': self.min_child_weight,
                'objective': self.objective,
                'eval_metric': self.eval_metric,
                'n_estimators': self.n_estimators,
                'random_state': self.random_state
            }
            mlflow_uri = "https://dagshub.com/MurariHarish/Zillow-data-ML-project.mlflow"
            mlflow.set_registry_uri(mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            # mlflow.set_tracking_uri("http://localhost:5000")

            with mlflow.start_run():
            # Log parameters
                mlflow.log_params(params)
            # Train the model
            model = xgb.XGBRegressor(**params)
            model.fit(X_train, y_train)

            # Log model
            mlflow.xgboost.log_model(model, "model")

            return model

        except Exception as e:
            raise CustomException(e, sys)

