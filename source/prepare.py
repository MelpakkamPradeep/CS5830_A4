import pandas as pd
import os

# Specify directories, URLs, and parameters
paramsdir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/data/" 

df_list = []

for file_name in os.listdir(datadir):
	if file_name.endswith('csv') and file_name.startswith('filtered'):
		df = pd.read_csv(f'{datadir}{file_name}')
		df = df[df.columns.drop(list(df.filter(regex='Monthly')))]
		for col in df.columns:
			df[col] = df[col].replace('s$', '', regex=True)
			# Convert the column to float64
			df[col] = pd.to_numeric(df[col], errors='coerce')
		grouped = df.groupby(['DATE'], as_index=False)
		monthly_means = grouped.mean()
		location = [file_name[9:-4]] * len(monthly_means.index)
		monthly_means.insert(loc=0, column='station', value=location)
		#monthly_means.insert(loc=1, column='month', value=grouped['DATE'])
		df_list.append(monthly_means.values.tolist())

list_of_dfs = [sublist for sublist_list in df_list for sublist in sublist_list]
computed_averages = pd.DataFrame(list_of_dfs, columns=['Station', 'Month', 'CalcMonthlyMeanTemperature', 'CalcMonthlyMaximumTemperature', 'CalcMonthlyMinimumTemperature'])
# Save the DataFrame to a CSV file
computed_averages.to_csv(f'{datadir}computed_monthly_averages.csv', index=False)
