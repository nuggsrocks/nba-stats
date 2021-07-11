import re
from sklearn import linear_model
from scipy import stats
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import find_teams

url = 'https://www.basketball-reference.com/leagues/NBA_2021.html'

time1 = time.time()

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

strings = soup.find_all(string=re.compile('Total Stats'))

table = None

for string in strings:
    for parent in string.parents:
        if parent.name == 'table' and 'team' in parent.attrs['id']:
            table = parent

dataframe = pd.read_html(str(table))[0]


def compare_teams(team_names, stat_key):
    team_stats = dataframe.loc[dataframe['Team'].str.contains('|'.join(team_names))]

    team_stats = team_stats.sort_values(by=[stat_key], ascending=False, ignore_index=True)

    delta = team_stats[stat_key].diff()[1] / team_stats.iloc[0]['G']

    print(f'The {team_stats.iloc[0]["Team"]} had {abs(delta):.2f} more {stat_key} per game than the {team_stats.iloc[1]["Team"]}')


dataframe = dataframe.drop([30])


def map_to_per_game_values(series):
    return series.map(lambda x: x / 72 if type(x) == int else x)


per_game_df = dataframe.apply(map_to_per_game_values, axis=1)

y = per_game_df['PTS']

correlated_values = []

for key in per_game_df.keys():
    if re.match('Team|Rk|G|MP|PTS', key) is None:
        x = per_game_df[key]

        res = stats.linregress(x, y)

        if res.rvalue > 0.5:
            correlated_values.append(key)

X = per_game_df[correlated_values]

regression = linear_model.LinearRegression()

regression.fit(X, y)

team = per_game_df.iloc[0]

predicted = regression.predict([[team['FG'], team['FG%'], team['3P%'], team['2P%']]])

print(f'{team["Team"]} - predicted average points: {predicted[0]:.2f}, actual average: {team["PTS"]:.2f}')
team_links_df = find_teams.create_team_links_df()


def strip_asterisks_from_team_names(dataframe):
    def df_apply(series):
        return series.map(lambda x: x.replace('*', '') if type(x) is str else x)

    return dataframe.apply(df_apply)


per_game_df = strip_asterisks_from_team_names(per_game_df)

combined_df = team_links_df.set_index('Name').join(per_game_df.set_index('Team'))

print(f'it took {time.time() - time1:.2f} seconds')
