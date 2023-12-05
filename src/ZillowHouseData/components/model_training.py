#environment Imports
import os, sys, pickle
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from sklearn.preprocessing import LabelEncoder

#model imports
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization,Dropout
from tensorflow.keras.optimizers import Adam

class DataModeling:
    def __init__(self, file_path):
        self.file_path = file_path
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def read_csv_to_dataframe(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def prepare_data(self, df):
        try:
            
            # Encoding indicator_id
            label_encoder = LabelEncoder()
            df['encoded_indicator_id'] = label_encoder.fit_transform(df['indicator_id'])
            df.drop(['Unnamed: 0','indicator_id'], axis=1, inplace= True)

            # Select relevant columns
            columns_to_use = ['encoded_indicator_id', 'region_id', 'year', 'month', 'CRAM', 'IRAM', 'LRAM', 'MRAM', 'NRAM', 'SRAM']

            # Define features and target variable
            X = df[columns_to_use]
            y = df['value']

            return X, y

        except Exception as e:
            raise CustomException(e, sys)     

    def train_test_split(self, X, y):
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Store X_train, X_test  as attributes
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

        # Standardize the data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        return X_train_scaled, X_test_scaled, y_train, y_test, scaler

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
            model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

            return model

        except Exception as e:
            raise CustomException(e, sys)
        
    def train_model(self, model, X_train, y_train, epochs=1, batch_size=32, validation_split=0.1):
        try:

            # Train the model
            model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split, verbose=2)

            return model

        except Exception as e:
            raise CustomException(e, sys)

    # def predict_sample(self, model, scaler):
    #     try:
    #         if self.X_test is None:
    #             raise CustomException("X_test is not defined.", sys)

    #         random_index = self.X_test.sample().index[0]

    #         # Extract the features for the selected index
    #         X_test_random = self.X_test.loc[random_index, :].values.reshape(1, -1)

    #         # Extract the corresponding target variable (y_test) for the selected index
    #         y_test_random = self.y_test.loc[random_index]

    #         # Use the previously fitted scaler to transform the features
    #         X_test_random_scaled = scaler.transform(X_test_random)

    #         # Get the predicted value for the selected row
    #         predicted_value = model.predict(X_test_random_scaled)

    #         # Display the selected row, true target value, and predicted value
    #         logger.info(f"Selected Row (X_test):\n{self.X_test.loc[random_index, :]}\n")
    #         logger.info(f"True Target Value (y_test): {y_test_random}\n")
    #         logger.info(f"Predicted Value: {predicted_value[0][0]}")

    #     except Exception as e:
    #         raise CustomException(e, sys)

    # def predict_user_input(self, model, scaler):
    #     try:
    #         # Get user input for each column in X_train
    #         user_input = {}
    #         for column in self.X_train.columns:
    #             value = input(f"Enter value for {column}: ")
    #             user_input[column] = float(value) if column != 'indicator_id' else int(value)

    #         # Convert user input to DataFrame
    #         user_input_df = pd.DataFrame([user_input])

    #         # Use the previously fitted scaler to transform the features
    #         user_input_scaled = scaler.transform(user_input_df)

    #         # Get the predicted value for the user input
    #         predicted_value = model.predict(user_input_scaled)

    #         # Display the user input and predicted value
    #         logger.info(f"User Input:\n{user_input}\n")
    #         logger.info(f"Predicted Value: {predicted_value[0][0]}")
    #     except Exception as e:
    #         raise CustomException(e, sys)