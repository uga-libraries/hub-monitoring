"""Get updated NARA risk information for every accession in a directory

Parameters:
    directory (required): the directory that contains the risk data spreadsheets
    nara_csv (required): the path to the most recent NARA risk spreadsheet

Returns:
    New risk data spreadsheet added to each accession folder
"""
import os
import sys


def check_arguments(argument_list):
    """Check the required arguments report_folder and nara_csv are present and correct

    Copied from https://github.com/uga-libraries/format-report/blob/main/merge_format_reports.py

    Parameters:
        argument_list : list from sys.argv with the script parameters

    Returns:
        report_path : the path to the folder which contains ARCHive's group file format reports and usage report, or None
        nara_path : the path to NARA's Digital Preservation Plan spreadsheet, or None
        errors : the list of errors encountered, if any, or an empty list
    """

    # Makes variables with default values to store the results of the function.
    report_path = None
    nara_path = None
    errors = []

    # Verifies that the first required argument (report_folder) is present,
    # and if it is present that it is a valid directory.
    if len(argument_list) > 1:
        report_path = argument_list[1]
        if not os.path.exists(report_path):
            errors.append(f"Report folder '{report_path}' does not exist")
    else:
        errors.append("Required argument report_folder is missing")

    # Verifies that the second required argument (nara_csv) is present,
    # and if it is present that it is a valid directory.
    if len(argument_list) > 2:
        nara_path = argument_list[2]
        if not os.path.exists(nara_path):
            errors.append(f"NARA CSV '{nara_path}' does not exist")
    else:
        errors.append("Required argument nara_csv is missing")

    # Returns the results.
    return report_path, nara_path, errors


if __name__ == '__main__':

    # Gets the paths to the directory and NARA spreadsheet from the script arguments.
    # Exits the script if there are errors.
    directory, nara_csv, error_list = check_arguments(sys.argv)
    if len(error_list) > 0:
        for error in error_list:
            print(error)
        sys.exit()

    # Navigates to each risk spreadsheet.
    # Makes a new risk spreadsheet with the same format identifications and updated NARA risk levels.
