import requests
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_delphi():
    try:
        url = "https://api.delphi.cmu.edu/epidata/api.php"
        # Use recent dates only
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')  # last year
        params = {
            "source": "covidcast",
            "signal": "fb-survey:smoothed_cli",
            "geo_type": "country",
            "geo_id": "*",
            "time_type": "day",
            "time_values": f"{start_date}:{end_date}"
        }
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        json_data = r.json()
        if 'epidata' in json_data and json_data.get('epidata'):
            data = pd.DataFrame(json_data['epidata'])
            print(f"Delphi: fetched {len(data)} rows")
            return data
        else:
            print("Delphi: No epidata returned")
            return pd.DataFrame()
    except Exception as e:
        print(f"Delphi fetch failed (expected for deprecated API): {e}")
        return pd.DataFrame()

def fetch_who_outbreaks():
    try:
        # Note: WHO endpoint may need update; current may not be public JSON
        r = requests.get("https://www.who.int/api/news/diseaseoutbreaknews", timeout=30)
        r.raise_for_status()
        json_data = r.json()
        events = pd.DataFrame(json_data)
        print(f"WHO: fetched {len(events)} events")
        return events
    except Exception as e:
        print(f"WHO fetch failed: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    print("Starting daily epi update...")
    df_signals = fetch_delphi()
    df_events = fetch_who_outbreaks()
    
    os.makedirs("data", exist_ok=True)
    
    # Only save if we have data (preserve existing otherwise)
    if not df_signals.empty:
        df_signals.to_csv("data/global_signals.csv", index=False)
        print("Saved global_signals.csv")
    else:
        print("No new signals data - keeping existing")
    
    if not df_events.empty:
        df_events.to_csv("data/significant_events.csv", index=False)
        print("Saved significant_events.csv")
    else:
        print("No new events data - keeping existing")
    
    print(f"Daily epi update completed at {datetime.now()}")