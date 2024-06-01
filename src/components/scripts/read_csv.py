import pandas as pd

def load_pas_data() -> pd.DataFrame:
    """
    Load pas data with count for different answers per question, borough, and year.
    :returns: dataframe loaded from a csv file.
    """
    df = pd.read_csv('../data/pas_data/pas_data_count_boroughs.csv')

    return df

def load_ethnicity_data() -> pd.DataFrame:
    """
    Load ethnicity and demographic data per borough.
    :returns: dataframe loaded from a csv file.
    """
    df = pd.read_csv('../data/ethnicity_data/ethnicity_boroughs.csv')

    return df

def load_outcomes_data() -> pd.DataFrame:
    """
    Load crime data about outcomes per borough.
    :returns: dataframe loaded from a csv file.
    """
    df = pd.read_csv('../data/crime_data/outcomes_21_24_boroughs.csv')

    return df

def load_street_data() -> pd.DataFrame:
    """
    Load crime data about street per borough.
    :returns: dataframe loaded from a csv file.
    """
    df = pd.read_csv('../data/crime_data/street_21_24_boroughs.csv')

    return df

def load_ss_data() -> pd.DataFrame:
    """
    Load crime data about stop and search per borough.
    :returns: dataframe loaded from a csv file.
    """
    df = pd.read_csv('../data/crime_data/ss_21_24_boroughs.csv')

    return df




