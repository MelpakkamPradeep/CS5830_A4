import pandas as pd
import numpy as np
import os

# Specify directories, URLs, and parameters
paramsdir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/data/"

df_list = []

for file_name in os.listdir(datadir):
	if file_name.endswith('csv') and file_name.startswith('filtered'):
		df = pd.read_csv(f'{datadir}{file_name}')
		df = df[df.columns.drop(list(df.filter(regex='Daily')))]

		for col in df.columns:
			df[col] = df[col].replace('s$', '', regex=True)
			# Convert the column to float64
			df[col] = pd.to_numeric(df[col], errors='coerce')
		grouped = df.groupby(['DATE'], as_index=False)
		grouped_df = grouped.apply(lambda x : x)
		location = [file_name[9:-4]] * len(grouped_df.index)
		grouped_df.insert(loc=0, column='station', value=location)
		df_list.append(grouped_df.values.tolist())
		
list_of_dfs = [sublist for sublist_list in df_list for sublist in sublist_list]
computed_averages = pd.DataFrame(list_of_dfs, columns=['Station', 'Month', 'ActualMonthlyMeanTemperature', 'ActualMonthlyMaximumTemperature', 'ActualMonthlyMinimumTemperature'])
computed_averages.dropna(subset=['ActualMonthlyMeanTemperature', 'ActualMonthlyMaximumTemperature', 'ActualMonthlyMinimumTemperature'], how='all', inplace=True)
# Save the DataFrame to a CSV file
computed_averages.to_csv(f'{datadir}actual_monthly_averages.csv', index=False)