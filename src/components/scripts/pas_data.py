import pandas as pd
import os
from pathlib import Path
import datetime

data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')


def import_clean_PAS_data(data_directory):
    # Construct the file path
    file_path = os.path.join(data_directory, 'pas_data/pas_original.csv')


    df_data = pd.read_csv(os.path.join(data_directory, 'pas_data/pas_original.csv'), delimiter=";")
    # Drop the 'Survey' column
    df_data = df_data.drop(columns='Survey', axis=1)


 # Change column type of 'Date' to datetime, filter on just one date (for now)
    df_data['Date'] = pd.to_datetime(df_data['Date'])
    df_data = df_data[~(df_data['Date'] == datetime.date(2014, 12, 31))]
    df_data['Proportion'] = df_data['Proportion'].str.replace(',', '.').astype(float)
    return df_data

def restructure_PAS_data(df_data, category_types, geo_boroughs):
    # Define a new dataframe, which has the measures as columns

    df_data1 = pd.DataFrame(columns=['Date', 'Borough', *category_types])
    df_data1['Date'] = df_data['Date']
    df_data1['Borough'] = df_data['Borough']

    for i in range(len(df_data)):
        measure = df_data.loc[i, 'Measure']
        value = df_data.loc[i, 'Proportion']
        borough = df_data.loc[i, 'Borough']
        df_data1.loc[df_data1.index[df_data1['Borough'] == borough].tolist()[0], measure] = value

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
