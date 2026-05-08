import requests
import pandas as pd
from datetime import datetime
import os

def fetch_who_global_data():
    """Fetch latest WHO global COVID-19 daily data."""
    url = 'https://srhdpeuwpubsa.blob.core.windows.net/whdh/COVID/WHO-COVID-19-global-daily-data.csv'
    try:
        print(f'Fetching WHO global data from {url}...')
        df = pd.read_csv(url)
        print(f'Success: fetched {len(df):,} rows of WHO data. Columns: {list(df.columns)}')
        # Ensure date column is datetime
        if 'Date_reported' in df.columns:
            df['Date_reported'] = pd.to_datetime(df['Date_reported'])
        return df
    except Exception as e:
        print(f'WHO global data fetch failed: {e}')
        return pd.DataFrame()

def fetch_owid_data():
    """Fetch latest OWID COVID data (more comprehensive)."""
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    try:
        print(f'Fetching OWID data from {url}...')
        # Use low_memory=False for large file
        df = pd.read_csv(url, low_memory=False)
        print(f'Success: fetched {len(df):,} rows of OWID data.')
        return df
    except Exception as e:
        print(f'OWID data fetch failed: {e}')
        return pd.DataFrame()

if __name__ == '__main__':
    print('Starting daily epi update...')
    
    # Fetch primary data sources
    who_df = fetch_who_global_data()
    owid_df = fetch_owid_data()
    
    os.makedirs('data', exist_ok=True)
    
    # Save primary signals (WHO daily is reliable and current)
    if not who_df.empty:
        who_df.to_csv('data/global_signals.csv', index=False)
        print('Saved updated global_signals.csv from WHO data')
    else:
        print('No WHO data - keeping existing global_signals.csv')
    
    # Save full OWID data as well (for richer dashboard use)
    if not owid_df.empty:
        owid_df.to_csv('data/owid-covid-data.csv', index=False)
        print('Saved full owid-covid-data.csv')
    
    # Optional: create a lightweight world aggregates if needed
    print(f'Daily epi update completed successfully at {datetime.now()}')