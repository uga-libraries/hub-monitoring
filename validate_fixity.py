"""Validates the fixity for every accession in a directory

Accessions are most commonly in bags, but legacy accessions may have a manifest instead.

Parameter:
    directory (required): the directory that contains the accession folders

Returns:
    Updates the preservation_log.txt of each accession with the result
    Creates a summary report of the validations
"""
import bagit
import csv
from datetime import date
import hashlib
import os
import sys

import pandas as pd


def check_argument(arg_list):
    """Check if the required argument is present and a valid directory

    :parameter
    arg_list (list): the contents of sys.argv after the script is run

    :returns
    dir_path (string, None): string with the path to the folder with accessions to validate, or None if error
    error (string, None): string with the error message, or None if no error
    """

    # Verifies the required argument (directory) is present and a valid path.
    # If the number of arguments is incorrect, dir_path is set to None.
    # If there is no error, error is set to None.
    if len(arg_list) == 1:
        return None, "Missing required argument: directory"
    elif len(arg_list) == 2:
        dir_path = arg_list[1]
        if os.path.exists(dir_path):
            return dir_path, None
        else:
            return None, f"Provided directory '{dir_path}' does not exist"
    else:
        return None, "Too many arguments. Should just have one argument, directory"


def update_preservation_log(acc_dir, validation_result, validation_type):
    """Update an accession's preservation log with the bag validation results

    :parameter
    acc_dir (string): the path to an accession folder, which contains the preservation log
    validation_result (Boolean): if an accession's file fixity is valid
    validation_type (string): bag or manifest

    :returns
    None
    """

    # Gets the collection and accession numbers from the preservation log.
    # These are the first two columns, the values are the same for every row in the preservation log,
    # and they are formatted differently than the folder names so must be taken from the log.
    log_path = os.path.join(acc_dir, 'preservation_log.txt')
    with open(log_path, 'r') as open_log:
        last_row = open_log.readlines()[-1].split('\t')
        collection = last_row[0]
        accession = last_row[1]

    # Formats today's date YYYY-MM-DD to include in the log entry for bag validation.
    today = date.today().strftime('%Y-%m-%d')

    # Calculates the action to include in the log entry for the validation.
    if validation_result:
        action = f'Validated {validation_type} for accession {accession}. The {validation_type} is valid.'
    else:
        action = f'Validated {validation_type} for accession {accession}. The {validation_type} is not valid.'

    # Adds a row to the end of the preservation log for the bag validation.
    log_row = [collection, accession, today, None, action, 'validate_fixity.py']
    with open(log_path, 'a', newline='') as open_log:
        log_writer = csv.writer(open_log, delimiter='\t')
        log_writer.writerow(log_row)


def update_report(text_list, report_dir):
    """Add a line of text (the header or the result of an accession validation) to the summary report

    :parameter
    text_list (list): text for the three columns
    report_dir (string): directory where the report is saved

    :returns
    None
    """

    report_path = os.path.join(report_dir, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")
    with open(report_path, 'a', newline='') as open_report:
        report_writer = csv.writer(open_report)
        report_writer.writerow(text_list)


def validate_bag(bag_dir):
    """Validate an accession's bag

    :parameter
    bag_dir (string): the path to an accession bag

    :returns
    valid (Boolean): True if bag is valid, False if bag is not valid
    error_msg (None, string): None if bag is valid, string with error if bag is not valid
    """

    new_bag = bagit.Bag(bag_dir)
    try:
        new_bag.validate()
        valid = True
        error_msg = None
    except bagit.BagValidationError as errors:
        valid = False
        error_msg = str(errors)
    return valid, error_msg


def validate_manifest(acc_dir, manifest):
    """Validate an accession that has a manifest instead of being bagged

    Accession's with long file paths cannot be bagged.
    They contain a file "initialmanifest_YYYYMMDD.csv" instead.
    Inspired by https://github.com/uga-libraries/verify-md5-KDPmanifests/blob/main/hashverify.py

    :parameter
    acc_dir (string): the path to an accession folder
    manifest (string): the path to the accession manifest file

    :returns
    valid (Boolean): True if the accession matched the manifest, False if the accession did not match the manifest
    error_list (list): Empty list if accession matched the manifest,
                       otherwise a list with the path, md5, and source of any that did not match
    """

    # Gets the path to the folder with the accession's files.
    # The accession folder contains this folder and optionally a folder with FITS XML files.
    acc_files = None
    for item in os.listdir(acc_dir):
        if os.path.isdir(os.path.join(acc_dir, item)) and not item.endswith('FITS'):
            acc_files = os.path.join(acc_dir, item)

    # Makes a dataframe with the path and MD5 of every file in acc_files.
    files_list = []
    for root, dirs, files in os.walk(acc_files):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'rb') as f:
                data = f.read()
                md5_generated = hashlib.md5(data).hexdigest()
            files_list.append([filepath, md5_generated.upper()])
    df_files = pd.DataFrame(files_list, columns=['Acc_Path', 'Acc_MD5'], dtype=object)

    # Reads the manifest into a dataframe.
    df_manifest = pd.read_csv(os.path.join(acc_dir, manifest), dtype=object)

    # Merge the two dataframes to compare them.
    df_compare = pd.merge(df_manifest, df_files, how='outer', left_on='MD5', right_on='Acc_MD5', indicator='Match')

    # Determines if everything matched (values in Match will all be both)
    valid = df_compare['Match'].eq('both').all(axis=0)

    # Makes a list of the path, MD5, and source of the MD5 (manifest or file) for any that did not match,
    # if there were any that did not match.
    error_list = []
    if not valid:
        df_left = df_compare[df_compare['Match'] == 'left_only']
        df_left = df_left[['File', 'MD5']]
        df_left['MD5_Source'] = 'Manifest'
        error_list.extend(df_left.values.tolist())
        df_right = df_compare[df_compare['Match'] == 'right_only']
        df_right = df_right[['Acc_Path', 'Acc_MD5']]
        df_right['MD5_Source'] = 'Current'
        error_list.extend(df_right.values.tolist())

    return valid, error_list


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    # Exits the script if there is an error.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Starts a report for all validations in the directory provided as a script argument.
    update_report(['Accession', 'Valid', 'Errors'], directory)

    # Navigates to each accession, validates it, and updates the preservation log.
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            if folder.endswith('_bag'):
                is_valid, error = validate_bag(os.path.join(root, folder))
                update_preservation_log(root, is_valid, 'bag')
                update_report([folder, is_valid, error], directory)
        for file in files:
            if file.startswith('initialmanifest'):
                is_valid, errors_list = validate_manifest(root, file)
                update_preservation_log(root, is_valid, 'manifest')
                update_report([os.path.basename(root), is_valid, f'{len(errors_list)} errors'], directory)
                # Saves the list of each file with fixity differences.
                if not is_valid:
                    with open(os.path.join(directory, f'{root}_manifest_validation_errors.csv'), 'a', newline='') as f:
                        f_write = csv.writer(f)
                        f_write.writerow(['File', 'MD5', 'MD5_Source'])
                        f_write.writerows(errors_list)
