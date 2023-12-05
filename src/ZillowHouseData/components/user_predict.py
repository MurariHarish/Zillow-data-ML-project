import sys
import pandas as pd
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException

class Predict:
     def __init__(self):
          pass
     
     def predict_user_input(self, model, scaler):
        try:
            # Get user input for each column in X_train
            user_input = {}
            for column in self.X_train.columns:
                value = input(f"Enter value for {column}: ")
                user_input[column] = float(value) if column != 'encoded_indicator_id' else int(value)
                print("LOL")

            # Convert user input to DataFrame
            user_input_df = pd.DataFrame([user_input])

            # Use the previously fitted scaler to transform the features
            user_input_scaled = scaler.transform(user_input_df)

            # Get the predicted value for the user input
            predicted_value = model.predict(user_input_scaled)

            # Display the user input and predicted value
            logger.info(f"User Input:\n{user_input}\n")
            logger.info(f"Predicted Value: {predicted_value[0][0]}")
        except Exception as e:
            raise CustomException(e, sys)