# imports
import pandas as pd
import numpy as np

# get data
url = "https://www.pro-football-reference.com/years/2023/games.htm"
nfl_games = pd.read_html(url)[0]

# remove row without real data
nfl_games = nfl_games[nfl_games["Date"] != "Playoffs"]

# check for no ties
assert np.sum(nfl_games["PtsW"] == nfl_games["PtsL"]) == 0

# split data into winners and losers
nfl_winners = nfl_games[["Week", "Winner/tie"]]
nfl_losers = nfl_games[["Week", "Loser/tie"]]

# rename columns
nfl_winners = nfl_winners.rename(columns={"Week": "week", "Winner/tie": "team"})
nfl_losers = nfl_losers.rename(columns={"Week": "week", "Loser/tie": "team"})

# add outcome variable 1 = win, -1 = lose
nfl_winners["outcome"] = 1
nfl_losers["outcome"] = -1

# create somewhat tidy data
nfl = pd.concat([nfl_winners, nfl_losers], ignore_index=True)

# define weeks that are not the regular season
playoff_rounds = ["ConfChamp", "Division", "SuperBowl", "Week", "WildCard"]

# subset to regular season games
nfl_regular = nfl[~nfl["week"].isin(playoff_rounds)]

# coerce week variable to be int
nfl_regular.loc[:, "week"] = nfl_regular["week"].astype(int)

# create weekly win-loss differential
nfl_regular = nfl_regular.sort_values(["team", "week"])
nfl_regular["differential"] = nfl_regular.groupby("team")["outcome"].cumsum()
nfl_regular = nfl_regular.drop("outcome", axis=1)

# get list of teams
teams = nfl_regular["team"].unique()

# create a df with a week of 0 and a differential of 0 for each team
week_zero = pd.DataFrame({"team": teams, "week": 0, "differential": 0})

# add week 0 to full data
nfl_regular = pd.concat([week_zero, nfl_regular], ignore_index=True)

# view full data
nfl_regular

# spot check an individual team
nfl_regular[nfl_regular["team"] == "San Francisco 49ers"]

# write processed data to disk
nfl_regular.to_csv("data/nfl.csv", index=False)

# TODO: encode bye weeks into data!

# create list of team information
teams = [
    ["BUF", "Buffalo Bills", "AFC", "East"],
    ["MIA", "Miami Dolphins", "AFC", "East"],
    ["NYJ", "New York Jets", "AFC", "East"],
    ["NE", "New England Patriots", "AFC", "East"],
    ["BAL", "Baltimore Ravens", "AFC", "North"],
    ["CLE", "Cleveland Browns", "AFC", "North"],
    ["PIT", "Pittsburgh Steelers", "AFC", "North"],
    ["CIN", "Cincinnati Bengals", "AFC", "North"],
    ["HOU", "Houston Texans", "AFC", "South"],
    ["JAX", "Jacksonville Jaguars", "AFC", "South"],
    ["IND", "Indianapolis Colts", "AFC", "South"],
    ["TEN", "Tennessee Titans", "AFC", "South"],
    ["KC", "Kansas City Chiefs", "AFC", "West"],
    ["LV", "Las Vegas Raiders", "AFC", "West"],
    ["DEN", "Denver Broncos", "AFC", "West"],
    ["LAC", "Los Angeles Chargers", "AFC", "West"],
    ["DAL", "Dallas Cowboys", "NFC", "East"],
    ["PHI", "Philadelphia Eagles", "NFC", "East"],
    ["NYG", "New York Giants", "NFC", "East"],
    ["WAS", "Washington Commanders", "NFC", "East"],
    ["DET", "Detroit Lions", "NFC", "North"],
    ["GB", "Green Bay Packers", "NFC", "North"],
    ["MIN", "Minnesota Vikings", "NFC", "North"],
    ["CHI", "Chicago Bears", "NFC", "North"],
    ["TB", "Tampa Bay Buccaneers", "NFC", "South"],
    ["NO", "New Orleans Saints", "NFC", "South"],
    ["ATL", "Atlanta Falcons", "NFC", "South"],
    ["CAR", "Carolina Panthers", "NFC", "South"],
    ["SF", "San Francisco 49ers", "NFC", "West"],
    ["LAR", "Los Angeles Rams", "NFC", "West"],
    ["SEA", "Seattle Seahawks", "NFC", "West"],
    ["ARI", "Arizona Cardinals", "NFC", "West"],
]

# create df of team info and write to disk
teams = pd.DataFrame(teams, columns=["abbreviation", "full_name", "conference", "division"])
teams.to_csv("data/teams.csv", index=False)
