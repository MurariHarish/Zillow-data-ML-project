import pytest
import pandas as pd
from src.ZillowHouseData.components.data_preprocessing import DataPreprocessing
from src.ZillowHouseData.entity.config_entity import DataPreprocessingConfig

@pytest.fixture
def data_preprocessing_config(tmpdir):
    # Create a sample DataPreprocessingConfig with test paths
    test_file = str(tmpdir.join("pytest_sample_data.csv"))
    region_test_file = str(tmpdir.join("pytest_region_sample_data.csv"))
    stats_path = str(tmpdir.join("stats.csv"))
    final_csv_path = str(tmpdir.join("final.csv"))

    config = DataPreprocessingConfig(
        file_name=test_file,
        region_file_name = region_test_file,
        start_date="2020-01-01",
        interested_columns=['date', 'region_id', 'indicator_id', 'value'], 
        interested_indicators_stats=['Z4BR', 'ZABT'],  
        interested_indicators_zhvi=['CRAM', 'IRAM'],  
        stats_path=stats_path,
        final_csv_path=final_csv_path
    )
    return config


def test_read_and_filter_data(data_preprocessing_config):
    # Initialize DataPreprocessing
    dp = DataPreprocessing(config=data_preprocessing_config)
    
    # Create a test CSV file with test data
    test_data = {
        'date': ['2020-01-01', '2020-02-01'],
        'region_id': [1, 2],
        'indicator_id': ['Z4BR', 'ZABT'],
        'value': [100, 200]
    }
    test_df = pd.DataFrame(test_data)
    test_df.to_csv(data_preprocessing_config.file_name, index=False)

    # Test read_and_filter_data
    filtered_df = dp.read_and_filter_data()
    assert not filtered_df.empty
    assert all(column in filtered_df.columns for column in data_preprocessing_config.interested_columns)

def test_get_year_month(data_preprocessing_config):
    dp = DataPreprocessing(config=data_preprocessing_config)
    
    # Create a test DataFrame
    test_data = {
        'date': ['2020-01-01', '2020-02-01'],
        'region_id': [1, 2],
        'indicator_id': ['IRAM', 'CRAM'],
        'value': [100, 200]
    }
    test_df = pd.DataFrame(test_data)
    test_df['date'] = pd.to_datetime(test_df['date'])

    # Test get_year_month
    result_df = dp.get_year_month(test_df)
    assert 'year' in result_df.columns and 'month' in result_df.columns
    assert result_df['year'].iloc[0] == 2020 and result_df['month'].iloc[0] == 1


def test_get_stats(data_preprocessing_config):
    dp = DataPreprocessing(config=data_preprocessing_config)

    # Create a test DataFrame
    test_data = {
        'date': pd.to_datetime(['2022-07-31', '2022-07-31']),
        'region_id': [66027, 97813],
        'indicator_id': ['Z4BR', 'Z4BR'],  # Assuming these are in interested_indicators_stats
        'value': [472191.62, 2146551.00],
        'year': [2022, 2022],
        'month': [7, 7]
    }
    test_df = pd.DataFrame(test_data)

    # Test get_stats
    stats_df = dp.get_stats(test_df)
    assert not stats_df.empty
    assert 'Z4BR' in stats_df.columns

