import pandas as pd
import os
import yaml

# Function to read parameters from a YAML file
def read_params_from_yaml(file_path):
    with open(file_path, 'r') as file:
        params = yaml.safe_load(file)
    return params

# Specify directories, URLs, and parameters
paramsdir = "params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "data/" 
resultsdir = "results/" 

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
computed_averages.to_csv(f'{resultsdir}computed_monthly_averages.csv', index=False)
