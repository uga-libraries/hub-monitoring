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

- directory (parent folder being analyzed)
    - status (if it is in the backlog or closed due to restrictions)
        - collection_id/name
            - accession_id
                - accession_id_bag
                - accession_id_bag_full_risk_data.csv
                - preservation_log.txt
                - additional metadata files (optional)

Additionally, the department name should be part of the directory path, 
although does not need to be in the directory folder.

### Script Arguments

collection_summary.py

- directory (required): the directory with the folders to be summarized

### Testing

There are unit tests for each function and for the script overall.
The tests use files stored in the repo (test_data) as input. 
The risk spreadsheet has the correct columns and files, but the FITS and NARA data are made up to fit testing needs.
The preservation log is empty because the contents aren't used by this script. 
The reports generated with these files are stored in [documentation](documentation) to serve as examples. 

## Workflow

TBD

## Author

Adriane Hanson, Head of Digital Stewardship, University of Georgia Libraries

## Acknowledgements

Script specifications and user testing by Emmeline Kaser, Digital Archivist, University of Georgia Libraries
