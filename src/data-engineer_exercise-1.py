"""
This script completes Data Engineer, Exercise 1 
distributed by ALS as part of the hiring process.

A notebook with a walkthrough of the process behind creating
this script is included in the `EDA` directory of this repository.

Input data is read directly from the shared AWS S3
buckets:

- https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons.csv
- https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email.csv
- https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email_chapter_subscription.csv

Output is saved to the `results` directory of
this repository as a .csv:
- people.csv

Main assumptions are listed in the README of this repository.
"""

import pandas as pd
import datetime as dt
pd.options.mode.chained_assignment = None

###### DATA SOURCES ######
print("Importing data...")
# Constituent data
cons_data = pd.read_csv(r'https://als-hiring.s3.amazonaws.com/fake_data/'
                        r'2020-07-01_17%3A11%3A00/cons.csv')
# Constituent e-mail data
email_data = pd.read_csv(r'https://als-hiring.s3.amazonaws.com/fake_data/20'
                         r'20-07-01_17%3A11%3A00/cons_email.csv')
# Constituent subscription data
sub_data = pd.read_csv(r'https://als-hiring.s3.amazonaws.com/fake_data/2020-07'
                       r'-01_17%3A11%3A00/cons_email_chapter_subscription.csv')

###### BEGIN SCRIPT ######

# Check if cons_id is a primary key in cons_data
assert all(cons_data.cons_id.value_counts().values == 1), \
"cons_id is not unique in the cons_data table"

# Check if cons_email_id is a primary key in email_data
assert all(email_data.cons_email_id.value_counts().values == 1), \
"cons_email_id is not unique in the email_data table"

# Filter Data to relevant columns, and restrictions mentioned in instructions
print("Filtering Data...")
# Relevant columns per dataframe:
cons_cols = ['cons_id', 'source', 'create_dt', 'modified_dt']
email_cols = ['cons_id', 'cons_email_id', 'email', 'create_dt', 'modified_dt']
sub_cols = ['cons_email_id', 'isunsub', 'chapter_id', 'modified_dt']

# Drop irrelevant columns from constituent data
cons_data_filtered = cons_data.drop(columns = [col for col in cons_data.columns
                                              if col not in cons_cols])

# Filter e-mail data to primary address and drop irrelevant columns
email_data_filtered = (email_data[email_data.is_primary == 1]
                       .drop(columns = [col for col in 
                                        email_data.columns 
                                        if col not in email_cols]))

# Filter subscription data to chapter 1 and drop irrelevant columns
sub_data_filtered = (sub_data[sub_data.chapter_id == 1]
                     .drop(columns = [col for col in 
                                     sub_data.columns
                                     if col not in sub_cols]))

# Check that all non-primary emails were removed
assert (email_data[email_data.is_primary == 0].shape[0] == 
        email_data.shape[0] - email_data_filtered.shape[0]), \
"All rows with non-primary emails should be removed"

# Check that each constituent has only 1 primary email
assert (all(email_data_filtered.cons_id.value_counts() == 1)), \
"Some constituents have more than one primary email"

# Merge 3 data sets (cons, email, sub)
print("Merging data...")
# Join cons_data and email_data on `cons_id` (established as primary key)
#    - Right join retians any constituent with a recorded primary e-mail
cons_email = pd.merge(cons_data_filtered, email_data_filtered, 
                      on='cons_id', how='right')

# Join subscription data to merged cons/email data on `cons_email_id`
#    - Left join maintains all constituents with a recorded primary e-mail
crm_df = pd.merge(cons_email, sub_data_filtered, 
                  on = 'cons_email_id', how='left')

# Determine created_dt and updated_dt
print("Transforming columns to datetime format...")
# Transform create_dt, modified_dt columns (from 3 data sets) to datetime
crm_df[['create_dt_x', 'create_dt_y', 
        'modified_dt_x', 'modified_dt_y', 'modified_dt']] = \
        (crm_df[['create_dt_x', 'create_dt_y', 
        'modified_dt_x', 'modified_dt_y', 'modified_dt']]
        .apply(lambda x: pd.to_datetime(
            x, format = '%a, %Y-%m-%d %H:%M:%S'), axis = 1))

# Set created_dt as minimum of create_dt from cons and email dataframes
crm_df['created_dt'] = crm_df[['create_dt_x', 'create_dt_y']].min(axis = 1)

# Set updated_dt as maximum of modified_dt from cons, email and sub dataframes
crm_df['updated_dt'] = crm_df[['create_dt_x', 'create_dt_y']].min(axis = 1)

print("Finalizing data...")

# Emails not included in the subscription data are assumed to be subscribed
crm_df['isunsub'] = crm_df['isunsub'].fillna(0.0)

# Drop extraneous columns
crm_df = crm_df.drop(columns = ['create_dt_x', 'create_dt_y', 'modified_dt_x',
                                'modified_dt_y', 'modified_dt', 'cons_id', 
                                'cons_email_id', 'chapter_id'])

# Export to csv
crm_df.to_csv('results/people.csv', 
              header=crm_df.columns.tolist(), 
              index=False)

print(r"Processing Complete! View the people.csv file"
      r" in the `results` folder")
