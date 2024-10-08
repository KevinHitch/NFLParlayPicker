import requests
import json
from tkinter import *
from tkinter import scrolledtext

def get_game_data():
    # Replace with the correct ESPN API endpoint
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def analyze_games(data):
    results = ""
    if data is not None:
        for event in data.get('events', []):
            home_team = event['competitions'][0]['competitors'][0]
            away_team = event['competitions'][0]['competitors'][1]
            home_score = home_team['score']
            away_score = away_team['score']
            
            results += f"{home_team['team']['displayName']} ({home_score}) vs {away_team['team']['displayName']} ({away_score})\n"
            if home_score > away_score:
                results += f"{home_team['team']['displayName']} wins!\n\n"
            elif home_score < away_score:
                results += f"{away_team['team']['displayName']} wins!\n\n"
            else:
                results += "It's a tie!\n\n"
    else:
        results = "Error fetching data from ESPN API."
    
    return results

def fetch_and_display():
    game_data = get_game_data()
    results = analyze_games(game_data)
    output_area.delete(1.0, END)  # Clear previous output
    output_area.insert(END, results)  # Insert new results

# Create the main window
root = Tk()
root.title("ESPN Game Results")
root.geometry("500x400")

# Create a button to fetch results
fetch_button = Button(root, text="Fetch Game Results", command=fetch_and_display)
fetch_button.pack(pady=10)

# Create a scrolled text area to display results
output_area = scrolledtext.ScrolledText(root, wrap=WORD, width=60, height=20)
output_area.pack(pady=10)

# Run the application
root.mainloop()
