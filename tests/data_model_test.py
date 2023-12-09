# tests/test_model_training_pipeline.py
import os
from unittest.mock import patch, Mock
import pytest
from src.ZillowHouseData.components.model_training import DataModeling
from src.ZillowHouseData.pipeline.stage_03_model_training_pipeline import DataModellingPipeline

@pytest.fixture
def test_data_model(self):
    # Create an instance of the Modelling class   
    
    file_path = os.path.join('artifacts', 'data_ingestion', 'final.csv')

    # Read data
    df = read_csv_to_dataframe(file_path)
    #logger.info(">>>>>> CSV read <<<<<<\n\nx==========x")

    #logger.info(f">>>>>> Preparing data fror training <<<<<<\n\nx==========x")
    # Preprocess data
def test_prepare_data(tmpdir):   
    X, y = prepare_data(df)

def test_train_and_test_split(tmpdir)
    #Train test Split
    X_train_scaled, X_test_scaled, y_train, y_test, scaler = train_and_test_split(X, y)
    #logger.info(">>>>>> Test train split completed <<<<<<\n\nx==========x")

    save_object_to_pickle( X_test_scaled, "models", "X_test_scaled.pkl")
    save_object_to_pickle( y_test, "models", "y_test.pkl")
    save_object_to_pickle(scaler, "models", "scaler.pkl")
    #logger.info(">>>>>> Saved X_test and y_test as pickle for model evaluation <<<<<<\n\nx==========x")


    config = ConfigurationManager()
    model_training_config = config.get_model_training_config()
    data_modeling = DataModeling(config = model_training_config)

def test_build_model():
    # Build model
    model = data_modeling.build_model(X_train_scaled.shape[1])
    #logger.info(">>>>>> Model building completed<<<<<<\n\nx==========x")

def test_train_model():
    #logger.info(">>>>>> Train model <<<<<<\n\nx==========x")
    model = data_modeling.train_model(model, X_train_scaled, y_train)
    #logger.info(">>>>>> Model training completed<<<<<<\n\nx==========x")

def test_summary():
    #logger.info(">>>>>> model details for me to see : <<<<<<\n\nx==========x")
    model_details = model.summary()
    #logger.info(">>>>>> Model Summary <<<<<<\n\nx==========x")
    #logger.info(model_details)

def test_save_model_to_keras():
    save_model_to_keras(model, "models", "model.keras")
    #logger.info(">>>>>> Saved model as pickle <<<<<<\n\nx==========x")
