import json

# Simple test data generator for BoilerStats

# No API calls, just creates sample data structure

def main():
print(“Creating test data…”)

```
data = {
    "2024-25": {
        "all": [
            {"x": 250, "y": 100, "made": True, "type": "2pt", "player": "Team", "game": "Test Game 1"},
            {"x": 350, "y": 280, "made": True, "type": "3pt", "player": "Team", "game": "Test Game 1"},
            {"x": 150, "y": 290, "made": False, "type": "3pt", "player": "Team", "game": "Test Game 1"},
            {"x": 250, "y": 50, "made": True, "type": "2pt", "player": "Team", "game": "Test Game 2"},
            {"x": 200, "y": 300, "made": False, "type": "3pt", "player": "Team", "game": "Test Game 2"}
        ],
        "braden-smith": [],
        "trey-kaufman": [],
        "fletcher-loyer": [],
        "zach-edey": []
    },
    "2023-24": {
        "all": [],
        "braden-smith": [],
        "trey-kaufman": [],
        "fletcher-loyer": [],
        "zach-edey": []
    },
    "2022-23": {
        "all": [],
        "braden-smith": [],
        "trey-kaufman": [],
        "fletcher-loyer": [],
        "zach-edey": []
    }
}

with open("purdue-shot-data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Test data created successfully!")
```

if **name** == “**main**”:
main()
