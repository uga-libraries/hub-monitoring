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


def manifest_validation_log(acc_dir, acc, errors):
    """Make a CSV file with all validation errors from a single accession

    This is too much information to include in the preservation log.
    The file is saved in the directory with the accessions.

    :parameter
    acc_dir (string): the path to the directory where the report is saved (script argument)
    acc (string): the accession number, used for naming the report
    errors (list): a list of validation errors to include in the report

    :returns
    None
    """

    with open(os.path.join(acc_dir, f'{acc}_manifest_validation_errors.csv'), 'w', newline='', encoding='utf-8') as f:
        f_write = csv.writer(f)
        f_write.writerow(['File', 'MD5', 'MD5_Source'])
        f_write.writerows(errors)


def update_preservation_log(acc_dir, validation_result, validation_type, error_msg=None):
    """Update an accession's preservation log with the bag validation results

    If there is no preservation log, it will print an error and not do the rest of the function.
    The validation result will only be in the fixity_validation.csv, not in the accession folder.

    :parameter
    acc_dir (string): the path to an accession folder, which contains the preservation log
    validation_result (Boolean): if an accession's file fixity is valid
    validation_type (string): bag, bag manifest, or manifest
    error_msg (None or string; optional): included for bag validation so error details can be in the log

    :returns
    None
    """

    # Verifies the preservation log exists.
    # If not, prints an error and does not do the rest of this function.
    log_path = os.path.join(acc_dir, 'preservation_log.txt')
    if not os.path.exists(log_path):
        print(f'\nERROR: accession {os.path.basename(acc_dir)} has no preservation log.')
        return

    # Gets the collection and accession numbers from the preservation log.
    # These are the first two columns, the values are the same for every row in the preservation log,
    # and they are formatted differently than the folder names so must be taken from the log.
    with open(log_path, 'r') as open_log:
        last_row = open_log.readlines()[-1].split('\t')
        collection = last_row[0]
        accession = last_row[1]

    # Formats today's date YYYY-MM-DD to include in the log entry for bag validation.
    today = date.today().strftime('%Y-%m-%d')

    # Calculates the action to include in the log entry for the validation.
    # It includes the type of validation, if it was valid, and any bag validation error.
    if validation_result:
        action = f'Validated {validation_type} for accession {accession}. The {validation_type} is valid.'
    else:
        if validation_type == 'bag':
            if error_msg.startswith('BagError'):
                action = f'Validated bag for accession {accession}. The bag could not be validated.'
            else:
                action = f'Validated bag for accession {accession}. The bag is not valid. {error_msg}'
        elif validation_type == 'bag manifest':
            action = f'Validated bag manifest for accession {accession}. The bag manifest is not valid.'
        else:
            action = f'Validated manifest for accession {accession}. The manifest is not valid.'

    # Reads the contents of preservation_log.txt for checking for legacy formatting.
    with open(log_path) as open_log:
        log_text = open_log.read()

    # Checks if the log starts with the expected column row.
    # If not, prints an error and does not update the log.
    if not log_text.startswith('Collection\tAccession\tDate\tMedia Identifier\tAction\tStaff'):
        print(f'\nERROR: accession {os.path.basename(acc_dir)} has nonstandard columns in the preservation log; '
              f'could not update with validation result.')
        return

    # Adds a row to the end of the preservation log for the bag validation.
    # First adds a line return after existing text, if missing, so the new data is on its own row.
    log_row = [collection, accession, today, None, action, 'validate_fixity.py']
    with open(log_path, 'a', newline='') as open_log:
        if not log_text.endswith('\n'):
            open_log.write('\n')
        log_writer = csv.writer(open_log, delimiter='\t')
        log_writer.writerow(log_row)


def update_report(acc, error_msg, report_dir):
    """Add a line of text to the summary report

    If it doesn't already exist, it makes the report with the header before adding the text.

    :parameter
    acc (string): the folder name of the accession with the error
    error_msg (string): validation error
    report_dir (string): directory where the report is saved (script argument)

    :returns
    None
    """

    report_path = os.path.join(report_dir, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")

    # If the report doesn't already exist, starts a report with a header.
    if not os.path.exists(report_path):
        with open(report_path, 'w', newline='') as open_report:
            report_writer = csv.writer(open_report)
            report_writer.writerow(['Accession', 'Validation_Error'])

    # Adds the error text to the report.
    with open(report_path, 'a', newline='', encoding='utf-8') as open_report:
        report_writer = csv.writer(open_report)
        report_writer.writerow([acc, error_msg])


def validate_bag(bag_dir, report_dir):
    """Validate an accession's bag

    :parameter
    bag_dir (string): the path to an accession bag
    report_dir (string): directory where the report is saved (script argument)

    :returns
    None
    Updates the preservation_log.txt, and if it is not valid also updates the script report
    """

    # The accession number is the name of the bag's parent folder.
    accession_number = os.path.basename(os.path.dirname(bag_dir))

    # Tries to make a bag object, so that bagit library can validate it.
    # There are cases where filenames prevent it from making a bag,
    # in which case it updates the preservation log and script report
    # and also tries to validate the bag using the manifest.
    try:
        new_bag = bagit.Bag(bag_dir)
    except bagit.BagError as errors:
        update_preservation_log(os.path.dirname(bag_dir), False, 'bag', f'BagError: {str(errors)}')
        update_report(accession_number, f'Could not make bag for validation: {str(errors)}', report_dir)
        validate_bag_manifest(bag_dir, report_dir)
        return

    # Validates the bag and updates the preservation log.
    # If there is a validation error, also adds it to the script report.
    try:
        new_bag.validate()
        update_preservation_log(os.path.dirname(bag_dir), True, 'bag')
    except bagit.BagValidationError as errors:
        update_preservation_log(os.path.dirname(bag_dir), False, 'bag', str(errors))
        update_report(accession_number, str(errors), report_dir)


def validate_bag_manifest(bag_dir, report_dir):
    """Validate an accession using the bag manifest if the bagit functionality fails

    Bagit cannot validate a bag if the path is too long.

    :parameter
    bag_dir (string): the path to an accession bag
    report_dir (string): directory where the report is saved (script argument)

    :returns
    None
    Updates the preservation log, and if there are errors updates the report and makes a log
    """

    # Makes a dataframe with the path and MD5 of every file in the data folder of the bag.
    files_list = []
    for root, dirs, files in os.walk(os.path.join(bag_dir, 'data')):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'rb') as f:
                data = f.read()
                md5_generated = hashlib.md5(data).hexdigest()
            files_list.append([filepath, md5_generated])
    df_files = pd.DataFrame(files_list, columns=['Acc_Path', 'Acc_MD5'], dtype=object)

    # Reads the bag manifest into a dataframe.
    # Each row is "MD5  data/path" and does not have a header row.
    df_manifest = pd.read_csv(os.path.join(bag_dir, 'manifest-md5.txt'), delimiter='  data/', engine='python',
                              names=['Bag_MD5', 'Bag_Path'], dtype=object)

    # Merge the two dataframes to compare them.
    df_compare = pd.merge(df_manifest, df_files, how='outer', left_on='Bag_MD5', right_on='Acc_MD5', indicator='Match')

    # Determines if everything matched (values in Match will all be both).
    valid = df_compare['Match'].eq('both').all(axis=0)

    # Updates the preservation log.
    update_preservation_log(os.path.dirname(bag_dir), valid, 'bag manifest')

    # If there were errors, updates the script report and makes a manifest log.
    if not valid:

        # Makes a list of each path, MD5, and source of the MD5 (manifest or file) that did not match.
        error_list = []
        df_left = df_compare[df_compare['Match'] == 'left_only']
        df_left = df_left[['Bag_Path', 'Bag_MD5']]
        df_left['MD5_Source'] = 'Manifest'
        error_list.extend(df_left.values.tolist())
        df_right = df_compare[df_compare['Match'] == 'right_only']
        df_right = df_right[['Acc_Path', 'Acc_MD5']]
        df_right['MD5_Source'] = 'Current'
        error_list.extend(df_right.values.tolist())

        # Adds a summary of the errors to the script report (fixity_validation.csv).
        accession_number = os.path.basename(os.path.dirname(bag_dir))
        update_report(accession_number, f'{len(error_list)} bag manifest errors', report_dir)

        # Makes a log with every file that does not match (acc_manifest_validation_errors.csv).
        manifest_validation_log(report_dir, accession_number, error_list)


def validate_manifest(acc_dir, manifest, report_dir):
    """Validate an accession that has a manifest instead of being bagged

    Accession's with long file paths cannot be bagged.
    They contain a file "initialmanifest_YYYYMMDD.csv" instead.
    Inspired by https://github.com/uga-libraries/verify-md5-KDPmanifests/blob/main/hashverify.py

    :parameter
    acc_dir (string): the path to an accession folder
    manifest (string): the path to the accession manifest file
    report_dir (string): directory where the report is saved (script argument)

    :returns
    None
    Updates the preservation log, and if there are errors updates the report and makes a log
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
            #TODO: temporary to get through testing
            try:
                with open(filepath, 'rb') as f:
                    data = f.read()
                    md5_generated = hashlib.md5(data).hexdigest()
                files_list.append([filepath, md5_generated.upper()])
            except FileNotFoundError:
                print('Cannot get md5 for file in ', acc_dir)
    df_files = pd.DataFrame(files_list, columns=['Acc_Path', 'Acc_MD5'], dtype=object)

    # Reads the manifest into a dataframe.
    df_manifest = pd.read_csv(os.path.join(acc_dir, manifest), dtype=object)

    # Merge the two dataframes to compare them.
    df_compare = pd.merge(df_manifest, df_files, how='outer', left_on='MD5', right_on='Acc_MD5', indicator='Match')

    # Determines if everything matched (values in Match will all be both)
    all_match = df_compare['Match'].eq('both').all(axis=0)

    # Makes a list of the path, MD5, and source of the MD5 (manifest or file) for any that did not match,
    # if there were any that did not match.
    error_list = []
    if not all_match:
        df_left = df_compare[df_compare['Match'] == 'left_only']
        df_left = df_left[['File', 'MD5']]
        df_left['MD5_Source'] = 'Manifest'
        error_list.extend(df_left.values.tolist())
        df_right = df_compare[df_compare['Match'] == 'right_only']
        df_right = df_right[['Acc_Path', 'Acc_MD5']]
        df_right['MD5_Source'] = 'Current'
        error_list.extend(df_right.values.tolist())

    # Compares the number of files in the accession to the number of files in the manifest
    # to detect if the number of duplicate files has changed.
    accession_count = len(df_files.index)
    manifest_count = len(df_manifest.index)
    if accession_count != manifest_count:
        error_list.append([f'Number of files does not match. '
                          f'{accession_count} files in the accession folder and {manifest_count} in the manifest.'])

    # Determines if there were any errors, based on the contents of errors_list.
    valid = len(error_list) == 0

    # Updates the preservation log.
    update_preservation_log(acc_dir, valid, 'manifest')

    # If there are any validation errors, adds a summary of the errors to the script report (fixity_validation.csv)
    # and makes a log with every file that does not match (acc_manifest_validation_errors.csv)
    if not valid:
        accession_number = os.path.basename(acc_dir)
        update_report(accession_number, f'{len(error_list)} manifest errors', report_dir)
        manifest_validation_log(report_dir, accession_number, error_list)


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    # Exits the script if there is an error.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Navigates to each accession, validates it, and updates the preservation log.
    for root, dirs, files in os.walk(directory):
        # Identifies bags based on the folder name ending with "_bag".
        for folder in dirs:
            if folder.endswith('_bag'):
                print(f'Starting on accession {root} (bag)')
                validate_bag(os.path.join(root, folder), directory)
        # Identifies manifests based on the name of the manifest (initialmanifest_date.csv),
        # but only validates if it is not also an accession with a bag.
        # If there are both, the bag folder and initial manifest will be in the same parent folder.
        for file in files:
            if file.startswith('initialmanifest') and len([x for x in dirs if x.endswith("_bag")]) == 0:
                print(f'Starting on accession {root} (manifest)')
                validate_manifest(root, file, directory)

    # Prints if there were any validation errors, based on if the validation log was made or not.
    log = os.path.join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")
    if os.path.exists(log):
        print('\nValidation errors found, see fixity_validation.csv in the directory provided as the script argument.')
    else:
        print('\nNo validation errors.')
