import os, sys
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException
import pandas as pd

class DataPreprocessing:
    def __init__(self, file_name='ZILLOW_DATA_962c837a6ccefddddf190101e0bafdaf.csv', start_date='2012-01-01'):
        self.file_name = os.path.join('artifacts', 'data_ingestion', file_name)
        self.start_date = pd.to_datetime(start_date)

        # Define data types for columns
        self.dtypes = {
            'indicator_id': 'object',
            'region_id': 'int32',
            'value': 'float32',
            'date': 'object'
        }

    def read_and_filter_data(self):
        # Read the CSV file
        df = pd.read_csv(self.file_name, usecols=['indicator_id', 'region_id', 'date', 'value'], dtype=self.dtypes)

        # Filter rows by date
        df['date'] = pd.to_datetime(df['date'])  # Ensure date column is in datetime format
        df = df[df['date'] >= self.start_date]

        return df

    def get_year_month(self, df):
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        return df
    
    def get_stats(self, df):
        intersted_indicators_stats = ['IRAM', 'CRAM', 'MRAM', 'LRAM', 'NRAM', 'SRAM']
        stat_df = df[df['indicator_id'].isin(intersted_indicators_stats)]
        stat_pivot_df = stat_df.pivot_table(index=['region_id', 'year', 'month'], columns='indicator_id',
                                           values='value', aggfunc='mean').reset_index()
        stat_pivot_df.dropna(inplace=True)
        stat_pivot_df.to_csv("./artifacts/data_ingestion/stats.csv")
        print(stat_pivot_df.head())
        return stat_pivot_df

    def get_merge(self, df_stats, df_month_year):
        interested_indicators_ZHVI = ['ZATT', 'ZSFH', 'ZALL', 'ZCON', 'ZABT', 'Z2BR', 'Z5BR', 'Z3BR', 'Z1BR', 'Z4BR']
        ZHVI_df = df_month_year[df_month_year['indicator_id'].isin(interested_indicators_ZHVI)]
        
        final_df = pd.merge(ZHVI_df, df_stats, on=['region_id', 'year', 'month'], how='inner')
        final_df.to_csv("./artifacts/data_ingestion/final.csv")
        return final_df