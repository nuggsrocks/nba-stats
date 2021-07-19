import datetime
import unittest
from unittest.mock import patch
import pandas as pd
import boxscores
from bs4 import BeautifulSoup


class TestScrapeForBoxscore(unittest.TestCase):

    def test_scrape_boxscore_links(self):
        html = '<!DOCTYPE html><a href="foo">Box Score</a>'

        links = boxscores.scrape_for_boxscore_links(html_string=html)

        self.assertEqual(links, ['foo'])

    def test_scrape_for_boxscore(self):
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
        <table id="BRK-game-foobar">
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
                <td>BAR</td>
            </tr>
            </tbody>
        </table>
        '''

        mock_id = 'XY5430'

        df = boxscores.scrape_for_boxscore(BeautifulSoup(html, 'html.parser'), mock_id)

        expected = pd.DataFrame(data={'foo': ['bar', 'BAR'], 'TEAM': ['GSW', 'BRK'], 'GAME_ID': [mock_id, mock_id]}, index=[0, 1])

        self.assertIsInstance(df, pd.DataFrame)
        pd.testing.assert_frame_equal(df, expected)

    def test_format_dataframe(self):
        mock_data = {
            'Starters': ['a', 'b', 'c', 'd', 'e', 'Reserves', 'g', 'h', 'Team Totals', 'a', 'b', 'c', 'd', 'e', 'Reserves', 'g', 'h', 'Team Totals'],
            'MP': ['11:00', '1:00', '1:00', '1:00', '1:00', 'foobar', '1:00', 'Did Not Play', '44:00', '11:00', '1:00', '1:00', '1:00', '1:00', 'foobar', '1:00', 'Did Not Play', '44:00'],
            'FG%': [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            '3P%': [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'FT%': [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
        mock_df = pd.DataFrame(data=mock_data)

        expected_data = {
            'NAME': ['a', 'b', 'c', 'd', 'e', 'g', 'a', 'b', 'c', 'd', 'e', 'g'],
            'MP': ['11:00', '1:00', '1:00', '1:00', '1:00', '1:00', '11:00', '1:00', '1:00', '1:00', '1:00', '1:00']
        }

        expected_df = pd.DataFrame(data=expected_data)
        formatted_df = boxscores.format_dataframe(mock_df)

        pd.testing.assert_frame_equal(formatted_df, expected_df)

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
