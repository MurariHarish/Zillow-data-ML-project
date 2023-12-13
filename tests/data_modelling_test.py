import pytest
import pandas as pd
import os, sys
from src.ZillowHouseData.components.model_training import DataModeling
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.utils.common import save_model_to_keras, save_object_to_pickle, read_csv_to_dataframe, prepare_data, train_and_test_split
from src.ZillowHouseData.utils import common
from src.ZillowHouseData.config.configuration import ConfigurationManager
from src.ZillowHouseData.entity.config_entity import ModelTrainingConfig
from src.ZillowHouseData.components.model_training import DataModeling
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler


########################################################################################################################
@pytest.fixture
def create_temp_csv(tmp_path):
    # Create a temporary CSV file with sample data
    temp_csv_path = tmp_path / "temp_sample_data.csv"
    sample_data = {
        'indicator_id': ['ZATT', 'ZSFH', 'ZALL'],
        'region_id': [394521, 394521, 394521],
        'date': ['2020-06-30', '2020-06-30', '2020-06-30'],
        'value': [247142.0, 143910.0, 142059.0],
        'year': [2020, 2020, 2020],
        'month': [6, 6, 6],
        'CRAM': [0.14970, 0.14970, 0.14970],
        'IRAM': [2210.0, 2210.0, 2210.0],
        'LRAM': [208990.0, 208990.0, 208990.0],
        'MRAM': [25.0, 25.0, 25.0],
        'NRAM': [4.0, 4.0, 4.0],
        'SRAM': [158400.0, 158400.0, 158400.0]
    }
    pd.DataFrame(sample_data).to_csv(temp_csv_path, index=False)
    return temp_csv_path    
########################################################################################################################
def test_read_csv_to_dataframe(create_temp_csv):
    # Arrange
    temp_csv_path = create_temp_csv
    # Act
    result_df = read_csv_to_dataframe(temp_csv_path)

    # Assert
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape == (3, 12)
    assert all(column in result_df.columns for column in ['indicator_id', 'region_id', 'date', 'value', 'year', 'month', 'CRAM', 'IRAM', 'LRAM', 'MRAM', 'NRAM', 'SRAM'])
    assert not result_df.empty
########################################################################################################################

########################################################################################################################
def test_prepare_data(create_temp_csv):
    # Arrange
    temp_csv_path = create_temp_csv
    df = pd.read_csv(temp_csv_path)
    # Act
    X, y, label_encoder = prepare_data(df)

    # Assert
    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, pd.Series)
    # Check the shape of X and y
    assert X.shape == (3, 10)
    assert y.shape == (3,)
    # Check that 'encoded_indicator_id' is present in X columns
    assert 'encoded_indicator_id' in X.columns
    # Check that the original 'indicator_id' is dropped from X
    assert 'indicator_id' not in X.columns    
    # Check the content of columns_to_use in X
    expected_columns = ['encoded_indicator_id', 'region_id', 'year', 'month', 'CRAM', 'IRAM', 'LRAM', 'MRAM', 'NRAM', 'SRAM']
    assert all(column in X.columns for column in expected_columns)
    # Check that 'value' is the target variable in y
    assert y.name == 'value'
    assert label_encoder[0] == 'ZALL'
    assert label_encoder[1] == 'ZATT'
    assert label_encoder[2] == 'ZSFH'
########################################################################################################################

########################################################################################################################
@pytest.fixture
def test_train_and_test_split():
    # Arrange
    X_data = {
        'encoded_indicator_id': [0, 1, 2],
        'region_id': [394521, 394521, 394521],
        'year': [2020, 2020, 2020],
        'month': [6, 6, 6],
        'CRAM': [0.14970, 0.14970, 0.14970],
        'IRAM': [2210.0, 2210.0, 2210.0],
        'LRAM': [208990.0, 208990.0, 208990.0],
        'MRAM': [25.0, 25.0, 25.0],
        'NRAM': [4.0, 4.0, 4.0],
        'SRAM': [158400.0, 158400.0, 158400.0]
    }
    X = pd.DataFrame(X_data)
    # Hardcoded y DataFrame
    y_data = {'value': [247142.0, 143910.0, 142059.0]}
    y = pd.DataFrame(y_data)

    # Act
    X_train_scaled, X_test_scaled, y_train, y_test, scaler = train_and_test_split(X, y)
    print("X_train_scaled:", X_train_scaled, "X_test_scaled:", X_test_scaled, "y_train:", y_train, "y_test:", y_test, "scaler:", scaler)
    # Assert
    assert isinstance(X_train_scaled, pd.DataFrame)
    assert isinstance(X_test_scaled, pd.DataFrame)
    assert isinstance(y_train, pd.DataFrame)
    assert isinstance(y_test, pd.DataFrame)
    assert isinstance(scaler, StandardScaler)
    # Check the shape of X_train_scaled, X_test_scaled, y_train, and y_test
    assert X_train_scaled.shape == (2, 10)
    assert X_test_scaled.shape == (1, 10)
    assert y_train.shape == (2, 1)
    assert y_test.shape == (1, 1)
    # Check that X_train_scaled and X_test_scaled have different values
    assert not X_train_scaled.equals(X_test_scaled)
########################################################################################################################

########################################################################################################################
@pytest.fixture
def data_model_training_config(tmpdir):
    final_csv_path = str(tmpdir.join("model_final.csv"))

    config = ModelTrainingConfig(
        learning_rate=0.001,
        epochs=10,
        batch_size=32,
        validation_split=0.2,
        verbose=1,
        final_csv_path=final_csv_path)

    return config

def test_build_model(data_model_training_config):


    data_model = DataModeling(config=data_model_training_config)
    input_shape = 10
    model = data_model.build_model(input_shape)
    

    # Check the architecture of the model
    expected_layers = [
        Dense(128, activation='relu', input_shape=(input_shape,)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(64, activation='relu', kernel_regularizer='l2'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(32, activation='relu', kernel_regularizer='l2'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(1, kernel_regularizer='l2')
    ]

    for expected_layer, actual_layer in zip(expected_layers, model.layers):
        assert isinstance(actual_layer, type(expected_layer))
        if isinstance(expected_layer, Dense):
            assert actual_layer.units == expected_layer.units
            assert actual_layer.activation.__name__ == expected_layer.activation.__name__
            assert actual_layer.kernel_regularizer.__class__ == expected_layer.kernel_regularizer.__class__

    # Check the optimizer and loss function
    assert model.optimizer.__class__ == Adam
    assert model.loss == 'mse'

def test_train_model(data_model_training_config):
    # Arrange
    data_model = DataModeling(config=data_model_training_config)
    input_shape = 10
    model = data_model.build_model(input_shape)

    # Hardcoded X_train and y_train
    X_train_data = {
        'encoded_indicator_id': [0, 1, 2],
        'region_id': [394521, 394521, 394521],
        'year': [2020, 2020, 2020],
        'month': [6, 6, 6],
        'CRAM': [0.14970, 0.14970, 0.14970],
        'IRAM': [2210.0, 2210.0, 2210.0],
        'LRAM': [208990.0, 208990.0, 208990.0],
        'MRAM': [25.0, 25.0, 25.0],
        'NRAM': [4.0, 4.0, 4.0],
        'SRAM': [158400.0, 158400.0, 158400.0]
    }
    X_train = pd.DataFrame(X_train_data)
    y_train_data = {'value': [247142.0, 143910.0, 142059.0]}
    y_train = pd.DataFrame(y_train_data)

    X_train_scaled, X_test_scaled, y_train, y_test, scaler = train_and_test_split(X_train, y_train)

    # Act
    model = data_model.train_model(model, X_train_scaled, y_train)

    # Assert
    #assert isinstance(trained_model, Sequential)
    assert model.optimizer.__class__ == Adam
    assert model.loss == 'mse'
    assert model.optimizer.lr == data_model_training_config.learning_rate
#######################################################################################################################   

#######################################################################################################################
