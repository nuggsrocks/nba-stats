import datetime
import unittest
from unittest.mock import patch
import pandas as pd
import boxscores
from bs4 import BeautifulSoup


class TestScrapeForBoxscores(unittest.TestCase):

    def test_scrape_boxscore_links(self):
        html = '<!DOCTYPE html><a href="foo">Box Score</a>'

        links = boxscores.scrape_for_boxscore_links(html_string=html)

        self.assertEqual(links, ['foo'])

    def test_scrape_for_boxscores(self):
        html = '''
        <!DOCTYPE html>
        <table id="GSW-game-foobar">
        <thead>
        <tr>
        <th>Basic Box Score</th>
        </tr>
        <tr>
        <th>foo</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td>bar</td>
        </tr>
        </tbody>
        </table>
        <table id="GSW-1q-foobar">
        <thead>
        <tr>
        <th>Basic Box Score</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
        </table>
        '''

        dfs = boxscores.scrape_for_boxscores(BeautifulSoup(html, 'html.parser'))

        expected = pd.DataFrame(data={'foo': 'bar'}, index=[0])

        pd.testing.assert_frame_equal(expected, dfs['GSW'])

    def test_format_dataframe(self):
        mock_data = {
            'Starters': ['a', 'b', 'c', 'd', 'e', 'Reserves', 'g', 'h', 'Team Totals'],
            'MP': ['11:00', '1:00', '1:00', '1:00', '1:00', 'foobar', '1:00', 'Did Not Play', '44:00'],
            'FG%': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            '3P%': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'FT%': [1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
        mock_df = pd.DataFrame(data=mock_data)

        expected_data = {
            'NAME': ['a', 'b', 'c', 'd', 'e', 'g'],
            'MP': ['11:00', '1:00', '1:00', '1:00', '1:00', '1:00']
        }

        formatted_df = boxscores.format_dataframe(mock_df)

        self.assertEqual(formatted_df.to_dict(orient='list'), expected_data)

    def test_set_dtypes(self):
        test_cases = {
            'NAME': {'series': ['Hello', 'World', 'foo', 'bar'], 'dtype': 'string'},
            'MP': {'series': ['11:11', '12:12', '13:13', '0:23'], 'dtype': 'timedelta64[ns]'},
            'FG': {'series': ['1', '2', '3', '4'], 'dtype': 'int64'}
        }

        mock_data = {}

        for key in test_cases.keys():
            mock_data[key] = test_cases[key]['series']

        mock_df = pd.DataFrame(data=mock_data)

        for index, series in mock_df.items():
            self.assertEqual('object', series.dtype)

        mock_df = mock_df.apply(boxscores.set_dtypes)

        for index, series in mock_df.items():
            self.assertEqual(test_cases[series.name]['dtype'], series.dtype)

    def test_scrape_date_range(self):
        start = datetime.date(2020, 12, 22)
        end = datetime.date(2020, 12, 25)

        mock_data = {'GSW': pd.DataFrame(data={'NAME': ['x']}, index=[0]),
                     'BRK': pd.DataFrame(data={'NAME': ['y']}, index=[0])}

        with patch.object(boxscores, 'scrape_for_boxscores', return_value=[mock_data]) as mock_boxscore_scrape:
            stats = boxscores.scrape_date_range(start, end)

        self.assertEqual((end - start).days, stats['GAME_ID'].max())

        for key in mock_data.keys():
            self.assertEqual(stats['GAME_ID'].max() + 1, len(stats.loc[stats['TEAM'] == key]))

        for date in pd.date_range(start, end):
            mock_boxscore_scrape.assert_any_call(pd.Timestamp(year=date.year, month=date.month, day=date.day, freq='D'))
