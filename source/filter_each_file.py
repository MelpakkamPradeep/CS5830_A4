import pandas as pd
import os

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
    # Remove rows with no values in the required columns
    df.dropna(subset=required_columns, how='all', inplace=True)
    
    for daily_col, monthly_col in pairs:
        if daily_col in df.columns and monthly_col in df.columns:
            if not df[daily_col].notna().any() and not df[monthly_col].notna().any():
                print(df[daily_col].notna().any(), df[monthly_col].notna().any())
                return False
    
    return True

# Function to extract the month from the date column
def extract_month(date_str):
    return pd.to_datetime(date_str).strftime('%m')

def filter(csv_file_path):
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
            
            print(f"Filtered file created: {filtered_file_path}")
        else:
            os.remove(csv_file_path)
            print(f"No valid columns found in {csv_file_path}. Deleted the file.")
    else:
        os.remove(csv_file_path)
        print(f"No valid columns found in {csv_file_path}. Deleted the file.")

datadir = "/home/melpradeep/Desktop/CS5830/Assignment_4/CS5830_A4/data/" 
for csv in os.listdir(datadir):
	if csv.endswith('csv'):	
		filter(f"{datadir}{csv}")
