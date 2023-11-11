import os, sys
from ZillowHouseData.logger import logger
from ZillowHouseData.exception import CustomException
import pandas as pd
import pickle

class DataPreprocessing:
    def __init__(self, file_name='ZILLOW_DATA_962c837a6ccefddddf190101e0bafdaf.csv', start_date='2012-01-01'):
        #self.file_name = file_name
        self.file_name = os.path.join('artifacts', 'data_ingestion',file_name)
        self.start_date = start_date

    def data_preprocessing(self):
        dtypes = {
            'indicator_id': 'object',
            'region_id': 'int32',
            'value': 'float32',
            'date': 'object'
        }
        df_list = []
        count = 0
        
        for chunk in pd.read_csv(self.file_name, chunksize=1000000,
                                 usecols=['indicator_id', 'region_id', 'date', 'value'],
                                 dtype=dtypes,
                                 parse_dates=['date']):
            filtered_chunk = chunk[(chunk['date'] >= self.start_date)]
            df_list.append(filtered_chunk)

        trimmed_df = pd.concat(df_list, ignore_index=True)

        del df_list
        
        trimmed_data = pickle.dumps(trimmed_df)
    
        return trimmed_data

    def get_year_month(self, data):
        trimmed_df = pickle.loads(data)
        trimmed_df['year'] = pd.to_datetime(trimmed_df['date']).dt.year
        trimmed_df['month'] = pd.to_datetime(trimmed_df['date']).dt.month
        trimmed_data = pickle.dumps(trimmed_df)
        return trimmed_data

    def get_stats(self, data):
        trimmed_df = pickle.loads(data)
        intersted_indicators_stats = ['IRAM', 'CRAM', 'MRAM', 'LRAM', 'NRAM', 'SRAM']
        stat_df = trimmed_df[trimmed_df['indicator_id'].isin(intersted_indicators_stats)]
        stat_pivot_df = stat_df.pivot_table(index=['region_id', 'year', 'month'], columns='indicator_id',
                                           values='value', aggfunc='mean')
        stat_pivot_df.reset_index(inplace=True)
        stat_pivot_df.dropna(inplace=True)
        stat_pivot_df.to_csv("./artifacts/data_ingestion/stats.csv")
        del stat_df
        trimmed_data = pickle.dumps(trimmed_df)
        return trimmed_data

    def get_merge(self, data):
        trimmed_df = pickle.loads(data)
        df = pd.read_csv('stat.csv')
        intersted_indicators_ZHVI = ['ZATT', 'ZSFH', 'ZALL', 'ZCON', 'ZABT', 'Z2BR', 'Z5BR', 'Z3BR', 'Z1BR', 'Z4BR']
        ZHVI_df = trimmed_df[trimmed_df['indicator_id'].isin(intersted_indicators_ZHVI)]
        del trimmed_df
        final_df = pd.merge(ZHVI_df, df, on=['region_id', 'year', 'month'], how='inner')
        final_data = pickle.dumps(final_df)
        final_df.to_csv("./artifacts/data_ingestion/final.csv")
        return final_data
