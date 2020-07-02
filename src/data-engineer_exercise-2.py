"""
This script completes Data Engineer, Exercise 2 
distributed by ALS as part of the hiring process.

A notebook with a walkthrough of the process behind creating
this script is included in the `EDA` directory of this repository.

Input data is created during Exercise 1 and stored in
the root of this repository:
- people.csv

Output is saved to the root of this repository as a .csv:
- acquisition_facts.csv

Main assumptions are listed in the README of this repository.
"""

import pandas as pd
import datetime as dt

print("########### Beginning data-engineer_exercise-2.py ###########")
###### DATA SOURCES ######
print("Reading in data sources...")
# Data created during exercise 1
people_data = pd.read_csv('people.csv', parse_dates=['created_dt'])

###### BEGIN SCRIPT ######
print("Parsing dates...")
# Parse year, month, day from `create_dt` timestamp
people_data['cal_date'] = people_data.created_dt.dt.strftime('%Y-%m-%d')
print("Summarizing data...")
# Calculate number of acquisitions per day, assuming `create_dt` 
# is acquisition date.
# - Group on cal_date (year, month, day)
# - Count on 'created_dt' because no NaN values exist in this column
acq_data = (people_data.groupby('cal_date')['created_dt']
            .count().reset_index()
            .rename(columns={'cal_date':'acquision_date', 
                             'created_dt':'acquisitions'}))
print('Exporting to csv...')
# Export to csv
acq_data.to_csv('acquisition_facts.csv', 
                header=acq_data.columns.tolist(), 
                index=False)

print("Processing complete! View the created/updated `acquisition_facts.csv file.")