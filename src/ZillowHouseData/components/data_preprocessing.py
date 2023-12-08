import os, sys
import pandas as pd
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
from src.ZillowHouseData.entity.config_entity import DataPreprocessingConfig


class DataPreprocessing:

    def __init__(self, config: DataPreprocessingConfig):
        self.config = config
        self.file_name = self.config.file_name
        self.file_name = os.path.join('artifacts', 'data_ingestion', self.file_name)
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

    def read_and_filter_data(self):
        try:
        # Read the CSV file
            df = pd.read_csv(self.file_name, usecols= self.interested_columns, dtype=self.dtypes)
            start_date_pd = pd.to_datetime(self.start_date)

            # Filter rows by date
            df['date'] = pd.to_datetime(df['date'])  # Ensure date column is in datetime format
            df = df[df['date'] >= start_date_pd]
            return df
        except Exception as e:
            raise CustomException(e,sys)

    def get_year_month(self, df):
        try:
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
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
            return final_df
        except Exception as e:
            raise CustomException(e,sys)
    
