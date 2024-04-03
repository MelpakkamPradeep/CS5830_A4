import pandas as pd 	# Import for csv file processing
import os		# Import for file saving

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
		# Read file and remove all Daily columns
		df = pd.read_csv(f'{datadir}{file_name}')
		df = df[df.columns.drop(list(df.filter(regex='Daily')))]
		
		# Process the daily columns data
		for col in df.columns:
			df[col] = df[col].replace('s$', '', regex=True)
			# Convert the column to float64
			df[col] = pd.to_numeric(df[col], errors='coerce')
		# Group the given data by date
		grouped = df.groupby(['DATE'], as_index=False)
		# Get list of months in the dataset
		month = df['DATE'].values.tolist()
		# Extract the monthly mean of the grouped data
		grouped_df = grouped.apply(lambda x : x, include_groups=False)
		# Add the station as a new column
		location = [file_name[9:-4]] * len(grouped_df.index)
		grouped_df.insert(loc=0, column='station', value=location)
		# Add the month as a new column
		grouped_df.insert(loc=1, column='month', value=month)
		# Add to list of dataframes
		df_list.append(grouped_df.values.tolist())

# Flatten the list of dataframes	
list_of_dfs = [sublist for sublist_list in df_list for sublist in sublist_list]
# Create the new dataframe
computed_averages = pd.DataFrame(list_of_dfs, columns=['Station', 'Month', 'ActualMonthlyMeanTemperature', 'ActualMonthlyMaximumTemperature', 'ActualMonthlyMinimumTemperature'])
computed_averages.dropna(subset=['ActualMonthlyMeanTemperature', 'ActualMonthlyMaximumTemperature', 'ActualMonthlyMinimumTemperature'], how='all', inplace=True)
# Save the DataFrame to a CSV file
computed_averages.to_csv(f'{resultsdir}actual_monthly_averages.csv', index=False)
