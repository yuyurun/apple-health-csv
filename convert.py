#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import pandas as pd
from pandas import DataFrame
from lxml import objectify

def main(filename):
    headers = ['type','unit','startDate','endDate','value']
    parsed = objectify.parse(open(filename))
    root = parsed.getroot()

    data = [({k: v for k, v in elem.attrib.items() if k in headers})
            for elem in root.Record]
    df = DataFrame(data)
    print(df.head())
    print(len(df))
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_path',help='input path (.xml)')
    args = parser.parse_args()

    main(args.input_path)
