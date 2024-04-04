"""Makes a spreadsheet with the format data from every full risk spreadsheet in a given folder

Data included: TBD

Parameter:
    directory (required): the directory with spreadsheets to be combined

Returns:
    CSV with all format data
"""
import os
import sys


if __name__ == '__main__':

    # Gets the path to the directory with the accessions to be validated from the script argument.
    directory = sys.argv[1]

    # Count how many are added.
    total = 0

    # Starts a spreadsheet for all format data.
    with open(os.path.join(directory, 'combined_format_data.csv'), 'w') as combo:
        combo.write('FITS_File_Path,FITS_Format_Name,FITS_Format_Version,FITS_PUID,FITS_Identifying_Tool(s),'
                    'FITS_Multiple_IDs,FITS_Date_Last_Modified,FITS_Size_KB,FITS_MD5,FITS_Creating_Application,'
                    'FITS_Valid,FITS_Well-Formed,FITS_Status_Message,NARA_Format_Name,NARA_File_Extensions,'
                    'NARA_PRONOM_URL,NARA_Risk_Level,NARA_Proposed_Preservation_Plan,NARA_Match_Type,'
                    'Technical_Appraisal_Format,Technical_Appraisal_Trash,Other_Risk_Indicator\n')

        # Finds every risk spreadsheet and adds it to the spreadsheet.
        for root, directories, files in os.walk(directory):
            for file in files:
                if 'full_risk_data' in file:
                    total += 1

                    # Save everything but the header row, skipped by next, to the combined csv.
                    with open(os.path.join(root, file), 'r') as f:
                        next(f)
                        combo.writelines(f)

    print('Number of risk spreadsheets combined:', total)
