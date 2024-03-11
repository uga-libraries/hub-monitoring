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
import os
import sys


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


def update_log(bag_dir, validation_result):
    """Update an accession's preservation log with the bag validation results

    :parameter
    bag_dir (string): the path to an accession bag
    validation_result (Boolean): if an accession bag is valid

    :returns
    None
    """

    # Calculates the path to the preservation_log.txt file, which is in the same directory as the accession bag.
    bag_parent = os.path.dirname(bag_dir)
    log_path = os.path.join(bag_parent, 'preservation_log.txt')

    # Gets the collection and accession numbers from the preservation log.
    # These are the first two columns, the values are the same for every row in the preservation log,
    # and they are formatted differently than the folder names so must be taken from the log.
    with open(log_path, 'r') as open_log:
        last_row = open_log.readlines()[-1].split('\t')
        collection = last_row[0]
        accession = last_row[1]

    # Formats today's date YYYY-MM-DD to include in the log entry for bag validation.
    today = date.today().strftime('%Y-%m-%d')

    # Calculates the action to include in the log entry for bag validation, based on the value of validation_result.
    if validation_result is True:
        action = f'Validated bag for accession {accession}. The bag was valid.'
    else:
        action = f'Validated bag for accession {accession}. The bag was not valid.'

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


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    # Exits the script if there is an error.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Starts a report for all validations in the directory provided as a script argument.
    update_report(['Bag', 'Valid', 'Errors'], directory)

    # Navigates to each accession bag, validates it, and updates the preservation log.
    for root, folders, files in os.walk(directory):
        for folder in folders:
            if folder.endswith('_bag'):
                bag_path = os.path.join(root, folder)
                is_valid, error = validate_bag(bag_path)
                update_log(bag_path, is_valid)
                update_report([folder, is_valid, error], directory)
