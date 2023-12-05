import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
# from kneed import KneeLocator
import pickle
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

    subprocess.run(['mv', os.path.join(os.path.dirname(__file__), '../data/')+file_name, os.path.join(os.path.dirname(__file__), '../data/zillow_data.csv')])
    # serialized_data = pickle.dumps(df)
    #
    # return serialized_data


def load_data(**kwargs):
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.

    Returns:
        bytes: Serialized data.
    """
    logger = logging.getLogger("airflow.task")

    logger.info("Starting Load data task")

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/zillow_data.csv'))
    del df
    # serialized_data = pickle.dumps(df)
    #
    # return serialized_data


def data_preprocessing(**kwargs):
    """
    Deserializes data, performs data preprocessing, and returns serialized clustered data.

    Args:
        data (bytes): Serialized data to be deserialized and processed.

    Returns:
        bytes: Serialized clustered data.
    """
    logger = logging.getLogger("airflow.task")

    logger.info("Starting data preprocessing task")

    # Construct file path
    file_name = os.path.join(os.path.dirname(__file__), '../data/zillow_data.csv')
    logger.info(f"File path set to {file_name}")
    start_date = '2012-01-01'  # Example start date

    # Define the data types for more efficient memory usage
    dtypes = {
        'indicator_id': 'object',
        'region_id': 'int32',
        'value': 'float32',
        'date': 'object'
    }

    # Initialize a list to hold chunks of the processed dataframe
    df_list = []
    count = 0
    # Process the CSV in chunks
    for chunk in pd.read_csv(file_name, chunksize=1000000,
                             usecols=['indicator_id', 'region_id', 'date', 'value'],
                             dtype=dtypes,
                             parse_dates=['date']):
        # Filter the chunk and append to the list
        filtered_chunk = chunk[(chunk['date'] >= start_date) ]
        # filtered_chunk.to_csv(f'/Users/dheeraj/Desktop/mlops data/df_chunk_{count}.csv')
    #     print(count)
        logger.info(f"chunk:  {count} reading done")
        count = count +1
        df_list.append(filtered_chunk)
    logger.info("Reading chunks finished")
    # Concatenate the filtered chunks into one dataframe
    trimmed_df = pd.concat(df_list, ignore_index=True)
    logger.info("Chunks have been concated")

    # Save the filtered data to a new CSV file
    trimmed_df.to_csv(os.path.join(os.path.dirname(__file__), '../data/trimmed_dataset.csv'), index=False)
    logger.info("Trimmed Dataframe stored successfully")

    del df_list
    del chunk
    del trimmed_df
    # del df_filtered
    # trimmed_data = pickle.dumps(trimmed_df)
    # return trimmed_data

def get_year_month(**kwargs):

    # trimmed_df = pickle.loads(data)
    logger = logging.getLogger("airflow.task")
    logger.info("Starting Get year month task")
    trimmed_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/trimmed_dataset.csv'))

    trimmed_df['year'] = pd.to_datetime(trimmed_df['date']).dt.year
    trimmed_df['month'] = pd.to_datetime(trimmed_df['date']).dt.month

    logger.info("Year and month extraction done")

    trimmed_df.to_csv(os.path.join(os.path.dirname(__file__), '../data/trimmed_dataset.csv'), index=False)
    logger.info("File Saving done")
    del trimmed_df
    # trimmed_data = pickle.dumps(trimmed_df)
    # return trimmed_data

def get_stats(**kwargs):

    # trimmed_df = pickle.loads(data)
    logger = logging.getLogger("airflow.task")
    logger.info("Starting get_stats task")
    trimmed_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/trimmed_dataset.csv'))
    # getting just stats

    intersted_indicators_stats = ['IRAM', 'CRAM', 'MRAM', 'LRAM', 'NRAM', 'SRAM']

    stat_df = trimmed_df[trimmed_df['indicator_id'].isin(intersted_indicators_stats)]

    logger.info("Stats trimming done")

    stat_pivot_df = stat_df.pivot_table(index=['region_id', 'year', 'month'], columns='indicator_id', values='value', aggfunc='mean')
   
    logger.info("Pivoting the table done")

    # Reset the index to have a flat DataFrame
    stat_pivot_df.reset_index(inplace=True)
    stat_pivot_df.dropna(inplace = True)

    logger.info("Na's has been dropped")

    del stat_df
    del trimmed_df
    stat_pivot_df.to_csv(os.path.join(os.path.dirname(__file__), '../data/stat.csv'), indelx =False)
    logger.info("File Saving done")
    # trimmed_data = pickle.dumps(trimmed_df)
    # return trimmed_data

def get_merge(**kwargs):

    # trimmed_df = pickle.loads(data)
    logger = logging.getLogger("airflow.task")
    logger.info("Starting get merge task")
    trimmed_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/trimmed_dataset.csv'))
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/stat.csv'))
    
    logger.info("Datasets reading done")
    
    intersted_indicators_ZHVI = ['ZATT', 'ZSFH', 'ZALL', 'ZCON', 'ZABT', 'Z2BR', 'Z5BR', 'Z3BR', 'Z1BR', 'Z4BR']

    ZHVI_df = trimmed_df[trimmed_df['indicator_id'].isin(intersted_indicators_ZHVI)]
    
    logger.info("House values Trimming done")
    
    del trimmed_df

    final_df = pd.merge(ZHVI_df, df, on=['region_id', 'year', 'month'], how='inner')
    logger.info("Final df done")

    # final_data = pickle.dumps(final_df)
    final_df.to_csv(os.path.join(os.path.dirname(__file__), '../data/final.csv'),index = False)
    logger.info("File Saving done")
    # return final_data

def get_data_to_model(**kwargs):
    # trimmed_df = pickle.loads(data)
    logger = logging.getLogger("airflow.task")
    logger.info("Starting get data to model task")

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/final.csv'))

    # Drop unnecessary columns
    columns_to_remove = ['date']
    df = df.drop(columns=columns_to_remove)

    logger.info("Datasets reading done")

    # Encoding indicator_id
    indicator_encoding = {'Z1BR': 0, 'Z2BR': 1, 'Z3BR': 2, 'Z4BR': 3, 'Z5BR': 4, 'ZABT': 5, 'ZALL': 6, 'ZATT': 7,
                          'ZCON': 8, 'ZSFH': 9}
    df['indicator_id'] = df['indicator_id'].map(indicator_encoding)
    df['indicator_id'] = df['indicator_id'].astype(int)

    logger.info("indicator encoding done")

    # final_data = pickle.dumps(final_df)ß
    df.to_csv(os.path.join(os.path.dirname(__file__), '../data/final.csv'), index= False)
    logger.info("File Saving done")

    del df

    # return final_data

# logger = logging.getLogger("mylogger")
# download_data()
# load_data()
# data_preprocessing()
# get_year_month()
# get_stats()
# get_merge()
# get_data_to_model()