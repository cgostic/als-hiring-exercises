# als-hiring-exercises


## Repository Overview

This repository includes scripts and outputs that fulfill the Data Engineer exercises distributed by ALS as part of the hiring process. 

_Exercise 1_ takes in three provided CRM data sets and returns a cleaned dataframe with a specified subset of constituents. _Excercise 2_ takes in the resulting dataframe from _Exercise 1_ and summarizes the data as specified. Assumptions included in the creation of these scripts include:

**Exercise 1**

- Constituents without recorded e-mail addresses should not be included in the final table.
  - Subscription data cannot be linked to these constituents (`cons_email_id` is the linking key) so there is little value to displaying these records in the final result.
- Recorded e-mail is the primary form of identification for the final result.
  - Constituents with a recorded e-mail addresses that do not appear in the constituent data are included in the final result and have `source == NaN`.
- `created_dt` should be the earliest recorded `create_dt` across the constituent and e-mail data.
  - The earliest date varies between these columns for each record.
- `updated_dt` should be the latest recorded `modified_dt` across the constituent, e-mail, and subscription data.
  - The latest date varies between these columns for each record.
- Constituents with a recorded e-mail that do not appear in the subscription table are of interest despite the misssing indication of chapter designation.
  - It's noted that (1) we're only interested in subscription status for constituents with `chapter_id == 1` and that (2) constituents whose e-mails do not appear in the subscription data are still subscribed. This indicates that the constituents whose e-mails do not appear in the subscription data are still of interest, and these constituents appear in the final result with `chapter_id = NaN`.
  
**Exercise 2**

- Acquisition date is the earliest recorded `create_dt` across the three available datasets (as recorded in Exercise 1

### Scripts

The following scripts are saved in the `src` directory:

- data-engineer_exercise-1.py
- data-engineer_exercise-2.py

### Outputs

The following files are saved in the `results` directory:

- people.csv
- acquisition_facts.csv

### Data Flow

## Directions to Run Scripts

**Requirements:**

These scripts require Python 3.0 +, as well as the following packages:

- pandas
- datetime

1. Clone or download this repository
2. Navigate to the root of this repository via the command line
3. In the command line, run one of the following commands:

To run both scripts in sequence and create `people.csv` and `acquisition_facts.csv`:

```
python src/.*
```

To run `data-engineer_exercise-1.py` and create `people.csv`:

```
python src/data-engineer_exercise-1.py
```

To run `data-engineer_exercise-2.py` and create `acquisition_facts.csv`:

```
python src/data-engineer_exercise-2.py
```
