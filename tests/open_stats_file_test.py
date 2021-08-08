import unittest
from unittest import mock
from unittest.mock import patch, mock_open
import os
from open_stats_file import open_stats_file


class TestOpenStatsFile(unittest.TestCase):
    def setUp(self):
        self.mock_os = mock.Mock(spec=os)
        self.mock_open = mock_open()

    def tearDown(self):
        self.mock_os.reset_mock()
        self.mock_open.reset_mock()

    def test_dir_does_not_exist(self):
        self.mock_os.path.isdir.return_value = False

        with patch('__main__.open', self.mock_open):
            file = open_stats_file(self.mock_os, self.mock_open)

        self.mock_os.path.isdir.assert_called_once()
        self.mock_os.mkdir.assert_called_once_with('stats')
        self.mock_open.assert_called_once_with('./stats/stats.json', 'x')
        self.assertEqual(file, self.mock_open())

    def test_dir_exists_but_file_does_not(self):
        self.mock_os.path.isdir.return_value = True
        self.mock_os.path.exists.return_value = False

        with patch('__main__.open', self.mock_open):
            file = open_stats_file(self.mock_os, self.mock_open)

        self.mock_os.path.isdir.assert_called_once()
        self.mock_open.assert_called_once_with('./stats/stats.json', 'x')
        self.assertEqual(file, self.mock_open())

    def test_dir_and_file_exist(self):
        self.mock_os.path.isdir.return_value = True
        self.mock_os.path.exists.return_value = True

        with patch('__main__.open', self.mock_open):
            file = open_stats_file(self.mock_os, self.mock_open)

        self.mock_os.path.isdir.assert_called_once()
        self.mock_open.assert_called_once_with('./stats/stats.json', 'x')
        self.assertEqual(file, self.mock_open())
