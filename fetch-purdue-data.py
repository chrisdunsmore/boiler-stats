“””
BoilerStats Data Fetcher - Python Version
Scrapes Purdue basketball shot data from ESPN and saves as JSON
“””

import requests
import json
from datetime import datetime
import time

# Configuration

TEAM_NAME = “Purdue Boilermakers”
TEAM_ID = “2509”  # Purdue’s ESPN team ID
SEASONS = [“2025”, “2024”, “2023”, “2022”]  # Year the season ends
OUTPUT_FILE = “purdue-shot-data.json”

def get_team_schedule(team_id, season):
“”“Get Purdue’s game schedule for a season”””
url = f”https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule?season={season}”

```
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    games = []
    if 'events' in data:
        for event in data['events']:
            games.append({
                'id': event['id'],
                'name': event['name'],
                'date': event['date']
            })
    
    return games
except Exception as e:
    print(f"Error fetching schedule: {e}")
    return []
```

def get_game_pbp(game_id):
“”“Get play-by-play data for a game including shot locations”””
url = f”https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/summary?event={game_id}”

```
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    shots = []
    
    # Extract shot data from plays
    if 'plays' in data:
        for play in data['plays']:
            if 'scoringPlay' in play or 'shotPlay' in play:
                # This is a simplified version - ESPN's API structure varies
                shot = {
                    'text': play.get('text', ''),
                    'type': play.get('type', {}).get('text', ''),
                    'made': play.get('scoringPlay', False),
                    'period': play.get('period', {}).get('number', 1)
                }
                
                # Try to extract coordinates if available
                if 'coordinate' in play:
                    shot['x'] = play['coordinate'].get('x', 0)
                    shot['y'] = play['coordinate'].get('y', 0)
                else:
                    # Generate pseudo-random coordinates based on shot type
                    # This is a fallback - real coordinates may not be in ESPN API
                    shot['x'] = 0
                    shot['y'] = 0
                
                shots.append(shot)
    
    return shots
except Exception as e:
    print(f"Error fetching game {game_id}: {e}")
    return []
```

def format_shot_data(shots, game_name):
“”“Format shots for the website”””
formatted = []

```
for shot in shots:
    # Determine shot type
    shot_type = "3pt" if "three" in shot['text'].lower() else "2pt"
    
    # Scale coordinates (adjust based on actual coordinate system)
    x = shot.get('x', 250) * 2  # Default to middle if no coords
    y = shot.get('y', 200) * 2
    
    formatted.append({
        'x': x,
        'y': y,
        'made': shot.get('made', False),
        'type': shot_type,
        'player': 'Team',  # Can be enhanced with player name extraction
        'game': game_name
    })

return formatted
```

def main():
print(“BoilerStats Data Fetcher (Python)”)
print(”=” * 50)
print()

```
all_data = {}

for season in SEASONS:
    season_key = f"{int(season)-1}-{season[-2:]}"
    print(f"Fetching {season_key} season...")
    
    # Get schedule
    games = get_team_schedule(TEAM_ID, season)
    print(f"  Found {len(games)} games")
    
    all_shots = []
    
    for game in games[:5]:  # Limit to first 5 games for testing
        print(f"  Processing: {game['name']}")
        shots = get_game_pbp(game['id'])
        formatted_shots = format_shot_data(shots, game['name'])
        all_shots.extend(formatted_shots)
        time.sleep(1)  # Be nice to the API
    
    print(f"  Total shots: {len(all_shots)}\n")
    
    all_data[season_key] = {
        'all': all_shots
    }

# Save to JSON
with open(OUTPUT_FILE, 'w') as f:
    json.dump(all_data, f, indent=2)

print("=" * 50)
print(f"Data saved to: {OUTPUT_FILE}")
print("Upload this file to your GitHub repo")
print("=" * 50)
```

if **name** == “**main**”:
main()
