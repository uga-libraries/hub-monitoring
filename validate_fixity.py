"""Validates the fixity for every accession in a directory

Accessions are most commonly in bags, but legacy accessions may have a manifest instead.
If bagit cannot work with the bag, the bag manifest is used instead.

The preservation_log.txt (in the accession folder) will be updated with the validation result for every accession.
If there are validation errors, they are added to fixity_validation.csv in the input_directory.
If there are validation errors from a manifest, they are also saved to manifest_validation_errors.csv in the input_directory.

Parameter:
    input_directory (required): the directory that contains the accession folders

Returns:
    Updates the preservation_log.txt of each accession with the validation result
    Creates a summary report of the validation errors
    For manifest validation, creates a file report of the validation errors
"""
import bagit
import csv
from datetime import date
import hashlib
import os
import sys

import pandas as pd


def accession_test(bag_name):
    """Determine if a bagged folder within an accession folder is accession content based on the folder name

    Some accession folders also contain bags for other purposes like risk remediation work.

    This is similar to the function accession_test in collection_summary.py,
    but expects the folder name to end in _bag and does not need to evaluate if it is a file.

    @:parameter
    bag_name (string): the name of the bag folder, which will be accession-number_bag if it is an accession

    @:return
    Boolean: True if it is an accession folder and False if not
    """

    # Folder name without "_bag" at the end, which should be an accession number.
    acc_id = bag_name[:-4]

    # Pattern one: ends with -er or -ER.
    if acc_id.lower().endswith('-er'):
        return True
    # Pattern two: ends with _er or _ER.
    elif acc_id.lower().endswith('_er'):
        return True
    # Temporary designation for legacy content while determining an accession number.
    elif acc_id == 'no-acc-num':
        return True
    # Folder that matches none of the patterns for an accession.
    else:
        return False


def check_argument(arg_list):
    """Check if the required argument input_directory is present and a valid directory

    @:parameter
    arg_list (list): the contents of sys.argv after starting the script

    @:returns
    dir_path (string, None): string with the path to the folder with accessions to validate, or None if error
    error (string, None): string with the error message, or None if no error
    """

    # Verifies the required argument (input_directory) is present and a valid path.
    # If the number of arguments is incorrect, dir_path is set to None.
    # If there is no error, error is set to None.
    if len(arg_list) == 1:
        return None, "Missing required argument: input_directory"
    elif len(arg_list) == 2:
        dir_path = arg_list[1]
        if os.path.exists(dir_path):
            return dir_path, None
        else:
            return None, f"Provided input_directory '{dir_path}' does not exist"
    else:
        return None, "Too many arguments. Should just have one argument, input_directory"


def manifest_validation_log(report_dir, acc_id, errors):
    """Make a log with all file validation errors from a single accession

    This is too much information to include in the preservation log.
    The file is saved in the input_directory.

    @:parameter
    report_dir (string): directory where the report is saved (script argument input_directory)
    acc_id (string): the accession number, used for naming the report
    errors (list): a list of validation errors to include in the report

    @:returns
    None
    """

    with open(os.path.join(report_dir, f'{acc_id}_manifest_validation_errors.csv'), 'w', newline='',
              encoding='utf-8') as open_log:
        log_writer = csv.writer(open_log)
        log_writer.writerow(['File', 'MD5', 'MD5_Source'])
        log_writer.writerows(errors)


def manifest_validation_log(report_dir, acc_id, errors):
    """Make a log with all file validation errors from a single accession

    This is too much information to include in the preservation log.
    The file is saved in the input_directory.

    @:parameter
    report_dir (string): directory where the report is saved (script argument input_directory)
    acc_id (string): the accession number, used for naming the report
    errors (list): a list of validation errors to include in the report

    @:returns
    None
    """

    with open(os.path.join(report_dir, f'{acc_id}_manifest_validation_errors.csv'), 'w', newline='',
              encoding='utf-8') as open_log:
        log_writer = csv.writer(open_log)
        log_writer.writerow(['File', 'MD5', 'MD5_Source'])
        log_writer.writerows(errors)


def update_preservation_log(acc_dir, validation_result, validation_type, error_msg=None):
    """Update an accession's preservation log with the validation results

    If there is no preservation log, or it does not have the expected columns,
    it will print an error and not do the rest of the function.
    The validation result will still be in fixity_validation.csv.

    @:parameter
    acc_dir (string): the path to an accession folder, which contains the preservation log
    validation_result (Boolean): if an accession's file fixity is valid
    validation_type (string): bag, bag manifest, or manifest
    error_msg (None or string; optional): included for bag validation so error details can be in the log

    @:returns
    None
    """

    # Verifies the preservation log exists.
    # If not, prints an error and does not do the rest of this function.
    log_path = os.path.join(acc_dir, 'preservation_log.txt')
    if not os.path.exists(log_path):
        print(f'ERROR: accession {os.path.basename(acc_dir)} has no preservation log.\n')
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
                action = f'Validated bag for accession {accession}. The bag could not be validated. {error_msg}'
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
        print(f'ERROR: accession {os.path.basename(acc_dir)} has nonstandard columns in the preservation log; '
              f'could not update with validation result.\n')
        return

    # Adds a row to the end of the preservation log for the bag validation.
    # First adds a line return after existing text, if missing, so the new data is on its own row.
    log_row = [collection, accession, today, None, action, 'validate_fixity.py']
    with open(log_path, 'a', newline='') as open_log:
        if not log_text.endswith('\n'):
            open_log.write('\n')
        log_writer = csv.writer(open_log, delimiter='\t')
        log_writer.writerow(log_row)


def update_report(acc_dir, error_msg, report_dir):
    """Add a line of text to the report fixity_validation.csv

    The report lists every accession that did not validate with the validation error information.
    If it doesn't already exist, it makes the report with the header before adding the text.

    @:parameter
    acc_dir (string): the path to an accession folder, which may be a bag
    error_msg (string): validation error
    report_dir (string): directory where the report is saved (script argument input_directory)

    @:returns
    None
    """

    # Parse status (backlogged or closed), collection, and accession from acc_dir.
    # If it is a bag, the acc_dir is root/status/collection/accession/accession_bag
    # and if it is a manifest, the acc_dir is root/status/collection/accession
    acc_dir_list = acc_dir.split('\\')
    if acc_dir.endswith('_bag'):
        status = acc_dir_list[-4]
        collection = acc_dir_list[-3]
        accession = acc_dir_list[-2]
    else:
        status = acc_dir_list[-3]
        collection = acc_dir_list[-2]
        accession = acc_dir_list[-1]

    # If the report doesn't already exist, starts a report with a header.
    report_path = os.path.join(report_dir, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")
    if not os.path.exists(report_path):
        with open(report_path, 'w', newline='') as open_report:
            report_writer = csv.writer(open_report)
            report_writer.writerow(['Status', 'Collection', 'Accession', 'Validation_Error'])

    # Adds the error text to the report.
    with open(report_path, 'a', newline='', encoding='utf-8') as open_report:
        report_writer = csv.writer(open_report)
        report_writer.writerow([status, collection, accession, error_msg])


def validate_bag(bag_dir, report_dir):
    """Validate an accession's bag with bagit and log the results

    @:parameter
    bag_dir (string): the path to an accession's bag
    report_dir (string): directory where the report is saved (script argument input_directory)

    @:returns
    None
    """

    # Tries to make a bag object, so that bagit library can validate it.
    # There are cases where filenames prevent it from making a bag,
    # in which case it updates the preservation log and script report
    # and also tries to validate the bag using the manifest.
    try:
        new_bag = bagit.Bag(bag_dir)
    except bagit.BagError as errors:
        update_preservation_log(os.path.dirname(bag_dir), False, 'bag', f'BagError: {str(errors)}')
        update_report(bag_dir, f'Could not make bag for validation: {str(errors)}', report_dir)
        validate_bag_manifest(bag_dir, report_dir)
        return

    # Validates the bag and updates the preservation log.
    # If there is a validation error, also adds it to the script report.
    try:
        new_bag.validate()
        update_preservation_log(os.path.dirname(bag_dir), True, 'bag')
    except bagit.BagValidationError as errors:
        update_preservation_log(os.path.dirname(bag_dir), False, 'bag', str(errors))
        update_report(bag_dir, str(errors), report_dir)


def validate_bag_manifest(bag_dir, report_dir):
    """Validate an accession with the bag manifest and log the results

    Used if the accession cannot be validated using bagit, which happens if the path is too long.

    @:parameter
    bag_dir (string): the path to an accession's bag
    report_dir (string): directory where the report is saved (script argument input_directory)

    @:returns
    None
    """

    # Makes a dataframe with the path and MD5 of every file in the data folder of the bag.
    files_list = []
    for root, dirs, files in os.walk(os.path.join(bag_dir, 'data')):
        for file in files:
            filepath = os.path.join(root, file)
            # If the file path is too long, it causes a FileNotFoundError and cannot calculate the MD5.
            try:
                with open(filepath, 'rb') as open_file:
                    data = open_file.read()
                    md5_generated = hashlib.md5(data).hexdigest()
                files_list.append([filepath, md5_generated])
            except FileNotFoundError:
                files_list.append([filepath, 'FileNotFoundError-cannot-calculate-md5'])
    df_files = pd.DataFrame(files_list, columns=['Acc_Path', 'Acc_MD5'], dtype=object)

    # Reads the bag manifest into a dataframe.
    # Each row is "MD5  data/path" and does not have a header row.
    df_manifest = pd.read_csv(os.path.join(bag_dir, 'manifest-md5.txt'), delimiter='  data/', engine='python',
                              names=['Bag_MD5', 'Bag_Path'], dtype=object)

    # Merge the two dataframes to compare them.
    df_compare = pd.merge(df_manifest, df_files, how='outer', left_on='Bag_MD5', right_on='Acc_MD5', indicator='Match')

    # Determines if everything matched (values in Match will all be both).
    all_match = df_compare['Match'].eq('both').all(axis=0)

    # Updates the preservation log.
    update_preservation_log(os.path.dirname(bag_dir), all_match, 'bag manifest')

    # If there were no errors, updates the script report to show the earlier bag error is resolved.
    # If there were errors, updates the script report with the error count and makes a manifest log.
    if all_match:
        update_report(bag_dir, 'Validated with bag manifest instead of bagit. The bag manifest is valid.', report_dir)
    else:

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
        update_report(bag_dir, f'{len(error_list)} bag manifest errors', report_dir)

        # Makes a log with every file that does not match (acc_manifest_validation_errors.csv).
        accession_number = os.path.basename(os.path.dirname(bag_dir))
        manifest_validation_log(report_dir, accession_number, error_list)


def validate_manifest(acc_dir, manifest, report_dir):
    """Validate an accession with an initial manifest and log the results

    Accession's with long file paths cannot be bagged.
    They contain a file "initialmanifest_YYYYMMDD.csv" instead.
    Inspired by https://github.com/uga-libraries/verify-md5-KDPmanifests/blob/main/hashverify.py

    @:parameter
    acc_dir (string): the path to an accession folder
    manifest (string): the path to the accession's manifest file
    report_dir (string): directory where the report is saved (script argument input_directory)

    @:returns
    None
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
            # If the file path is too long, it causes a FileNotFoundError and cannot calculate the MD5.
            try:
                with open(filepath, 'rb') as open_file:
                    data = open_file.read()
                    md5_generated = hashlib.md5(data).hexdigest()
                files_list.append([filepath, md5_generated.upper()])
            except FileNotFoundError:
                files_list.append([filepath, 'FileNotFoundError-cannot-calculate-md5'])
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
        update_report(acc_dir, f'{len(error_list)} manifest errors', report_dir)
        accession_number = os.path.basename(acc_dir)
        manifest_validation_log(report_dir, accession_number, error_list)


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    # Exits the script if there is an error.
    input_directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Navigates to each accession, validates it, and updates the preservation log.
    for root, dirs, files in os.walk(input_directory):
        # Identifies bags based on the folder name ending with "_bag" and starting with an accession number.
        for folder in dirs:
            if folder.endswith('_bag') and accession_test(folder):
                print(f'Starting on accession {root} (bag)')
                validate_bag(os.path.join(root, folder), input_directory)
        # Identifies manifests based on the name of the manifest (initialmanifest_date.csv),
        # but only validates if it is not also an accession with a bag.
        # If there are both, the bag folder and initial manifest will be in the same parent folder.
        for file in files:
            if file.startswith('initialmanifest') and len([x for x in dirs if x.endswith("_bag")]) == 0:
                print(f'Starting on accession {root} (manifest)')
                validate_manifest(root, file, input_directory)

    # Prints if there were any validation errors, based on if the validation log was made or not.
    log = os.path.join(input_directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")
    if os.path.exists(log):
        print('\nValidation errors found, see fixity_validation.csv in the directory provided as the script argument.')
    else:
        print('\nNo validation errors.')
