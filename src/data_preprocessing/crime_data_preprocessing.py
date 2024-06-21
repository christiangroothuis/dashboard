import os
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from typing import Tuple, Optional

def load_data() -> Tuple[gpd.GeoDataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the data needed for crime data preprocessing.
    :returns: geodataframe with borough data and three dataframes with outcomes, stop-and-search, and street data, respectively.
    """
    # define paths
    borough_file = '../data/London_Boroughs.gpkg'
    outcomes_file = '../data/crime_data/outcomes_combined.csv'
    ss_file = '../data/crime_data/ss_combined.csv'
    street_file = '../data/crime_data/street_combined.csv'

    # load the data
    borough_data = gpd.read_file(borough_file)
    outcomes_df = pd.read_csv(outcomes_file)
    ss_df = pd.read_csv(ss_file)
    street_df = pd.read_csv(street_file)

    return borough_data, outcomes_df, ss_df, street_df

def find_borough(point: Point, borough_data: gpd.GeoDataFrame) -> Optional[str]:
    """
    Find borough name for a given point.
    :param point: point representing a location
    :param borough_data: dataframe with borough data
    :returns: the name of the borough containing the point, or None if no borough contains the point.
    """
    # create spatial index
    borough_data.sindex

    # find possible matches within the spatial index
    possible_matches_index = list(borough_data.sindex.intersection(point.bounds))
    possible_matches = borough_data.iloc[possible_matches_index]

    # find the exact match, or return None
    for idx, borough in possible_matches.iterrows():
        if borough['geometry'].contains(point):
            return borough['name']
    return None

def add_borough_name(df: pd.DataFrame, borough_data: gpd.GeoDataFrame, type: str) -> pd.DataFrame:
    """
    Add borough name to the dataframe based on longitude and latitude and save the resulting dataframe.
    :param df: input dataframe with longitude and latitude.
    :param borough_data: geodataframe with borough data
    :param type: type of the data to be saved, e.g. outcomes, stop-and-search, street
    :returns: dataframe with added column with borough names for each row
    """
    # split the dataframe into chunks
    df_split = np.array_split(df, 10000)
    processed_chunks = []
    i = 1

    # iterate over chunks
    for chunk in df_split:
        print('chunk: ', i, '/10000')

        # create a GeoDataFrame from the latitude and longitude coordinates
        geometry = [Point(xy) for xy in zip(chunk['longitude'], chunk['latitude'])]
        points_gdf = gpd.GeoDataFrame(chunk, geometry=geometry)

        # ensure both GeoDataFrames use the same coordinate reference system (CRS)
        borough_data = borough_data.to_crs(epsg=4326)  # assuming WGS84 CRS
        points_gdf = points_gdf.set_crs(epsg=4326)

        # find borough name
        points_gdf['borough_name'] = points_gdf['geometry'].apply(lambda x: find_borough(x, borough_data))

        processed_chunks.append(points_gdf)
        i += 1

    # concatenate the chunks into one dataframe
    df_combined = pd.concat(processed_chunks)
    
    # remove entries without borough names
    df_final = df_combined.dropna(subset=['borough_name'])

    return df_final

def finalize_data(df: pd.DataFrame, type: str) -> pd.DataFrame:
    """
    Check borough assignment and rearrange columns for the final dataframe.
    :param df: dataframe with outcomes data with borough names.
    :param type: type of data, e.g. outcomes, stop and search (abbr. ss), street.
    :returns: final outcomes dataframe.
    """
    # drop City of Lodon
    borough_df = df[df['borough_name'] != 'City of London']

    if type == 'outcomes':
        # drop irrelevant columns
        compact_df = borough_df.drop(['crime_id', 'lsoa_code', 'lsoa_name', 'quarter', 'geometry'], axis=1).copy()

        # rearrange columns
        cols = compact_df.columns.tolist()
        cols1 = cols[-2:] + [cols[4]] + cols[:4]
        reorder_df = compact_df[cols1]
    
    elif type == 'street':
        # drop irrelevant columns
        compact_df = borough_df.drop(['crime_id', 'lsoa_code', 'lsoa_name', 'quarter', 'geometry'], axis=1).copy()

        # rearrange columns
        cols = compact_df.columns.tolist()
        cols1 = cols[-2:] + [cols[5]] + cols[:5]
        reorder_df = compact_df[cols1]
    
    elif type == 'ss':
        # drop irrelevant columns
        compact_df = borough_df.drop(['quarter', 'geometry'], axis=1).copy()

        # rearrange columns
        cols = compact_df.columns.tolist()
        cols1 = [cols[-5]] + cols[-1:] + cols[-4:-1] + cols[:-5]
        reorder_df = compact_df[cols1]

    return reorder_df

def save_data_to_csv(df: pd.DataFrame, type: str) -> None:
    """
    Save dataframe to csv in data/crime_data.
    :param df: dataframe to be saved
    :param type: type of the data to be saved, e.g. outcomes, stop-and-search, street
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

# add borough names
borough_df, outcomes_df, ss_df, street_df = load_data()
print('data loaded')
borough_outcomes_df = add_borough_name(outcomes_df, borough_df, 'outcomes')
print('boroughs for outcomes done')
borough_ss_df = add_borough_name(ss_df, borough_df, 'ss')
print('boroughs for ss done')
borough_street_df = add_borough_name(street_df, borough_df, 'street')
print('boroughs for street done')

# borough_outcomes_df = pd.read_csv('../data/crime_data/outcomes_boroughs_joined.csv')
# borough_ss_df = pd.read_csv('../data/crime_data/ss_boroughs_joined.csv')
# borough_street_df = pd.read_csv('../data/crime_data/street_boroughs_joined.csv')

# finalize data for the dashboard
final_outcomes = finalize_data(borough_outcomes_df, 'outcomes')
print('outcomes done')
final_ss = finalize_data(borough_ss_df, 'ss')
print('ss done')
final_street = finalize_data(borough_street_df, 'street')
print('street done')

# save results to csv
save_data_to_csv(final_outcomes, 'outcomes')
save_data_to_csv(final_ss, 'stop_search')
save_data_to_csv(final_street, 'street')