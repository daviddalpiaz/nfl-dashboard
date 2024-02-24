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

# get list of teams
teams = nfl_regular["team"].unique()

# create a df with a week of 0 and a differential of 0 for each team
week_zero = pd.DataFrame({"team": teams, "week": 0, "outcome": 0})

# add week 0 to full data
nfl_regular = pd.concat([week_zero, nfl_regular], ignore_index=True)

# view full data
nfl_regular

# thanks to CoPilot and all the open source maintainers who provided code
# the following prompt was used to generate some of the code below
# TODO: insert rows for bye week
# TODO: create win column, create loss column
# TODO: cumulative sum to get record for each week
# TODO: diff the cumulative win and loss column to get differential

# get arrays of teams and weeks
teams = nfl_regular["team"].unique()
weeks = nfl_regular["week"].unique()

# create a DataFrame with all possible team-week combinations
all_combinations = pd.MultiIndex.from_product([teams, weeks], names=["team", "week"]).to_frame(index=False)

# merge with the existing DataFrame and fill missing values
nfl_regular = pd.merge(all_combinations, nfl_regular, on=["team", "week"], how="left")
nfl_regular["outcome"].fillna(0, inplace=True)

# create win and loss columns
nfl_regular["win"] = np.where(nfl_regular["outcome"] == 1, 1, 0)
nfl_regular["loss"] = np.where(nfl_regular["outcome"] == -1, 1, 0)

# get cumulative sum of wins and losses for each team
nfl_regular["cumulative_win"] = nfl_regular.groupby("team")["win"].cumsum()
nfl_regular["cumulative_loss"] = nfl_regular.groupby("team")["loss"].cumsum()

# get differential
nfl_regular["differential"] = nfl_regular["cumulative_win"] - nfl_regular["cumulative_loss"]

# remove 'win', 'loss', and 'outcome' columns
nfl_regular = nfl_regular.drop(columns=["win", "loss", "outcome"])

# rename 'cumulative_win' to 'wins' and 'cumulative_loss' to 'losses'
nfl_regular = nfl_regular.rename(columns={"cumulative_win": "wins", "cumulative_loss": "losses"})

# spot check an individual team
nfl_regular[nfl_regular["team"] == "San Francisco 49ers"]

# write processed data to disk
nfl_regular.to_csv("data/nfl.csv", index=False)

# create list of team information
teams_list = [
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
teams_list = pd.DataFrame(teams_list, columns=["abbreviation", "full_name", "conference", "division"])
teams_list.to_csv("data/teams.csv", index=False)
