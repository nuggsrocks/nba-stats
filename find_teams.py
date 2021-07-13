import numpy as np
import bs4.element
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.basketball-reference.com'

r = requests.get(url + '/teams/')

soup = BeautifulSoup(r.text, 'html.parser')

active_franchises = soup.find(string='Active Franchises')

table = None

for parent in active_franchises.parents:
    if parent.table is not None:
        table = parent.table
        break

for child in table.tbody.children:
    if type(child) is bs4.element.Tag:
        if 'partial_table' in child['class']:
            child.extract()


def create_teams_info_df():
    teams_info = []

    for row in table.tbody.find_all('tr'):
        teams_info.append({
            'Name': row.a.get_text(),
            'Link': row.a['href']
        })

    for team in teams_info:
        team['Code'] = team['Link'].replace('/teams/', '').replace('/', '')

        if team['Code'] == 'NJN':
            team['Code'] = 'BRK'
            team['Link'] = '/teams/BRK/'

        if team['Code'] == 'CHA':
            team['Link'] = '/teams/CHO/'

        if team['Code'] == 'NOH':
            team['Code'] = 'NOP'
            team['Link'] = '/teams/NOP/'

    df = pd.DataFrame.from_dict(teams_info)

    return df


df = create_teams_info_df()

rosters = []

for index, series in df.iterrows():
    team_res = requests.get(url + df.iloc[index]['Link'] + '2021.html')

    soup = BeautifulSoup(team_res.text, 'html.parser')

    parents = soup.find_all(string='Roster')[0].parents

    for parent in parents:
        if parent.table is not None:
            table = parent.table
            break

    roster_df = pd.read_html(str(table))[0]

    roster_df.rename(columns={'No.': 'No', 'Unnamed: 6': 'Nationality'}, inplace=True)

    team = [df.iloc[index]['Name'] for i in range(0, roster_df.index.max() + 1)]

    roster_df['Team'] = team

    for player_index in roster_df.index:
        if pd.isna(roster_df.iloc[player_index]['College']):
            roster_df.loc[player_index, 'College'] = None

    rosters.append(roster_df)

    if index == 1:
        break

print(rosters[0].append(rosters[1], ignore_index=True))
