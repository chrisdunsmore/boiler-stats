"""
BoilerStats Data Fetcher - Python Version
Scrapes Purdue basketball shot data from ESPN and saves as JSON
"""

import requests
import json
from datetime import datetime
import time

# Configuration
TEAM_NAME = "Purdue Boilermakers"
TEAM_ID = "2509"
SEASONS = ["2025", "2024", "2023", "2022"]
OUTPUT_FILE = "purdue-shot-data.json"

def get_team_schedule(team_id, season):
    """Get Purdue's game schedule for a season"""
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule?season={season}"
    
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

def get_game_pbp(game_id):
    """Get play-by-play data for a game including shot locations"""
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/summary?event={game_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        shots = []
        
        if 'plays' in data:
            for play in data['plays']:
                if 'scoringPlay' in play or 'shotPlay' in play:
                    shot = {
                        'text': play.get('text', ''),
                        'type': play.get('type', {}).get('text', ''),
                        'made': play.get('scoringPlay', False),
                        'period': play.get('period', {}).get('number', 1)
                    }
                    
                    if 'coordinate' in play:
                        shot['x'] = play['coordinate'].get('x', 0)
                        shot['y'] = play['coordinate'].get('y', 0)
                    else:
                        shot['x'] = 0
                        shot['y'] = 0
                    
                    shots.append(shot)
        
        return shots
    except Exception as e:
        print(f"Error fetching game {game_id}: {e}")
        return []

def format_shot_data(shots, game_name):
    """Format shots for the website"""
    formatted = []
    
    for shot in shots:
        shot_type = "3pt" if "three" in shot['text'].lower() else "2pt"
        
        x = shot.get('x', 250) * 2
        y = shot.get('y', 200) * 2
        
        formatted.append({
            'x': x,
            'y': y,
            'made': shot.get('made', False),
            'type': shot_type,
            'player': 'Team',
            'game': game_name
        })
    
    return formatted

def main():
    print("BoilerStats Data Fetcher")
    print("=" * 50)
    print()
    
    all_data = {}
    
    for season in SEASONS:
        season_key = f"{int(season)-1}-{season[-2:]}"
        print(f"Fetching {season_key} season...")
        
        games = get_team_schedule(TEAM_ID, season)
        print(f"  Found {len(games)} games")
        
        all_shots = []
        
        for game in games[:10]:
            print(f"  Processing: {game['name']}")
            shots = get_game_pbp(game['id'])
            formatted_shots = format_shot_data(shots, game['name'])
            all_shots.extend(formatted_shots)
            time.sleep(1)
        
        print(f"  Total shots: {len(all_shots)}\n")
        
        all_data[season_key] = {
            'all': all_shots
        }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print("=" * 50)
    print(f"Data saved to: {OUTPUT_FILE}")
    print("=" * 50)

if __name__ == "__main__":
    main()
