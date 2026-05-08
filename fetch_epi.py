import requests
import pandas as pd
import os
from datetime import datetime, timedelta

def fetch_owid():
    """Fetch latest OWID COVID-19 data"""
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    print("Fetching OWID COVID data...")
    try:
        df = pd.read_csv(url, parse_dates=['date'])
        print(f"Fetched {len(df):,} rows of OWID data")
        
        # Keep relevant columns
        cols = ['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases', 
                'new_cases_smoothed', 'total_deaths', 'new_deaths', 'new_deaths_smoothed',
                'new_vaccinations_smoothed', 'population', 'people_vaccinated_per_hundred']
        
        df = df[[c for c in cols if c in df.columns]].copy()
        
        # Filter to last 6 months to keep file size manageable
        cutoff = datetime.now() - timedelta(days=180)
        recent_df = df[df['date'] >= cutoff].copy()
        
        return recent_df
    except Exception as e:
        print(f"OWID fetch failed: {e}")
        return pd.DataFrame()

def fetch_who_events():
    """Attempt to fetch recent WHO Disease Outbreak News"""
    try:
        r = requests.get("https://www.who.int/api/news/diseaseoutbreaknews", timeout=20)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame(data)
        print(f"WHO events: fetched {len(df)} items")
        return df
    except Exception as e:
        print(f"WHO events fetch failed (using placeholder): {e}")
        # Fallback
        today = datetime.now().strftime('%Y-%m-%d')
        return pd.DataFrame([{
            'date': today,
            'title': 'Daily Epi Update - OWID refreshed',
            'description': 'COVID-19 data updated from Our World in Data. WHO outbreaks fetch had temporary issue.',
            'source': 'Our World in Data / WHO'
        }])

def main():
    print("Starting upgraded daily epi update with OWID...")
    os.makedirs("data", exist_ok=True)
    
    # Main signals from OWID
    signals_df = fetch_owid()
    if not signals_df.empty:
        signals_df.to_csv("data/global_signals.csv", index=False)
        print(f"✅ Saved global_signals.csv with {len(signals_df):,} rows (last 6 months)")
    else:
        print("⚠️  No new signals data - keeping existing")
    
    # Events
    events_df = fetch_who_events()
    events_df.to_csv("data/significant_events.csv", index=False)
    print("✅ Saved significant_events.csv")
    
    print(f"🎉 Daily epi update completed successfully at {datetime.now()}")

if __name__ == "__main__":
    main()