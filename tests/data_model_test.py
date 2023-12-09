# tests/test_model_training_pipeline.py
import os
from unittest.mock import patch, Mock
import pytest
from src.ZillowHouseData.components.model_training import DataModeling
from src.ZillowHouseData.pipeline.model_training_pipeline import DataModellingPipeline

@pytest.fixture
def mock_load_csv_to_dataframe():
    with patch("src.ZillowHouseData.pipeline.model_training_pipeline.read_csv_to_dataframe") as mock_load:
        yield mock_load

@pytest.fixture
def mock_prepare_data():
    with patch("src.ZillowHouseData.pipeline.model_training_pipeline.prepare_data") as mock_prepare:
        yield mock_prepare

@pytest.fixture
def mock_train_and_test_split():
    with patch("src.ZillowHouseData.pipeline.model_training_pipeline.train_and_test_split") as mock_split:
        yield mock_split

@pytest.fixture
def mock_save_object_to_pickle():
    with patch("src.ZillowHouseData.pipeline.model_training_pipeline.save_object_to_pickle") as mock_save:
        yield mock_save

@pytest.fixture
def mock_modeling():
    with patch("src.ZillowHouseData.pipeline.model_training_pipeline.DataModeling") as mock_modeling:
        yield mock_modeling

def test_data_model(mock_load_csv_to_dataframe, mock_prepare_data, mock_train_and_test_split, mock_save_object_to_pickle, mock_modeling):
    # Set up mocks
    mock_load_csv_to_dataframe.return_value = Mock()  # Provide a DataFrame for testing
    mock_prepare_data.return_value = (Mock(), Mock())  # Provide X and y for testing
    mock_train_and_test_split.return_value = (Mock(), Mock(), Mock(), Mock(), Mock())  # Provide split data for testing
    mock_modeling_instance = mock_modeling.return_value
    mock_modeling_instance.build_model.return_value = Mock()  # Provide a model for testing

    # Run the pipeline
    pipeline = DataModellingPipeline()
    pipeline.data_model()

    # Assertions
    mock_load_csv_to_dataframe.assert_called_once_with(os.path.join('artifacts', 'data_ingestion', 'final.csv'))
    mock_prepare_data.assert_called_once_with(mock_load_csv_to_dataframe.return_value)
    mock_train_and_test_split.assert_called_once_with(mock_prepare_data.return_value[0], mock_prepare_data.return_value[1])
    mock_modeling.assert_called_once_with(config=Mock())
    mock_modeling_instance.build_model.assert_called_once_with(mock_train_and_test_split.return_value[0].shape[1])
    mock_modeling_instance.train_model.assert_called_once_with(mock_modeling_instance.build_model.return_value, *mock_train_and_test_split.return_value[:2])
    mock_save_object_to_pickle.assert_called_with(*mock_train_and_test_split.return_value[:2], "models", "X_test_scaled.pkl")
    mock_save_object_to_pickle.assert_called_with(mock_train_and_test_split.return_value[3], "models", "y_test.pkl")
    mock_save_object_to_pickle.assert_called_with(mock_train_and_test_split.return_value[4], "models", "scaler.pkl")
    mock_modeling_instance.save_model_to_keras.assert_called_once_with(mock_modeling_instance.train_model.return_value, "models", "model.keras")
