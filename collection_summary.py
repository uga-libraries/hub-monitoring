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
from datetime import datetime
import os
import pandas as pd
import sys


def check_argument(arg_list):
    # Checks if the expected arguments are present: script path (default in sys.argv) and directory path.
    if len(arg_list) == 2:
        # Checks if the provided directory path exists.
        dir_path = arg_list[1]
        if os.path.exists(dir_path):
            return dir_path, None
        else:
            return None, f"Provided directory {dir_path} does not exist"
    # Do not have the expected arguments.
    else:
        return None, "Missing required argument: directory"


def get_accession_data(path):
    """Calculate the size, date, and risk profile of a single accession folder, using other functions

    :parameter
        path : the path to the accession folder

    :return
        A list of the data
    """
    size = get_size(path)
    files = get_file_count(path)
    date = get_date(path)
    risk = get_risk(path)
    acc_list = [size, files, date]
    acc_list.extend(risk)
    return acc_list


def get_date(path):
    # If preservation log is present, use its date created.
    # If not, parse the year from the start of the accession folder name.
    log_path = os.path.join(path, "preservation_log.txt")
    if os.path.exists(log_path):
        timestamp = os.stat(log_path).st_ctime
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    else:
        acc_folder = os.path.basename(path)
        date = acc_folder[:4]
    return date


def get_file_count(path):
    file_count = 0
    for root, dirs, files in os.walk(path):
        file_count += len(files)
    return file_count


def get_risk(path):
    acc = os.path.basename(path)
    risk_csv_path = os.path.join(path, f"{acc}_full_risk_data.csv")
    risk_df = pd.read_csv(risk_csv_path)
    risk_list = []
    for risk in ('No Match', 'High Risk', 'Moderate Risk', 'Low Risk'):
        risk_list.append((risk_df['NARA_Risk Level'] == risk).sum())
    return risk_list


def get_size(path):
    size_bytes = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            size_bytes += os.stat(file_path).st_size
    size_gb = size_bytes/1000000000
    return size_gb


if __name__ == '__main__':

    # Gets the path to the directory with the information to be summarized from the script argument.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit()

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
