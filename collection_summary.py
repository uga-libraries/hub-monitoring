"""Makes a spreadsheet with summary data about each collection in a given department folder

Data included:
- Collection
- Status (if backlog or closed)
- Accession date (date range if more than one)
- Size (GB and number of files)
- Risk percentages (based on the number of files at each NARA risk level)
- Notes (empty column for archivist notes)

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
import re
import sys
from risk_update import most_recent_risk_csv
from validate_fixity import check_argument


def accession_test(acc_id):
    """Determine if a folder within a collection folder is an accession based on the folder name

    @:parameter
    acc_id (string): the accession id, which is a folder within acc_coll

    @:return
    test (Boolean): True if it is an accession and False if not
    """

    # The most common pattern is YYYY-##-er, sometimes with underscores, three numbers, or ER.
    if re.match('[0-9]{4}[-|_][0-9]{2,3}[-|_][er|ER]', acc_id):
        test = True
    # The string no-acc-num is used on legacy accessions that were never assigned a number.
    elif acc_id == 'no-acc-num':
        test = True
    # Legacy format with the pattern LastnameFirstinitial_ER.
    elif re.match('[A-Za-z]+_ER', acc_id):
        test = True
    # University archives variation, ua##-###.
    elif re.match('ua[0-9]{2}-[0-9]{3}', acc_id):
        test = True
    # University archives variation, ua_##_###.
    elif re.match('ua_[0-9]{2}_[0-9]{3}', acc_id):
        test = True
    else:
        test = False

    return test


def combine_collection_data(acc_df):
    """Combine data for collections with multiple accessions

    @:parameter
    acc_df (Pandas dataframe): the data for every accession

    @:returns
    coll_df (Pandas dataframe): the data for every collection
    """

    # Adds the values in GB, Files, and the four risk category columns for each collection.
    coll_df = acc_df.groupby(['Collection', 'Status'], as_index=False).sum()

    # Rounds the size to 2 decimal places, or more places if needed to not be 0.
    coll_df['GB'] = coll_df['GB'].map(round_non_zero)

    # Combines the dates into a date range and adds to the dataframe.
    # Removes the existing "Date" column, so it doesn't conflict with the new "Date" column made by the function.
    coll_df.drop(['Date'], axis=1, inplace=True)
    date_df = combine_collection_dates(acc_df)
    coll_df = pd.merge(date_df, coll_df, on='Collection', how='outer')

    return coll_df


def combine_collection_dates(acc_df):
    """Combine date information for each collection into a single date or date range

    @:parameter
    acc_df (Pandas dataframe): the data for every accession

    @:returns
    date_df (Pandas dataframe): the date or date range for every collection, columns Collection and Date
    """

    # Makes the column "Date", which is a string with the year,
    # into numbers so the minimum and maximum can be calculated.
    acc_df['Date'] = pd.to_numeric(acc_df['Date'])

    # Makes a dataframe with the earliest date for each collection.
    min_df = acc_df.groupby('Collection')['Date'].min().reset_index()
    min_df = min_df.rename(columns={'Date': 'Earliest_Date'})

    # Makes a dataframe with the latest date for each collection.
    max_df = acc_df.groupby('Collection')['Date'].max().reset_index()
    max_df = max_df.rename(columns={'Date': 'Latest_Date'})

    # Combines the two dataframes into one,
    # making a column "Date" with the date range (earliest-latest), or a single date if they are the same,
    # and removing the columns no longer needed after "Date" is made.
    date_df = pd.merge(min_df, max_df, on='Collection', how='outer')
    conditions = [date_df['Earliest_Date'] != date_df['Latest_Date'],
                  date_df['Earliest_Date'] == date_df['Latest_Date']]
    values = [date_df['Earliest_Date'].map(str) + '-' + date_df['Latest_Date'].map(str),
              date_df['Earliest_Date'].map(str)]
    date_df['Date'] = np.select(conditions, values)
    date_df.drop(columns=['Earliest_Date', 'Latest_Date'], axis=1, inplace=True)

    return date_df


def get_accession_data(acc_dir, acc_status, acc_coll, acc_id):
    """Calculate the data about a single accession folder, mostly using other functions

    @:parameter
    acc_dir (string): the path to the folder with data to be summarized (script argument)
    acc_status (string): if the accession is backlogged or closed, which is a folder within acc_dir
    acc_coll (string): the collection the accession is part of, which is a folder within acc_status
    acc_id (string): the accession id, which is a folder within acc_coll

    @:returns
    acc_list (list): collection, status, date, size (GB), files, and the number of files at each of the 4 risk levels
    """

    # Calculates the path to the accession folder, which combines the four function parameters.
    acc_path = os.path.join(acc_dir, acc_status, acc_coll, acc_id)

    # Gets the data which requires additional calculation.
    # Size, Files, and Date are single data points, while risk is a list of four items.
    # Skips size for an extremely large collection so the report finishes sooner.
    date = get_date(acc_path)
    if acc_coll == 'rbrl246jhi':
        size = 0
        files = 0
    else:
        size = get_size(acc_path)
        files = get_file_count(acc_path)
    risk = get_risk(acc_path)

    # Combines the data into a single list.
    acc_list = [acc_coll, acc_status, date, size, files]
    acc_list.extend(risk)

    return acc_list


def get_date(acc_path):
    """Determine the year the accession was copied to storage, which is the year the accession folder was made

    @:parameter
    acc_path (string): the path to the accession folder

    @:returns
    date (string): the year
    """

    # Gets the creation date of the accession folder.
    timestamp = os.path.getctime(acc_path)

    # Reformats the timestamp to just the year.
    date = datetime.fromtimestamp(timestamp).strftime('%Y')

    return date


def get_file_count(acc_path):
    """Calculate the number of files in an accession

    For bagged accessions, this is the number of files in the bag data folder.
    For unbagged accessions, this is the number of files in the folder within the accession folder
    that is not for the FITS files.

    @:parameter
    acc_path (string): the path to the accession folder

    @:returns
    file_count (integer): the number of files in the accession folder
    """

    # Calculates the path with the accession content,
    # which is either the bag's data folder or the folder within the accession folder that isn't for the FITS files.
    accession_number = os.path.basename(acc_path)
    data_path = os.path.join(acc_path, f'{accession_number}_bag', 'data')
    if os.path.exists(data_path):
        content_path = data_path
    else:
        for item in os.listdir(acc_path):
            if os.path.isdir(os.path.join(acc_path, item)) and not item.endswith('_FITS'):
                content_path = os.path.join(acc_path, item)
    try:
        # Counts the files at each level within the folder with the accession's content.
        file_count = 0
        for root, dirs, files in os.walk(content_path):
            file_count += len(files)

        return file_count
    except UnboundLocalError:
        return 0


def get_risk(acc_path):
    """Calculate the number of files at each of the four NARA risk levels in an accession

    The accession's risk spreadsheet is used to calculate the data.
    If there is more than one, the most recent spreadsheet is used.

    @:parameter
    acc_path (string): the path to the accession folder

    @:returns
    risk_list (list): a list of 4 integers, with the number of files each risk level, ordered highest-lowest risk
    """

    # Uses a function from risk_update.py (also in this repo) to get the name of the most recent risk csv.
    # It requires a list of files at the first level within the accession list as input.
    # If there is no risk csv for this accession, it will return None.
    accession_file_list = []
    for item in os.listdir(acc_path):
        if os.path.isfile(os.path.join(acc_path, item)):
            accession_file_list.append(item)
    risk_csv_name = most_recent_risk_csv(accession_file_list)

    # If the risk csv is present, reads it into a dataframe to summarize.
    # If not, prints the error and returns a list with 0 for the number of files at every risk level.
    # If an accession has a path length error, it may not have a risk data csv yet.
    if risk_csv_name:
        risk_df = pd.read_csv(os.path.join(acc_path, risk_csv_name))
    else:
        print(f'Accession {os.path.basename(acc_path)} has no risk csv')
        return [0, 0, 0, 0]

    # Makes a new dataframe with the FITS_File_Path and NARA_Risk Level to remove duplicates.
    # Duplicates may be from multiple FITS format identifications or multiple NARA matches.
    # Each file is in the new dataframe once per NARA risk level, if it has more than one possible risk level.
    risk_dedup_df = risk_df[['FITS_File_Path', 'NARA_Risk Level']]
    risk_dedup_df = risk_dedup_df.drop_duplicates()

    # Counts the number of files (dataframe rows) with each possible NARA risk level and saves to a list.
    # Uses sum() to aggregate because the equality has a Boolean result, and True=1, False=0.
    risk_list = []
    for risk in ('No Match', 'High Risk', 'Moderate Risk', 'Low Risk'):
        risk_list.append((risk_dedup_df['NARA_Risk Level'] == risk).sum())

    return risk_list


def get_size(acc_path):
    """Calculate the size of the accession in GB

    For bagged accessions, this is the size of the bag data folder.
    For unbagged accessions, this is the size of the folder within the accession folder that is not for FITS files.

    @:parameter
    acc_path (string): the path to the accession folder

    @:returns
    size_gb (float): the size, in GB, of the accession folder
    """

    # Calculates the path with the accession content,
    # which is either the bag's data folder or the folder within the accession folder that isn't for the FITS files.
    accession_number = os.path.basename(acc_path)
    data_path = os.path.join(acc_path, f'{accession_number}_bag', 'data')
    if os.path.exists(data_path):
        content_path = data_path
    else:
        for item in os.listdir(acc_path):
            if os.path.isdir(os.path.join(acc_path, item)) and not item.endswith('_FITS'):
                content_path = os.path.join(acc_path, item)

    try:
        # Adds the size of the files at each level within the folder with the accession's content.
        size_bytes = 0
        for root, dirs, files in os.walk(content_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size_bytes += os.stat(file_path).st_size
                except FileNotFoundError:
                    with open('size_error.txt', 'a', newline='', encoding='utf-8') as f:
                        f.write(file_path + '\n')
        size_gb = round_non_zero(size_bytes / 1000000000)
        return size_gb
    except UnboundLocalError:
        print('Cannot find the content path for', acc_path)
        return 0


def round_non_zero(number):
    """Round a number to the fewest decimal places that don't make the number 0

    This is used in calculating percentage of files at each risk level in combine_collection_data()
    and size (converted to GB) in get_size()

    @:parameter
    number (float): a number to be rounded

    @:returns
    round_number (float): the number rounded to the fewest decimal places that don't make it 0
    """

    # If the number is 0, returns it immediately, or else would get stuck in the while loop.
    # There are collections with no files of a risk category, resulting in 0%.
    if number == 0:
        return 0.00

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

    @:parameter
    coll_df (Pandas dataframe): the data for each collection
    dir_path (string): the path to the folder with data to be summarized (script argument)

    @:returns
    None
    """

    # Adds an empty column for archivist notes as the last column.
    coll_df['Notes'] = ''

    # Calculates today's date, formatted YYYY-MM-DD, to include in the report name.
    today = datetime.today().strftime('%Y-%m-%d')

    # Saves the dataframe to a CSV in the directory (script argument).
    coll_df.to_csv(os.path.join(dir_path, f'hub-collection-summary_{today}.csv'), index=False)


if __name__ == '__main__':

    # Gets the path to the directory with the information to be summarized from the script argument.
    # Exits the script if there is an error.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Starts a dataframe for information about each accession.
    # It will be summarized later to be by collection.
    accession_df = pd.DataFrame(columns=['Collection', 'Status', 'Date', 'GB', 'Files',
                                         'No_Match_Risk', 'High_Risk', 'Moderate_Risk', 'Low_Risk'])

    # Navigates to each accession folder, gets the information, and saves it to the accession dataframe.
    # Folders used for other purposes at the status and accession level are skipped.
    for status in os.listdir(directory):
        if status in ('backlogged', 'closed'):
            for collection in os.listdir(os.path.join(directory, status)):
                if collection == 'ua22-008 Linguistic Atlas Project':
                    continue
                # print('\nStarting on collection', collection)
                for accession in os.listdir(os.path.join(directory, status, collection)):
                    is_accession = accession_test(accession)
                    if is_accession and os.path.isdir(os.path.join(directory, status, collection, accession)):
                        accession_df.loc[len(accession_df)] = get_accession_data(directory, status,
                                                                                 collection, accession)

    # Combines accession information for each collection and saves to a CSV in "directory" (the script argument).
    collection_df = combine_collection_data(accession_df)
    save_report(collection_df, directory)
