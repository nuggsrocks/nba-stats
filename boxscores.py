import re
import requests
import datetime
from calendar import Calendar
from bs4 import BeautifulSoup
import pandas as pd
from pandas.core.common import flatten


def create_date_list():
    c = list(flatten(Calendar().yeardatescalendar(2020)))
    c.extend(list(flatten(Calendar().yeardatescalendar(2021))))

    season_start_date = datetime.date(year=2020, month=12, day=22)
    season_end_date = datetime.date(year=2021, month=5, day=16)

    c = pd.Series(c).drop_duplicates()

    c = c.loc[lambda x: x >= season_start_date]

    c = c.loc[lambda x: x <= season_end_date]

    c = c.reset_index(drop=True)

    return list(c)


def scrape_for_stats(date):
    url = 'https://www.basketball-reference.com/boxscores/'

    params = {
        'month': date.month,
        'day': date.day,
        'year': date.year
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
                    team_totals_index = stat_df['Name'][lambda x: x == 'Team Totals'].index[0]
                    stat_df.drop(index=team_totals_index, inplace=True)
                    stat_dfs[team_code] = stat_df

        boxscores.append(stat_dfs)

    return boxscores


dates = create_date_list()

full_df = pd.DataFrame()

game_index = 0

for date in dates:
    games = scrape_for_stats(date)

    for game in games:
        for team_code in game:
            game[team_code]['GAME_ID'] = game_index
            game[team_code]['TEAM'] = team_code
            full_df = full_df.append(game[team_code], ignore_index=True)
        game_index += 1

print(full_df)
