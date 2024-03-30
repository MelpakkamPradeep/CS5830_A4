import random
import os
import pandas as pd
import yaml
import requests
from bs4 import BeautifulSoup

# Function to read parameters from a YAML file
def read_params_from_yaml(file_path):
    with open(file_path, 'r') as file:
        params = yaml.safe_load(file)
    return params

# Function to fetch the HTML page containing location-wise datasets
def fetch_html_page(base_url, year, datadir):
    html_file = f"{datadir}/ncei_data_{year}.html"
    fetch_command = f"curl -o {html_file} {base_url}{year}/"
    os.system(fetch_command)
    return html_file

# Function to check if a file is valid based on the required conditions
def is_file_valid(file_path):
    df = pd.read_csv(file_path)
    
    required_columns = [
        'DailyAverageDryBulbTemperature', 'DailyMaximumDryBulbTemperature', 'DailyMinimumDryBulbTemperature',
        'MonthlyMaximumTemperature', 'MonthlyMeanTemperature', 'MonthlyMinimumTemperature'
    ]
    
    if all(col not in df.columns or df[col].isnull().all() for col in required_columns):
        return False
    
    pairs = [
        ('DailyAverageDryBulbTemperature', 'MonthlyMeanTemperature'),
        ('DailyMaximumDryBulbTemperature', 'MonthlyMaximumTemperature'),
        ('DailyMinimumDryBulbTemperature', 'MonthlyMinimumTemperature')
    ]
    
    for daily_col, monthly_col in pairs:
        if daily_col in df.columns and monthly_col in df.columns:
            if not df[daily_col].notna().any() and not df[monthly_col].notna().any():
                return False
    
    return True
    
# Function to extract the month from the date column
def extract_month(date_str):
    return pd.to_datetime(date_str).strftime('%m')

# Specify directories, URLs, and parameters
paramsdir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/params/"     
base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/"
datadir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/data/" 
params = read_params_from_yaml(f"{paramsdir}params.yaml")
year = params['ncei']['year']
n_locs = params['ncei']['n_locs']

# Step 1: Fetch the page containing the location-wise datasets
html_file = fetch_html_page(base_url, year, datadir)

# Step 2: Read the HTML file to extract CSV file links
with open(html_file, 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
csv_links = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.csv')]

# Step 3: Process random CSV files until n_locs filtered files are present in datadir
filtered_files = 0
while filtered_files < n_locs and len(csv_links) > 0:
    random_csv_link = random.choice(csv_links)
    fetch_command = f"curl -o {datadir}{random_csv_link} {base_url}{year}/{random_csv_link}"
    os.system(fetch_command)
    csv_file_path = f"{datadir}{random_csv_link}"
    
    # Check if the downloaded file is valid and filter it if necessary
    if os.path.exists(csv_file_path) and is_file_valid(csv_file_path):
        df = pd.read_csv(csv_file_path)
        
        # Filter columns with Daily* and Monthly* columns having the same suffix
        pairs = [
            ('DailyAverageDryBulbTemperature', 'MonthlyMeanTemperature'),
            ('DailyMaximumDryBulbTemperature', 'MonthlyMaximumTemperature'),
            ('DailyMinimumDryBulbTemperature', 'MonthlyMinimumTemperature')
        ]
        
        filtered_cols = []
        for daily_col, monthly_col in pairs:
            if daily_col in df.columns and monthly_col in df.columns:
                filtered_cols.append(daily_col)
                filtered_cols.append(monthly_col)
                
        # Remove rows with no values in the required columns
        df.dropna(subset=filtered_cols, how='all', inplace=True)
        
        if len(filtered_cols) > 0:
            filtered_df = df[['DATE'] + filtered_cols]
            
            # Extract month from the date column
            filtered_df['DATE'] = filtered_df['DATE'].apply(extract_month)
            
            # Specify the path for the new filtered CSV file
            filtered_file_path = os.path.join(datadir, f'filtered_{os.path.basename(csv_file_path)}')
            
            # Save the filtered DataFrame to the new CSV file
            filtered_df.to_csv(filtered_file_path, index=False)
            
            filtered_files += 1
            print(f"Filtered file created: {filtered_file_path}")
        else:
            os.remove(csv_file_path)
            print(f"No valid columns found in {csv_file_path}. Deleted the file.")
    else:
        os.remove(csv_file_path)
        print(f"No valid columns found in {csv_file_path}. Deleted the file.")
    csv_links.remove(random_csv_link)  # Remove the processed CSV link from the list

print(f"Total filtered files created: {filtered_files}")
