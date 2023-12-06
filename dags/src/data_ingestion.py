import os
import zipfile
import pandas as pd
import os
import json
import subprocess
import logging

def download_data(**kwargs):
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.

    Returns:
        bytes: Serialized data.
    """
    logger = logging.getLogger("airflow.task")

    logger.info("Starting download data task")
    # Run the curl command using subprocess
    subprocess.run(['curl', '-o', os.path.join(os.path.dirname(__file__), '../data/download_link.json'),
                    'https://data.nasdaq.com/api/v3/datatables/ZILLOW/DATA?qopts.export=true&api_key=yaXdjWK7YAbeWZMoqphn'])

    logger.info("Json file with download link to zip file downloaded")
    # Specify the path to your JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/download_link.json')

    # Open and read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    download_link = data["datatable_bulk_download"]["file"]["link"]

    # Run the curl command using subprocess
    subprocess.run(['curl', '-o', os.path.join(os.path.dirname(__file__), '../data/zillow_data.zip'),
                    download_link])

    logger.info("Data zip file downloaded")

    # !curl -o zillow_data.zip '{download_link}'

    # Get the current working directory
    current_directory = os.getcwd()
    zip_file_path = os.path.join(os.path.dirname(__file__), '../data/zillow_data.zip')
    # Path where you want to extract the CSV file
    output_dir = current_directory

    logger.info("Starting zip file extraction")

    # Open the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        # List the contents of the ZIP file (optional)
        zip_file_contents = zip_file.namelist()
        print("Contents of the ZIP file:", zip_file_contents)

        # Extract the CSV file (assuming there's only one CSV file in the ZIP)
        for file_name in zip_file_contents:
            if file_name.endswith('.csv'):
                zip_file.extract(file_name, os.path.join(os.path.dirname(__file__), '../data/'))
                extracted_csv_path = output_dir + file_name
                print(f"Extracted CSV file: {extracted_csv_path}")
    logger.info(f"Extracted CSV file: {extracted_csv_path}")
    logger.info("zip file extraction done")

    subprocess.run(['mv', os.path.join(os.path.dirname(__file__), '../data/') + file_name,
                    os.path.join(os.path.dirname(__file__), '../data/zillow_data.csv')])
    # serialized_data = pickle.dumps(df)
    #
    # return serialized_data
