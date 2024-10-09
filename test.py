import tkinter as tk
from tkinter import ttk
import random
import requests
import json

class NFLParlayApp:
    def __init__(self, master):
        self.master = master
        self.master.title("NFL Parlay Betting")
        self.master.geometry("800x600")

        self.games = []
        self.selected_games = []
        self.checkbuttons = []  # Store checkbutton references

        self.create_widgets()
        self.update_games()  # Fetch current week's games

    def create_widgets(self):
        # Create a frame for the games list
        games_frame = ttk.LabelFrame(self.master, text="This Week's Games")
        games_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create a canvas and scrollbar for the games list
        canvas = tk.Canvas(games_frame)
        scrollbar = ttk.Scrollbar(games_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add games to the scrollable frame
        self.scrollable_frame = scrollable_frame  # Keep a reference for refresh
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create a frame for the parlay information
        parlay_frame = ttk.LabelFrame(self.master, text="Your Parlay")
        parlay_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.parlay_info = tk.Text(parlay_frame, wrap=tk.WORD, width=40, height=15)
        self.parlay_info.pack(padx=5, pady=5, fill="both", expand=True)

    def get_game_data(self):
        # Replace with the correct ESPN API endpoint for current week's games
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=2024&seasontype=2&week=6"
        response = requests.get(url)

        print(f"Response Status Code: {response.status_code}")  # Debug line
        if response.status_code == 200:
            data = response.json()
            games = []
            for event in data.get('events', []):
                home_team = event['competitions'][0]['competitors'][0]['team']
                away_team = event['competitions'][0]['competitors'][1]['team']
                odds = random.uniform(1.5, 3.0)  # Simulated odds
                date_time = event['date']
                games.append({
                    "home": home_team['displayName'],
                    "away": away_team['displayName'],
                    "odds": odds,
                    "date": date_time.split("T")[0],
                    "time": date_time.split("T")[1][:5]  # Just getting the time part
                })
            return games
        else:
            print(f"Response Content: {response.text}")  # Debug line
            return None

    def update_games(self):
        current_games = self.get_game_data()
        if current_games:
            self.games = current_games
            self.selected_games.clear()  # Clear previously selected games
            self.update_parlay_info()     # Refresh the parlay info
            self.refresh_checkbuttons()    # Update checkbuttons
        else:
            print("Error fetching current games.")

    def refresh_checkbuttons(self):
        # Clear existing checkbuttons
        for cb, _ in self.checkbuttons:
            cb.destroy()
        self.checkbuttons.clear()

        # Recreate checkbuttons for the new games
        for index, game in enumerate(self.games):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.scrollable_frame, text=f"{game['away']} @ {game['home']} - {game['date']} {game['time']} (Odds: {game['odds']:.2f})", 
                                 variable=var, command=lambda g=game, v=var: self.toggle_game(g, v))
            cb.grid(row=index, column=0, sticky="w", padx=5, pady=2)
            self.checkbuttons.append((cb, var))

    def toggle_game(self, game, var):
        if var.get():
            self.selected_games.append(game)
        else:
            self.selected_games = [g for g in self.selected_games if g['home'] != game['home'] and g['away'] != game['away']]
        self.update_parlay_info()

    def update_parlay_info(self):
        self.parlay_info.delete(1.0, tk.END)
        if not self.selected_games:
            self.parlay_info.insert(tk.END, "Select games to create your parlay")
        else:
            for game in self.selected_games:
                self.parlay_info.insert(tk.END, f"{game['away']} @ {game['home']} - Odds: {game['odds']:.2f}\n")
            
            probability = self.calculate_probability()
            potential_payout = self.calculate_potential_payout()
            total_odds = self.calculate_total_odds()

            self.parlay_info.insert(tk.END, f"\nWin Probability: {probability:.2f}%\n")
            self.parlay_info.insert(tk.END, f"Potential Payout: ${potential_payout:.2f}\n")
            self.parlay_info.insert(tk.END, f"Total Odds: {total_odds:.2f}\n")

    def calculate_probability(self):
        return (1 / self.calculate_total_odds()) * 100 if self.selected_games else 0

    def calculate_potential_payout(self):
        return self.calculate_total_odds() * 10  # Assuming $10 bet

    def calculate_total_odds(self):
        if not self.selected_games:
            return 1
        total_odds = 1
        for game in self.selected_games:
            total_odds *= game['odds']
        return total_odds

if __name__ == "__main__":
    root = tk.Tk()
    app = NFLParlayApp(root)
    root.mainloop()
