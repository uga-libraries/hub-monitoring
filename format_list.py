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


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    directory = sys.argv[1]

    # Makes a list of every risk spreadsheet, anywhere in the directory.
    csv_list = []
    for root, directories, files in os.walk(directory):
        for file in files:
            if 'full_risk_data' in file:
                csv_list.append(os.path.join(root, file))

    # Makes a dataframe with the contents of every spreadsheet.
    df_all = pd.concat([pd.read_csv(f) for f in csv_list])

    # Makes a copy of the dataframe with just the needed columns and no duplicate rows (from multiple NARA matches).
    df = df_all[['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk Level']].copy()
    df = df.rename({'NARA_Risk Level': 'NARA_Risk_Level'}, axis=1)
    df = df.drop_duplicates()
    df = df.drop(columns='FITS_File_Path')

    # Fill blanks in NARA (legacy practice) with No Match (current practice).
    df['NARA_Risk_Level'] = df['NARA_Risk_Level'].fillna('No Match')

    # print('Number of risk spreadsheets combined:', len(csv_list))
