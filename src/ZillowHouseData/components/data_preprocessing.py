import os, sys
import pandas as pd
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.entity.config_entity import DataPreprocessingConfig
import numpy as np
from functools import reduce


class DataPreprocessing:

    def __init__(self, config: DataPreprocessingConfig):
        self.config = config
        self.file_name = self.config.file_name
        self.file_path = os.path.join('artifacts', 'data_ingestion', self.file_name)
        self.region_file_name = self.config.region_file_name
        self.region_file_path = os.path.join('artifacts', 'data_ingestion', self.region_file_name)
        self.start_date = self.config.start_date
        self.interested_columns = self.config.interested_columns
        self.interested_indicators_stats = self.config.interested_indicators_stats
        self.interested_indicators_zhvi = self.config.interested_indicators_zhvi
        self.stats_path = self.config.stats_path
        self.final_csv_path = self.config.final_csv_path

        # Define data types for columns
        self.dtypes = {
            'indicator_id': 'object',
            'region_id': 'int32',
            'value': 'float32',
            'date': 'object'
        }

    def read_and_filter_data(self, chunk_size=10000):
        # Read the CSV file in chunks
        try:
            logger.info(">>>>>> filename data <<<<<<\n\nx==========x")
            logger.info(self.file_name)
            logger.info(">>>>>> path data <<<<<<\n\nx==========x")
            logger.info(self.file_path)

            chunks = pd.read_csv(self.file_path, usecols=['indicator_id', 'region_id', 'date', 'value'],
                                dtype=self.dtypes, chunksize=chunk_size)
            
            filtered_chunks = []
            for chunk_number, chunk in enumerate(chunks, start=1):
                #logger.info(f"Processing Chunk {chunk_number}")
                # Filter rows by date
                chunk['date'] = pd.to_datetime(chunk['date'])  # Ensure date column is in datetime format
                start_date = np.datetime64(self.start_date) # Convert self.start_date to datetime64[ns]
                chunk = chunk[chunk['date'] >= start_date]
                filtered_chunks.append(chunk)

            # Concatenate the filtered chunks into a single DataFrame
            filtered_df = pd.concat(filtered_chunks, ignore_index=True)
            return filtered_df
        except Exception as e:
            raise CustomException(e,sys)


    def get_year_month(self, df):
        try:
            df['year'] = df['date'].dt.year.astype('int16')
            df['month'] = df['date'].dt.month.astype('int8')
            return df
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_stats(self, df):
        try:
            interested_indicators_stats = self.interested_indicators_stats
            stat_df = df[df['indicator_id'].isin(interested_indicators_stats)]
            stat_pivot_df = stat_df.pivot_table(index=['region_id', 'year', 'month'], columns='indicator_id',
                                            values='value', aggfunc='mean').reset_index()
            stat_pivot_df.dropna(inplace=True)
            stat_pivot_df.to_csv(self.stats_path)
            return stat_pivot_df
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_merge(self, df_stats, df_month_year):
        try:
            interested_indicators_ZHVI = self.interested_indicators_zhvi
            ZHVI_df = df_month_year[df_month_year['indicator_id'].isin(interested_indicators_ZHVI)]
            
            final_df = pd.merge(ZHVI_df, df_stats, on=['region_id', 'year', 'month'], how='inner')
            final_df.to_csv(self.final_csv_path)
            logger.info(f">>>>>> Saved final.csv to {self.final_csv_path} <<<<<<\n\nx==========x")

            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                print(f"The file '{self.file_path}' has been deleted.")
            else:
                print(f"The file '{self.file_path}' does not exist.")

            return final_df
        
        except Exception as e:
            raise CustomException(e,sys)

    # def optimize_memory_usage(self, df):
    #     # Optimize memory usage for individual DataFrame
    #     df['year'] = df['date'].dt.year.astype('int16')
    #     df['month'] = df['date'].dt.month.astype('int8')
    #     return df

    # def get_merge(self, df_stats, df_month_year):
    #     try:
    #         logger.info(f">>>>>> test1 <<<<<<\n\nx==========x")
    #         # Filter the DataFrame in-place instead of creating a new one
    #         interested_indicators_ZHVI = self.interested_indicators_zhvi
    #         df_month_year = df_month_year[df_month_year['indicator_id'].isin(interested_indicators_ZHVI)]

    #         logger.info(f">>>>>> test2 <<<<<<\n\nx==========x")
    #         # Specify the data types to minimize memory usage
    #         dtype_dict = {'region_id': 'int32', 'year': 'int16', 'month': 'int8'}
    #         df_stats = df_stats.astype(dtype_dict)
    #         df_month_year = df_month_year.astype(dtype_dict)

    #         logger.info(f">>>>>> test3 <<<<<<\n\nx==========x")
    #         # Explicitly specify 'inner' join to reduce memory consumption
    #         final_df = pd.merge(df_month_year, df_stats, on=['region_id', 'year', 'month'], how='inner')

    #         logger.info(f">>>>>> test4 <<<<<<\n\nx==========x")
    #         # Save the CSV file with minimal memory usage settings
    #         final_df.to_csv(self.final_csv_path, index=False, float_format='%.2f')

    #         # Log a message indicating that the CSV file has been saved
    #         logger.info(f">>>>>> Saved final.csv to {self.final_csv_path} <<<<<<\n\nx==========x")

    #         logger.info(f">>>>>> filter_df Delete <<<<<<\n\nx==========x")    
    #         filter_df_csv_path = 'artifacts/data_ingestion/filter_df.csv'
    #         os.remove(filter_df_csv_path)

    #         return final_df
    #     except Exception as e:
    #         raise CustomException(e, sys)

    
    def extract_unique_regions(self, df):
        """
        Reads a CSV file, merges it with a given DataFrame on 'region_id',
        extracts and sorts unique 'region_id' and 'region', and returns a dictionary for region_id to region lookup.

        :param df: DataFrame to merge with the CSV data.
        :return: Dictionary for region_id to region lookup.
        """
        try:
            # Read CSV file
            df_regions = pd.read_csv(self.region_file_path)

            # Merge the provided DataFrame with the CSV data
            df_region_merge = pd.merge(df, df_regions, on='region_id', how='inner')

            # Extract unique 'region_id' and 'region', and reset the index
            unique_regions_df = df_region_merge[['region_id', 'region']].drop_duplicates(subset=['region_id', 'region'])

            # Sort the DataFrame based on 'region'
            sorted_unique_regions_df = unique_regions_df.sort_values(by='region').reset_index(drop=True)

            # Convert sorted DataFrame to dictionary for region_id to region lookup
            region_id_to_region = dict(zip(sorted_unique_regions_df['region_id'], sorted_unique_regions_df['region']))

            return region_id_to_region
        except Exception as e:
            raise CustomException(e, sys)