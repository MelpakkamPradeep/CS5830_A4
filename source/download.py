import random  # Importing the random module for random selection
import os  # Importing the os module for system operations
import pandas as pd  # Importing pandas for data manipulation
import yaml  # Importing yaml for reading YAML files
import requests  # Importing requests for making HTTP requests
from bs4 import BeautifulSoup  # Importing BeautifulSoup for HTML parsing

# Function to read parameters from a YAML file
def read_params_from_yaml(file_path):
    with open(file_path, 'r') as file:
        params = yaml.safe_load(file)  # Using yaml.safe_load to read YAML content safely
    return params

# Function to fetch the HTML page containing location-wise datasets
def fetch_html_page(base_url, year, datadir):
    html_file = f"{datadir}/ncei_data_{year}.html"  # Naming the HTML file
    fetch_command = f"curl -o {html_file} {base_url}{year}/"  # Using curl command to fetch HTML
    os.system(fetch_command)  # Executing the curl command to download the HTML file
    return html_file  # Returning the path to the downloaded HTML file

# Function to check if a file is valid based on the required conditions
def is_file_valid(file_path):
    df = pd.read_csv(file_path)  # Reading the CSV file into a DataFrame
    
    # List of required columns
    required_columns = [
        'DailyAverageDryBulbTemperature', 'DailyMaximumDryBulbTemperature', 'DailyMinimumDryBulbTemperature',
        'MonthlyMaximumTemperature', 'MonthlyMeanTemperature', 'MonthlyMinimumTemperature'
    ]
    
    # Checking if all required columns are present and not all values are NaN
    if all(col not in df.columns or df[col].isnull().all() for col in required_columns):
        return False  # File is not valid if any required column is missing or all values are NaN
    
    # Checking specific pairs of daily and monthly columns for non-null values
    pairs = [
        ('DailyAverageDryBulbTemperature', 'MonthlyMeanTemperature'),
        ('DailyMaximumDryBulbTemperature', 'MonthlyMaximumTemperature'),
        ('DailyMinimumDryBulbTemperature', 'MonthlyMinimumTemperature')
    ]
    
    for daily_col, monthly_col in pairs:
        if daily_col in df.columns and monthly_col in df.columns:
            if not df[daily_col].notna().any() or not df[monthly_col].notna().any():
                return False  # File is not valid if any required pair has no non-null values
    
    return True  # File is valid if it passes all checks

# Function to extract the month from the date column
def extract_month(date_str):
    return pd.to_datetime(date_str).strftime('%m')  # Converting date string to month format

# Specify directories, URLs, and parameters
paramsdir = "params/"  # Directory containing parameter files
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"  # Base URL for data access
params = read_params_from_yaml(f"{paramsdir}params.yaml")  # Reading parameters from YAML file
year = params['ncei']['year']  # Getting the year from parameters
n_locs = params['ncei']['n_locs']  # Getting the number of locations from parameters
datadir = "data/"  # Directory for downloaded data
resultsdir = "results/"  # Directory for results

os.makedirs(datadir)  # Creating the data directory if it doesn't exist

# Step 1: Fetch the page containing the location-wise datasets
html_file = fetch_html_page(base_url, year, datadir)  # Fetching the HTML page

# Step 2: Read the HTML file to extract CSV file links
with open(html_file, 'r') as f:
    html_content = f.read()  # Reading the HTML content

soup = BeautifulSoup(html_content, 'html.parser')  # Parsing HTML content with BeautifulSoup
csv_links = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.csv')]  # Extracting CSV links

# Step 3: Process random CSV files until n_locs filtered files are present in datadir
filtered_files = 0  # Initializing the counter for filtered files
while filtered_files < n_locs and len(csv_links) > 0:  # Loop until desired number of filtered files is reached or no CSV links left
    random_csv_link = random.choice(csv_links)  # Selecting a random CSV link from the list
    fetch_command = f"curl -o {datadir}{random_csv_link} {base_url}{year}/{random_csv_link}"  # Fetching the random CSV file
    os.system(fetch_command)  # Executing the curl command to download the CSV file
    csv_file_path = f"{datadir}{random_csv_link}"  # Getting the path to the downloaded CSV file
    
    # Check if the downloaded file is valid and filter it if necessary
    if os.path.exists(csv_file_path) and is_file_valid(csv_file_path):  # Checking if file exists and is valid
        df = pd.read_csv(csv_file_path)  # Reading the CSV file into a DataFrame
        
        # Filtering valid columns based on specific pairs
        pairs = [
            ('DailyAverageDryBulbTemperature', 'MonthlyMeanTemperature'),
            ('DailyMaximumDryBulbTemperature', 'MonthlyMaximumTemperature'),
            ('DailyMinimumDryBulbTemperature', 'MonthlyMinimumTemperature')
        ]
        
        filtered_cols = []  # Initializing list for filtered columns
        for daily_col, monthly_col in pairs:
            if daily_col in df.columns and monthly_col in df.columns:
                filtered_cols.append(daily_col)  # Adding daily column to filtered list
                filtered_cols.append(monthly_col)  # Adding monthly column to filtered list
                
        df.dropna(subset=filtered_cols, how='all', inplace=True)  # Removing rows with all NaN values in filtered columns
        
        if len(filtered_cols) > 0:  # Checking if any filtered columns exist
            filtered_df = df[['DATE'] + filtered_cols]  # Selecting DATE and filtered columns
            
            # Extracting month from date column and saving filtered data to new CSV file
            filtered_df['DATE'] = filtered_df['DATE'].apply(extract_month)  # Extracting month from date column
            filtered_file_path = os.path.join(datadir, f'filtered_{os.path.basename(csv_file_path)}')  # Generating filtered file path
            filtered_df.to_csv(filtered_file_path, index=False)  # Saving filtered DataFrame to CSV file
            
            filtered_files += 1  # Incrementing filtered files counter
            os.remove(csv_file_path)  # Removing the original CSV file
            print(f"Filtered file created: {filtered_file_path}")  # Printing confirmation message
        else:
            os.remove(csv_file_path)  # Removing the original CSV file if no valid columns found
            print(f"No valid columns found in {csv_file_path}. Deleted the file.")
    else:
        os.remove(csv_file_path)  # Removing the original CSV file if not valid
        print(f"No valid columns found in {csv_file_path}. Deleted the file.")
    csv_links.remove(random_csv_link)  # Remove the processed CSV link from the list

print(f"Total filtered files created: {filtered_files}")
