import pandas as pd
import numpy as np
import os

# Specify directories, URLs, and parameters
paramsdir = "params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "data/"
resultsdir = "results/"

calc_df = pd.read_csv(f"{resultsdir}computed_monthly_averages.csv")
act_df = pd.read_csv(f"{resultsdir}actual_monthly_averages.csv")

merged_df =  pd.merge(calc_df, act_df, on=['Station', 'Month'], how='inner')
grouped = merged_df.groupby(['Station'])

def find_r2_score(group):
	r21 = np.corrcoef(group['CalcMonthlyMeanTemperature'].values, group['ActualMonthlyMeanTemperature'].values)[0, 1] ** 2
	r22 = np.corrcoef(group['CalcMonthlyMaximumTemperature'].values, group['ActualMonthlyMaximumTemperature'].values)[0, 1] ** 2
	r23 = np.corrcoef(group['CalcMonthlyMinimumTemperature'].values, group['ActualMonthlyMinimumTemperature'].values)[0, 1] ** 2
	return pd.Series([r21, r22, r23], index=['R2_MonthlyMeanTemperature', 'R2_MonthlyMaximumTemperature', 'R2_MonthlyMinimumTemperature'])
r2_scores = grouped.apply(find_r2_score, include_groups=False).reset_index() 

r2_scores.to_csv(f'{resultsdir}computed_r2_scores.csv', index=False)

