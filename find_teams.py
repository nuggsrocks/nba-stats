import re

import bs4.element
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.basketball-reference.com/teams/'

r = requests.get(url)

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

team_links = []

for row in table.tbody.find_all('tr'):
    team_links.append({'Name': row.a.get_text(), 'Link': row.a['href']})


df = pd.DataFrame.from_dict(team_links)


def create_team_links_df():
    return df
