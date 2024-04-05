"""Makes a spreadsheet with the format data from every full risk spreadsheet in a given folder

Data included: TBD

Parameter:
    directory (required): the directory with spreadsheets to be combined

Returns:
    CSV with all format data
"""
import os
import pandas as pd
import sys


def combine_risk_csvs(dir):
    """Combine the data from every risk csv in the directory into one dataframe"""

    # Makes a list of every risk spreadsheet, anywhere in the directory.
    csv_list = []
    for root, directories, files in os.walk(dir):
        for file in files:
            if 'full_risk_data' in file:
                csv_list.append(os.path.join(root, file))

    # Combines every spreadsheet into one dataframe.
    df = pd.concat([pd.read_csv(f) for f in csv_list])
    return df


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    directory = sys.argv[1]

    # Combines the risk data into one dataframe.
    df_all = combine_risk_csvs(directory)

    # Makes a copy of the dataframe with just the needed columns and no duplicate rows (from multiple NARA matches).
    df = df_all[['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk Level']].copy()
    df = df.rename({'NARA_Risk Level': 'NARA_Risk_Level'}, axis=1)
    df = df.drop_duplicates()
    df = df.drop(columns='FITS_File_Path')

    # Fill blanks in NARA (legacy practice) with No Match (current practice).
    df['NARA_Risk_Level'] = df['NARA_Risk_Level'].fillna('No Match')

    # Number of files and KB for each format name/version/risk combination.
    files = df.groupby(['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level']).size().reset_index()
    files = files.rename({0: 'File_Count'}, axis=1)
    size = df.groupby(['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'])['FITS_Size_KB'].sum().reset_index()
    size['Size_GB'] = size['FITS_Size_KB']/1000000
    size = size.drop(columns='FITS_Size_KB')
    df_formats = pd.merge(files, size, how='outer')

    # Save the result to a CSV in directory.
    df_formats.to_csv(os.path.join(directory, 'combined_format_data.csv'), index=False)
