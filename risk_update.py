"""Get updated NARA risk information for every accession in a directory

Parameters:
    directory (required): the directory that contains the risk data spreadsheets
    nara_csv (required): the path to the most recent NARA Digital Preservation Plan spreadsheet

Returns:
    New risk data spreadsheet added to each accession folder
"""
from datetime import datetime
import os
import pandas as pd
import sys


def check_arguments(argument_list):
    """Check the required arguments directory and nara_csv are present and correct

    Adapted from https://github.com/uga-libraries/format-report/blob/main/merge_format_reports.py

    Parameters:
        argument_list : list from sys.argv with the script parameters

    Returns:
        dir_path : the path to the folder which contains the risk data spreadsheets, or None
        nara_path : the path to NARA's Digital Preservation Plan spreadsheet, or None
        errors : the list of errors encountered, if any, or an empty list
    """

    # Makes variables with default values to store the results of the function.
    dir_path = None
    nara_path = None
    errors = []

    # Verifies that the first required argument (directory) is present,
    # and if it is present that it is a valid directory.
    if len(argument_list) > 1:
        dir_path = argument_list[1]
        if not os.path.exists(dir_path):
            errors.append(f"Directory '{dir_path}' does not exist")
    else:
        errors.append("Required argument directory is missing")

    # Verifies that the second required argument (nara_csv) is present,
    # and if it is present that it is a valid directory.
    if len(argument_list) > 2:
        nara_path = argument_list[2]
        if not os.path.exists(nara_path):
            errors.append(f"NARA CSV '{nara_path}' does not exist")
    else:
        errors.append("Required argument nara_csv is missing")

    # Returns the results.
    return dir_path, nara_path, errors


def match_nara_risk(update_df, nara_df):
    """Match format identifications to NARA's Digital Preservation Plan spreadsheet

    The match techniques are applied in order of accuracy, and stop for each format when a match is found.

    This function is based on https://github.com/uga-libraries/accessioning-scripts/blob/main/format_analysis_functions.py

    Returns a dataframe with all the format data, the NARA Risk Level and Proposed Preservation Plan,
    and the name of the technique that produced the match (NARA_Match_Type).

    :parameters
        update_df : a dataframe with FITS columns from a risk data spreadsheet
        nara_df " a dataframe from NARA Digital Preservation Plan spreadsheet

    Returns:
        df_result : a dataframe with the format information and corresponding NARA risk information, if matched
    """

    # PART ONE: ADD TEMPORARY COLUMNS TO BOTH DATAFRAMES FOR BETTER MATCHING

    # Formats FITS version as a string to avoid type errors during merging.
    update_df['version_string'] = update_df['FITS_Format_Version'].astype(str)

    # Combines FITS format name and version, since NARA has that information in one column.
    # Removes " NO VALUE" from the combined column, which happens if there is no version.
    update_df['name_version'] = update_df['FITS_Format_Name'].str.lower() + ' ' + update_df['version_string']
    update_df['name_version'] = update_df['name_version'].str.replace(' NO VALUE', '')

    # Makes FITS and NARA format names lowercase for case-insensitive matching.
    update_df['name_lower'] = update_df['FITS_Format_Name'].str.lower()
    nara_df['nara_format_lower'] = nara_df['NARA_Format_Name'].str.lower()

    # Makes a column with the NARA version, since FITS has that in a separate column.
    # The version is assumed to be anything after the last space in the format name, the most common pattern.
    # For ones that don't actually end in a version, it gets the last word, which does not interfere with matching.
    nara_df['nara_version'] = nara_df['NARA_Format_Name'].str.split(' ').str[-1]

    # List of relevant columns in the NARA dataframe.
    nara_columns = ['NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                    'nara_format_lower', 'nara_version']

    # For each matching technique, it makes a dataframe by merging NARA into FITS based on one or two columns
    # and creates two dataframes:
    #   one with files that matched (has a value in NARA_Risk Level after the merge)
    #   one with files that did not match (NARA_Risk Level is empty after the merge).
    # A column NARA_Match_Type is added to the matched dataframe with the matching technique name and
    # the entire dataframe is added to df_result, which is what the function will return.
    # The NARA columns are removed from the unmatched dataframe so they aren't duplicated in future merges.
    # The next technique is applied to just the files that are unmatched.
    # After all techniques are tried, default values are assigned to NARA columns for files that cannot be matched
    # and this is added to df_result as well.

    # PART TWO: FORMAT IDENTIFICATIONS THAT HAVE A PUID
    # If an FITS format id has a PUID, it should only match something in NARA with the same PUID or no PUID.

    # Makes dataframes needed for part two matches:

    # FITS identifications that have a PUID.
    df_format_puid = update_df[update_df['FITS_PUID'] != 'NO VALUE'].copy()

    # NARA identifications that do not have a PUID.
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

    # Makes dataframes needed for part three matches:

    # FITS identifications that have no PUID.
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


def new_risk_spreadsheet(parent_folder, risk_csv, nara_df):
    """docstring tbd"""
    # Reads the risk csv into a dataframe, removing the older NARA information.
    current_df = pd.read_csv(os.path.join(parent_folder, risk_csv))
    update_df = current_df.loc[:, 'FITS_File_Path':'FITS_Status_Message']

    # Adds the new NARA information.
    update_df = match_nara_risk(update_df, nara_df)

    # Saves the dataframe to a csv in the same folder as the original risk_csv.
    accession_number = os.path.basename(parent_folder)
    today = datetime.today().strftime('%Y-%m-%d')
    update_csv_path = os.path.join(parent_folder, f'{accession_number}_full_risk_data_{today}.csv')
    update_df.to_csv(update_csv_path, index=False)


def read_nara_csv(nara_csv_path):
    """Read the NARA Digital Preservation Plan spreadsheet into a dataframe and rename columns

    Columns used in the final script output are renamed to have a "NARA" prefix
    and underscores instead of spaces.

    :parameter
    nara_csv_path (string): path to the NARA CSV, which is a script argument

    :return
    nara_df (pandas DataFrame): dataframe with all data from the NARA CSV and select column renamed
    """
    nara_df = pd.read_csv(nara_csv_path)
    nara_df = nara_df.rename(columns={'Format Name': 'NARA_Format_Name',
                                      'File Extension(s)': 'NARA_File_Extensions',
                                      'PRONOM URL': 'NARA_PRONOM_URL',
                                      'NARA Risk Level': 'NARA_Risk_Level',
                                      'NARA Proposed Preservation Plan': 'NARA_Proposed_Preservation_Plan'})
    return nara_df


if __name__ == '__main__':

    # Gets the paths to the directory and NARA spreadsheet from the script arguments.
    # Exits the script if there are errors.
    directory, nara_csv, errors_list = check_arguments(sys.argv)
    if len(errors_list) > 0:
        for error in errors_list:
            print(error)
        sys.exit()

    # Reads the NARA CSV into a dataframe and updates column names.
    nara_risk_df = read_nara_csv(nara_csv)

    # Navigates to each risk spreadsheet.
    for root, directories, files in os.walk(directory):
        for file in files:
            if 'full_risk_data' in file and file.endswith('.csv'):
                # Makes a new risk spreadsheet with the same format identifications and updated NARA risk levels.
                new_risk_spreadsheet(root, file, nara_risk_df)
