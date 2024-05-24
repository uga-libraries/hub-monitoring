"""Analyze all accessions in a given folder for completeness and make a report of any that are not complete.

Testing that the preservation log and full risk report are present and the files are bagged.
Accessions may be incomplete because they were created prior to current procedures
or because file path lengths or other errors prevent current procedures from being done.
"""
import csv
import os
import sys


def accession_paths(status, coll):
    """Find the accession folder(s), which can be in a few places in the collection folder

    Most accessions are in folders named with the accession number within the collection folder.
    Some are in a folder named Preservation Copies, which may or may not include folders by accession number.
    A few are in the collection folder without any additional folders.

    @:parameter
    status (string): parent folder of collection folder, either "backlogged" or "closed"
    coll (string): the name of the collection folder

    @:returns
    acc_paths (list): a list of paths to the folders with the accession content
    """

    acc_paths = []
    coll_path = os.path.join(collection_directory, status, coll)

    # Navigates the collection folder looking for the folder with the accession content.
    for acc in os.listdir(coll_path):

        # Skips anything that is a file instead of a folder.
        if os.path.isfile(os.path.join(coll_path, acc)):
            continue

        # Skips non-accession folders that may be sibling folders of accessions.
        # Multiple folders are about appraisal, which all match the pattern starts with 'Apprais'.
        skip = ['Access Copies', 'AIPs V2', 'Arranged by series', 'to ingest', 'Risk_remediation', 'Risk remediation']
        if acc in skip or acc.startswith('Apprais') or acc.startswith('Risk') or acc.endswith('FITS'):
            continue

        # Accession folder is directly inside the collection folder.
        acc_paths.append(os.path.join(coll_path, acc))

    return acc_paths


def check_completeness(acc_path):
    """Test if the accession has a preservation log, full risk report, and if the content is bagged

    @:parameter
    acc_path (string): the full path to the accession folder

    @:returns
    result (dictionary): keys are 'pres_log', 'full_risk', 'bag' and values are True/False for if each are present
    """

    # Starts a dictionary with the default value of False for all three completeness criteria.
    # These are updated to True if they are found in the accession.
    result = {'pres_log': False, 'full_risk': False, 'bag': False}

    # Looks for the completeness criteria, which are in the first level within the accession folder.
    for item in os.listdir(acc_path):

        # Preservation log has a consistent file name.
        if item == 'preservation_log.txt':
            result['pres_log'] = True

        # Full risk data spreadsheet may have a date between full_risk_data and the file extension.
        elif 'full_risk_data' in item and item.endswith('.csv'):
            result['full_risk'] = True

        # Bags follow the naming convention of ending with _bag.
        elif item.endswith('_bag'):
            result['bag'] = True

    return result


def update_report(status, coll, acc_path, result):
    """Adds an accession to the completeness report

    The report is saved in the collections_directory.

    @:parameter
    status (string): parent folder of collection folder, either "backlogged" or "closed"
    coll (string): the name of the collection folder
    acc_path (string): the full path to the accession folder
    result (dictionary): keys are 'pres_log', 'full_risk', 'bag' and values are True/False for if each are present

    @:returns
    None
    """

    # If the report does not already exist, makes a report with a header row.
    report_path = os.path.join(collection_directory, 'accession_completeness_report.csv')
    if not os.path.exists(report_path):
        with open(report_path, 'w', newline='') as report:
            writer = csv.writer(report)
            writer.writerow(['Status', 'Collection', 'Accession', 'Preservation_Log', 'Full_Risk', 'Bag'])

    # Gets the accession number from the path.
    acc = os.path.basename(acc_path)

    # Saves the information to the report.
    with open(report_path, 'a', newline='') as report:
        writer = csv.writer(report)
        writer.writerow([status, coll, acc, result['pres_log'], result['full_risk'], result['bag']])


if __name__ == '__main__':
    collection_directory = sys.argv[1]

    # First level within the collection_directory is status folders (backlogged or closed),
    # as well as additional folders and files that are not part of this analysis.
    for status_folder in os.listdir(collection_directory):
        if status_folder == 'backlogged' or status_folder == 'closed':

            # All folders within the status folders should be collections.
            for collection in os.listdir(os.path.join(collection_directory, status_folder)):

                # Skips unconventional collections.
                unconventional = ['ua22-008 Linguistic Atlas Project', 'RBRL_275_GEPO', 'rbrl349', 'rbrl409', 'rbrl462']
                if collection in unconventional:
                    continue

                # Gets a list of the path to every folder with accession content and tests their completeness.
                accession_list = accession_paths(status_folder, collection)
                for accession_path in accession_list:
                    completeness_dict = check_completeness(accession_path)
                    # If any of the criteria are missing, saves the information to the report.
                    if False in completeness_dict.values():
                        update_report(status_folder, collection, accession_path, completeness_dict)

    # Prints if there were any incomplete accessions (the report was made) or not.
    report_path = os.path.join(collection_directory, 'accession_completeness_report.csv')
    if os.path.exists(report_path):
        print(f'\nIncomplete accessions found. See accession_completeness_report.csv in {collection_directory}.')
    else:
        print(f'\nAll accessions are complete.')
