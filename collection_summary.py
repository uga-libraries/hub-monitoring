"""Summary of data about each collection in a given department folder

Data included:
- Collection
- Status (if backlog or closed)
- Accession date (date range if more than one)
- Size (GB and number of files)
- Risk percentages (based on the number of files at each NARA risk level)

If there is more than one accession for the collection, the information is combined.

Parameter:
directory (required): the directory with the folders to be summarized

Returns:
CSV with one row per collection
"""
from datetime import datetime
import numpy as np
import os
import pandas as pd
import sys


def check_argument(arg_list):
    """Check if the required argument is present and a valid directory

    :parameter
    arg_list (list): the contents of sys.argv after the script is run

    :returns
    dir_path (string): the path to the folder with data to be summarized, or None (if error)
    error (string): the error message, or None (if no error)
    """

    # Checks if the expected arguments are present: script path (default in sys.argv) and directory path.
    if len(arg_list) == 2:
        # Checks if the provided directory path exists.
        dir_path = arg_list[1]
        if os.path.exists(dir_path):
            return dir_path, None
        else:
            return None, f"Provided directory {dir_path} does not exist"
    # Do not have the expected arguments.
    else:
        return None, "Missing required argument: directory"


def combine_collection_data(acc_df):
    """Combine data for collections with multiple accessions

    :parameter
    acc_df (Pandas dataframe): the data for every accession

    :returns
    coll_df (Pandas dataframe): the data for every collection
    """

    # Adds the values in GB, Files, and the four risk category columns for each collection.
    coll_df = acc_df.groupby(['Collection', 'Status'], as_index=False).sum()

    # Replaces risk columns (file counts) with risk columns that have the percentage of files.
    # If files have multiple identifications, the combined percentages will be more than 100%.
    coll_df['No_Match_Risk_%'] = (coll_df['No_Match_Risk'] / coll_df['Files'] * 100).map(round_non_zero)
    coll_df['High_Risk_%'] = (coll_df['High_Risk'] / coll_df['Files'] * 100).map(round_non_zero)
    coll_df['Moderate_Risk_%'] = (coll_df['Moderate_Risk'] / coll_df['Files'] * 100).map(round_non_zero)
    coll_df['Low_Risk_%'] = (coll_df['Low_Risk'] / coll_df['Files'] * 100).map(round_non_zero)
    coll_df.drop(['Date', 'No_Match_Risk', 'High_Risk', 'Moderate_Risk', 'Low_Risk'], axis=1, inplace=True)

    # Combines the dates into a date range and adds to the dataframe.
    date_df = combine_collection_dates(acc_df)
    coll_df = pd.merge(date_df, coll_df, on='Collection', how='outer')

    return coll_df


def combine_collection_dates(acc_df):
    """Combine date information for each collection into a single date or date range

    :parameter
    acc_df (Pandas dataframe): the data for every accession

    :returns
    date_df (Pandas dataframe): the date or date range for every collection, columns Collection and Date
    """

    # Makes the column "Date", which is a string, into numbers so the minimum and maximum can be calculated.
    acc_df['Date'] = pd.to_numeric(acc_df['Date'])

    # Makes a dataframe with the earliest date for each collection.
    min_df = acc_df.groupby('Collection')['Date'].min().reset_index()
    min_df = min_df.rename(columns={'Date': 'Earliest_Date'})

    # Makes a dataframe with the latest date for each collection.
    max_df = acc_df.groupby('Collection')['Date'].max().reset_index()
    max_df = max_df.rename(columns={'Date': 'Latest_Date'})

    # Combines the two dataframes into one,
    # makes a column "Date" with the date range (earliest-latest), or a single date if they are the same,
    # and removes the columns no longer needed after "Date" is made.
    date_df = pd.merge(min_df, max_df, on='Collection', how='outer')
    conditions = [date_df['Earliest_Date'] != date_df['Latest_Date'],
                  date_df['Earliest_Date'] == date_df['Latest_Date']]
    values = [date_df['Earliest_Date'].map(str) + "-" + date_df['Latest_Date'].map(str),
              date_df['Earliest_Date'].map(str)]
    date_df['Date'] = np.select(conditions, values)
    date_df.drop(columns=['Earliest_Date', 'Latest_Date'], axis=1, inplace=True)

    return date_df


def get_accession_data(acc_dir, acc_status, acc_coll, acc_id):
    """Calculate the data about a single accession folder, mostly using other functions

    :parameter
    acc_dir (string): the path to the folder with data to be summarized (script argument)
    acc_status (string): if the accession is backlogged or closed, which is a folder within acc_dir
    acc_coll (string): the collection the accession is part of, which is a folder within acc_status
    acc_id (string): the accession id, which is a folder within acc_coll

    :returns
    acc_list (list): collection, status, date, size (GB), files, and the number of files at each of the 4 risk levels
    """

    # Calculates the path to the accession folder, which combines the four function parameters.
    # Some parameters are also included in the accession data, so they are passed separately rather than as the path.
    acc_path = os.path.join(acc_dir, acc_status, acc_coll, acc_id)

    # Gets the data which requires additional calculation.
    # Size, Files, and Date are single data points, while risk is a list of four items.
    date = get_date(acc_path)
    size = get_size(acc_path)
    files = get_file_count(acc_path)
    risk = get_risk(acc_path)

    # Combines the data into a single list.
    acc_list = [acc_coll, acc_status, date, size, files]
    acc_list.extend(risk)

    return acc_list


def get_date(path):
    """Determine the year of the accession

    The preferred method is to use the year from the accession number,
    but for naming conventions that do not include the year, it will use the date created of the preservation log.

    :parameter
    path (string): the path to the accession folder

    :returns
    date (string): the year or "unknown"
    """

    # Option 1: The first 4 characters of the accession folder name are the year (are numbers).
    acc_folder = os.path.basename(path)
    if acc_folder[:4].isdigit():
        date = acc_folder[:4]
    # Option 2: The year the preservation log was created.
    else:
        log_path = os.path.join(path, "preservation_log.txt")
        timestamp = os.stat(log_path).st_ctime
        date = datetime.fromtimestamp(timestamp).strftime('%Y')

    return date


def get_file_count(path):
    """Calculate the number of files in an accession's bag data folder

    :parameter
    path (string): the path to the accession folder

    :returns
    file_count (integer): the number of files in the accession folder
    """

    # Calculates the path of the bag's data folder.
    accession_number = os.path.basename(path)
    data_path = os.path.join(path, f'{accession_number}_bag', 'data')

    # Counts the files at each level within the bag's data folder.
    file_count = 0
    for root, dirs, files in os.walk(data_path):
        file_count += len(files)

    return file_count


def get_risk(path):
    """Calculate the number of files at each of the four NARA risk levels

    :parameter
    path (string): the path to the accession folder

    :returns
    risk_list (list): a list of 4 integers, with the number of files each risk level, ordered highest-lowest risk
    """

    # Constructs the path to the spreadsheet with risk data in the accession folder and reads it into a dataframe.
    accession_number = os.path.basename(path)
    risk_csv_path = os.path.join(path, f"{accession_number}_full_risk_data.csv")
    risk_df = pd.read_csv(risk_csv_path)

    # Counts the number of files (dataframe rows) with each possible NARA risk level and saves to a list.
    risk_list = []
    for risk in ('No Match', 'High Risk', 'Moderate Risk', 'Low Risk'):
        risk_list.append((risk_df['NARA_Risk Level'] == risk).sum())

    return risk_list


def get_size(path):
    """Calculate the number of files in an accession's bag data folder

    :parameter
    path (string): the path to the accession folder

    :returns
    size_gb (float): the size, in GB, of the accession folder
    """

    # Calculates the path of the bag's data folder.
    accession_number = os.path.basename(path)
    data_path = os.path.join(path, f'{accession_number}_bag', 'data')

    # Adds the size of the files at each level within the bag's data folder.
    size_bytes = 0
    for root, dirs, files in os.walk(data_path):
        for file in files:
            file_path = os.path.join(root, file)
            size_bytes += os.stat(file_path).st_size
    size_gb = round_non_zero(size_bytes / 1000000000)

    return size_gb


def round_non_zero(number):
    """Round a number to the fewest decimal places that don't make the number 0

    This is used in calculating percentage of files at each risk level in combine_collection_data()
    and size (converted to GB) in get_size()

    :parameter
    number (float): a number to be rounded

    :returns
    round_number (float): the number rounded to the fewest decimal places that don't make it 0
    """

    # If the number is 0, returns it immediately, or else would get stuck in the while loop.
    # There are collections with no files of a risk category, resulting in 0%.
    if number == 0:
        return 0.0

    # Starts with 2 decimal places, the minimum that we use.
    places = 2
    round_number = round(number, 2)

    # As long as the rounded number is 0, keep adding one to the number of decimal places.
    while round_number == 0:
        places += 1
        round_number = round(number, places)

    return round_number


def save_report(coll_df, dir_path):
    """Save the collection data to a CSV in the directory provided as the script argument

    :parameter
    coll_df (Pandas dataframe): the data for each collection
    dir_path (string): the path to the folder with data to be summarized (script argument)

    :returns:
    None
    """

    # Determines the department based on a keyword in the directory path to include in the report name.
    if "Hargrett" in dir_path:
        dept = "harg"
    else:
        dept = "rbrl"

    # Calculates today's date, formatted YYYY-MM-DD, to include in the report name.
    today = datetime.today().strftime('%Y-%m-%d')

    # Saves the dataframe to a CSV in the directory (script argument).
    coll_df.to_csv(os.path.join(dir_path, f'{dept}_hub-collection-summary_{today}.csv'), index=False)


if __name__ == '__main__':

    # Gets the path to the directory with the information to be summarized from the script argument.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit()

    # Starts a dataframe for information about each accession.
    # It will be summarized later to be by collection.
    accession_df = pd.DataFrame(columns=['Collection', 'Status', 'Date', 'GB', 'Files',
                                         'No_Match_Risk', 'High_Risk', 'Moderate_Risk', 'Low_Risk'])

    # Navigates to each accession folder, gets the information, and saves to the accession dataframe.
    for status in os.listdir(directory):
        for collection in os.listdir(os.path.join(directory, status)):
            for accession in os.listdir(os.path.join(directory, status, collection)):
                accession_df.loc[len(accession_df)] = get_accession_data(directory, status, collection, accession)

    # Combines accession information for each collection and saves to a CSV in "directory".
    collection_df = combine_collection_data(accession_df)
    save_report(collection_df, directory)
