"""Summary of data about each collection in a given department folder

Data included:
- Collection
- Size (GB and number of files)
- Accession date (oldest if more than one)
- Status (if backlog or closed)
- Risk percentages (based on NARA risk data)

If there is more than one accession for the collection, the information is combined.

Parameter:
    directory (required) : the directory with the folders to be summarized

Returns:
    CSV with one row per collection
"""
import os
import pandas as pd
import sys


def get_accession_data(path):
    """Calculate the size, date, and risk profile of a single accession folder, using other functions

    :parameter
        dir : the path to the accession folder

    :return
        A list of the data
    """
    size = get_size(path)
    files = get_file_count(path)
    date = ""
    risk = []
    acc_list = [size, files, date].extend(risk)
    return acc_list


def get_file_count(path):
    file_count = 0
    for root, dirs, files in os.walk(path):
        file_count += len(files)
    return file_count


def get_size(path):
    bytes = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            bytes += os.stat(file_path).st_size
    gb = bytes/1000000000
    return gb


if __name__ == '__main__':

    # Gets the path to the directory with the information to be summarized from the script argument.
    directory = sys.argv[1]

    # Starts a dataframe for information about each accession.
    # It will be summarized later to be by collection.
    df = pd.DataFrame(columns=['Collection', 'Status', 'GB', 'Files', 'Accession Date',
                               'No_Match_Risk', 'High_Risk', 'Moderate_Risk', 'Low_Risk'])

    # Navigate to each accession folder.
    for status in os.listdir(directory):
        for collection in os.listdir(os.path.join(directory, status)):
            for accession in os.listdir(os.path.join(directory, status, collection)):
                accession_path = os.path.join(directory, status, collection, accession)
                accession_list = [collection, status].extend(get_accession_data(accession_path))
