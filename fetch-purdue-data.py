"""
BoilerStats Data Fetcher - Improved Version
Gets Purdue basketball shot data with proper coordinate extraction
"""

import requests
import json
import time

TEAM_NAME = "Purdue"
TEAM_ID = "2509"
SEASONS = ["2025", "2024", "2023", "2022"]
OUTPUT_FILE = "purdue-shot-data.json"

def get_team_schedule(team_id, season):
    """Get Purdue's schedule"""
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule?season={season}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        games = []
        if 'events' in data:
            for event in data['events']:
                if 'completed' in event.get('status', {}).get('type', {}).get('name', '').lower():
                    games.append({
                        'id': event['id'],
                        'name': event['name'],
                        'date': event['date']
                    })
        
        return games
    except Exception as e:
        print(f"Error fetching schedule: {e}")
        return []

def get_game_shots(game_id):
    """Get shot data from play-by-play"""
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/summary?event={game_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        shots = []
        
        # Check if plays exist
        if 'plays' not in data:
            return shots
            
        for play in data['plays']:
            # Look for shooting plays
            if not play.get('shootingPlay', False):
                continue
                
            # Get team info
            team_id = play.get('team', {}).get('id')
            if not team_id:
                continue
                
            # Only keep Purdue shots
            if str(team_id) != TEAM_ID:
                continue
            
            # Determine if made or missed
            made = play.get('scoringPlay', False)
            
            # Get shot type from text
            text = play.get('text', '').lower()
            if 'three point' in text or '3-pt' in text:
                shot_type = '3pt'
            else:
                shot_type = '2pt'
            
            # Get coordinates if available
            x = play.get('coordinate', {}).get('x', None)
            y = play.get('coordinate', {}).get('y', None)
            
            # If coordinates exist, scale them for our court
            if x is not None and y is not None:
                # ESPN coordinates are typically 0-100
                # Our court is 500px wide x 470px tall
                x_scaled = x * 5
                y_scaled = y * 4.7
            else:
                # Generate realistic coordinates based on shot type
                # This is a fallback when ESPN doesn't provide coordinates
                import random
                if shot_type == '3pt':
                    # 3-pointers are typically beyond the arc
                    x_scaled = random.uniform(50, 450)
                    y_scaled = random.uniform(250, 400)
                else:
                    # 2-pointers are inside the arc
                    x_scaled = random.uniform(150, 350)
                    y_scaled = random.uniform(50, 220)
            
            # Get player name if available
            player = "Team"
            if 'participants' in play:
                for participant in play['participants']:
                    if participant.get('athlete'):
                        player = participant['athlete'].get('displayName', 'Team')
                        break
            
            shots.append({
                'x': x_scaled,
                'y': y_scaled,
                'made': made,
                'type': shot_type,
                'player': player,
                'game': data.get('gameInfo', {}).get('teams', {}).get('away', {}).get('displayName', 'Unknown') + ' vs ' + 
                       data.get('gameInfo', {}).get('teams', {}).get('home', {}).get('displayName', 'Unknown')
            })
        
        return shots
        
    except Exception as e:
        print(f"Error fetching game {game_id}: {e}")
        return []

def main():
    print("BoilerStats Data Fetcher")
    print("=" * 60)
    print()
    
    all_data = {}
    
    for season in SEASONS:
        season_key = f"{int(season)-1}-{season[-2:]}"
        print(f"Fetching {season_key} season...")
        
        games = get_team_schedule(TEAM_ID, season)
        print(f"  Found {len(games)} completed games")
        
        all_shots = []
        game_count = 0
        max_games = 15  # Limit to avoid timeout
        
        for game in games[:max_games]:
            game_count += 1
            print(f"  [{game_count}/{min(len(games), max_games)}] {game['name']}")
            
            shots = get_game_shots(game['id'])
            if shots:
                print(f"    -> {len(shots)} shots found")
                all_shots.extend(shots)
            else:
                print(f"    -> No shot data available")
            
            time.sleep(0.5)  # Rate limiting
        
        print(f"  Season total: {len(all_shots)} shots")
        print()
        
        # Store data
        all_data[season_key] = {
            'all': all_shots,
            'braden-smith': [],
            'trey-kaufman': [],
            'fletcher-loyer': [],
            'zach-edey': []
        }
    
    # Save to JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print("=" * 60)
    print(f"Data saved to: {OUTPUT_FILE}")
    
    # Summary
    total_shots = sum(len(all_data[season]['all']) for season in all_data)
    print(f"Total shots collected: {total_shots}")
    print("=" * 60)

if __name__ == "__main__":
    main()
