import re

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.basketball-reference.com/boxscores/'

params = {
    'month': '12',
    'day': '22',
    'year': '2020'
}

r = requests.get(url, params)


soup = BeautifulSoup(r.text, 'html.parser')

boxscore_links = map(lambda x: x.parent['href'], soup.find_all(string='Box Score'))

boxscores = []

for link in boxscore_links:

    link = link.replace('/boxscores/', '')

    res = requests.get(url + link, timeout=5)

    soup = BeautifulSoup(res.text, 'html.parser')

    stat_dfs = {}

    for tag in soup.find_all(string=re.compile('Basic Box Score')):
        for parent in tag.parents:
            if parent.name == 'table' and re.search('game', parent['id']) is not None:
                team_code = re.search('[A-Z]{3}', parent['id']).group()
                stat_df = pd.read_html(str(parent), header=1)[0]
                stat_df.rename(columns={'Starters': 'Name'}, inplace=True)
                stat_df.drop(index=[5], inplace=True)
                stat_dfs[team_code] = stat_df

    boxscores.append(stat_dfs)

print(boxscores)


