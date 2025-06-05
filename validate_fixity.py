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
from datetime import date, datetime
import hashlib
import os
import sys

import pandas as pd


def accession_test(folder_name):
    """Determine if a folder name is an accession number

    This is similar to the function accession_test in collection_summary.py,
    but does not need to evaluate if it is a file.

    @:parameter
    folder_name (string): the name of a folder to be checked for accession number formatting

    @:return
    Boolean: True if it is an accession number and False if not
    """

    # Pattern one: ends with -er or -ER.
    if folder_name.lower().endswith('-er'):
        return True
    # Pattern two: ends with _er or _ER.
    elif folder_name.lower().endswith('_er'):
        return True
    # Temporary designation for legacy content while determining an accession number.
    elif folder_name == 'no-acc-num':
        return True
    # Folder that matches none of the patterns for an accession.
    else:
        return False


def check_argument(arg_list):
    """Check if the required argument input_directory is present and a valid directory with the expected name

    @:parameter
    arg_list (list): the contents of sys.argv after starting the script

    @:returns
    dir_path (string, None): string with the path to the folder with accessions to validate, or None if error
    error (string, None): string with the error message, or None if no error
    """

    # Verifies the required argument (input_directory) is present
    # and a valid path with the expected name (Born-digital or born-digital).
    # If there is an error, dir_path is set to None. If there is no error, error is set to None.
    if len(arg_list) == 1:
        return None, "Missing required argument: input_directory"
    elif len(arg_list) == 2:
        dir_path = arg_list[1]
        if os.path.exists(dir_path):
            if os.path.basename(dir_path).lower() == 'born-digital':
                return dir_path, None
            else:
                return None, f"Provided input_directory '{dir_path}' is not to folder 'Born-digital' or 'born-digital'"
        else:
            return None, f"Provided input_directory '{dir_path}' does not exist"
    else:
        return None, "Too many arguments. Should just have one argument, input_directory"


def check_restart(acc_dir):
    """Determine if the script has restarted based on if the fixity validation log is present

    The log name includes the date, so the path cannot be predicted.

    @:parameter
    acc_dir (string): directory where the log would be saved (script argument input_directory)

    @:returns
    log_path (string, None): path to the log, if it is present, or None if it is not present
    """

    log_path = None
    for item in os.listdir(acc_dir):
        if os.path.isfile(os.path.join(acc_dir, item)) and item.startswith('fixity_validation_log'):
            log_path = os.path.join(acc_dir, item)
    return log_path


def fixity_validation_log(acc_dir):
    """Make a log for fixity validation with every folder at the accession level in the input_directory

    Status is backlogged or closed (name of folder at first level within input_directory).
    Collection is an identifier and potentially the name (name of folder at second level within input_directory).
    Accession is an identifier OR a non-accession folder (name of folder at third level within input_directory).
    Accession_Path is the full path to the folder which contains the digital content.
    Fixity_Type is Bag or Zip and will be used to determine how to validate the accession, or None.
    Fixity is the name of the bag folder or zip md5 file with the fixity information, or None.
    Pres_Log is None for all, and is for errors encountered updating the preservation log during validation.
    Valid is None or has text if Result also has text.
    Valid_Time is None for all, and is for the time that validation finishes.
    Result is None for accessions to validate, "Not an accession", or "No fixity".

    There are other folders frequently at the accession level, such as FITS files and copies for appraisal.
    Everything at this level is included in the log so the archivist can verify
    they are not accessions that did not follow naming conventions.

    @:parameter
    acc_dir (string): directory with the accessions and where the log is saved (script argument input_directory)

    @:returns
    None
    """

    # Makes the fixity validation log csv with a header in the input_directory.
    log_path = os.path.join(acc_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv")
    with (open(log_path, 'w', newline='') as open_log):
        log_writer = csv.writer(open_log)
        log_writer.writerow(['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                             'Pres_Log', 'Valid', 'Valid_Time', 'Result'])

        # Navigates the input_directory to get information about each folder at the accession level and adds to the log.
        for status in os.listdir(acc_dir):
            # There are sometimes additional folders at the status level, which never contain accessions to validate.
            if status == 'backlogged' or status == 'closed' and os.path.isdir(os.path.join(acc_dir, status)):
                # Every folder at the collection level is included.
                for collection in os.listdir(os.path.join(acc_dir, status)):
                    # Every folder at the accession level is included but has text in Result
                    # if it is not identified as an accession to be validated.
                    if os.path.isdir(os.path.join(acc_dir, status, collection)):
                        for folder in os.listdir(os.path.join(acc_dir, status, collection)):
                            accession_path = os.path.join(acc_dir, status, collection, folder)
                            if os.path.isdir(accession_path):
                                is_accession = accession_test(folder)
                                if is_accession:
                                    if os.path.exists(os.path.join(accession_path, f'{folder}_bag')):
                                        fixity_type = 'Bag'
                                        fixity = f'{folder}_bag'
                                        is_valid = None
                                        result = None
                                    elif os.path.exists(os.path.join(accession_path, f'{folder}_zip_md5.txt')):
                                        fixity_type = 'Zip'
                                        fixity = f'{folder}_zip_md5.txt'
                                        is_valid = None
                                        result = None
                                    else:
                                        fixity_type = None
                                        fixity = None
                                        is_valid = 'False'
                                        result = 'No fixity information'
                                else:
                                    fixity_type = None
                                    fixity = None
                                    is_valid = 'Skipped'
                                    result = 'Not an accession'
                                # Adds information for folder to the log.
                                row = [status, collection, folder, accession_path, fixity_type, fixity,
                                       None, is_valid, None, result]
                                log_writer.writerow(row)


def update_preservation_log(acc_dir, validation_result, validation_type, error_msg=None):
    """Update an accession's preservation log with the validation results

    If there is no preservation log, or it does not have the expected columns,
    it will print an error and not do the rest of the function.
    The validation result will still be in fixity_validation.csv.

    @:parameter
    acc_dir (string): the path to an accession folder, which contains the preservation log
    validation_result (Boolean): if an accession's file fixity is valid
    validation_type (string): bag, bag manifest, or zip md5
    error_msg (None or string; optional): included if there are additional error details to add to the log

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
        collection_id = last_row[0]
        accession_id = last_row[1]

    # Calculates the action to include in the log entry for the validation.
    # It includes the type of validation, if it was valid, and any additional error message.
    if validation_result:
        action = f'Validated {validation_type} for accession {accession_id}. The {validation_type} is valid.'
    else:
        if validation_type == 'bag':
            if error_msg.startswith('BagError'):
                action = f'Validated bag for accession {accession_id}. The bag could not be validated. {error_msg}'
            else:
                action = f'Validated bag for accession {accession_id}. The bag is not valid. {error_msg}'
        elif validation_type == 'bag manifest':
            action = f'Validated bag manifest for accession {accession_id}. The bag manifest is not valid.'
        else:
            action = f'Validated zip md5 for accession {accession_id}. The zip is not valid. {error_msg}'

    # Reads the contents of preservation_log.txt for checking for legacy formatting.
    with open(log_path) as open_log:
        log_text = open_log.read()

    # Checks if the log starts with the expected column row.
    # If not, prints an error and does not update the log.
    if not log_text.startswith('Collection\tAccession\tDate\tMedia Identifier\tAction\tStaff'):
        print(f'ERROR: accession {os.path.basename(acc_dir)} has nonstandard columns in the preservation log; '
              f'could not update with validation result.\n')
        return

    # Adds a row to the end of the preservation log for the accession validation.
    # First adds a line return after existing text, if missing, so the new data is on its own row.
    validation_date = date.today().strftime('%Y-%m-%d')
    log_row = [collection_id, accession_id, validation_date, None, action, 'validate_fixity.py']
    with open(log_path, 'a', newline='') as open_log:
        if not log_text.endswith('\n'):
            open_log.write('\n')
        log_writer = csv.writer(open_log, delimiter='\t')
        log_writer.writerow(log_row)


def update_fixity_validation_log(log_path, df, row, result):
    """Add the validation result for an accession to the fixity validation log dataframe and csv

    @:parameter
    log_path (string): the path to the fixity_validation_log.csv
    df (dataframe): the dataframe with the current fixity validation log information
    row (dataframe index): the dataframe index number of the accession
    result (string): the validation error or "Valid"
    report_dir (string): directory where the report is saved (script argument input_directory)

    @:returns
    None
    """

    # Adds validation result to Result column.
    df.loc[row, 'Result'] = result

    # Determines if valid, based on result, and adds to Valid column.
    # Rows skipped for not being an accession already have a value in this column.
    if result.startswith('Valid'):
        is_valid = True
    else:
        is_valid = False
    df.loc[row, 'Valid'] = is_valid

    # Adds the time of validation (using the current time, when the log is updated just after validation) to log.
    # This is used to update preservation logs if they had formatting errors and for stats on this process.
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    df.loc[row, 'Valid_Time'] = timestamp

    # Saves the updated information to fixity_validation_log.csv, so if the script breaks,
    # the information is correct for all accessions prior to the break.
    df.to_csv(log_path, index=False)


def validate_bag(bag_dir, report_dir):
    """Validate an accession's bag with bagit and log the results

    @:parameter
    bag_dir (string): the path to an accession's bag
    report_dir (string): directory where the report is saved (script argument input_directory)

    @:returns
    validation_result (string): the validation error, "Valid", or "Valid (bag manifest)"
    """

    # Tries to make a bag object, so that bagit library can validate it.
    # There are cases where filenames prevent it from making a bag,
    # in which case it updates the preservation log and script report
    # and also tries to validate the bag using the manifest.
    try:
        new_bag = bagit.Bag(bag_dir)
    except bagit.BagError as errors:
        try:
            update_preservation_log(os.path.dirname(bag_dir), False, 'bag', f'BagError: {str(errors)}')
        except IndexError:
            print("Cannot update preservation log: nonstandard delimiter")
        validation_result = validate_bag_manifest(bag_dir, report_dir)
        return validation_result

    # Validates the bag and updates the preservation log.
    # If there is a validation error, also adds it to the script report.
    try:
        new_bag.validate()
        try:
            update_preservation_log(os.path.dirname(bag_dir), True, 'bag')
        except IndexError:
            print("Cannot update preservation log: nonstandard delimiter")
        return "Valid"
    except bagit.BagValidationError as errors:
        try:
            update_preservation_log(os.path.dirname(bag_dir), False, 'bag', str(errors))
        except IndexError:
            print("Cannot update preservation log: nonstandard delimiter")
        return str(errors)


def validate_bag_manifest(bag_dir, report_dir):
    """Validate an accession with the bag manifest and return the result for the logs

    Used if the accession cannot be validated using bagit, which happens if the path is too long.

    @:parameter
    bag_dir (string): the path to an accession's bag
    report_dir (string): directory where the report is saved (script argument input_directory)

    @:returns
    validation_result (string): "Valid (bag manifest)" or the number of errors
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

    # Returns the validation result, either the number of errors or "Valid".
    # If there were errors, also saves the path, MD5, and source of the MD5 (manifest or file) that did not match
    # to a log in the input_directory.
    if all_match:
        validation_result = 'Valid (bag manifest - could not validate with bagit)'
    else:
        error_list = []
        df_left = df_compare[df_compare['Match'] == 'left_only']
        df_left = df_left[['Bag_Path', 'Bag_MD5']]
        df_left['MD5_Source'] = 'Manifest'
        error_list.extend(df_left.values.tolist())
        df_right = df_compare[df_compare['Match'] == 'right_only']
        df_right = df_right[['Acc_Path', 'Acc_MD5']]
        df_right['MD5_Source'] = 'Current'
        error_list.extend(df_right.values.tolist())
        accession_number = os.path.basename(os.path.dirname(bag_dir))
        with open(os.path.join(report_dir, f'{accession_number}_manifest_validation_errors.csv'), 'w', newline='',
                  encoding='utf-8') as open_log:
            log_writer = csv.writer(open_log)
            log_writer.writerow(['File', 'MD5', 'MD5_Source'])
            log_writer.writerows(error_list)
        validation_result = f'Could not validate with bagit. Bag manifest not valid: {len(error_list)} errors'
    return validation_result


def validate_zip(acc_dir, zip_md5):
    """Validate a zipped accession with a zip md5 text file and return the result for the logs

    Accession's with long file paths cannot be bagged.
    They are zipped and have a file accession-id_zip_md5.txt with the zip MD5 instead.

    @:parameter
    acc_dir (string): the path to an accession folder
    zip_md5 (string): the name of the file in the accession folder

    @:returns
    validation_result (string): "Valid" or how the fixity changed
    """

    # Reads the expected MD5 from the zip_md5 text file.
    # The file has one row, with text formatted MD5<space><space>Zip_Path (md5deep output)
    zip_md5_path = os.path.join(acc_dir, zip_md5)
    with open(zip_md5_path) as open_file:
        text = open_file.read()
        expected_md5 = text.split(' ')[0]

    # Calculates the current MD5 of the accession zip file.
    # The file is named accession-id.zip
    acc_zip_path = os.path.join(acc_dir, f'{os.path.basename(acc_dir)}.zip')
    with open(acc_zip_path, 'rb') as open_file:
        data = open_file.read()
        current_md5 = hashlib.md5(data).hexdigest()

    # Returns the validation result, which is used to update the preservation log and fixity validation log.
    # The accession is valid if the MD5s are identical.
    if expected_md5 == current_md5:
        validation_result = 'Valid'
    else:
        validation_result = f'Fixity changed from {expected_md5} to {current_md5}.'
    return validation_result


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    # Exits the script if there is an error.
    input_directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Makes the fixity_validation_log.csv, if it does not exist, with accession folders to check.
    # If it already exists, it means the script is being restarted and will use the log to restart where it left off.
    fixity_validation_log_path = check_restart(input_directory)
    if not fixity_validation_log_path:
        fixity_validation_log(input_directory)
        today = date.today().strftime('%Y-%m-%d')
        fixity_validation_log_path = os.path.join(input_directory, f'fixity_validation_log_{today}.csv')

    # Validates every accession in the log that has not yet been validated (Result is blank).
    log_df = pd.read_csv(fixity_validation_log_path)
    for accession in log_df[log_df['Result'].isnull()].itertuples():

        # Prints the script progress.
        print(f'Starting on accession {accession.Accession_Path} ({accession.Fixity_Type})')

        # Calculates the row index in the dataframe for the accession, to use for adding the validation result.
        df_row_index = log_df.index[log_df['Accession'] == accession.Accession].tolist()[0]

        # Validates the accession, including updating the preservation log and fixity validation log.
        # Different validation functions are used depending on if it is in a bag or is zipped.
        if accession.Fixity_Type == 'Bag':
            valid = validate_bag(os.path.join(accession.Accession_Path, accession.Fixity), input_directory)
            update_fixity_validation_log(fixity_validation_log_path, log_df, df_row_index, valid)
        else:
            valid = validate_zip(accession.Accession_Path, accession.Fixity)
            update_fixity_validation_log(fixity_validation_log_path, log_df, df_row_index, valid)

    # Prints if there were any validation errors, based on the Result column.
    error_df = log_df.loc[~log_df['Result'].isin(['Valid', 'Valid (bag manifest)', 'Not an accession'])]
    if error_df.empty:
        print('\nNo validation errors.')
    else:
        print('\nValidation errors found, see fixity_validation_log.csv in the input_directory.')
