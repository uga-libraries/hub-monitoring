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


def combine_collection_data(coll_df):
    # Combine data from multiple accessions in the same collection.
    # Collection and Status are the same for each group.
    # GB, Files, and the four risk categories are added.
    # TODO: this is dropping the Date column, because we haven't decided how to aggregate it.
    coll_df = coll_df.groupby(['Collection', 'Status'], as_index=False).sum()

    # Replaces risk columns with file counts with risk columns with the percentage of files.
    coll_df['No_Match_Risk_%'] = round(coll_df['No_Match_Risk'] / coll_df['Files'] * 100, 1)
    coll_df['High_Risk_%'] = round(coll_df['High_Risk'] / coll_df['Files'] * 100, 1)
    coll_df['Moderate_Risk_%'] = round(coll_df['Moderate_Risk'] / coll_df['Files'] * 100, 1)
    coll_df['Low_Risk_%'] = round(coll_df['Low_Risk'] / coll_df['Files'] * 100, 1)
    coll_df.drop(['No_Match_Risk', 'High_Risk', 'Moderate_Risk', 'Low_Risk'], axis=1, inplace=True)

    return coll_df


def get_accession_data(acc_dir, acc_status, acc_coll, acc_id):
    """Calculate the data about a single accession folder, mostly using other functions

    :parameter
        acc_dir : the name of the directory that contains the accession (script argument)
        acc_status : if the accession is backlogged or closed, which is a folder within acc_dir
        acc_coll : the collection the accession is part of, which is a folder within acc_status
        acc_id : the accession id, which is a folder within acc_coll

    :return
        A list with the collection, status, size (GB), files, date, and number of files at each of the 4 risk levels
    """
    # Calculates the path to the accession folder, which combines the four function parameters.
    # Some parameters are also included in the accession data, so they are passed separately rather than as the path.
    acc_path = os.path.join(acc_dir, acc_status, acc_coll, acc_id)

    # Gets the data which requires additional calculation.
    # Size, Files, and Date are single data points, while risk is a list of four items.
    size = get_size(acc_path)
    files = get_file_count(acc_path)
    date = get_date(acc_path)
    risk = get_risk(acc_path)

    # Combines the data into a single list.
    acc_list = [acc_coll, acc_status, size, files, date]
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
    accession_df = pd.DataFrame(columns=['Collection', 'Status', 'GB', 'Files', 'Date',
                                         'No_Match_Risk', 'High_Risk', 'Moderate_Risk', 'Low_Risk'])

    # Navigates to each accession folder, gets the information, and saves to the accession dataframe.
    for status in os.listdir(directory):
        for collection in os.listdir(os.path.join(directory, status)):
            for accession in os.listdir(os.path.join(directory, status, collection)):
                accession_df.loc[len(accession_df)] = get_accession_data(directory, status, collection, accession)

    # Combines accession information for each collection and saves to a CSV in "directory".
    collection_df = combine_collection_data(accession_df)
    pd.to_csv(os.path.join(directory, 'hub-collection-summary.csv'))
