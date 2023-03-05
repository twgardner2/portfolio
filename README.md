# Lessons learned in blood

Pandas dataframes must have a monotonic index in order to subset it by slice. Use `.sort_index()`. See [this](https://github.com/pandas-dev/pandas/issues/5821) GitHub issue.

## Bad Error Messages, How to Fix Them
 * `ValueError: cannot reindex on an axis with duplicate labels`:  Check the `date` column of all input files, make sure you updated the most recent one to the new month, instead of just copying the old one down.