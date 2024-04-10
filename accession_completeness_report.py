"""Analyze all accessions in a given folder for completeness

Hargrett-specific navigation so far.
"""
import os
import sys


if __name__ == '__main__':
    directory = sys.argv[1]

    # First level within the folder is the collection.
    for collection in os.listdir(directory):

        # Skip files and non-collection folder
        if os.path.isfile(os.path.join(directory, collection)) or collection == 'scripts':
            continue

        print()
        print(collection)

        # First level within the collection is either the accessions or a folder "Preservation Copies" with accessions.
        for accession in os.listdir(os.path.join(directory, collection)):

            # Skip files.
            if os.path.isfile(os.path.join(directory, collection, accession)):
                continue

            # Skip non-accession folders that are siblings of accessions.
            if accession == 'Risk_remediation' or accession.startswith('Apprais') or accession.endswith('FITS'):
                continue

            # Gets accessions that are inside Preservation copies.
            if os.path.exists(os.path.join(directory, collection, 'Preservation Copies')):
                for accession_folder in os.listdir(os.path.join(directory, collection, 'Preservation Copies')):
                    print(accession_folder)
            else:
                print("access in collection folder")
