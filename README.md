# Digital Production Hub Monitoring

## Overview

Scripts for summarizing and validating content on the Digital Production Hub, 
the UGA Libraries' centralized storage for digital objects that are not suitable for our digital preservation system.

## Getting Started

### Dependencies

- numpy (https://numpy.org/)
- pandas (https://pandas.pydata.org/docs/)

### Installation

The file directory structure should be:

- directory (parent folder being analyzed - optional if not doing collection summary)
    - status (if it is in the backlog or closed due to restrictions - optional if not doing collection summary)
        - collection_id/name
            - accession_id
                - accession_id_bag (or folder with unbagged accession contents)
                - accession_id_bag_full_risk_data.csv (will be missing if accession has long path errors)
                - preservation_log.txt
                - additional metadata files (optional)

For the risk update, download the latest version of NARA's Digital Preservation Plan spreadsheet (CSV version) from the 
[U.S. National Archives Digital Preservation GitHub Repo](https://github.com/usnationalarchives/digital-preservation).

For validating fixity, accessions should be bags or have a manifest. (UPDATE WITH MANIFEST INFO WHEN HAVE IT)

### Script Arguments

accession_completeness_report.py

- input_directory (required): the directory with the folders to be checked for completeness, 
  which must be the directory containing the status folders 

collection_summary.py

- directory (required): the directory with the folders to be summarized

format_list.py

- directory (required): the directory with the folders to be summarized

risk_update.py

- directory (required): the directory that contains the risk spreadsheets
- nara_csv (required): the path to the most recent NARA Preservation Action Plan spreadsheet

validate_fixity.py

- directory (required): the directory with the folders to be summarized

### Testing

There are unit tests for each function and for each script overall for collection_summary.py, risk_update.py, and validate_fixity.py.
The tests mostly use files stored in the repo (test_data) as input. 
Preservation metadata files may be missing if they are not needed for a test 
or have fake data to give the needed variations for the test.
 
Tests for format_list.py are preliminary and all use the same input test data.
It is the common data variations, but is not explicitly testing for all possible variations.

There are no tests for accession_completeness_report.py.
Check a sample of the accessions to see the report has the correct information.

The reports generated with these files are stored in [documentation](documentation) to serve as examples. 

## Workflow

TBD

For the file list, after the script runs:
1. Add a "Source" column as the first column with the Hub DEPARTMENT for combining it with other format data.
2. Merge rows where only the NARA risk level is different.  
   a. If one of the NARA risk levels is No Match, only include the other risk level(s).  
   b. For multiple other risk levels, convert to a range, e.g. Low-High Risk or Low-Moderate Risk.

## Author

Adriane Hanson, Head of Digital Stewardship, University of Georgia Libraries

## Acknowledgements

Script specifications and user testing by Emmeline Kaser, Digital Archivist, University of Georgia Libraries
