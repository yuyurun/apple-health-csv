#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import pandas as pd
from pandas import DataFrame
from lxml import objectify


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
    
    print(exdf)
    print(len(exdf))



    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_path',help='input path (.xml)')
    args = parser.parse_args()

    df = convert_to_df(args.input_path)
    extract_data(df, 'HKQuantityTypeIdentifierStepCount')
