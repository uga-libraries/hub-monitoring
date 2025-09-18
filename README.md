# Digital Production Hub Monitoring

## Overview

Scripts for summarizing and validating content on the Digital Production Hub, 
the UGA Libraries' centralized storage for digital objects that are not suitable for our digital preservation system.

The reports generated with these files are stored in [documentation](documentation) to serve as examples. 

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

For validating fixity, accessions should be bags or be zipped with the zip md5 stored in a text file. 
Bags may be named accession_bag or accession_zipped_bag, where the contents of the bag are zipped to allow 
bagging when there are character or path length issues we can't resolve at that time.
Zipped accessions should be named accession.zip and have a file in the same directory named accession_zip_md5.txt,
which contains one row of text formatted "MD5 path/to/accession.zip"

### Script Arguments

accession_completeness_report.py

- input_directory (required): the directory with the folders to be checked for completeness, 
  which must be the directory containing the status folders 

collection_summary.py

- input_directory (required): the directory with the folders to be summarized,
  which must be the directory containing the status folders ("born-digital")

format_list.py

- input_directory (required): the directory with the folders to be summarized, 
  which may be any folder in the expected file directory structure

risk_update.py

- input_directory (required): the directory that contains the risk spreadsheets,
  which may be any folder in the expected file directory structure
- nara_csv (required): the path to the most recent NARA Preservation Action Plan spreadsheet

validate_fixity.py

- input_directory (required): the directory that contains the content to be validated (in bags or zipped),
  which must be in the directory containing the status folders ("born-digital" or "Born-digital")

### Testing

There are unit tests for each function and for each script overall for all scripts.
The tests mostly use files stored in the repo as input. 
Preservation metadata files may be missing if they are not needed for a test 
or have fake data to give the needed variations for the test.
The directory structure may be simplified if the full standard structure is not needed for a test.

A few tests are for errors caused by path length, which could not be replicated in our current computing environment.
Instead, there are tests to use with real data in Hub.
They are commented out by default and indicate what information to provide for them to work.

## Workflow

Primary monitoring workflow that uses these scripts: 
[Monitoring Born-Digital Collections on Hub](documentation/Workflow_%20Monitoring_Born-Digital_Collections_Hub.md)

Manual edits for the format_list.py output:
1. Add a "Source" column as the first column with the Hub DEPARTMENT for combining it with other format data.
2. Normalize format names that are different for each file, e.g., Cannot open PATH or Cabinet # Files.
3. Merge rows where the format name and version are the same and the NARA risk level is different.  
   a. If one of the NARA risk levels is No Match, only include the other risk level(s).  
   b. For multiple other risk levels, convert to a range, e.g. Low-High Risk or Low-Moderate Risk.
   c. Add the File_Count and Size_GB for all rows.

## Author

Adriane Hanson, Head of Digital Stewardship, University of Georgia Libraries

## Acknowledgements

Script specifications and user testing by Emmeline Kaser, Digital Archivist, University of Georgia Libraries
