#environment Imports
import os, sys, pickle
# from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
# from sklearn.preprocessing import LabelEncoder
from src.ZillowHouseData.entity.config_entity import ModelTrainingConfig

#model imports
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization,Dropout
from tensorflow.keras.optimizers import Adam

class DataModeling:
        
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        self.learning_rate = self.config.learning_rate
        self.epochs = self.config.epochs
        self.batch_size = self.config.batch_size
        self.validation_split = self.config.validation_split
        self.verbose = self.config.verbose

    def build_model(self, input_shape):
        try:
            model = Sequential()
            model.add(Dense(128, activation='relu', input_shape=(input_shape,)))
            model.add(BatchNormalization())
            model.add(Dropout(0.5))
            model.add(Dense(64, activation='relu', kernel_regularizer='l2'))
            model.add(BatchNormalization())
            model.add(Dropout(0.3))
            model.add(Dense(32, activation='relu', kernel_regularizer='l2'))
            model.add(BatchNormalization())
            model.add(Dropout(0.3))
            model.add(Dense(1, kernel_regularizer='l2'))

            # Compile the model
            model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse')

            return model

        except Exception as e:
            raise CustomException(e, sys)

    def train_model(self, model, X_train, y_train):
        try:

            # Train the model
            model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_split=self.validation_split, verbose=self.verbose)

            return model

        except Exception as e:
            raise CustomException(e, sys)