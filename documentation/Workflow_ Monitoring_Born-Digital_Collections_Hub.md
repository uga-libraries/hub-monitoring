# Monitoring Born-Digital Collections Stored on the DP Hub 

Version 1.0, updated by Emmeline Kaser, July 2024 

## Purpose 

This document outlines policy and workflows for monitoring Hargrett and Russell born-digital archival collections 
stored on the Digital Production Hub. These monitoring activities are the responsibility of the Digital Archivist. 
They include: 

* Analyzing the completeness of the documentation for each collection (preservation log, risk data, and fixity data) 
* Validating the fixity of the files in each collection 
* Updating the format risk data for each collection using the most recent NARA risk levels 
* Analyzing format risk levels to identify files requiring immediate reformatting to prevent data loss 

## Background 

Born-digital collections for the Hargrett and Russell Libraries are stored in the Digital Production (DP) Hub while 
they are being processed or in the queue for processing. This includes backlogged collections that are ready to be 
opened once they are processed, and materials that are closed due to donor restrictions. Each library’s Hub share has a 
“Born-digital” directory that is broken up into “Backlogged” and “Closed” subdirectories so that collections are 
separated by status. Once a collection is processed and ingested into the ARCHive digital preservation system, the 
ingested version is considered the definitive version of the collection materials. At that time, preservation copies of 
the material are deleted from the Hub.  

## Policy  

The Hub is considered temporary preservation storage and is designed to hold collections material for extended periods 
of time as needed. Hub content is automatically backed up, but unlike the ARCHive digital preservation system, material 
can be altered or deleted by any user with write permissions and there is no automated fixity validation. As a result, 
it is the responsibility of the Digital Archivist to regularly perform checks on these materials to validate fixity, 
ensure the completeness of the collection, fill any gaps in preservation documentation, and migrate high-risk formats 
as needed. Together, these processes serve as a holistic audit of the materials in temporary preservation storage, 
allowing the Digital Archivist to catch, document, and rectify any issues that may result in unintended data loss.  

The Hub monitoring workflow described in this document ensures that all collections are fully documented, that their 
fixity is valid, and that we are aware of any high-risk formats that need to be imminently migrated to prevent data 
loss.  The Digital Archivist should run these checks every three years, record the results, and be prepared to take 
action on materials determined to be at imminent risk for data loss. The fixity validation script should be run annually.  

## Workflow 

This information is collected by running a series of Python scripts to generate reports. All relevant scripts are 
stored in the [hub-monitoring repository](https://github.com/uga-libraries/hub-monitoring) on the UGA Libraries GitHub.  

All materials on the Hub should be accessioned as fully as possible before running this workflow. See the workflow on 
GitHub for accessioning instructions. Each collection’s folder organization must follow the directory structure 
outlined in the repository README. If they do not follow this structure, the scripts will not work as expected.  

Scripts should be run in the following order: 

| Script Name                      | Script Function                                                                                                                              |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| accession_completeness_report.py | Checks each accession for the presence of a bag, preservation log, and full risk report, and generates a report of anything that is missing. |
| validate_fixity.py               | Validates the fixity for every accession in a directory using either bag data or a zip md5.                                                  |
| risk_update.py                   | Makes an updated risk spreadsheet for every accession in a directory.                                                                        |
| format_list.py                   | Makes a spreadsheet with the format data from every full risk spreadsheet in a directory.                                                    |
| collection_summary.py            | Makes spreadsheets with summary data about each accession and collection in each department folder.                                          |

Each script represents a phase of the audit process. After running each script, the Digital Archivist should review the 
resulting reports and document or remediate issues as appropriate before moving on to the next.  

A narrative summary of the audit process, including an overview of the scripts run and the actions taken after each, 
should be saved for future reference. 

## Accession Completeness Report 

The accession-completeness-report.py script must be run on the top-level “born-digital” folder in each library’s Hub 
share (the folders containing the “backlogged” and “closed” status folders). It generates a report of any accessions 
that are incomplete and what is missing from them. 

Complete accessions include:  

* A preservation log (preservation_log.txt) 
* A full risk report (acc_full_risk_data.csv) 
* Bagged files (folder ends with '_bag') 

Some accessions may be incomplete if they were created following a legacy workflow, or if ubiquitous file path issues 
make it impossible to run the bagging and format analysis script. **All accessions must have an initial file manifest 
containing checksum data and a preservation log.** 

### Actions Taken 

The Digital Archivist should either create the missing documentation or, if it can’t be created, make a note in the 
report explaining why the accession is incomplete.  Instructions for creating a preservation log, risk report, and bag 
can be found in the [born-digital-accessioning GitHub repo](https://github.com/uga-libraries/born-digital-accessioning). 
Initial file manifests are created using the [technical-appraisal-logs.py](https://github.com/uga-libraries/accessioning-scripts/blob/main/technical-appraisal-logs.py) 
script. 

The report should be re-run after any errors are fixed. Only the most up-to-date version needs to be retained until the 
next auditing cycle.

## Validate Fixity 

The validate-fixity.py script should be run six months, to keep up with the Hub backup schedule. 
It can be run at the top-level “born-digital” folder in each library’s Hub share. 
It will validate the fixity for each file in an accession and update each accession’s preservation log with the result. 
It also creates a summary report of the validations for easier review. 

In rare cases, an accession is split into multiple bags. 
It will have a folder acc-id_bags at the level where there is normally a single bag, 
and will be in the fixity validation log with a result of "Validate separately"

By default, the script uses each bag’s built-in validation function to check the fixity of the contents. 
The bag may be named accession_bag or accession_zipped_bag (the contents of the bag are zipped, not the bag itself).
If the bag cannot validate, it will use the bag manifest to validate.
If the accession is zipped and has a file named accession_zip_md5.txt', it will validate the md5 of the zip.

We tried using the initial manifest for validation, but it is too inconsistent about if it could find the path to calculate MD5.
This seems to be from how Python interacts with Hub, as the same file may or may not be found on different occasions
and every file we've checked is still present.

This is time-consuming to run, taking days for each born-digital folder.
Create just the fixity_validation_log to verify everything is correctly identified as an accession or not an accession 
and all accessions have fixity before running it to actually validate.

### Actions Taken 

If the summary report flags instances of invalid fixity, submit a Libraries IT ticket to restore the file from the 
backup. If this is not an option, determine if the affected file(s) can still be opened or if there is something 
visibly wrong with the way the data is rendered. Thoroughly document any findings. 

All actions must be documented in the accession’s preservation log.
The validation log and a narrative report are being kept for now to help us track and improve the process.
We may not keep these permanently. 

## Risk Update 

The risk_update.py script can be run at the top-level “born-digital” folder in each library’s Hub share or at the 
status folder level. It requires the file path to a downloaded copy of the latest version of the NARA Preservation 
Action Plan CSV, sourced from NARA’s [digital-preservation repo](https://github.com/usnationalarchives/digital-preservation/tree/master). 
It generates a new risk spreadsheet for each accession folder and saves a log of all the updated accessions to the 
top-level directory.  

### Actions Taken 

None, beyond fixing any errors that may prevent the script from finishing. The data will be interpreted once it is 
summarized using the format_list.py script. 

The most recent risk spreadsheets should be retained in their respective accession folders. Outdated full-risk-data 
CSVs generated by this script can be deleted. 

## Format List 

The format_list.py script can be run at the top-level “born-digital” folder in each library’s Hub share or at the 
status folder level. It produces a spreadsheet report with the format data from every full risk spreadsheet in the 
selected directory.  

The report includes:  

* FITS_Format_Name 

* FITS_Format_Version 

* NARA_Risk_Level 

* File_Count 

* Size_GB 

### Actions Taken 

None, beyond fixing any errors that may prevent the script from finishing. The data will be interpreted once it is 
summarized using the collection_summary.py script.  

The most recent summary report should be retained until the next auditing cycle.  

## Collection Summary 

The collection_summary.py script must be run on the top-level “born-digital” folder in each library’s Hub share. It 
creates two summary reports, one containing all the accessions and another containing all the collections in the 
department folder. 

The reports include: 

* Accession (accession report only) 

* Collection 

* Status (backlogged or closed) 

* Accession date (date range if more than one) 

* Size (GB and number of files) 

* Risk (number of files at each NARA risk level) 

* Notes (if there was no risk CSV and for additional archivist notes) 

### Actions Taken 

Use the accession summary to analyze the current amount of format risk. Reformatting should be prioritized for only 
the most high-risk materials on the Hub. Refer to the at-risk formats documentation for information about when format 
conversion is necessary and specific migration pathways.  

If files need to be reformatted, make a copy of the affected accessions so that the original formats can still be 
ingested as Version 1 when the collection is processed. If previously-reformatted files are being reformatted again 
from the original file, the intermediary format(s) does not need to be retained – only the original and the newest 
reformatted version. Document all changes in a collection-level reformatting log, as well as the relevant accession 
records and preservation logs. Reformatting logs are retained permanently with the collection documentation. 

The collection summary report can be shared with stakeholders in each library. It provides a snapshot of our 
born-digital holdings that can help with reappraisal, prioritizing collections for processing, and conceptualizing 
the labor requirements and complexity of the backlog. The Digital Archivist may want to manually update the report by 
calculating the collection size where the script could not. To better reflect the labor requirements of collections 
on the Hub, it is recommended to also add [processing tier](https://github.com/uga-libraries/born-digital-processing/blob/main/processing-tiers.md) 
and priority information.  

## Review Schedule 

Last reviewed: July 2024
Last review of fixity validation: September 2025
