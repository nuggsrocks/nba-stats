import datetime
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_for_boxscores(date):
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
                    stat_df = pd.read_html(str(parent), header=1)[0]

                    processed_df = stat_df.rename(columns={'Starters': 'NAME'})
                    processed_df = processed_df.drop(index=[5])
                    team_totals_index = processed_df['NAME'][lambda x: x == 'Team Totals'].index[0]
                    processed_df = processed_df.drop(index=team_totals_index)

                    dnp_indexes = processed_df.loc[processed_df['MP'] == 'Did Not Play'].index

                    for index in dnp_indexes:
                        processed_df = processed_df.drop(index=index)

                    processed_df = processed_df.drop(['FG%', '3P%', 'FT%'], axis=1)

                    team = re.search('[A-Z]{3}', parent['id']).group()
                    stat_dfs[team] = processed_df

        boxscores.append(stat_dfs)

    return boxscores


def scrape_date_range(start, end):
    dates = pd.date_range(start=start, end=end, freq='D')

    full_df = pd.DataFrame()

    game_index = 0

    for date in dates:
        games = scrape_for_boxscores(date)

        for boxscore in games:
            for team_code in boxscore:
                boxscore[team_code]['GAME_ID'] = game_index
                boxscore[team_code]['TEAM'] = team_code
                full_df = full_df.append(boxscore[team_code], ignore_index=True)
            game_index += 1

        if date > datetime.date(2020, 12, 22):
            break

    def set_dtypes(series):
        if series.name == 'NAME' or series.name == 'TEAM':
            return series.astype('string')
        elif series.name == 'MP':
            time_list = list(series.str.split(':'))

            timedelta_list = list(map(lambda x: pd.Timedelta(minutes=int(x[0]), seconds=int(x[1])), time_list))

            return pd.Series(timedelta_list)
        else:
            return series.astype('int64')

    return full_df.apply(set_dtypes)
