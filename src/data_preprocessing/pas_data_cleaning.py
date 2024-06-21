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


def clean_pas_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the pas data, add and standardize borough names.
    :param df: a dataframe to be cleaned
    :returns: cleaned dataframe
    """
    # add borough names
    df['borough_name'] = df['BOROUGHNEIGHBOURHOOD'].str.split(' - ').str[0].str.strip()

    bm = (df.borough_name.str.contains("A")) | (df['borough_name'] == '')
    nan_index = df[bm].index

    for index in nan_index:
        df.loc[index, 'borough_name'] = df.loc[index, 'ward_unique'].split(' - ')[1].strip()

    # list of wrong borough names
    wrong_names = ['Greenw', 'Southwar', 'T', 'Ne']

    # drop rows with wrong borough names
    borough_df = df[df.borough_name.isin(wrong_names) == False]

    # Replace '&' with 'and' in borough names
    borough_df['borough_name'] = borough_df['borough_name'].str.replace('&', 'and')

    # add month and year columns
    borough_df['month_abbr'] = borough_df['MONTH'].str.extract(r'\((\w{3}) \d{4}\)')[0]
    borough_df['year'] = borough_df['MONTH'].str.extract(r'\((\w{3}) (\d{4})\)')[1]

    # create a mapping dictionary for month abbreviations to month numbers
    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    # map the month abbreviation to month number
    borough_df['month'] = borough_df['month_abbr'].map(month_map)

    # drop the temporary 'month_abbr' column
    pas_df = borough_df.drop(columns=['month_abbr'])

    # convert year column to integer
    pas_df['year'] = pas_df['year'].astype(int)

    return pas_df

def choose_questions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keeps only the relevant columns and gives them meaningful names.
    :param df: a dataframe with questions
    :returns: dataframe with relevant questions.
    """
    # chosen columns to keep
    col_names = ['A120', 'A121', 'BQ90A', 'NQ133A', 'NQ135BD', 'NQ135BH',
                 'NQ143', 'NQ43', 'NQ62B', 'Q1', 'Q13', 'Q131', 'Q133', 
                 'Q15', 'Q37', 'Q39A_2', 'Q3C', 'Q3F', 'Q3I', 'Q3J', 'Q3L', 
                 'Q60', 'Q61', 'Q62A', 'Q62B', 'Q62C', 'Q62F', 'Q62TG', 
                 'borough_name', 'month', 'year']
    
    # mapping of chosen questions
    questions_mapping = {'A120': 'Stop and Search Agree', 'A121': 'Stop and Search Fair', 
                     'BQ90A': 'Crime Victim', 'NQ133A': 'Officer Contact', 
                     'NQ135BD': 'Met Trust', 'NQ135BH': 'Police Accountable', 
                     'NQ143': 'Met Career', 'NQ43': 'Gangs', 'NQ62B': 'Law Obligation',
                     'Q1': 'Area Living Time', 'Q13': 'Crime Local Worry', 
                     'Q131': 'Informed Local', 'Q133': 'Informed London', 
                     'Q15': 'ASB Worry', 'Q37': 'Guns', 'Q39A_2': 'Knife Crime', 
                     'Q3C': 'People Trusted', 'Q3F': 'People Courtesy', 
                     'Q3I': 'People Help', 'Q3J': 'Call Suspicious', 
                     'Q3L': 'Different Backgrounds', 'Q60': 'Good Job Local', 
                     'Q61': 'Good Job London', 'Q62A': 'Police Reliance', 
                     'Q62B': 'Police Respect', 'Q62C': 'Police Fair Treat',
                     'Q62F': 'Community Matter', 'Q62TG': 'Local Concerns'}
    
    # filter the dataframe
    filtered_df = df[col_names].rename(columns=questions_mapping)

    # reorder the columns
    cols = filtered_df.columns.tolist()
    cols1 = cols[-1:] + cols[-3:-1] + cols[:-3]
    final_df = filtered_df[cols1]

    return final_df

def replace_nans_with_mode(df: pd.DataFrame, col: str) -> None:
    """
    Replace nan values with the mode for the same borough and year.
    :param df: a dataframe with questions containing nan values.
    :param col: specific column of the dataframe df from which nan values will be removed.
    """
    # define a function to replace nan values
    def mode_func(x):
        return x.mode().iloc[0] if not x.mode().empty else np.nan

    # replace nan values by the mode for the same borough and year
    mode_values = df.groupby(['borough_name', 'year'])[col].transform(mode_func)
    df.fillna({col: mode_values}, inplace=True)

def count_answers(df: pd.DataFrame, question_columns: List[str]) -> pd.DataFrame:
    """
    Count number of specific answers for each question.
    :param df: a dataframe with questions.
    :param question_columns: a list of names of columns with questions.
    :returns: dataframe with counts per question per answer, borough, and year.
    """
    result_dfs = []

    # iterate over questions
    for question in question_columns:

        # group by 'borough_name' and 'year', then count the occurrences of each unique value in the question column
        result = df.groupby(['borough_name', 'year'])[question].value_counts().unstack(fill_value=0).reset_index()

        # standardize column names
        question_answers = []
        for col in result.columns[2:]:
            # name = col.lower()
            # answer = name.replace(' ', '_')
            question_answers.append(col)

        # Rename the columns to indicate the question
        result.columns = ['borough_name', 'year'] + [question + ' ' + answer for answer in question_answers]
        
        # Append the result dataframe to the list
        result_dfs.append(result)

    # combine the results
    final_result = result_dfs[0]
    for result_df in result_dfs[1:]:
        final_result = pd.merge(final_result, result_df, on=['borough_name', 'year'], how='outer')

    return final_result

def calculate_proportions(df: pd.DataFrame, question_columns: List[str]) -> pd.DataFrame:
    """
    Calculate proportion of different answers for each question.
    :param df: a dataframe with counts per question per answer, borough, and year.
    :param question_columns: a list of names of columns with questions.
    :returns: dataframe with proportions per question per answer, borough, and year.
    """
    df_proportions = df[['borough_name', 'year']]

    for prefix in question_columns:
        # Select columns that match the prefix
        relevant_columns = [col for col in df.columns if col.startswith(prefix)]

        # Sum across the relevant columns for each row
        row_sums = df[relevant_columns].sum(axis=1)

        # Calculate and add the proportion columns
        for col in relevant_columns:
            proportion_col_name = f'{col} proportion'
            df_proportions[proportion_col_name] = df[col] / row_sums
    
    return df_proportions

def combine_pas_data() -> None:
    """
    Clean and save PAS data at the ward level.
    """
    root_dir = '../data/pas_data_ward_level'
    dfs = []
    
    # iterate over CSV files in the directory
    for csv_file in os.listdir(root_dir):
        parts = csv_file[:-4].split('_')

        if parts[1] == 'ward':

            # load the data
            csv_file_path = os.path.join(root_dir, csv_file)
            df = pd.read_csv(csv_file_path)

            # clean the data and choose relevant columns
            clean_df = clean_pas_data(df)
            filtered_df = choose_questions(clean_df)

            dfs.append(filtered_df)
        
    # combine data
    pas_df = pd.concat(dfs, ignore_index=True)

    # choose question columns
    question_columns = pas_df.columns.tolist()[3:]

    for question in question_columns:
        replace_nans_with_mode(pas_df, question)

    # count question answers
    count_pas_df = count_answers(pas_df, question_columns)

    # calculate proportions
    df_proportions = calculate_proportions(count_pas_df, question_columns)

    # rename year and borough_name columns 
    dct = {'year': 'Year', 'borough_name': 'Borough'}
    df_proportions.rename(columns=dct, inplace=True)

    # save the data to csv        
    save_df_to_csv(df_proportions, 'pas_proportions')

combine_pas_data()
