# Lessons learned in blood

Pandas dataframes must have a monotonic index in order to subset it by slice. Use `.sort_index()`. See [this](https://github.com/pandas-dev/pandas/issues/5821) GitHub issue.
