"""Validates the fixity for every accession in a directory

Accessions are most commonly in bags, but legacy accessions may have a manifest instead

Parameter:
    directory (required): the directory that contains the accession folders

Returns:
    Updates the preservation_log.txt of each accession with the result
    Creates a summary report of the validations
"""
import os
import sys


def check_argument(arg_list):
    """Check if the required argument is present and a valid directory

    :parameter
    arg_list (list): the contents of sys.argv after the script is run

    :returns
    dir_path (string): the path to the folder with data to be summarized, or None (if error)
    error (string): the error message, or None (if no error)
    """

    # Checks if the required argument (directory path) is present and a valid path.
    # It will be index 1 in the argument list, because sys.argv also includes the path to the script at index 0.
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


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    directory, error = check_argument(sys.argv)
    if error:
        print(error)
        sys.exit(1)

    # Navigates to each accession bag and validates it.
    for root, directories, files in os.walk(directory):
        for directory in directories:
            if directory.endswith('_bag'):
                print("Validate Bag")
