import datetime
import re
from bs4 import BeautifulSoup
import pandas as pd


def scrape_for_boxscore_links(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')

    return list(
        map(lambda x: x.parent['href'], soup.find_all(string='Box Score')))


def scrape_for_boxscore(soup: BeautifulSoup, game_id: str):
    df = pd.DataFrame()

    for tag in soup.find_all(string=re.compile('Basic Box Score')):
        for parent in tag.parents:
            if parent.name == 'table' and re.search('game',
                                                    parent['id']) is not None:
                team_df = pd.read_html(str(parent), header=1)[0]

                team = re.search('[A-Z]{3}', parent['id']).group()

                team_df['TEAM'] = team

                df = df.append(team_df, ignore_index=True)

    df['GAME_ID'] = game_id

    date_str = game_id[:-4]

    date = datetime.date(
        year=int(date_str[:4]),
        month=int(date_str[4:6]),
        day=int(date_str[6:])
    )

    df['DATE'] = date

    return df


def format_dataframe(df):
    processed_df = df.rename(columns={'Starters': 'NAME'})
    processed_df = processed_df.drop(
        index=processed_df.loc[lambda x: x['NAME'] == 'Reserves'].index)
    processed_df = processed_df.drop(
        index=processed_df['NAME'][lambda x: x == 'Team Totals'].index)
    processed_df = processed_df.drop(
        index=processed_df.loc[processed_df['MP'] == 'Did Not Play'].index)
    processed_df = processed_df.drop(
        index=processed_df.loc[processed_df['MP'] == 'Did Not Dress'].index)
    processed_df = processed_df.drop(columns=['FG%', '3P%', 'FT%'])

    return processed_df.reset_index(drop=True)


def set_dtypes(series):
    if series.name == 'NAME' or series.name == 'TEAM' or series.name == 'GAME_ID':
        return series.astype('string')
    elif series.name == 'MP':
        time_list = list(series.str.split(':'))

        timedelta_list = list(
            map(
                lambda x: pd.Timedelta(
                    minutes=int(x[0]),
                    seconds=int(x[1])
                ),
                time_list
            )
        )

        return pd.Series(timedelta_list, dtype='timedelta64[ns]')
    elif series.name == 'DATE':
        return series.astype('datetime64[ns]')
    else:
        return series.astype('int64')
