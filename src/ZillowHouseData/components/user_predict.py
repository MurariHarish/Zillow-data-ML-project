import sys
import pandas as pd
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.entity.config_entity import UserPredictConfig


class Predict:

    def __init__(self, config: UserPredictConfig):
          self.config = config
          self.user_input_reqs = self.config.user_input_reqs
     
    def predict_user_input(self, model, scaler, user_input):
        try:
            # Get user input for each column in X_train
            # user_input = {}
            # for column in self.user_input_reqs:
            #     value = input(f"Enter value for {column}: ")
            #     user_input[column] = float(value) if column != 'encoded_indicator_id' else int(value)

            # Convert user input to DataFrame
            user_input_df = pd.DataFrame([user_input])

            # Use the previously fitted scaler to transform the features
            user_input_scaled = scaler.transform(user_input_df)

            # Get the predicted value for the user input
            predicted_value = model.predict(user_input_scaled)

            # Display the user input and predicted value
            logger.info(f"User Input:\n{user_input}\n")
            logger.info(f"Predicted Value: {predicted_value[0][0]}")

            return predicted_value[0][0]
        
        except Exception as e:
            raise CustomException(e, sys)