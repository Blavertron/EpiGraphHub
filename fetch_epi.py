import requests
import pandas as pd
from datetime import datetime
import os

# 1. Delphi Epidata (global signals + incidents proxy)
def fetch_delphi():
    url = "https://api.delphi.cmu.edu/epidata/api.php"
    params = {"source": "covidcast", "signal": "fb-survey:smoothed_cli", "geo_type": "country", "geo_id": "*", "time_type": "day", "time_values": "2024-01-01:2026-05-06"}  # adjust dates
    r = requests.get(url, params=params)
    data = pd.DataFrame(r.json()['epidata'])
    return data

# 2. WHO Disease Outbreak News (significant events)
def fetch_who_outbreaks():
    # Simple RSS or API pull for recent global alerts
    r = requests.get("https://www.who.int/api/news/diseaseoutbreaknews")
    events = pd.DataFrame(r.json())
    return events

# Run & save
if __name__ == "__main__":
    df_signals = fetch_delphi()
    df_events = fetch_who_outbreaks()
    
    os.makedirs("data", exist_ok=True)
    df_signals.to_csv("data/global_signals.csv", index=False)
    df_events.to_csv("data/significant_events.csv", index=False)
    
    print(f"✅ Updated {datetime.now()}")
