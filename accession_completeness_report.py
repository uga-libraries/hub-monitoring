"""Analyze all accessions in a given folder (input_directory) for completeness
and make a report of any that are not complete.

An accession is complete if it contains a preservation log (preservation_log.txt),
 a full risk report (acc_full_risk_data.csv), and the files are bagged (folder ends with '_bag').

Accessions may be incomplete because they were created prior to current procedures
or because file path lengths or other errors prevent current procedures from being done.

Parameter:
    input_directory (required): the directory with the folders to be summarized,
                                which should be the parent folder of the status (backlogged and/or closed) folders

Returns:
    accession_completeness_report_YYYY-MM-DD.csv, saved in input_directory
"""
import csv
from datetime import date
import os
import sys


def accession_paths(acc_status, coll):
    """Find the paths for the accession folder(s) in a collection folder

    The collection folder also contains other folders and files.

    @:parameter
    acc_status (string): parent folder of collection folder, either "backlogged" or "closed"
    coll (string): the name of the collection folder

    @:returns
    acc_paths (list): a list of paths to the folders with the accession content
    """

    acc_paths = []
    coll_path = os.path.join(input_directory, acc_status, coll)

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
    """Test if the accession has a preservation log, full risk report, initial manifest, and if the content is bagged

    @:parameter
    acc_path (string): the full path to the accession folder

    @:returns
    result (dictionary): keys are 'pres_log', 'full_risk', 'initial_manifest', 'bag'
                         and values are True/False for if each are present
    """

    # Starts a dictionary with the default value of False for all three completeness criteria.
    # These are updated to True if they are found in the accession.
    result = {'pres_log': False, 'full_risk': False, 'initial_manifest': False, 'bag': False}

    # Looks for the completeness criteria, which are in the first level within the accession folder.
    for item in os.listdir(acc_path):

        # Preservation log has a consistent file name.
        if item == 'preservation_log.txt':
            result['pres_log'] = True

        # Full risk data spreadsheet may have a date between full_risk_data and the file extension.
        elif 'full_risk_data' in item and item.endswith('.csv'):
            result['full_risk'] = True

        # Initial Manifest includes the date between initialmanifest_ and the file extension.
        elif item.startswith('initialmanifest_') and item.endswith('.csv'):
            result['initial_manifest'] = True

        # Bags follow the naming convention of ending with _bag.
        elif item.endswith('_bag'):
            result['bag'] = True

    return result


def update_report(acc_status, coll, acc_path, result):
    """Make the completeness report, if it doesn't already exist, and add an accession to the report

    The report is saved in the input_directory.

    @:parameter
    acc_status (string): parent folder of collection folder, either "backlogged" or "closed"
    coll (string): the name of the collection folder
    acc_path (string): the full path to the accession folder
    result (dictionary): keys are 'pres_log', 'full_risk', 'initial_manifest', 'bag'
                         and values are True/False for if each are present

    @:returns
    None
    A row is added to the completeness report
    """

    # If the report does not already exist, makes a report with a header row.
    report_path = os.path.join(input_directory, f"accession_completeness_report_{date.today().strftime('%Y-%m-%d')}.csv")
    if not os.path.exists(report_path):
        with open(report_path, 'w', newline='') as report:
            writer = csv.writer(report)
            writer.writerow(['Status', 'Collection', 'Accession', 'Preservation_Log', 'Full_Risk',
                             'Initial_Manifest', 'Bag'])

    # Gets the accession number from the path.
    acc = os.path.basename(acc_path)

    # Saves the information to the report.
    with open(report_path, 'a', newline='') as report:
        writer = csv.writer(report)
        writer.writerow([acc_status, coll, acc, result['pres_log'], result['full_risk'],
                         result['initial_manifest'], result['bag']])


if __name__ == '__main__':
    # Script argument is the parent directory of the status folders.
    input_directory = sys.argv[1]

    # First level within the input_directory is folders named with the status (backlogged and/or closed),
    # as well as additional folders and files that are not part of this analysis.
    for status in os.listdir(input_directory):
        if status == 'backlogged' or status == 'closed':

            # All folders within the status folders should be collections.
            for collection in os.listdir(os.path.join(input_directory, status)):

                # Skips unconventional collections, which are not expected to follow these rules.
                unconventional = ['ua22-008 Linguistic Atlas Project', 'RBRL_275_GEPO', 'rbrl349', 'rbrl409', 'rbrl462']
                if collection in unconventional:
                    continue

                # Gets a list of the path to every folder with accession content and tests their completeness.
                accession_list = accession_paths(status, collection)
                for accession_path in accession_list:
                    print('Starting on accession', accession_path)
                    completeness_dict = check_completeness(accession_path)
                    # If any of the criteria are missing, saves the information to the report.
                    if False in completeness_dict.values():
                        update_report(status, collection, accession_path, completeness_dict)

    # Prints if there were any incomplete accessions (the report was made or not).
    date_today = date.today().strftime('%Y-%m-%d')
    completeness_report = os.path.join(input_directory, f"accession_completeness_report_{date_today}.csv")
    if os.path.exists(completeness_report):
        print(f'\nIncomplete accessions found. See {completeness_report}.')
    else:
        print(f'\nAll accessions are complete.')
