# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# plot data with seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(x="week", y="differential", hue="team", data=nfl_regular)
plt.title("Differential vs Week by Team")
plt.show()

# plot data with matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
teams = nfl_regular["team"].unique()
for team in teams:
    team_data = nfl_regular[nfl_regular["team"] == team]
    ax.plot(team_data["week"], team_data["differential"], label=team)
ax.set_title("Differential vs Week by Team")
ax.set_xlabel("Week")
ax.set_ylabel("Differential")
ax.legend()
plt.show()

# TODO: add "week 0"
# TODO: make plot better
