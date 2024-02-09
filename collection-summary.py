"""Summary of data about each collection in a given department folder

Data included:
- Collection ID
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


if __name__ == '__main__':

    # Gets the path to the directory with the information to be summarized from the script argument.
    directory = sys.argv[1]

    # Starts a dataframe for information about each accession.
    # It will be summarized later to be by collection.
    df = pd.DataFrame(columns=['Collection_ID', 'GB', 'Files', 'Accession Date', 'Status',
                               'No_Match_Risk', 'High_Risk', 'Moderate_Risk', 'Low_Risk'])

    # Navigate to each accession folder.
    for status in os.listdir(directory):
        for collection in os.listdir(os.path.join(directory, status)):
            for accession in os.listdir(os.path.join(directory, status, collection)):
                print(status, collection, accession)
