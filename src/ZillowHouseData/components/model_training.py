#environment Imports
import os, sys, pickle
# from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
# from sklearn.preprocessing import LabelEncoder
from src.ZillowHouseData.utils.common import save_object_to_pickle
from src.ZillowHouseData.entity.config_entity import ModelTrainingConfig

#model imports
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization,Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import GridSearchCV
from kerastuner.tuners import RandomSearch
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer
import tensorflow as tf
from kerastuner.engine.hyperparameters import HyperParameters
from tensorflow.keras.callbacks import TensorBoard as tb
from tensorflow.keras import backend as K
import datetime

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
            model.add(Dropout(0.4))
            model.add(Dense(64, activation='relu', kernel_regularizer='l2'))
            model.add(BatchNormalization())
            model.add(Dropout(0.3))
            model.add(Dense(32, activation='relu', kernel_regularizer='l2'))
            model.add(BatchNormalization())
            model.add(Dropout(0.4))
            model.add(Dense(1, kernel_regularizer='l2'))

            # Compile the model
            model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse')

            return model

        except Exception as e:
            raise CustomException(e, sys)
    


    def train_model(self, model, X_train, y_train):
        try:
            log_dir = "./artifacts/tensorflow_model/logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            tb_callback_model = tb(log_dir=log_dir, histogram_freq=1, profile_batch='5,10')
            params = {
                'learning_rate': self.learning_rate,
                'epochs': self.epochs,
                'batch_size': self.batch_size, 
                'validation_split': self.validation_split,
                'verbose': self.verbose
            }

            save_object_to_pickle(params, "models", "params.pkl")

            # Train the model
            model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_split=self.validation_split, verbose=self.verbose, callbacks=[tb_callback_model])

            return model

        except Exception as e:
            raise CustomException(e, sys)

    def build_model_tuned(self, X_train, hp):
        try:
            model = Sequential()
            model.add(Dense(units=hp.Int('units_1', min_value=32, max_value=256, step=32),
                            activation='relu', input_shape=(X_train.shape[1],)))
            model.add(BatchNormalization())
            model.add(Dropout(hp.Float('dropout_1', min_value=0.2, max_value=0.5, step=0.1)))
            model.add(Dense(units=hp.Int('units_2', min_value=32, max_value=128, step=32),
                            activation='relu', kernel_regularizer='l2'))
            model.add(BatchNormalization())
            model.add(Dropout(hp.Float('dropout_2', min_value=0.2, max_value=0.5, step=0.1)))
            model.add(Dense(units=hp.Int('units_3', min_value=16, max_value=64, step=16),
                            activation='relu', kernel_regularizer='l2'))
            model.add(BatchNormalization())
            model.add(Dropout(hp.Float('dropout_3', min_value=0.2, max_value=0.5, step=0.1)))
            model.add(Dense(1, kernel_regularizer='l2'))
            
            # Compile the model
            model.compile(optimizer=Adam(learning_rate=hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='log')), loss='mse')
            
            return model

        except Exception as e:
            raise CustomException(e, sys)

    def tune_model(self, X_train, y_train):
        try:
            log_dir = "./artifacts/tensorflow_hyperparameter/logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            tb_callback = tb(log_dir=log_dir, histogram_freq=1, profile_batch='5,10')
            
            hp = HyperParameters()
            tuner = RandomSearch(
                lambda hp: self.build_model_tuned(X_train, hp),
                objective='val_loss',
                max_trials=10,  # You can adjust the number of trials
                directory='artifacts/tuner_logs',
                project_name='neural_network_tuning')
        
            tuner.search(X_train, y_train, epochs=hp.Int('epochs', min_value=10, max_value=30),
                     batch_size=hp.Int('batch_size', min_value=16, max_value=32),
                     validation_split=hp.Float('validation_split', min_value=0.1, max_value=0.3),
                     callbacks=[tb_callback],verbose=2)

            # Get the best hyperparameter values
            best_hps = tuner.oracle.get_best_trials(num_trials=1)[0].hyperparameters.values
            print("Best Hyperparameters:", best_hps)

            print("Tuning completed successfully")
            print(best_hps.values)

        except Exception as e:
            raise CustomException(e, sys)
