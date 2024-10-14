"""Makes a spreadsheet with the format data from every full risk spreadsheet in a given directory

The risk spreadsheets are named accession#_full_risk_data.csv.

The script result (combined_format_data.csv) includes:
- FITS_Format_Name
- FITS_Format_Version
- NARA_Risk_Level
- File_Count
- Size_GB

Parameter:
    input_directory (required): the path to the directory with spreadsheets to be combined, which can be any folder

Returns:
    combined_format_data_YYYY-MM-DD.csv, saved in the input_directory folder (script argument)
"""
from datetime import date
import os
import pandas as pd
import re
import sys
from validate_fixity import check_argument


def combine_risk_csvs(dir_path):
    """Combine the data from the most recent risk csv for every accession into one dataframe

    @:parameter
    dir_path (string): path to the directory with risk csvs (script argument)

    @:returns
    df (pandas DataFrame): dataframe with all columns from the most recent risk csv for every accession
    """

    # Makes a list of the most recent risk spreadsheet for every accession.
    csv_list = []
    for root, directories, files in os.walk(dir_path):
        if any('full_risk_data' in x for x in files):
            print('Starting on accession', root)
            file = most_recent_risk_csv(files)
            csv_list.append(os.path.join(root, file))

    # Prints the number of CSVs, to give an idea of the amount of coverage since not all accessions have a risk CSV.
    print('\nNumber of CSVs to combine:', len(csv_list))

    # Combines every spreadsheet into one dataframe.
    df = pd.concat([pd.read_csv(f, low_memory=False) for f in csv_list])

    return df


def df_cleanup(df):
    """Remove unneeded columns, rename a column, remove duplicates, fill empty NARA and version, reformat version

    @:parameter
    df (pandas DataFrame): dataframe with all columns from the most recent risk csv for every accession

    @:returns
    df (pandas DataFrame): dataframe with a subset of cleaned data from the most recent risk csv for every accession
    """

    # Renames the NARA_Risk Level column, which is in older risk csvs, to the current NARA_Risk_Level.
    # If it is already NARA_Risk_Level, this will have no effect.
    df = df.rename({'NARA_Risk Level': 'NARA_Risk_Level'}, axis=1)

    # Keeps only the needed columns.
    # The other FITs data, NARA data, technical appraisal, and other risk columns are not used.
    df = df[['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level']

    # Removes duplicates from multiple NARA matches with the same NARA risk level to the same file.
    # The file will still be repeated once per NARA risk level.
    # The file path column is then removed, since it is only needed for removing duplicates.
    df = df.drop_duplicates()
    df = df.drop(columns='FITS_File_Path')

    # Fill blanks in the NARA risk level column (legacy practice) with "No Match" (current practice).
    df['NARA_Risk_Level'] = df['NARA_Risk_Level'].fillna('No Match')

    # Replace blank versions with text and then converts the version column to a string.
    # By default, if a CSV has all numeric versions, it is a float, but otherwise a string.
    # The data type needs to be the same for combining different instances of the same format version later.
    df['FITS_Format_Version'] = df['FITS_Format_Version'].fillna('no-version')
    df['FITS_Format_Version'] = df['FITS_Format_Version'].astype(str)

    return df


def files_per_format(df):
    """Calculate the number of files for each format name, version, and NARA risk level combination

    @:parameter
    df (pandas DataFrame): dataframe with a subset of cleaned data from the most recent risk csv for every accession

    @:returns
    files (pandas DataFrame): dataframe with format name, version, NARA risk level, and number of files
    """

    # Groupby includes NARA risk level so different possible risks for each name/version combination are kept.
    # Reset index keeps the name, version, and risk level as columns in the dataframe.
    # Without reset index, it would return a series with those columns as part of the index.
    group_list = ['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level']
    files = df.groupby(group_list).size().reset_index()

    # Renames the default column name for the count to be more descriptive.
    files = files.rename({0: 'File_Count'}, axis=1)

    return files


def most_recent_risk_csv(file_list):
    """Determine the most recent risk spreadsheet in the file list based on the file name

    From legacy practices, any spreadsheet with a date in the name is more recent than one without.
    The list will also include other types of files, such as preservation logs, which are ignored.

    Keep in sync with the copy of this function in collection_summary.py and risk_update.py
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


def size_per_format(df):
    """Calculate the size in GB for each format name, version, and NARA risk level combination

    @:parameter
    df (pandas Dataframe): dataframe with a subset of cleaned data from the most recent risk csv for every accession

    @:returns
    size (pandas Dataframe): dataframe with format name, version, NARA risk level, and size in GB
    """

    # Groupby includes NARA risk level so different possible risks for the name/version combination are kept.
    # Reset index keeps the name, version, and risk level as columns in the dataframe.
    # Without reset index, it would return a series with those columns as part of the index.
    group_list = ['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level']
    size = df.groupby(group_list)['FITS_Size_KB'].sum().reset_index()

    # Converts the KB to GB and rounds to 3 decimal places.
    # Anything less than 1 MB with have a size of 0.
    size['Size_GB'] = round(size['FITS_Size_KB'] / 1000000, 3)

    # Removes the KB column, which is not needed now that we have GB.
    size = size.drop(columns='FITS_Size_KB')

    return size


if __name__ == '__main__':

    # Gets the path to the directory with the risk CSVs to be combined from the script argument.
    # Exits the script if there is an error.
    input_directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Combines the most recent risk csv for each accession into one dataframe.
    df_all = combine_risk_csvs(input_directory)

    # Transforms the dataframe with all risk data to a dataframe with the desired data.
    df_formats = df_cleanup(df_all)

    # Calculates the number of files per format and GB per format, and combines them into one dataframe.
    # It also includes the format name, version, and NARA risk level.
    df_files = files_per_format(df_formats)
    df_size = size_per_format(df_formats)
    df_format_list = pd.merge(df_files, df_size, how='outer')

    # Saves the result to a CSV in the input directory (script argument).
    today = date.today().strftime('%Y-%m-%d')
    df_format_list.to_csv(os.path.join(input_directory, f'combined_format_data_{today}.csv'), index=False)
