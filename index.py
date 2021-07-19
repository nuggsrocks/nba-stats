import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from boxscores import scrape_for_boxscore_links, scrape_for_boxscores, scrape_date_range

url = 'https://www.basketball-reference.com/boxscores/'

start_date = datetime.date(2020, 12, 22)
end_date = datetime.date(2020, 12, 23)

date_range = pd.date_range(start=start_date, end=end_date)

for date in date_range:
    res = requests.get(url, {'year': date.year, 'month': date.month, 'day': date.day})

    links = scrape_for_boxscore_links(res.text)

    for link in links:
        link = link.replace('/boxscores/', '')

        res = requests.get(url + link)

        soup = BeautifulSoup(res.text, 'html.parser')

        print(scrape_for_boxscores(soup))
