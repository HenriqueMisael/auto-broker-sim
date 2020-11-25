from datetime import datetime, timedelta
from decimal import Decimal

import pandas as pd


def start_of_month(string_date):
    date = datetime.strptime(string_date, '%Y-%m-%d')
    return date.day == 1


def end_of_month(string_date):
    date = datetime.strptime(string_date, '%Y-%m-%d')
    last_day = (datetime(date.year, date.month, 1).__add__(datedelta(m)).today() - timedelta(
        days=1)).day
    return date.day == last_day


values = []
previous = None

for i, Data in pd.read_csv(
        '../output/2015-07-01 to 2016-06-30_dbd.tsv', header=0,
        sep='\t').iterrows():
    if start_of_month(Data['Date']):
        previous = Data
    elif end_of_month(Data['Date']):
        if previous is not None:
            values.append([
                Decimal(Data['Close value'].replace(",", ".")) / Decimal(
                    previous['Close value'].replace(",", ".")),
                Decimal(Data['Simple (14)'].replace(",", ".")) / Decimal(
                    previous['Simple (14)'].replace(",", ".")),
            ])
