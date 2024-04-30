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
        skip = ['Access Copies', 'AIPs V2', 'to ingest', 'Risk_remediation']
        if acc in skip or acc.startswith('Apprais') or acc.endswith('FITS'):
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
        elif coll in ['ms4466 Athens Metal Arts Guild', 'RBRL_041_CLC', 'RBRL_059_DDB', 'RBRL_189_SDB', 'rbrl390',
                      'rbrl459', 'rbrl480', 'rbrl481', 'rbrl483', 'rbrl496', 'rbrl501', 'rbrl507', 'rbrl508']:
            acc_paths.append(os.path.join(coll_dir, coll))

        # Collection with extra collection folder.
        # TODO: do not depend on knowing the coll.
        elif coll == 'rbrl499':
            for accession_folder in os.listdir(os.path.join(coll_dir, coll, coll)):
                if not accession_folder.endswith('.csv'):
                    acc_paths.append(os.path.join(coll_dir, coll, coll, accession_folder))

        # Accession folders that are inside the collection folder.
        else:
            acc_paths.append(os.path.join(coll_dir, coll, acc))

    return acc_paths


def check_completeness(acc_path):
    """Test if the accession has a preservation log, full risk report, and if content is bagged
    
    acc_path (string): full path to the accession folder
    
    Returns a dictionary with True/False for if each of the three expected criteria are met.
    """

    # Starts a dictionary with the default value of False for all 3 criteria.
    # These are updated to True if they are found in the accession.
    result = {'pres_log': False, 'full_risk': False, 'bag': False}

    # All the desired criteria are in the first level within the accession folder.
    for item in os.listdir(acc_path):

        # Preservation log has two possible naming conventions.
        if item == 'preservation_log.txt' or item.endswith('PreservationLog.txt'):
            result['pres_log'] = True

        # Full risk data spreadsheet may have a date between full_risk_data and the file extension.
        elif 'full_risk_data' in item and item.endswith('.csv'):
            result['full_risk'] = True

        elif item.endswith('_bag'):
            result['bag'] = True

    return result


if __name__ == '__main__':
    collection_directory = sys.argv[1]

    # First level within the folder is the collection.
    for collection in os.listdir(collection_directory):

        # Skips files and the non-collection folder.
        if os.path.isfile(os.path.join(collection_directory, collection)) or collection == 'scripts':
            continue

        # Skips unconventional collections.
        # TODO: confirm this
        unconventional = ['ua22-008 Linguistic Atlas Project', 'RBRL_275_GEPO', 'rbrl349', 'rbrl409', 'rbrl462']
        if collection in unconventional:
            continue

        # Gets a list of the path to every folder with accession content and tests their completeness.
        accession_list = accession_paths(collection_directory, collection)
        for accession_path in accession_list:
            complete_dict = check_completeness(accession_path)

