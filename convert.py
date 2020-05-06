#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import pandas as pd
from pandas import DataFrame
from lxml import objectify
import os


def convert_to_df(filename):
    '''
    xml fileをdfに格納
    '''

    headers = ['type','unit','startDate','endDate','value']
    parsed = objectify.parse(open(filename))
    root = parsed.getroot()

    data = [({k: v for k, v in elem.attrib.items() if k in headers})
            for elem in root.Record]
    df = DataFrame(data)
    print('\n'.join(df['type'].unique()))
    print('取得したデータ数: {}'.format(len(df)))
    return df

def extract_data(df,typename):
    '''
    特定のデータだけを取得
    '''

    exdf = df[df['type'] == typename]
    exdf['value'] = exdf['value'].astype(float)
    
    print(exdf)
    print(len(exdf))
    
    exdf.to_csv(args.output_path + os.path.basename(os.path.splitext(args.input_path)[0]) + '_step.csv')
    return exdf

def daily_count(df):
    '''
    日ごとに集計xxx
    '''

    dfstep = DataFrame({'step': df['value'].tolist()},index=df['endDate'])
    dfstep.index = pd.to_datetime(dfstep.index, utc=True)
    dfstep['datetime'] = dfstep.index.tz_convert('Asia/Tokyo')
    dfstep['date'] = dfstep['datetime'].dt.date
    sumdf = dfstep.groupby(['date']).sum()
    sumdf.to_csv(args.output_path + os.path.basename(os.path.splitext(args.input_path)[0]) + '_sumstep.csv')

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_path',help='input path (.xml)')
    parser.add_argument('-o','--output_path',help='output path (/)')
    args = parser.parse_args()

    df = convert_to_df(args.input_path)
    stepdf = extract_data(df, 'HKQuantityTypeIdentifierStepCount')
    daily_count(stepdf)
