"""Validates the fixity for every accession in a directory

Accessions are most commonly in bags, but legacy accessions may be zipped instead.
Bags may be named accession_bag or accession_zipped_bag (contents are zipped because they cannot be bagged otherwise; bag is not zipped)
If bagit cannot run on bag (generally a path length problem), the bag manifest is used instead.

The preservation log (in the accession folder) will be updated with the validation result for every accession
and a fixity validation log tracks the validation process.
If there are validation errors from a bag manifest, they are also saved to a log in the input_directory,
as it is too much information to put in the fixity validation log.

Parameter:
    input_directory (required): the directory that contains the accession folders,
                                structured born-digital/status/collection/accession

Returns:
    Updates the preservation log of each accession with the validation result
    Creates a summary report of the validation errors (fixity validation log)
"""
import bagit
import csv
from datetime import date, datetime
import hashlib
import os
import pandas as pd
import sys


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
    Path is the full path to the folder which contains the digital content (bag or zip) and preservation metadata.
    Fixity_Type is Bag or Zip and will be used to determine how to validate the accession, or None.
    Pres_Log is None for all, and is for errors encountered updating the preservation log during validation.
    Valid is None or has text if Result also has text.
    Valid_Time is None for all, and is for the time that validation finishes.
    Result is None for accessions to validate, "Not an accession", or "No fixity".

    There are other folders frequently at the accession level, such as FITS files and copies for appraisal.
    Everything at this level is included in the log so the archivist can verify they are not accessions.
    This gives us confidence that we didn't miss any accessions with naming errors.

    @:parameter
    acc_dir (string): directory with the accessions and where the log is saved (script argument input_directory)

    @:returns
    None
    """

    # Makes the fixity validation log with a header in the input_directory.
    log_path = os.path.join(acc_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv")
    header = ['Status', 'Collection', 'Accession', 'Path', 'Fixity_Type', 'Pres_Log', 'Valid', 'Valid_Time', 'Result']
    with open(log_path, 'w', newline='') as open_log:
        log_writer = csv.writer(open_log)
        log_writer.writerow(header)

        # Navigates the input_directory to get information about each folder at the accession level and adds to the log.
        for status in os.listdir(acc_dir):
            # There may be other folders at the status level that don't need to be checked
            # or files which cause an error from os.listdir(status).
            if status == 'backlogged' or status == 'closed' and os.path.isdir(os.path.join(acc_dir, status)):
                # Every folder at the collection level is included.
                for collection in os.listdir(os.path.join(acc_dir, status)):
                    # Every folder (not file) at the accession level is included but has text in Result
                    # if it is not identified as an accession, so it is skipped during validation.
                    if os.path.isdir(os.path.join(acc_dir, status, collection)):
                        # Folder is the accession number for those that are accessions.
                        for folder in os.listdir(os.path.join(acc_dir, status, collection)):
                            folder_path = os.path.join(acc_dir, status, collection, folder)
                            if os.path.isdir(folder_path):
                                is_accession = accession_test(folder)
                                # Gets information for log besides the iterators (status, collection, folder/accession).
                                if is_accession:
                                    if os.path.exists(os.path.join(folder_path, f'{folder}_bag')):
                                        fixity_type = 'Bag'
                                        is_valid = None
                                        result = None
                                    elif os.path.exists(os.path.join(folder_path, f'{folder}_zipped_bag')):
                                        fixity_type = 'Zipped_Bag'
                                        is_valid = None
                                        result = None
                                    elif os.path.exists(os.path.join(folder_path, f'{folder}_zip_md5.txt')):
                                        fixity_type = 'Zip'
                                        is_valid = None
                                        result = None
                                    else:
                                        fixity_type = None
                                        is_valid = 'False'
                                        result = 'No fixity information'
                                else:
                                    fixity_type = None
                                    is_valid = 'Skipped'
                                    result = 'Not an accession'
                                # Adds information for folder, regardless of if it is an accession, to the log.
                                row = [status, collection, folder, folder_path, fixity_type, None, is_valid, None, result]
                                log_writer.writerow(row)


def update_fixity_validation_log(log_path, df, row, pres_log, validation_result):
    """Add the validation result for an accession to the fixity validation log dataframe and csv

    @:parameter
    log_path (string): the path to the fixity validation log
    df (dataframe): the dataframe with the current fixity validation log information
    row (dataframe index): the dataframe index number of the accession
    pres_log(string): the status of the preservation log, "Updated" or an error message
    validation_result (string): the validation error or "Valid"

    @:returns
    None
    """

    # Adds validation result to the Result column.
    df.loc[row, 'Result'] = validation_result

    # If the validation result is "Path Error", no other information is included in the log.
    # This happens from running the script on the server and means it must be done over the network.
    # This is a placeholder in the validation log, so it can be restarted on the server without retrying,
    # but then easily deleted, so they can be retried over the network.
    if validation_result == 'Path Error':
        df.to_csv(log_path, index=False)
        return

    # Adds preservation log status to the Pres_Log column.
    df.loc[row, 'Pres_Log'] = pres_log

    # Determines if the fixity is valid, based on validation result, and adds to the Valid column.
    if validation_result.startswith('Valid'):
        is_valid = True
    else:
        is_valid = False
    df.loc[row, 'Valid'] = is_valid

    # Adds the time of validation to the "Valid_Type" column.
    # This is used to update preservation logs if they had formatting errors and for stats on this process.
    df.loc[row, 'Valid_Time'] = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Saves the updated information to fixity validation log, so if the script breaks,
    # the information is correct for all accessions validated prior to then.
    df.to_csv(log_path, index=False)


def update_preservation_log(acc_dir, validation_result, fixity_type):
    """Update an accession's preservation log with the validation results and return a status for the validation log

    Preservation log status is to have a record in the fixity validation log if there were problems updating the log,
    so that the archivist can address. This happens if the log is missing or has legacy formatting.

    @:parameter
    acc_dir (string): the path to an accession folder, which contains the preservation log
    validation_result (string): information returned from the validation function for the fixity type
    fixity_type (string): bag, bag manifest, or zip md5

    @:returns
    String: "Updated" or why it did not update
    """

    # Verifies the preservation log exists.
    # If not, returns the status for the fixity validation log and does not do the rest of this function.
    log_path = os.path.join(acc_dir, 'preservation_log.txt')
    if not os.path.exists(log_path):
        return 'Log path not found'

    # Checks if the log starts with the expected column header row.
    # If yes, gets the ids from the first two columns of the last row, so the id formatting in the log is consistent.
    # If not, or the last row is blank (IndexError), returns the status for the fixity validation log
    # and does not do the rest of the function. The preservation log will be updated manually.
    with open(log_path, 'r') as open_log:
        log_lines = open_log.readlines()
        first_row = log_lines[0]
        if not first_row == 'Collection\tAccession\tDate\tMedia Identifier\tAction\tStaff\n':
            return 'Nonstandard columns'
        try:
            last_row_list = log_lines[-1].split('\t')
            collection_id = last_row_list[0]
            accession_id = last_row_list[1]
        except IndexError:
            return 'Extra blank row'

    # Calculates the action to include in the log entry for the validation.
    # It includes the type of validation, if it was valid, and any additional error message.
    if validation_result == 'Valid':
        action = f'Validated {fixity_type.lower()} for accession {accession_id}. The {fixity_type.lower()} is valid.'
    elif validation_result.startswith('Valid (bag manifest'):
        action = f'Validated bag for accession {accession_id}. {validation_result}'
    else:
        if fixity_type == 'Bag':
            action = f'Validated bag for accession {accession_id}. The bag is not valid. {validation_result}'
        else:
            action = f'Validated zip md5 for accession {accession_id}. The zip is not valid. {validation_result}'

    # Adds a row to the end of the preservation log for the accession validation.
    # First adds a line return after existing text, if missing, so the new data is on its own row.
    validation_date = date.today().strftime('%Y-%m-%d')
    log_row = [collection_id, accession_id, validation_date, None, action, 'validate_fixity.py']
    with open(log_path, 'a', newline='') as open_log:
        if not log_lines[-1].endswith('\n'):
            open_log.write('\n')
        log_writer = csv.writer(open_log, delimiter='\t')
        log_writer.writerow(log_row)
    return 'Updated'


def validate_bag(acc_dir, report_dir, bag_name):
    """Validate an accession's bag with bagit and return the result for the logs

    @:parameter
    acc_dir (string): the path to an accession folder
    report_dir (string): directory where the report is saved (script argument input_directory)
    bag_name (string): the folder name of the bag, either acc_bag or acc_zipped_bag

    @:returns
    validation_result (string): "Valid", "Valid (bag manifest - ...)", or an error message
    """

    # Tries to make a bag object, so that bagit library can validate it.
    # There are cases where filenames or path length prevent it from making a bag,
    # in which case it tries to validate the bag using the manifest.
    try:
        new_bag = bagit.Bag(os.path.join(acc_dir, bag_name))
    except bagit.BagError:
        validation_result = validate_bag_manifest(acc_dir, report_dir, bag_name)
        return validation_result

    # If the bag object was made, validates the bag and returns the validation result,
    # which is used to update the preservation log and fixity validation log.
    # FileNotFoundError happens when running remotely on the server but the path will be found if run over the network.
    try:
        new_bag.validate()
        validation_result = 'Valid'
    except bagit.BagValidationError as errors:
        validation_result = str(errors)
    except FileNotFoundError:
        validation_result = 'Path Error'
    return validation_result


def validate_bag_manifest(acc_dir, report_dir, bag_name):
    """Validate an accession with the bag manifest and return the result for the logs

    Used if the accession cannot be validated using bagit, which happens if the path is too long.

    @:parameter
    acc_dir (string): the path to an accession folder
    report_dir (string): directory where the report is saved (script argument input_directory)
    bag_name (string): the folder name of the bag, either acc_bag or acc_zipped_bag

    @:returns
    validation_result (string): "Valid (bag manifest - ...)" or the number of errors
    """

    # Makes a dataframe with the path and MD5 of every file in the data folder of the bag.
    files_list = []
    for root, dirs, files in os.walk(os.path.join(acc_dir, bag_name, 'data')):
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
    # Each row is "MD5  data/path" and the file does not have a header row.
    df_manifest = pd.read_csv(os.path.join(acc_dir, bag_name, 'manifest-md5.txt'),
                              delimiter='  data/', engine='python', names=['Bag_MD5', 'Bag_Path'], dtype=object)

    # Merge the two dataframes to compare them.
    df_compare = pd.merge(df_manifest, df_files, how='outer', left_on='Bag_MD5', right_on='Acc_MD5', indicator='Match')

    # Determines if everything matched (values in Match will all be both).
    all_match = df_compare['Match'].eq('both').all(axis=0)

    # Returns the validation result, either the number of errors or "Valid",
    # which is used to update the preservation log and fixity validation log.
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
        accession_number = os.path.basename(os.path.basename(acc_dir))
        with open(os.path.join(report_dir, f'{accession_number}_manifest_validation_errors.csv'), 'w', newline='',
                  encoding='utf-8') as open_log:
            log_writer = csv.writer(open_log)
            log_writer.writerow(['File', 'MD5', 'MD5_Source'])
            log_writer.writerows(error_list)
        validation_result = f'Could not validate with bagit. Bag manifest not valid: {len(error_list)} errors'
    return validation_result


def validate_zip(acc_dir):
    """Validate a zipped accession with a zip md5 text file and return the result for the logs

    Accessions with long file paths cannot be bagged.
    They are zipped and have a file accession-id_zip_md5.txt with the zip MD5 instead.

    @:parameter
    acc_dir (string): the path to an accession folder

    @:returns
    validation_result (string): "Valid" or how the fixity changed
    """

    # Reads the expected MD5 from the zip_md5 text file.
    # The file has one row, with text formatted MD5<space><space>Zip_Path (md5deep output)
    zip_md5_path = os.path.join(acc_dir, f'{os.path.basename(acc_dir)}_zip_md5.txt')
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

    # Makes the fixity validation log, if it does not exist, with all folders at the accession level of the directory.
    # If the log already exists, it means the script was restarted and will use that log to restart where it left off.
    fixity_validation_log_path = check_restart(input_directory)
    if not fixity_validation_log_path:
        fixity_validation_log(input_directory)
        today = date.today().strftime('%Y-%m-%d')
        fixity_validation_log_path = os.path.join(input_directory, f'fixity_validation_log_{today}.csv')

    # Validates every accession in the log that has not yet been validated (Result is blank).
    log_df = pd.read_csv(fixity_validation_log_path)
    for acc in log_df[log_df['Result'].isnull()].itertuples():

        # Prints the script progress.
        print(f'Starting on accession {acc.Path} ({acc.Fixity_Type})')

        # Calculates the row index in the fixity validation log dataframe for the accession for updating the log.
        # The collection is tested because accession numbers may be duplicated in different collections,
        # either from no-acc-num or errors when assigning the numbers.
        df_row_index = log_df.index[(log_df['Collection'] == acc.Collection) & (log_df['Accession'] == acc.Accession)][0]

        # Validates the accession, including updating the preservation log and fixity validation log.
        # Different validation functions are used depending on if it is in a bag or is zipped.
        if acc.Fixity_Type == 'Bag':
            valid = validate_bag(acc.Path, input_directory, f'{acc.Accession}_bag')
            # Path Error happens on the server (faster) and means that accession needs to be re-run over the network,
            # so no permanent record of the error in the preservation log is needed.
            if valid == 'Path Error':
                update_fixity_validation_log(fixity_validation_log_path, log_df, df_row_index, 'skipped', valid)
            else:
                log_status = update_preservation_log(acc.Path, valid, acc.Fixity_Type)
                update_fixity_validation_log(fixity_validation_log_path, log_df, df_row_index, log_status, valid)
        elif acc.Fixity_Type == 'Zipped_Bag':
            valid = validate_bag(acc.Path, input_directory, f'{acc.Accession}_zipped_bag')
            # Path Error happens on the server (faster) and means that accession needs to be re-run over the network,
            # so no permanent record of the error in the preservation log is needed.
            if valid == 'Path Error':
                update_fixity_validation_log(fixity_validation_log_path, log_df, df_row_index, 'skipped', valid)
            else:
                log_status = update_preservation_log(acc.Path, valid, acc.Fixity_Type)
                update_fixity_validation_log(fixity_validation_log_path, log_df, df_row_index, log_status, valid)
        else:
            valid = validate_zip(acc.Path)
            log_status = update_preservation_log(acc.Path, valid, acc.Fixity_Type)
            update_fixity_validation_log(fixity_validation_log_path, log_df, df_row_index, log_status, valid)

    # Prints if there were any validation errors, based on the Result column.
    error_df = log_df.loc[~log_df['Result'].isin(['Valid', 'Valid (bag manifest)', 'Not an accession'])]
    if error_df.empty:
        print('\nNo validation errors.')
    else:
        print('\nValidation errors found, see the fixity validation log in the input_directory.')
