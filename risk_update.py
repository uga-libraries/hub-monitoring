"""Makes an updated risk spreadsheet for every accession in a directory

Parameters:
    directory (required): the directory that contains the risk spreadsheets
    nara_csv (required): the path to the most recent NARA Preservation Action Plan spreadsheet

Returns:
    New risk spreadsheet is added to each accession folder
"""
from datetime import date, datetime
import os
import pandas as pd
import re
import sys


def check_arguments(argument_list):
    """Check the required arguments, directory and nara_csv, are present and correct

    Adapted from https://github.com/uga-libraries/format-report/blob/main/merge_format_reports.py

    :parameter
    argument_list (list): the contents of sys.argv after the script is run

    :returns
    dir_path (string, None): string with the path to the directory to check for risk spreadsheets, or None if missing
    nara_path (string, None): string with the path to NARA's Preservation Action Plan spreadsheet, or None if missing
    errors (list): the list of errors encountered, if any, or an empty list
    """

    # Makes variables with default values to store the results of the function.
    dir_path = None
    nara_path = None
    errors = []

    # Verifies that the first required argument (directory) is present,
    # and if it is present that it is a valid path.
    if len(argument_list) > 1:
        dir_path = argument_list[1]
        if not os.path.exists(dir_path):
            errors.append(f"Directory '{dir_path}' does not exist")
    else:
        errors.append("Required argument directory is missing")

    # Verifies that the second required argument (nara_csv) is present,
    # and if it is present that it is a valid path.
    if len(argument_list) > 2:
        nara_path = argument_list[2]
        if not os.path.exists(nara_path):
            errors.append(f"NARA CSV '{nara_path}' does not exist")
    else:
        errors.append("Required argument nara_csv is missing")

    return dir_path, nara_path, errors


def match_nara_risk(update_df, nara_df):
    """Match format identifications to NARA's Preservation Action Plan spreadsheet

    The match techniques are applied in order of accuracy,
    and no additional match techniques are tried once a match is found.

    Adopted from https://github.com/uga-libraries/accessioning-scripts/blob/main/format_analysis_functions.py

    :parameter
    update_df (Pandas dataframe): a dataframe with FITS columns from a risk spreadsheet
    nara_df (Pandas dataframe): a dataframe with all columns from the NARA Preservation Action Plan spreadsheet

    :returns
    df_result (Pandas dataframe): a dataframe with the FITS format information and NARA risk information
    """

    # PART ONE: ADD TEMPORARY COLUMNS TO BOTH DATAFRAMES FOR BETTER MATCHING

    # Formats FITS version as a string to avoid type errors during merging.
    update_df['version_string'] = update_df['FITS_Format_Version'].astype(str)

    # Combines FITS format name (lowercase) and version, since NARA has that information in one column.
    # Removes " NO VALUE" from the combined column, which happens if there is no version.
    update_df['name_version'] = update_df['FITS_Format_Name'].str.lower() + ' ' + update_df['version_string']
    update_df['name_version'] = update_df['name_version'].str.replace(' NO VALUE', '')

    # Makes lowercase versions of FITS and NARA format names for case-insensitive matching.
    update_df['name_lower'] = update_df['FITS_Format_Name'].str.lower()
    nara_df['nara_format_lower'] = nara_df['NARA_Format_Name'].str.lower()

    # Makes a column with the NARA version, since FITS has that in a separate column.
    # The version is assumed to be anything after the last space in the format name, the most common pattern.
    # For ones that don't actually end in a version, it gets the last word, which does not interfere with matching.
    nara_df['nara_version'] = nara_df['NARA_Format_Name'].str.split(' ').str[-1]

    # List of columns in the NARA dataframe used for matching or that should be in the final result.
    nara_columns = ['NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                    'NARA_Proposed_Preservation_Plan', 'nara_format_lower', 'nara_version']

    # For each matching technique, it makes a dataframe by merging NARA into FITS based on one or two columns
    # and creates two dataframes:
    #   one with files that matched (has a value in NARA_Risk Level after the merge)
    #   one with files that did not match (NARA_Risk Level is empty after the merge).
    # A column NARA_Match_Type is added to the matched dataframe with the matching technique name and
    # the it is added to df_result, which is what the function will return.
    # The NARA columns are removed from the unmatched dataframe so they aren't duplicated in the next technique.
    # The next technique is applied to just the files that are unmatched.
    # After all techniques are tried, default values are assigned to NARA columns for files that cannot be matched
    # and this is added to df_result as well.

    # PART TWO: FORMAT IDENTIFICATIONS THAT HAVE A PUID
    # If an FITS format id has a PUID, it should only match something in NARA with the same PUID or no PUID.
    df_format_puid = update_df[update_df['FITS_PUID'] != 'NO VALUE'].copy()
    df_nara_no_puid = nara_df[nara_df['NARA_PRONOM_URL'].isnull()]

    # Technique 1: PRONOM Identifier and Format Version are both a match.
    df_merge = pd.merge(df_format_puid, nara_df[nara_columns], left_on=['FITS_PUID', 'version_string'],
                        right_on=['NARA_PRONOM_URL', 'nara_version'], how='left')
    df_result = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_result = df_result.assign(NARA_Match_Type='PRONOM and Version')
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Technique 2: PRONOM Identifier and Format Name are both a match.
    df_merge = pd.merge(df_unmatched, nara_df[nara_columns], left_on=['FITS_PUID', 'name_lower'],
                        right_on=['NARA_PRONOM_URL', 'nara_format_lower'], how='left')
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type='PRONOM and Name')
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Technique 3: PRONOM Identifier is a match.
    df_merge = pd.merge(df_unmatched, nara_df[nara_columns], left_on='FITS_PUID', right_on='NARA_PRONOM_URL', how='left')
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type='PRONOM')
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Technique 4: Format Name, and Format Version if it has one, are both a match.
    # This only works if the NARA Format Name is structured name[SPACE]version.
    df_merge = pd.merge(df_unmatched, df_nara_no_puid[nara_columns], left_on='name_version',
                        right_on='nara_format_lower', how='left')
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type='Format Name')
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Adds default text for risk and match type for any that are still unmatched.
    df_unmatched = df_unmatched.copy()
    df_unmatched['NARA_Format_Name'] = 'No Match'
    df_unmatched['NARA_Risk_Level'] = 'No Match'
    df_unmatched['NARA_Match_Type'] = 'No NARA Match'
    df_result = pd.concat([df_result, df_unmatched], ignore_index=True)

    # PART THREE: FORMAT IDENTIFICATIONS THAT DO NOT HAVE A PUID
    # If an FITS format id has no PUID, it can match anything in NARA (has a PUID or no PUID).
    df_format_no_puid = update_df[update_df['FITS_PUID'] == 'NO VALUE'].copy()

    # Technique 4 (repeated with different format DF): Format Name, and Format Version if it has one, are both a match.
    # This only works if the NARA Format Name is structured name[SPACE]version.
    df_merge = pd.merge(df_format_no_puid, nara_df[nara_columns], left_on='name_version',
                        right_on='nara_format_lower', how='left')
    df_matched = df_merge[df_merge['NARA_Risk_Level'].notnull()].copy()
    df_matched = df_matched.assign(NARA_Match_Type='Format Name')
    df_result = pd.concat([df_result, df_matched], ignore_index=True)
    df_unmatched = df_merge[df_merge['NARA_Risk_Level'].isnull()].copy()
    df_unmatched.drop(nara_columns, inplace=True, axis=1)

    # Adds default text for risk and match type for any that are still unmatched.
    df_unmatched['NARA_Format_Name'] = 'No Match'
    df_unmatched['NARA_Risk_Level'] = 'No Match'
    df_unmatched['NARA_Match_Type'] = 'No NARA Match'
    df_result = pd.concat([df_result, df_unmatched], ignore_index=True)

    # PART FOUR: CLEAN UP AND RETURN FINAL DATAFRAME

    # Removes the temporary columns used for better matching.
    df_result.drop(['version_string', 'name_version', 'name_lower', 'nara_format_lower', 'nara_version'],
                   inplace=True, axis=1)

    return df_result


def most_recent_spreadsheet(file_list):
    """Determine the most recent preservation spreadsheet in the file list based on the file name

    From legacy practices, any spreadsheet with a date in the name is more recent than one without.
    The list will also include other types of files, such as preservation logs, which are ignored.

    :parameter
    file_list (list): list of all file names in a folder with at least one preservation spreadsheet

    :returns
    recent_file (string): the name of the preservation spreadsheet that is the most recent
    """

    # Variables for tracking which file is the most recent.
    recent_file = None
    recent_date = None

    # Tests each file in the file list looking for the most recent one, based on the date in the file name.
    for file_name in file_list:

        # Skips files that are not risk spreadsheets, like the preservation log.
        if not('full_risk_data' in file_name and file_name.endswith('.csv')):
            continue

        # Extracts the date from the risk spreadsheet file name, if it has one. If it doesn't, assigns 1900-01-01
        # for comparison since any spreadsheet with a date is more recent than one without.
        # Converts the date from a string to type date so that it can be compared to other dates.
        try:
            regex = re.search("_full_risk_data_([0-9]{4})-([0-9]{2})-([0-9]{2}).csv", file_name)
            file_date = date(int(regex.group(1)), int(regex.group(2)), int(regex.group(3)))
        except AttributeError:
            file_date = date(1900, 1, 1)

        # If this is the first file evaluated, or this file's date is more recent than the current recent_date,
        # updates recent_file and recent_date with the current file and its date.
        if recent_date is None or recent_date < file_date:
            recent_file = file_name
            recent_date = file_date

    return recent_file


def new_risk_spreadsheet(parent_folder, risk_csv, nara_df):
    """Make a new risk spreadsheet from the most current risk spreadsheet and NARA risk data

    The new spreadsheet is named accession_full_risk_data_date.csv,
    and is saved in the same folder as the original risk spreadsheet.

    :parameter
    parent_folder (string): path to the folder which contains the risk spreadsheet to be updated
    risk_csv (string): name of the risk spreadsheet to be updated
    nara_df (Pandas DataFrame): dataframe with all columns from NARA's Preservation Action Plan spreadsheet

    :returns
    None
    """

    # Reads the risk csv into a dataframe and makes a second dataframe without the older NARA information.
    current_df = pd.read_csv(os.path.join(parent_folder, risk_csv))
    update_df = current_df.loc[:, 'FITS_File_Path':'FITS_Status_Message']

    # Adds the new NARA information to the format identifications from the risk csv.
    update_df = match_nara_risk(update_df, nara_df)

    # Saves the dataframe to a csv in the same folder as the original risk_csv.
    accession_number = os.path.basename(parent_folder)
    today = datetime.today().strftime('%Y-%m-%d')
    update_csv_path = os.path.join(parent_folder, f'{accession_number}_full_risk_data_{today}.csv')
    update_df.to_csv(update_csv_path, index=False)


def read_nara_csv(nara_csv_path):
    """Read the NARA Preservation Action Plan spreadsheet into a dataframe and rename columns

    Columns used in the final script output are renamed to have a "NARA" prefix
    and underscores instead of spaces.

    :parameter
    nara_csv_path (string): path to the NARA spreadsheet, which is a script argument

    :return
    nara_df (pandas DataFrame): dataframe with all data from the NARA spreadsheet and select columns renamed
    """
    nara_df = pd.read_csv(nara_csv_path)
    nara_df = nara_df.rename(columns={'Format Name': 'NARA_Format_Name',
                                      'File Extension(s)': 'NARA_File_Extensions',
                                      'PRONOM URL': 'NARA_PRONOM_URL',
                                      'NARA Risk Level': 'NARA_Risk_Level',
                                      'NARA Proposed Preservation Plan': 'NARA_Proposed_Preservation_Plan'})
    return nara_df


if __name__ == '__main__':

    # Gets the paths to the directory and NARA Preservation Action Plan spreadsheet from the script arguments.
    # Exits the script if there are errors.
    directory, nara_csv, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Reads the NARA CSV into a dataframe and updates column names.
    nara_risk_df = read_nara_csv(nara_csv)

    # Navigates to each folder with a risk spreadsheet
    # and makes a new version of it using the most recent risk spreadsheet in each folder.
    for root, directories, files in os.walk(directory):
        if any('full_risk_data' in x for x in files):
            file = most_recent_spreadsheet(files)
            new_risk_spreadsheet(root, file, nara_risk_df)
