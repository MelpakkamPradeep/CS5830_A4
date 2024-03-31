import pandas as pd
import numpy as np
import os

# Specify directories, URLs, and parameters
paramsdir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/data/"

calc_df = pd.read_csv(f"{datadir}computed_monthly_averages.csv")
act_df = pd.read_csv(f"{datadir}actual_monthly_averages.csv")

merged_df =  pd.merge(calc_df, act_df, on=['Station', 'Month'], how='inner')
print(f"The R^2 score of the Monthly Mean Temperature is : {np.corrcoef(merged_df['CalcMonthlyMeanTemperature'].values, merged_df['ActualMonthlyMeanTemperature'].values)[0, 1] ** 2}")
print(f"The R^2 score of the Monthly Maximum Temperature is :{np.corrcoef(merged_df['CalcMonthlyMaximumTemperature'].values, merged_df['ActualMonthlyMaximumTemperature'].values)[0, 1] ** 2}")
print(f"The R^2 score of the Monthly Minimum Temperature is :{np.corrcoef(merged_df['CalcMonthlyMinimumTemperature'].values, merged_df['ActualMonthlyMinimumTemperature'].values)[0, 1] ** 2}")
