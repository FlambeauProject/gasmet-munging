# gasmet-munging
Wrangling the gasmet data into submission.

## app.py
This script contains two functions: *trim_data* and *adjust_datetime*. *trim_data* is used to truncate the data when the gasmets was started more than once under the same file name. This function makes a copy of the orginal then makes a new ```Results.txt``` using only the last run. *adjust_datetime* uses the diffrence in the licor time and gasment time to sync the observations.
