import pytest
import os
from src.ZillowHouseData.entity.config_entity import DataIngestionConfig
from src.ZillowHouseData.components.data_ingestion import DataIngestion

@pytest.fixture
def data_ingestion_config():
    # Create a DataIngestionConfig object with your configuration
    config = DataIngestionConfig(
        root_dir= 'artifacts/data_ingestion',
        source_URL='https://drive.google.com/file/d/1WqpLl5PbrhODaj4WuBB5tDvNCpQDm8MW/view',
        local_data_file='artifacts/data_ingestion/zillow_files.zip',
        unzip_dir='artifacts/data_ingestion'
    )
    return config

def test_download_and_extract(data_ingestion_config):
    data_ingestion = DataIngestion(config=data_ingestion_config)
    
    # Call download
    data_ingestion.download_file()

    # Check if the file has been downloaded
    assert os.path.exists(data_ingestion_config.local_data_file)

    # Test extract
    data_ingestion.extract_zip_file()
    assert os.path.exists(data_ingestion_config.unzip_dir)

    # Your test assertions and other code...

    # Cleanup
    if os.path.exists(data_ingestion_config.local_data_file):
        os.remove(data_ingestion_config.local_data_file)
    if os.path.exists(data_ingestion_config.unzip_dir):
        # Remove extracted files and directory
        for root, dirs, files in os.walk(data_ingestion_config.unzip_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(data_ingestion_config.unzip_dir)

