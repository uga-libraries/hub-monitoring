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
from validate_fixity import check_argument


def combine_risk_csvs(dir_path):
    """Combine the data from every risk csv in the directory into one dataframe"""

    # Makes a list of every risk spreadsheet, anywhere in the directory.
    csv_list = []
    for root, directories, files in os.walk(dir_path):
        for file in files:
            if 'full_risk_data' in file:
                csv_list.append(os.path.join(root, file))

    # Combines every spreadsheet into one dataframe.
    df = pd.concat([pd.read_csv(f) for f in csv_list])

    # Converts version to string. If a CSV has all numeric versions, it is a float, but otherwise a string.
    # The data type needs to be the same for combining different instances of the same version.
    df['FITS_Format_Version'] = df['FITS_Format_Version'].astype(str)

    return df


def df_cleanup(df):
    """Remove columns, remove duplicates, fill empty NARA risk levels"""

    # Makes a copy of the dataframe with just the needed columns.
    df = df[['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk Level']]

    # Rename the only column with spaces to use underscores instead.
    df = df.rename({'NARA_Risk Level': 'NARA_Risk_Level'}, axis=1)

    # Removes duplicates from multiple NARA matches to the same file with the same NARA risk level.
    # The file path column is only needed for removing duplicates.
    df = df.drop_duplicates()
    df = df.drop(columns='FITS_File_Path')

    # Fill blanks in NARA (legacy practice) with No Match (current practice).
    df['NARA_Risk_Level'] = df['NARA_Risk_Level'].fillna('No Match')

    return df


def files_per_format(df):
    """Number of files for each format name, version, risk level combination"""

    # Groupby includes NARA risk level so different possible risks for the name/version combination are kept.
    # Reset index keeps the name, version, and risk level as columns in the dataframe.
    # Without reset index, it would return a series with those columns as part of the index.
    group_list = ['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level']
    files = df.groupby(group_list).size().reset_index()

    # Renames the default column name for the sum to be more descriptive.
    files = files.rename({0: 'File_Count'}, axis=1)

    return files


def size_per_format(df):
    """Size in GB for each format name, version, risk level combination"""

    # Groupby includes NARA risk level so different possible risks for the name/version combination are kept.
    # Reset index keeps the name, version, and risk level as columns in the dataframe.
    # Without reset index, it would return a series with those columns as part of the index.
    group_list = ['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level']
    size = df.groupby(group_list)['FITS_Size_KB'].sum().reset_index()

    # Convert the KB to GB and round to 3 decimal places.
    size['Size_GB'] = round(size['FITS_Size_KB'] / 1000000, 3)

    # Remove the KB column, which is not needed now that we have GB.
    size = size.drop(columns='FITS_Size_KB')

    return size


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    # Exits the script if there is an error.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Combines the risk data into one dataframe.
    df_all = combine_risk_csvs(directory)

    # Transforms dataframe with all risk data to a dataframe with desired data.
    df_formats = df_cleanup(df_all)

    # Gets the number of files per format and GB per format, and combines into one dataframe.
    df_files = files_per_format(df_formats)
    df_size = size_per_format(df_formats)
    df_format_list = pd.merge(df_files, df_size, how='outer')

    # Save the result to a CSV in directory.
    df_format_list.to_csv(os.path.join(directory, 'combined_format_data.csv'), index=False)
