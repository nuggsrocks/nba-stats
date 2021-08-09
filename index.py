import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from boxscores import scrape_for_boxscore_links, scrape_for_boxscore, \
    set_dtypes, format_dataframe
from create_stats_file import create_stats_file
from save_stats_to_json import save_stats_to_json
import os


def index(date_range):
    url = 'https://www.basketball-reference.com/boxscores/'

    stats_df = pd.DataFrame()

    for date in date_range:
        res = requests.get(url, {'year': date.year, 'month': date.month,
                                 'day': date.day})

        links = scrape_for_boxscore_links(res.text)

        for link in links:
            link = link.replace('/boxscores/', '')

            game_id = link.replace('.html', '')

            res = requests.get(url + link)

            soup = BeautifulSoup(res.text, 'html.parser')

            boxscore = scrape_for_boxscore(soup, game_id)

            stats_df = stats_df.append(format_dataframe(boxscore),
                                       ignore_index=True)

    return stats_df.apply(set_dtypes)


def input_date():
    year = int(input('Year: '))
    month = int(input('Month: '))
    day = int(input('Day: '))

    return datetime.date(year, month, day)


print('Start Date')
start_date = input_date()
print('End Date')
end_date = input_date()

stat_df = index(pd.date_range(start_date, end_date))

stats_file = create_stats_file(os, open)

save_stats_to_json(stats_file, stat_df.to_json())
