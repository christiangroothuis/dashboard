import os
import numpy as np
import pandas as pd
from typing import List

def save_df_to_csv(df: pd.DataFrame, type: str) -> None:
    """
    Save dataframe to csv in data/pas_data.
    :param df: dataframe to be saved
    :param type: type of the data to be saved
    """
    # path to the data folder
    data_folder = "../data"

    # check if the directory exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print('The new directory is created!')

    # save dataframe
    df.to_csv(f'{data_folder}/{type}.csv', index=False)
    print(f"CSV {type} saved.")

def clean_ethnicity_data(borough_names: List[str]) -> None:
    """
    Combine, clean and save ethnicity data.
    :param borough_names: list with the names of Greater London boroughs.
    """
    # load the data
    file_path = '../data/ethnic-groups-by-borough.xls'
    df_ethnicity = pd.read_excel(file_path, sheet_name=None)

    # create column mapping
    column_mapping = {'Code': 'code', 'Area': 'borough_name', 'Number': 'white', 'Unnamed: 3': 'asian',
                        'Unnamed: 4': 'black', 'Unnamed: 5': 'mixed_other', 'Unnamed: 6': 'total',
                        'Unnamed: 7': 'delete', '95% Confidence Interval': 'delete', 'Unnamed: 9': 'delete',
                        'Unnamed: 10': 'delete', 'Unnamed: 11': 'delete', 'Unnamed: 12': 'delete'}
    
    selected_columns = ["year"] + list(column_mapping.values())

    # iterate over dataframes for different years and combine them
    cleaned_dfs = []
    for year, df in df_ethnicity.items():
        if year.isdigit() == False:
            continue

        df = df.rename(columns=column_mapping)
        df["year"] = year
        df = df[selected_columns]
        df = df.rename(columns=column_mapping)
        cleaned_dfs.append(df)

    merged_cleaned_df = pd.concat(cleaned_dfs, ignore_index=True)

    # delete NaN entries
    merged_cleaned_df.dropna(subset=["borough_name"], inplace=True)
    # remove irrelevant columns
    merged_cleaned_df = merged_cleaned_df.drop(['code', 'delete'], axis=1).copy()
    # keep only the data for boroughs
    merged_cleaned_df = merged_cleaned_df[merged_cleaned_df['borough_name'].isin(borough_names)]
    merged_cleaned_df = merged_cleaned_df[merged_cleaned_df['borough_name'] != 'City of London']
    # sort by borough name and year
    merged_cleaned_df.sort_values(by=["borough_name", "year"], inplace=True)

    # save the data to csv        
    save_df_to_csv(merged_cleaned_df, 'ethnicity')

# create a list of borough names
borough_names = ['Kingston upon Thames', 'Croydon', 'Bromley', 'Hounslow', 'Ealing', 'Havering', 'Hillingdon', 
                 'Harrow', 'Brent', 'Barnet', 'Lewisham', 'Greenwich', 'Bexley', 'Enfield', 'Waltham Forest', 
                 'Lambeth', 'Redbridge', 'Sutton', 'Richmond upon Thames', 'Merton', 'Wandsworth', 'Hammersmith and Fulham', 
                 'Southwark', 'Kensington and Chelsea', 'Westminster', 'Camden', 'Tower Hamlets', 'Islington', 'Hackney', 
                 'Haringey', 'Newham', 'Barking and Dagenham']

clean_ethnicity_data(borough_names)