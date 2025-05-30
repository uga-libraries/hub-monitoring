"""
Copied validate_manifest() on 4-8-2025, with less logging and changing the paths to arguments,
to check a single accession that was skipped.
If this keeps being needed, import functions so that this stays in sync.
"""
from datetime import date
import hashlib
import os
import pandas as pd
import sys

# Gets the paths to the folder with the accession's files and the manifest.
acc_files = sys.argv[1]
acc_manifest = sys.argv[2]

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
df_manifest = pd.read_csv(acc_manifest, dtype=object)

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

# If it is valid, prints this fine.
# If there were errors, saves the full results to a log in the same folder as the manifest.
if valid:
    print('Valid')
else:
    print(f'{len(error_list)} manifest errors')
    log_path = os.path.join(os.path.dirname(acc_manifest),
                            f"manifest_validation_errors_{date.today().strftime('%Y-%m-%y')}.txt")
    with open(log_path, 'w') as open_log:
        for error in error_list:
            open_log.write(f'{error}\n')
