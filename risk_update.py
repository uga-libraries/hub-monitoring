"""Makes an updated risk spreadsheet for every accession in a directory

Parameters:
    input_directory (required): the directory that contains the risk spreadsheets,
                                which can be any folder (status, collection, etc.)
    nara_csv (required): the path to the most recent NARA Preservation Action Plan spreadsheet

Returns:
    New risk spreadsheet is added to each accession folder
    Log of all accessions (with collection and accession number) and if a new risk csv was made in the input_directory
"""
from datetime import date, datetime
import os
import pandas as pd
import re
import sys


def accession_test(acc_id, acc_path):
    """Determine if a folder is an accession based on the folder name

    There may be other folders used for other purposes, like risk remediation or appraisal, as well.
    These other folders are not part of the collection summary report.

    Keep in sync with the copy of this function in collection_summary.py. Unit tests are with that script.

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


def check_arguments(argument_list):
    """Check the required arguments, input_directory and nara_csv, are present and correct

    Adapted from https://github.com/uga-libraries/format-report/blob/main/merge_format_reports.py

    @:parameter
    argument_list (list): the contents of sys.argv after the script is run

    @:returns
    dir_path (string, None): string with the path to the directory to check for risk spreadsheets, or None if missing
    nara_path (string, None): string with the path to NARA's Preservation Action Plan spreadsheet, or None if missing
    errors (list): the list of errors encountered, if any, or an empty list
    """

    # Makes variables with default values to store the results of the function.
    dir_path = None
    nara_path = None
    errors = []

    # Verifies that the first required argument (input_directory) is present,
    # and if it is present that it is a valid path.
    if len(argument_list) > 1:
        dir_path = argument_list[1]
        if not os.path.exists(dir_path):
            errors.append(f"Input directory '{dir_path}' does not exist")
    else:
        errors.append('Required argument input_directory is missing')

    # Verifies that the second required argument (nara_csv) is present,
    # and if it is present that it is a valid path.
    if len(argument_list) > 2:
        nara_path = argument_list[2]
        if not os.path.exists(nara_path):
            errors.append(f"NARA CSV '{nara_path}' does not exist")
    else:
        errors.append('Required argument nara_csv is missing')

    # Verifies that there are not too many arguments, which could mean the input was not in the correct order.
    if len(argument_list) > 3:
        errors.append('Too many arguments. Should just have two, input_directory and nara_csv')

    return dir_path, nara_path, errors


def match_nara_risk(risk_df, nara_df):
    """Match format identifications to NARA's Preservation Action Plan spreadsheet

    The match techniques are applied in order of accuracy,
    and no additional match techniques are tried once a match is found.

    Adopted from https://github.com/uga-libraries/accessioning-scripts/blob/main/format_analysis_functions.py

    @:parameter
    risk_df (Pandas dataframe): a dataframe with FITS format information columns from a risk spreadsheet
    nara_df (Pandas dataframe): a dataframe with all columns from the NARA Preservation Action Plan spreadsheet

    @:returns
    df_result (Pandas dataframe): a dataframe with the FITS format information and NARA risk information
    """

    # PART ONE: ADD TEMPORARY COLUMNS TO BOTH DATAFRAMES FOR BETTER MATCHING

    # Formats FITS version as a string to avoid type errors during merging.
    risk_df['version_string'] = risk_df['FITS_Format_Version'].astype(str)

    # Combines FITS format name (lowercase) and version, since NARA has that information in one column.
    # Removes " NO VALUE" from the combined column, which happens if there is no version.
    risk_df['name_version'] = risk_df['FITS_Format_Name'].str.lower() + ' ' + risk_df['version_string']
    risk_df['name_version'] = risk_df['name_version'].str.replace(' NO VALUE', '')

    # Makes lowercase versions of FITS and NARA format names for case-insensitive matching.
    risk_df['name_lower'] = risk_df['FITS_Format_Name'].str.lower()
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
    df_format_puid = risk_df[risk_df['FITS_PUID'] != 'NO VALUE'].copy()
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
    df_format_no_puid = risk_df[risk_df['FITS_PUID'] == 'NO VALUE'].copy()

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


def most_recent_risk_csv(file_list):
    """Determine the most recent risk spreadsheet in the file list based on the file name

    From legacy practices, any spreadsheet with a date in the name is more recent than one without.
    The list will also include other types of files, such as preservation logs, which are ignored.

    Keep in sync with the copy of this function in collection_summary.py and format_list.py
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
        if not('full_risk_data' in file_name):
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


def read_nara_csv(nara_csv_path):
    """Read select columns from the NARA Preservation Action Plan spreadsheet into a dataframe and rename

    If the columns do not have the expected names, a KeyError is raised and the script will exit.

    @:parameter
    nara_csv_path (string): path to the NARA spreadsheet, which is a script argument

    @:returns
    nara_df (pandas DataFrame): dataframe with all data from the NARA spreadsheet and select columns renamed
    or raises a KeyError if the select columns are not present
    """
    # Reads the NARA CSV into a dataframe, and makes another dataframe with just the 5 columns used in the report.
    # This will raise a KeyError if the columns do not have the expected names,
    # which happens if an old copy of the NARA CSV is used or if NARA changes how they name their columns.
    df = pd.read_csv(nara_csv_path, low_memory=False)
    used_columns = ['Format Name', 'File Extension(s)', 'PRONOM URL', 'NARA Risk Level',
                    'NARA Proposed Preservation Plan']
    nara_df = df[used_columns].copy()

    # Rename the columns to start with NARA and use underscores instead of spaces.
    nara_df = nara_df.rename(columns={'Format Name': 'NARA_Format_Name',
                                      'File Extension(s)': 'NARA_File_Extensions',
                                      'PRONOM URL': 'NARA_PRONOM_URL',
                                      'NARA Risk Level': 'NARA_Risk_Level',
                                      'NARA Proposed Preservation Plan': 'NARA_Proposed_Preservation_Plan'})
    return nara_df


def read_risk_csv(risk_csv_path):
    """Read the FITS format identification columns from the risk CSV into a dataframe

    @:parameter
    risk_csv_path (string): path to the most recent risk csv in the accession folder

    @:returns
    risk_df (pandas Dataframe): dataframe with all FITS formation information columns from the risk CSV
    """
    # Reads the risk csv into a dataframe.
    # Specifies dtype=object so blank columns are not interpreted as floats, which causes type errors during merges.
    df = pd.read_csv(risk_csv_path, dtype=object)

    # Makes a second dataframe without the older NARA information.
    risk_df = df.loc[:, 'FITS_File_Path':'FITS_Status_Message'].copy()

    # Blanks are fill with NO VALUE to match the formatting expected by match_nara_risk,
    # a function used by other scripts as well.
    risk_df.fillna('NO VALUE', inplace=True)

    return risk_df


def save_risk_csv(accession_path, risk_df):
    """Make a new risk spreadsheet from the combined most current risk spreadsheet and NARA risk data

    The new spreadsheet is named accession_full_risk_data_date.csv,
    and is saved in the same folder as the original risk spreadsheet.

    @:parameter
    accession_path (string): path to the accession folder, which is the folder that contains the risk csv(s).
    risk_df (Pandas DataFrame): dataframe with the FITS data and NARA risk data

    @:returns
    None
    """

    # Removes duplicate rows.
    # These are cases where the original data accidentally has a file, with the same identification, multiple times.
    risk_df.drop_duplicates(inplace=True)

    # Saves the dataframe to a csv in the same folder as the original risk_csv.
    accession_number = os.path.basename(accession_path)
    today = datetime.today().strftime('%Y-%m-%d')
    update_csv_path = os.path.join(accession_path, f'{accession_number}_full_risk_data_{today}.csv')
    risk_df.to_csv(update_csv_path, index=False)


def update_log(accession_path, log_dir, update_result):
    """Log every accession and if the risk csv was updated

    The log includes the collection and accession number, which are both part of the accession path,
    and if the risk csv was updated or not.

    @:parameter
    accession_path (string): path to the accession folder, which is the folder that contains the risk csv(s)
    log_dir (string): the path to the directory for saving the log (script argument input_directory)
    update_result (string): Yes (updated risk csv made) or No (no previous risk csv to update)

    @:returns
    None. Makes or updates the log.
    """

    # Parses the collection and accession number from the accession path.
    # The accession number is the last folder and the collection number is the second to last folder.
    accession_path_list = accession_path.split('\\')
    collection = accession_path_list[-2]
    accession = accession_path_list[-1]

    # If the log doesn't exist yet (this is the first CSV to be updated), makes the log with a header row.
    today = datetime.today().strftime('%Y-%m-%d')
    log_path = os.path.join(log_dir, f"update_risk_log_{today}.csv")
    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            f.write('Collection,Accession,Risk_Updated\n')

    # Adds the collection and accession to the log.
    with open(log_path, 'a') as f:
        f.write(f'{collection},{accession},{update_result}\n')


if __name__ == '__main__':

    # Gets the paths to the input directory and NARA Preservation Action Plan spreadsheet from the script arguments.
    # Exits the script if there are errors.
    input_directory, nara_csv, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit(1)

    # Reads the NARA CSV into a dataframe and updates column names.
    # Exits the script if the NARA CSV does not have the expected column names.
    try:
        nara_risk_df = read_nara_csv(nara_csv)
    except KeyError:
        print('\nThe NARA Preservation Action Plan spreadsheet does not have at least one of the expected columns: '
              'Format Name, File Extension(s), PRONOM URL, NARA Risk Level, and NARA Proposed Preservation Plan. '
              'The spreadsheet used may be out of date, or NARA may have changed their spreadsheet organization.')
        sys.exit(1)

    # Navigates to each accession folder and makes a new version of the risk spreadsheet
    # using the most recent risk spreadsheet in each folder and the current NARA risk CSV.
    # Also logs if it found a risk spreadsheet or not.
    for root, directories, files in os.walk(input_directory):
        if accession_test(os.path.basename(root), root):
            if any('full_risk_data' in x for x in files):
                print('Starting on accession', root)
                file = most_recent_risk_csv(files)
                new_risk_df = read_risk_csv(os.path.join(root, file))
                new_risk_df = match_nara_risk(new_risk_df, nara_risk_df)
                save_risk_csv(root, new_risk_df)
                update_log(root, input_directory, 'Yes')
            else:
                update_log(root, input_directory, 'No')
