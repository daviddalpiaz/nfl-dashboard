# imports
import pandas as pd
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from lets_plot import *
from utils import glimpse

# get data
url = "https://www.pro-football-reference.com/years/2023/games.htm"
nfl_2023 = pd.read_html(url)[0]
nfl_2023 = nfl_2023[nfl_2023["Date"] != "Playoffs"]


# week
# team
# wins
# loss
# tie
# diff
np.sum(nfl_2023["PtsW"] == nfl_2023["PtsL"])

nfl_winners = nfl_2023[["Week", "Winner/tie"]]
nfl_losers = nfl_2023[["Week", "Loser/tie"]]

nfl_winners = nfl_winners.rename(columns={'Week': 'week'})
nfl_winners = nfl_winners.rename(columns={'Winner/tie': 'team'})

nfl_losers = nfl_losers.rename(columns={'Week': 'week'})
nfl_losers = nfl_losers.rename(columns={'Loser/tie': 'team'})

nfl_winners["outcome"] = 1
nfl_losers["outcome"] = -1

nfl_winners
nfl_losers
nfl = pd.concat([nfl_winners, nfl_losers], ignore_index=True)

playoff_rounds = ['ConfChamp', 'Division', 'SuperBowl', 'Week', 'WildCard']
nfl_2023_regular = nfl[~nfl['week'].isin(playoff_rounds)]
nfl_2023_regular["week"] = nfl_2023_regular["week"].astype(int)

nfl_2023_regular = nfl_2023_regular.sort_values(['team', 'week'])
nfl_2023_regular['outcome_cumsum'] = nfl_2023_regular.groupby('team')['outcome'].cumsum()
nfl_2023_regular[nfl_2023_regular["team"] == "San Francisco 49ers"]
nfl_2023_regular = nfl_2023_regular.drop("outcome", axis=1)
nfl_2023_regular = nfl_2023_regular.rename(columns={'outcome_cumsum': 'differential'})

nfl_2023_regular

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.lineplot(x='week', y='differential', hue='team', data=nfl_2023_regular)
plt.title('Differential vs Week by Team')
plt.show()
