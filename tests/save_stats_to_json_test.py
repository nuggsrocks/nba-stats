import unittest
from unittest.mock import patch, mock_open
import json
from save_stats_to_json import save_stats_to_json


class TestSaveStatsToJson(unittest.TestCase):
    json = json.dumps([{'a': 1}, {'b': 2}])

    def test_save_stats_to_json(self):
        mo = mock_open()

        with patch('__main__.open', mo):
            save_stats_to_json(mo(), json)

        mo().write.assert_called_once_with(json)
        mo().close.assert_called_once()
