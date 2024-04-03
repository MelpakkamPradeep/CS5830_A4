import pandas as pd	# Import of csv manipulation
import numpy as np	# Import to calculate the R2 score
import os		# Import for saving files

# Specify directories, URLs, and parameters
paramsdir = "params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "data/"
resultsdir = "results/"

# Read the output of prepare.py
calc_df = pd.read_csv(f"{resultsdir}computed_monthly_averages.csv")
# Read the output of process.py
act_df = pd.read_csv(f"{resultsdir}actual_monthly_averages.csv")

# Merge the calculated and actual monthly average dataframes based on station and month
merged_df =  pd.merge(calc_df, act_df, on=['Station', 'Month'], how='inner')
# Group the merged dataframe by station
grouped = merged_df.groupby(['Station'])

# FUnction to find the R2 score for a group, for each temperature column
def find_r2_score(group):
	r21 = np.corrcoef(group['CalcMonthlyMeanTemperature'].values, group['ActualMonthlyMeanTemperature'].values)[0, 1] ** 2
	r22 = np.corrcoef(group['CalcMonthlyMaximumTemperature'].values, group['ActualMonthlyMaximumTemperature'].values)[0, 1] ** 2
	r23 = np.corrcoef(group['CalcMonthlyMinimumTemperature'].values, group['ActualMonthlyMinimumTemperature'].values)[0, 1] ** 2
	return pd.Series([r21, r22, r23], index=['R2_MonthlyMeanTemperature', 'R2_MonthlyMaximumTemperature', 'R2_MonthlyMinimumTemperature'])
	
# Compute the R2 score for a group, for each temperature column
r2_scores = grouped.apply(find_r2_score, include_groups=False).reset_index() 

# Save the R2 scores to a csv file
r2_scores.to_csv(f'{resultsdir}computed_r2_scores.csv', index=False)
