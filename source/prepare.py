import pandas as pd # Import for csv file processing
import os	# Import for saving files

# Specify directories, URLs, and parameters
paramsdir = "params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "data/" 
resultsdir = "results/" 

# List to append the dataframes of each calculated dataframe
df_list = []

# Iterate over all files in data directory
for file_name in os.listdir(datadir):
	# If the file is of form 'filtered*.csv'
	if file_name.endswith('csv') and file_name.startswith('filtered'):
		# Read file and remove all Monthly columns
		df = pd.read_csv(f'{datadir}{file_name}')
		df = df[df.columns.drop(list(df.filter(regex='Monthly')))]
		# Process the daily columns data
		for col in df.columns:
			df[col] = df[col].replace('s$', '', regex=True)
			# Convert the column to float64
			df[col] = pd.to_numeric(df[col], errors='coerce')
		# Group the given data by date
		grouped = df.groupby(['DATE'], as_index=False)
		# Compute the monthly mean of the grouped data
		monthly_means = grouped.mean()
		# Add the station as a new column
		location = [file_name[9:-4]] * len(monthly_means.index)
		monthly_means.insert(loc=0, column='station', value=location)
		# Add to list of dataframes
		df_list.append(monthly_means.values.tolist())

# Flatten the list of dataframes
list_of_dfs = [sublist for sublist_list in df_list for sublist in sublist_list]
# Create the new dataframe
computed_averages = pd.DataFrame(list_of_dfs, columns=['Station', 'Month', 'CalcMonthlyMeanTemperature', 'CalcMonthlyMaximumTemperature', 'CalcMonthlyMinimumTemperature'])
# Save the DataFrame to a CSV file
computed_averages.to_csv(f'{resultsdir}computed_monthly_averages.csv', index=False)
