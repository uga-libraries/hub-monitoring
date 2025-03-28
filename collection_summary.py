"""Makes two spreadsheets with summary data about each accession and collection in a given department folder

Data included:
- Accession (accession report only)
- Collection
- Status (if backlog or closed)
- Accession date (date range if more than one)
- Size (GB and number of files)
- Risk (number of files at each NARA risk level)
- Notes (if there was no risk csv and for additional archivist notes)
- Size_Error (if size could not be calculated and needs to be calculated manually using file properties)

If there is more than one accession for the collection,
the information is combined in the collection report.

Parameter:
    input_directory (required): the directory with the folders to be summarized

Returns:
    hub-accession-summary_DATE.csv
    hub-collection-summary_DATE.csv
"""
import csv
from datetime import date, datetime
import numpy as np
import os
import pandas as pd
import re
import sys
from validate_fixity import check_argument


def accession_test(acc_id, acc_path):
    """Determine if a folder is an accession based on the folder name

    There may be other folders used for other purposes, like risk remediation or appraisal, as well.
    These other folders are not part of the collection summary report.

    Keep in sync with the copy of this function in risk_update.py.

    @:parameter
    acc_id (string): the accession id, which is the name of a folder within acc_coll
    acc_path (string): the path to the accession folder

    @:return
    Boolean: True if it is an accession and False if not
    """

    # If the path is to a file, do not test the folder name.
    if os.path.isfile(acc_path):
        return False

    # Pattern one: ends with -er or -ER.
    if acc_id.lower().endswith('-er'):
        return True
    # Pattern two: ends with _er or _ER.
    elif acc_id.lower().endswith('_er'):
        return True
    # Temporary designation for legacy content while determining an accession number.
    elif acc_id == 'no-acc-num':
        return True
    # Folder that matches none of the patterns for an accession.
    else:
        return False


def combine_collection_data(acc_df):
    """Combine data for collections with multiple accessions

    If a collection has one accession, the accession data is assigned to the collection as is.

    @:parameter
    acc_df (Pandas dataframe): the data for every accession

    @:returns
    coll_df (Pandas dataframe): the data for every collection
    """

    # Removes the Accession folder, which is only needed for the accession report.
    acc_df.drop(['Accession'], axis=1, inplace=True)

    # Combines the values in GB, Files, and the four risk category columns for each collection.
    coll_df = acc_df.groupby(['Collection', 'Status'], as_index=False).sum()

    # Rounds the GB to 2 decimal places, or more places if needed to not be 0.
    coll_df['GB'] = coll_df['GB'].map(round_non_zero)

    # Resets GB and Files to 0 if there were any accessions with a size error
    # to make it clearer that the size for the collection needs to be calculated manually.
    # If there is an AttributeError, it means none of the rows have a value in Size_Error and no change is needed.
    try:
        coll_df.loc[coll_df['Size_Error'].str.startswith('Did not calculate size', na=False), 'GB'] = 0
        coll_df.loc[coll_df['Size_Error'].str.startswith('Did not calculate size', na=False), 'Files'] = 0
    except AttributeError:
        pass

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


def get_accession_data(input_dir, acc_status, acc_coll, acc_id):
    """Calculate the data about a single accession folder, mostly using other functions

    @:parameter
    input_dir (string): the path to the folder with data to be summarized (script argument)
    acc_status (string): if the accession is backlogged or closed, which is a folder within acc_dir
    acc_coll (string): the collection the accession is part of, which is a folder within acc_status
    acc_id (string): the accession id, which is a folder within acc_coll

    @:returns
    acc_list (list): accession, collection, status, date, size (GB), files,
    the number of files at each of the 4 risk levels, a note for if the accession has no risk csv,
    and a note for if the size and files could not be calculated
    """

    # Calculates the path to the accession folder, which combines the four function parameters.
    acc_path = os.path.join(input_dir, acc_status, acc_coll, acc_id)

    # Gets the data which requires additional calculation.
    # Size, Files, and Date are single data points, while risk is a list of four items.
    # Skips size for an extremely large collection so the report finishes sooner.
    date = get_date(acc_path)
    if acc_coll == 'rbrl246jhi':
        files = 0
        size_gb = 0
        size_error = 'Did not calculate size for collection rbrl246jhi due to the time required. '
    else:
        files, size_gb, size_error = get_size(acc_path)
    risk = get_risk(acc_path)

    # Combines the data into a single list.
    acc_list = [acc_id, acc_coll, acc_status, date, size_gb, files]
    acc_list.extend(risk)
    acc_list.append(size_error)

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


def get_risk(acc_path):
    """Calculate the number of files at each of the four NARA risk levels in an accession

    The accession's risk spreadsheet is used to calculate the data.
    If there is more than one spreadsheet, the most recent spreadsheet is used.
    If there is no risk spreadsheet, all risk level counts are set to 0.

    @:parameter
    acc_path (string): the path to the accession folder

    @:returns
    risk_list (list): a list of 4 integers, with the number of files each risk level, ordered highest-lowest risk
                      and a note, either None or that the accession has no risk csv
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
        risk_df = pd.read_csv(os.path.join(acc_path, risk_csv_name), low_memory=False)
    else:
        return [0, 0, 0, 0, f'Accession {os.path.basename(acc_path)} has no risk csv. ']

    # Renames the NARA_Risk Level column, which is in older risk csvs, to the current NARA_Risk_Level.
    # If it is already NARA_Risk_Level, this will have no effect.
    risk_df = risk_df.rename(columns={'NARA_Risk Level': 'NARA_Risk_Level'})

    # Makes a new dataframe with the FITS_File_Path and NARA_Risk Level to remove duplicates.
    # Duplicates may be from multiple FITS format identifications or multiple NARA matches.
    # Each file is in the new dataframe once per NARA risk level, if it has more than one possible risk level.
    risk_dedup_df = risk_df[['FITS_File_Path', 'NARA_Risk_Level']]
    risk_dedup_df = risk_dedup_df.drop_duplicates()

    # Counts the number of files (dataframe rows) with each possible NARA risk level and saves to a list.
    # Uses sum() to aggregate because the equality has a Boolean result, and True=1, False=0.
    risk_list = []
    for risk in ('No Match', 'High Risk', 'Moderate Risk', 'Low Risk'):
        risk_list.append((risk_dedup_df['NARA_Risk_Level'] == risk).sum())

    # Adds None to the end of the list, which is for the Notes column.
    # There is no information for Notes if there is a risk csv.
    risk_list.append(None)

    return risk_list


def get_size(acc_path):
    """Calculate the size of the accession in number of files and GB

    For bagged accessions, this is for the contents of the bag data folder.
    Otherwise, this is for the contents of the folder within the accession folder that is not for FITS files.
    If the folder cannot be found or size cannot be calculated for any file, size is set to 0.

    @:parameter
    acc_path (string): the path to the accession folder

    @:returns
    file_count (integer): the number of files in the accession folder
    size_gb (float): the size, in GB, of the accession folder
    error (string; None): an error message if the size could not be calculated or None
    """

    # Calculates the path to the folder with the accession content,
    # which should be in the bag's data folder or the folder within the accession folder that isn't for FITS files.
    content_path = None
    accession_number = os.path.basename(acc_path)
    data_path = os.path.join(acc_path, f'{accession_number}_bag', 'data')
    if os.path.exists(data_path):
        content_path = data_path
    else:
        for item in os.listdir(acc_path):
            if os.path.isdir(os.path.join(acc_path, item)) and not item.endswith('_FITS'):
                content_path = os.path.join(acc_path, item)

    # If content_path could not be determined, returns a size of 0. Size will need to be calculated manually.
    if not content_path:
        return 0, 0, f'Did not calculate size for accession {accession_number} due to folder organization. '

    # Adds the number and size of the files at each level within the folder with the accession's content.
    # If the size for any files cannot be calculated (usually due to path length), returns a size of 0.
    # Size for these will need to be calculated manually.
    file_count = 0
    size_bytes = 0
    for root, dirs, files in os.walk(content_path):
        file_count += len(files)
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size_bytes += os.stat(file_path).st_size
            except FileNotFoundError:
                return 0, 0, f'Could not calculate size for accession {accession_number} due to path length. '
    size_gb = round_non_zero(size_bytes / 1000000000)
    return file_count, size_gb, None


def most_recent_risk_csv(file_list):
    """Determine the most recent risk spreadsheet in the file list based on the file name

    From legacy practices, any spreadsheet with a date in the name is more recent than one without.
    The list will also include other types of files, such as preservation logs, which are ignored.

    Keep in sync with the copy of this function in format_list.py and risk_uudate.py
    The unit tests are in risk_update.

    @:parameter
    file_list (list): list of all file names in a folder with at least one risk spreadsheet

    @:returns
    most_recent_file (string): the name of the preservation spreadsheet that is the most recent
    """

    # Variables for tracking which file is the most recent.
    most_recent_file = None
    most_recent_date = None

    # Tests each file in the file list looking for the most recent one, based on the date in the file name.
    for file_name in file_list:

        # Skips files that are not risk spreadsheets, like the preservation log.
        if not ('full_risk_data' in file_name):
            continue

        # Extracts the date from the risk spreadsheet file name, if it has one. If it doesn't, assigns 1900-01-01
        # for comparison since any spreadsheet with a date is more recent than one without.
        # Converts the date from a string to type date so that it can be compared to other dates.
        try:
            regex = re.search("_full_risk_data_([0-9]{4})-([0-9]{2})-([0-9]{2}).csv", file_name)
            file_date = date(int(regex.group(1)), int(regex.group(2)), int(regex.group(3)))
        except AttributeError:
            file_date = date(1900, 1, 1)

        # If this is the first file evaluated, or this file's date is more recent than the current most_recent_date,
        # updates most_recent_file and most_recent_date with the current file and its date.
        if most_recent_date is None or most_recent_date < file_date:
            most_recent_file = file_name
            most_recent_date = file_date

    return most_recent_file


def round_non_zero(number):
    """Round a number to the fewest decimal places that don't make the number 0, but at least 2 decimal places

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


def save_accession_report(input_dir, row):
    """Save a row of data to a CSV in the input_directory provided as the script argument

    @:parameter
    input_dir (string): the path to the folder with data to be summarized (script argument)
    row (list or string): list with data for a row in the CSV or "header"
    """

    # Path to the accession report.
    report_path = os.path.join(input_dir, f"hub-accession-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")

    # Makes the report with a header row if row is "header". Otherwise, adds the row to the report.
    if row == 'header':
        with open(report_path, 'w', newline='') as report:
            report_writer = csv.writer(report)
            report_writer.writerow(['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk',
                                    'High_Risk', 'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'])
    else:
        with open(report_path, 'a', newline='') as report:
            report_writer = csv.writer(report)
            report_writer.writerow(row)


if __name__ == '__main__':

    # Gets the path to the input_directory with the information to be summarized from the script argument.
    # Exits the script if there is an error.
    input_directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Starts a CSV for information about each accession. It will also be summarized later by collection.
    save_accession_report(input_directory, 'header')

    # Navigates to each accession folder, gets the information, and saves it to the accession CSV.
    # Folders used for other purposes at each level are skipped.
    for status in os.listdir(input_directory):
        if status in ('backlogged', 'closed'):
            for collection in os.listdir(os.path.join(input_directory, status)):
                # Do not include ua22-008 in the report, since it is not our collection.
                if collection == 'ua22-008 Linguistic Atlas Project':
                    continue
                for accession in os.listdir(os.path.join(input_directory, status, collection)):
                    accession_dir = os.path.join(input_directory, status, collection, accession)
                    is_accession = accession_test(accession, accession_dir)
                    if is_accession:
                        print('Starting on accession', accession_dir)
                        accession_data = get_accession_data(input_directory, status, collection, accession)
                        save_accession_report(input_directory, accession_data)

    # Combines accession information for each collection and saves to a CSV in "input_directory" (the script argument).
    today = datetime.today().strftime('%Y-%m-%d')
    accession_df = pd.read_csv(os.path.join(input_directory, f'hub-accession-summary_{today}.csv')).fillna('')
    collection_df = combine_collection_data(accession_df)
    collection_df.to_csv(os.path.join(input_directory, f'hub-collection-summary_{today}.csv'), index=False)
