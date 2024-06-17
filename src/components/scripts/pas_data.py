import pandas as pd
import os
from pathlib import Path
import datetime

data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')


def import_clean_PAS_data(data_directory):
    df_data = pd.read_csv(os.path.join(data_directory, 'pas_data/pas_original.csv'), delimiter=";")
    # Drop the 'Survey' column
    df_data = df_data.drop(columns='Survey', axis=1)

    # Change column type of 'Date' to datetime, filter on just one date (for now)
    df_data['Date'] = pd.to_datetime(df_data['Date'])
    df_data['Proportion'] = df_data['Proportion'].str.replace(',', '.').astype(float)
    return df_data

def restructure_PAS_data(df_data, category_types, geo_boroughs):
    # Define a new dataframe, which has the measures as columns

    # df_data1 = df_data.drop(columns=['Survey', 'MPS'])
    df_data1 = df_data.pivot_table(index=['Borough', 'Date'], columns='Measure', values='Proportion', fill_value=0).reset_index()

    # Change necessary names, to make them match
    df_data1.loc[df_data1['Borough'] == 'City of Westminster', 'Borough'] = 'Westminster'
    df_data1.loc[df_data1['Borough'] == 'Richmond Upon Thames', 'Borough'] = 'City of London'
    # Duplicate "Richmond Upon Thames", no City of "London"

    boroughs = df_data1['Borough'].unique()

    for borough in boroughs:
        if borough not in geo_boroughs:
            print("boroughs not in geo_boroughs", borough)
    for borough in geo_boroughs:
        if borough not in boroughs:
            print("geo_boroughs not in boroughs", borough)

    # Make sure value type is ´float´
    for cat in category_types:
        df_data1[cat] = df_data1[cat].astype(float)

    return df_data1, boroughs
