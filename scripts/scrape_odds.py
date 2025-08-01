import pandas as pd
from datetime import datetime, timedelta
import random

def scrape_sportsbet():
    """Simulates scraping odds from Sportsbet."""
    return {"Labor": 1.50, "Coalition": 2.60}

def scrape_betr():
    """Simulates scraping odds from Betr."""
    return {"Labor": 1.52, "Coalition": 2.55}

def scrape_pointsbet():
    """Simulates scraping odds from Pointsbet."""
    return {"Labor": 1.48, "Coalition": 2.65}

def generate_mock_odds(base_odds):
    """Generates mock odds for the last 9 days based on the initial odds."""
    mock_data = []
    today = datetime.today()
    for i in range(1, 10):
        date = today - timedelta(days=i)
        for party, odds in base_odds.items():
            # Introduce some random variation
            mock_odds = round(odds + (random.random() - 0.5) * 0.1, 2)
            mock_data.append({"date": date.strftime("%Y-%m-%d"), "party": party, "odds": mock_odds, "bookmaker": "mock"})
    return mock_data

# Scrape real data for the first data point
today_str = datetime.today().strftime("%Y-%m-%d")
sportsbet_odds = scrape_sportsbet()
betr_odds = scrape_betr()
pointsbet_odds = scrape_pointsbet()

data = []
for party, odds in sportsbet_odds.items():
    data.append({"date": today_str, "party": party, "odds": odds, "bookmaker": "Sportsbet"})
for party, odds in betr_odds.items():
    data.append({"date": today_str, "party": party, "odds": odds, "bookmaker": "Betr"})
for party, odds in pointsbet_odds.items():
    data.append({"date": today_str, "party": party, "odds": odds, "bookmaker": "Pointsbet"})

# Generate mock data for the next 9 data points
base_odds = {
    "Labor": (sportsbet_odds["Labor"] + betr_odds["Labor"] + pointsbet_odds["Labor"]) / 3,
    "Coalition": (sportsbet_odds["Coalition"] + betr_odds["Coalition"] + pointsbet_odds["Coalition"]) / 3,
}
data.extend(generate_mock_odds(base_odds))

df = pd.DataFrame(data)

# Convert date to datetime objects
df['date'] = pd.to_datetime(df['date'])

# Calculate the average odds for each party on each day
avg_odds_df = df.groupby(['date', 'party'])['odds'].mean().reset_index()
avg_odds_df.rename(columns={'odds': 'average_odds'}, inplace=True)

# Calculate probability
avg_odds_df['probability'] = 1 / avg_odds_df['average_odds']

# Normalize probabilities
avg_odds_df['probability'] = avg_odds_df.groupby('date')['probability'].transform(lambda x: x / x.sum())

# Save to parquet
avg_odds_df.to_parquet("data/election_odds.parquet")

print("Scraped and mock data saved to data/election_odds.parquet")
