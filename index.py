import re

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

teams = [
    ['WAS', 'wizards', 'Washington', 'Wizards', ['#002b5c', '#e31837', '#002b5c']],
    ['UTA', 'jazz', 'Utah', 'Jazz', ['#002b5c', '#f9a01b', '#002b5c']],
    ['TOR', 'raptors', 'Toronto', 'Raptors', ['#000000', '#ce1141', '#000000']],
    ['SAS', 'spurs', 'San Antonio', 'Spurs', ['#061922', '#c4ced4', '#000000']],
    ['SAC', 'kings', 'Sacramento', 'Kings', ['#724c9f', '#5a2d81', '#5a2d81']],
    ['POR', 'blazers', 'Portland', 'Trail Blazers', ['#061922', '#e03a3e', '#e03a3e']],
    ['PHX', 'suns', 'Phoenix', 'Suns', ['#e56020', '#e56020', '#1d1160']],
    ['PHI', 'sixers', 'Philadelphia', '76ers', ['#ed174c', '#006bb6', '#006bb6']],
    ['ORL', 'magic', 'Orlando', 'Magic', ['#007dc5', '#0077c0', '#0077c0']],
    ['OKC', 'thunder', 'Oklahoma City', 'Thunder', ['#007dc3', '#007ac1', '#007ac1']],
    ['NYK', 'knicks', 'New York', 'Knicks', ['#006bb6', '#006bb6', '#006bb6']],
    ['NOP', 'pelicans', 'New Orleans', 'Pelicans', ['#002b5c', '#b4975a', '#002b5c']],
    ['MIN', 'timberwolves', 'Minnesota', 'Timberwolves', ['#005083', '#236192', '#0c2340']],
    ['MIL', 'bucks', 'Milwaukee', 'Bucks', ['#00471b', '#00471b', '#00471b']],
    ['MIA', 'heat', 'Miami', 'Heat', ['#98002e', '#98002E', '#98002e']],
    ['MEM', 'grizzlies', 'Memphis', 'Grizzlies', ['#7399c6', '#7399C6', '#5d76a9']],
    ['LAL', 'lakers', 'Los Angeles', 'Lakers', ['#552583', '#fdb927', '#552583']],
    ['LAC', 'clippers', 'LA', 'Clippers', ['#ed174c', '#c8102e', '#c8102e']],
    ['IND', 'pacers', 'Indiana', 'Pacers', ['#ffc633', '#fdbb30', '#002d62']],
    ['HOU', 'rockets', 'Houston', 'Rockets', ['#ce1141', '#ce1141', '#ce1141']],
    ['GSW', 'warriors', 'Golden State', 'Warriors', ['#fdb927', '#FDB927', '#006bb6']],
    ['DET', 'pistons', 'Detroit', 'Pistons', ['#006bb6', '#C80F2D', '#1d428a']],
    ['DEN', 'nuggets', 'Denver', 'Nuggets', ['#4d90cd', '#fec524', '#0e2240']],
    ['DAL', 'mavericks', 'Dallas', 'Mavericks', ['#0064b1', '#0053bc', '#0053BC']],
    ['CLE', 'cavaliers', 'Cleveland', 'Cavaliers', ['#860038', '#6f263d', '#6f263d']],
    ['CHI', 'bulls', 'Chicago', 'Bulls', ['#ce1141', '#ce1141', '#ce1141']],
    ['CHA', 'hornets', 'Charlotte', 'Hornets', ['#00788c', '#00788c', '#00788c']],
    ['BKN', 'nets', 'Brooklyn', 'Nets', ['#061922', '#dfdfdf', '#000000']],
    ['BOS', 'celtics', 'Boston', 'Celtics', ['#008348', '#008348', '#008348']],
    ['ATL', 'hawks', 'Atlanta', 'Hawks', ['#e13a3e', '#e03a3e', '#e03a3e']],
]


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

table_data = pd.read_html(str(table))[0]


def compare_stat(team_names, stat_key):
    team_stats = table_data.loc[table_data['Team'].str.contains('|'.join(team_names))]

    team_stats = team_stats.sort_values(by=[stat_key], ascending=False, ignore_index=True)

    delta = team_stats[stat_key].diff()[1] / team_stats.iloc[0]['G']

    print(f'The {team_stats.iloc[0]["Team"]} had {abs(delta):.2f} more {stat_key} per game than the {team_stats.iloc[1]["Team"]}')


compare_stat(['Suns', 'Bucks'], 'TOV')

print(f'it took {time.time() - time1:.2f} seconds')
