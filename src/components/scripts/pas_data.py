from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
import datetime
import geojson
import numpy as np
from pyproj import Proj, transform
import json

# data_directory = 'data'
data_directory = os.path.join(Path(os.getcwd()).parent.parent, 'data')
# import csv
#
# file_path = os.path.join(data_directory, 'pas_data3.csv')
#
# # Path to the input file
# input_file_path = 'C:/Users/20223080/PycharmProjects/police-data-analysis2/src/data/pas_data3.csv'
#
# # Define the column names without the 'Survey' column
# column_names = ["Date","Survey", "Borough", "Measure", "Proportion", "MPS"]
#
# # Create a list to hold the parsed data
# parsed_data = []
#
# # Open and read the input file
# with open(file_path, 'r') as infile:
#     for row in infile:
#         # Strip any leading/trailing whitespace and split by comma
#         split_row = row.strip().split(',')
#         # Drop the 'Survey' column (index 1) and append the relevant columns
#         parsed_data.append([split_row[0],split_row[1], split_row[2], split_row[3], split_row[4], split_row[5]])
#
# # Print the parsed data (optional)
# print(parsed_data)
#
# # Print the parsed data (optional)
# #print(parsed_data)
#
# # Overwrite the input file with the parsed data
# with open(input_file_path, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     # Write the column headers
#     writer.writerow(column_names)
#     # Write the data rows
#     writer.writerows(parsed_data)

# def import_clean_PAS_data(data_directory):
#     # Import PAS data
#     df_data = pd.read_csv(os.path.join(data_directory, 'pas_data2.csv'), delimiter=";")
#     df_data = df_data.drop(columns='Survey', axis=1)  # Clean unnecessary column
#     #df_data = './data/pas_data2.csv'
#    # df_data = df_data.drop(columns='Survey', axis=1)  # Clean unnecessary column
#     # Change column type of 'Date' to datetime, filter on just one date (for now)
#     df_data['Date'] = pd.to_datetime(df_data['Date'])
#     df_data = df_data[~(df_data['Date'] == datetime.date(2014, 12, 31))]
#     #df_data['Proportion'] = df_data['Proportion'].str.replace(',', '.').astype(float)
#     return df_data

def import_clean_PAS_data(data_directory):
    # Construct the file path
    file_path = os.path.join(data_directory, 'pas_data3.csv')

    # # Check if the file exists
    # if not os.path.isfile(file_path):
    #     raise FileNotFoundError(f"No such file or directory: '{file_path}'")

    # # Read the file line by line and split by commas
    # parsed_data = []
    # with open(file_path, 'r') as infile:
    #     for line in infile:
    #         parsed_data.append(line.strip().split(','))
    #
    # # Define the column names
    # column_names = ["Date", "Survey", "Borough", "Measure", "Proportion", "MPS"]
    #
    # # Create a DataFrame
    # df_data = pd.DataFrame(parsed_data, columns=column_names)
    df_data = pd.read_csv(os.path.join(data_directory, 'pas_data3.csv'), delimiter=";")
    # Drop the 'Survey' column
    df_data = df_data.drop(columns='Survey', axis=1)


 # Change column type of 'Date' to datetime, filter on just one date (for now)
    df_data['Date'] = pd.to_datetime(df_data['Date'])
    df_data = df_data[~(df_data['Date'] == datetime.date(2014, 12, 31))]
    df_data['Proportion'] = df_data['Proportion'].str.replace(',', '.').astype(float)
    return df_data

def restructure_PAS_data(df_data, category_types, boroughs):
    # Define a new dataframe, which has the measures as columns
    df_data1 = pd.DataFrame(columns=['Date', 'Borough', *category_types])
    df_data1['Borough'] = boroughs
    df_data1['Date'] = datetime.date(2014, 12, 31)
    for i in range(len(df_data)):
        measure = df_data.loc[i, 'Measure']
        value = df_data.loc[i, 'Proportion']
        borough = df_data.loc[i, 'Borough']
        df_data1.loc[df_data1.index[df_data1['Borough'] == borough].tolist()[0], measure] = value

    # Change necessary names, to make them match
    df_data1.loc[df_data1.index[df_data1['Borough'] == 'City of Westminster'].tolist()[0], 'Borough'] = 'Westminster'
    df_data1.loc[df_data1.index[df_data1['Borough'] == 'Richmond Upon Thames'].tolist()[0], 'Borough'] = 'City of London'
    # Duplicate "Richmond Upon Thames", no City of "London"

    boroughs = df_data1['Borough'].unique()

    # Make sure value type is ´float´
    for cat in category_types:
        df_data1[cat] = df_data1[cat].astype(float)

    return df_data1, boroughs

# df_data1 = pd.DataFrame(columns=['Date', 'Borough', *category_types])
# print(df_data1)