"""Makes a spreadsheet with the format data from every full risk spreadsheet in a given directory

Data included: format name, version, NARA risk level, number of files, and size in GB

Parameter:
    directory (required): the path to the directory with spreadsheets to be combined

Returns:
    CSV with all format data, in the directory folder (script argument)
"""
import os
import pandas as pd
import sys
from risk_update import most_recent_risk_csv
from validate_fixity import check_argument


def combine_risk_csvs(dir_path):
    """Combine the data from the most recent risk csv for every accession in the directory into one dataframe

    @:parameter
    dir_path (string): path to the directory with risk csvs (script argument)

    @:returns
    df (pandas DataFrame): dataframe with all columns from the most recent risk csv for every accession
    """

    # Makes a list of the most recent risk spreadsheet for every accession.
    csv_list = []
    for root, directories, files in os.walk(dir_path):
        if any('full_risk_data' in x for x in files):
            file = most_recent_risk_csv(files)
            csv_list.append(os.path.join(root, file))

    # Prints the number of CSVs, to give an idea of the amount of coverage since not all accessions have a risk CSV.
    print('Number of CSVs to combine:', len(csv_list))

    # Combines every spreadsheet into one dataframe.
    df = pd.concat([pd.read_csv(f, low_memory=False) for f in csv_list])

    # Converts the version column to a string.
    # By default, if a CSV has all numeric versions, it is a float, but otherwise a string.
    # The data type needs to be the same for combining different instances of the same format version later.
    df['FITS_Format_Version'] = df['FITS_Format_Version'].astype(str)

    return df


def df_cleanup(df):
    """Remove unneeded columns, rename a column, remove duplicates, fill empty NARA risk levels

    @:parameter
    df (pandas DataFrame): dataframe with all columns from the most recent risk csv for every accession

    @:returns
    df (pandas DataFrame): dataframe with select columns from the most recent risk csv for every accession
    """

    # Keeps only the needed columns.
    # The other FITs data, NARA data, technical appraisal, and other risk columns are not used.
    df = df[['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk Level']]

    # Renames the only column with spaces to use underscores instead.
    df = df.rename({'NARA_Risk Level': 'NARA_Risk_Level'}, axis=1)

    # Removes duplicates from multiple NARA matches with the same NARA risk level to the same file.
    # The file will still be repeated once per NARA risk level.
    # The file path column is then removed, since it is only needed for removing duplicates.
    df = df.drop_duplicates()
    df = df.drop(columns='FITS_File_Path')

    # Fill blanks in the NARA risk level column (legacy practice) with "No Match" (current practice).
    df['NARA_Risk_Level'] = df['NARA_Risk_Level'].fillna('No Match')

    return df


def files_per_format(df):
    """Calculate the number of files for each format name, version, and NARA risk level combination

    @:parameter
    df (pandas DataFrame): dataframe with select columns from the most recent risk csv for every accession

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


def size_per_format(df):
    """Calculate the size in GB for each format name, version, and NARA risk level combination

    @:parameter
    df (pandas Dataframe): dataframe with select columns from the most recent risk csv for every accession

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
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Combines the most recent risk csv for each accession into one dataframe.
    df_all = combine_risk_csvs(directory)

    # Transforms the dataframe with all risk data to a dataframe with the desired data.
    df_formats = df_cleanup(df_all)

    # Calculates the number of files per format and GB per format, and combines them into one dataframe.
    # It also includes the format name, version, and NARA risk level.
    df_files = files_per_format(df_formats)
    df_size = size_per_format(df_formats)
    df_format_list = pd.merge(df_files, df_size, how='outer')

    # Saves the result to a CSV in the directory.
    # To not save in the same directory as the script argument, update the value of directory.
    # This is sometimes necessary due to not having write permissions on the accession storage.
    # directory = 'insert-path'
    df_format_list.to_csv(os.path.join(directory, 'combined_format_data.csv'), index=False)
