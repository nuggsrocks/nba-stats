import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from boxscores import scrape_for_boxscore_links, scrape_for_boxscore, set_dtypes, format_dataframe

url = 'https://www.basketball-reference.com/boxscores/'

stats_df = pd.DataFrame()

date_range = pd.date_range(start=datetime.date(2020, 12, 22), end=datetime.date(2020, 12, 22))

for date in date_range:
    res = requests.get(url, {'year': date.year, 'month': date.month, 'day': date.day})

    links = scrape_for_boxscore_links(res.text)

    for link in links:
        link = link.replace('/boxscores/', '')

        game_id = link.replace('.html', '')

        res = requests.get(url + link)

        soup = BeautifulSoup(res.text, 'html.parser')

        boxscore = scrape_for_boxscore(soup, game_id)

        stats_df = stats_df.append(format_dataframe(boxscore), ignore_index=True)

print(stats_df)
