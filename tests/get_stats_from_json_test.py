import unittest
from unittest import mock
from unittest.mock import mock_open
import pandas
import pandas as pd

from get_stats_from_json import get_stats_from_json


class TestGetStatsFromJson(unittest.TestCase):
    def setUp(self):
        self.mock_pandas = mock.Mock(spec=pandas)
        self.mock_open = mock_open()

    def tearDown(self):
        self.mock_pandas.reset_mock()
        self.mock_open.reset_mock()

    def test_get_stats_from_json(self):
        self.mock_pandas.read_json.return_value = pd.DataFrame()

        path = 'foo/bar'

        df = get_stats_from_json(path, self.mock_pandas)

        self.assertIsInstance(df, pandas.DataFrame)
        self.mock_pandas.read_json.assert_called_once_with(path)

