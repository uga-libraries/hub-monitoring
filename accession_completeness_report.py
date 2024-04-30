"""Analyze all accessions in a given folder for completeness

Hargrett-specific navigation so far.
"""
import os
import sys


def accession_paths(coll_dir, coll):
    """Find the accession folder(s), which can be in a few places in the collection folder

    coll_dir (string): path to the folder with collections (script argument)
    coll (string): folder name of the collection

    returns a list of paths to the folders with the accession content,
    usually named with the accession number but may be the collection or Preservation Copies
    """

    acc_paths = []

    # First level within the collection is either the content, accession folders
    # or a folder "Preservation Copies" with the content or accession folders.
    for acc in os.listdir(os.path.join(coll_dir, coll)):

        # Skip files.
        if os.path.isfile(os.path.join(coll_dir, coll, acc)):
            continue

        # Skip non-accession folders that may be sibling folders of accessions.
        if acc == 'Risk_remediation' or acc == 'Access Copies' or acc.startswith('Apprais') or acc.endswith('FITS'):
            continue

        # Accession folders that are inside Preservation Copies folders.
        if os.path.exists(os.path.join(coll_dir, coll, 'Preservation Copies')):
            # Content is in Preservation Copies.
            # TODO: do not depend on knowing the coll.
            if coll in ['ua12-022 GLOBES records', 'ua16-010 Athens Music Project collection']:
                acc_paths.append(os.path.join(coll_dir, coll, 'Preservation Copies'))
            # Accession folders are in Preservation Copies.
            else:
                for accession_folder in os.listdir(os.path.join(coll_dir, coll, 'Preservation Copies')):
                    acc_paths.append(os.path.join(coll_dir, coll, 'Preservation Copies', accession_folder))
        # Accessions content inside the collection folder.
        # TODO: do not depend on knowing the coll.
        elif coll == 'ms4466 Athens Metal Arts Guild':
            acc_paths.append(os.path.join(coll_dir, coll))
        # Accession folders that are inside the collection folder.
        else:
            acc_paths.append(os.path.join(coll_dir, coll, acc))

    return acc_paths


if __name__ == '__main__':
    collection_directory = sys.argv[1]

    # First level within the folder is the collection.
    for collection in os.listdir(collection_directory):

        # Skip files and the non-collection folder
        if os.path.isfile(os.path.join(collection_directory, collection)) or collection == 'scripts':
            continue

        # Skip Linguistic Atlas Project, which is handled differently.
        # TODO: confirm this
        if collection == 'ua22-008 Linguistic Atlas Project':
            continue

        print()
        print(collection)

        accession_list = accession_paths(collection_directory, collection)
        print(accession_list)
