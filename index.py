import re
import requests
from bs4 import BeautifulSoup

teams_info = [

    ['1610612764', 'WAS', 'wizards', 'Washington', 'Wizards', 1, 5, 0, 2019, 2, ['#002b5c', '#e31837', '#002b5c'], 1,
     1],
    ['1610612762', 'UTA', 'jazz', 'Utah', 'Jazz', 2, 3, 0, 2019, 2, ['#002b5c', '#f9a01b', '#002b5c'], 1, 1],
    ['1610612761', 'TOR', 'raptors', 'Toronto', 'Raptors', 1, 1, 0, 2019, 2, ['#000000', '#ce1141', '#000000'], 1, 1],
    ['1610612759', 'SAS', 'spurs', 'San Antonio', 'Spurs', 2, 6, 0, 2019, 2, ['#061922', '#c4ced4', '#000000'], 1, 1],
    ['1610612758', 'SAC', 'kings', 'Sacramento', 'Kings', 2, 4, 0, 2019, 2, ['#724c9f', '#5a2d81', '#5a2d81'], 1, 1],
    ['1610612757', 'POR', 'blazers', 'Portland', 'Trail Blazers', 2, 3, 0, 2019, 2, ['#061922', '#e03a3e', '#e03a3e'],
     0, 0],
    ['1610612756', 'PHX', 'suns', 'Phoenix', 'Suns', 2, 4, 0, 2019, 2, ['#e56020', '#e56020', '#1d1160'], 1, 1],
    ['1610612755', 'PHI', 'sixers', 'Philadelphia', '76ers', 1, 1, 0, 2019, 2, ['#ed174c', '#006bb6', '#006bb6'], 2, 1],
    ['1610612753', 'ORL', 'magic', 'Orlando', 'Magic', 1, 5, 0, 2019, 2, ['#007dc5', '#0077c0', '#0077c0'], 0, 0],
    ['1610612760', 'OKC', 'thunder', 'Oklahoma City', 'Thunder', 2, 3, 0, 2019, 2, ['#007dc3', '#007ac1', '#007ac1'], 0,
     0],
    ['1610612752', 'NYK', 'knicks', 'New York', 'Knicks', 1, 1, 0, 2019, 2, ['#006bb6', '#006bb6', '#006bb6'], 0, 0],
    ['1610612740', 'NOP', 'pelicans', 'New Orleans', 'Pelicans', 2, 6, 0, 2019, 2, ['#002b5c', '#b4975a', '#002b5c'], 1,
     1],
    ['1610612750', 'MIN', 'timberwolves', 'Minnesota', 'Timberwolves', 2, 3, 0, 2019, 2,
     ['#005083', '#236192', '#0c2340'], 1, 1],
    ['1610612749', 'MIL', 'bucks', 'Milwaukee', 'Bucks', 1, 2, 0, 2019, 2, ['#00471b', '#00471b', '#00471b'], 1, 1],
    ['1610612748', 'MIA', 'heat', 'Miami', 'Heat', 1, 5, 0, 2019, 2, ['#98002e', '#98002E', '#98002e'], 0, 0],
    ['1610612763', 'MEM', 'grizzlies', 'Memphis', 'Grizzlies', 2, 6, 0, 2019, 2, ['#7399c6', '#7399C6', '#5d76a9'], 1,
     0],
    ['1610612747', 'LAL', 'lakers', 'Los Angeles', 'Lakers', 2, 4, 0, 2019, 2, ['#552583', '#fdb927', '#552583'], 1, 1],
    ['1610612746', 'LAC', 'clippers', 'LA', 'Clippers', 2, 4, 0, 2019, 2, ['#ed174c', '#c8102e', '#c8102e'], 1, 1],
    ['1610612754', 'IND', 'pacers', 'Indiana', 'Pacers', 1, 2, 0, 2019, 2, ['#ffc633', '#fdbb30', '#002d62'], 1, 1],
    ['1610612745', 'HOU', 'rockets', 'Houston', 'Rockets', 2, 6, 0, 2019, 2, ['#ce1141', '#ce1141', '#ce1141'], 2, 0],
    ['1610612744', 'GSW', 'warriors', 'Golden State', 'Warriors', 2, 4, 0, 2019, 2, ['#fdb927', '#FDB927', '#006bb6'],
     1, 1],
    ['1610612765', 'DET', 'pistons', 'Detroit', 'Pistons', 1, 2, 0, 2019, 2, ['#006bb6', '#C80F2D', '#1d428a'], 0, 0],
    ['1610612743', 'DEN', 'nuggets', 'Denver', 'Nuggets', 2, 3, 0, 2019, 2, ['#4d90cd', '#fec524', '#0e2240'], 1, 1],
    ['1610612742', 'DAL', 'mavericks', 'Dallas', 'Mavericks', 2, 6, 0, 2019, 2, ['#0064b1', '#0053bc', '#0053BC'], 1,
     1],
    ['1610612739', 'CLE', 'cavaliers', 'Cleveland', 'Cavaliers', 1, 2, 0, 2019, 2, ['#860038', '#6f263d', '#6f263d'], 0,
     0],
    ['1610612741', 'CHI', 'bulls', 'Chicago', 'Bulls', 1, 2, 0, 2019, 2, ['#ce1141', '#ce1141', '#ce1141'], 1, 1],
    ['1610612766', 'CHA', 'hornets', 'Charlotte', 'Hornets', 1, 5, 0, 2019, 2, ['#00788c', '#00788c', '#00788c'], 1, 1],
    ['1610612751', 'BKN', 'nets', 'Brooklyn', 'Nets', 1, 1, 0, 2019, 2, ['#061922', '#dfdfdf', '#000000'], 1, 1],
    ['1610612738', 'BOS', 'celtics', 'Boston', 'Celtics', 1, 1, 0, 2019, 2, ['#008348', '#008348', '#008348'], 1, 1],
    ['1610612737', 'ATL', 'hawks', 'Atlanta', 'Hawks', 1, 5, 0, 2019, 2, ['#e13a3e', '#e03a3e', '#e03a3e'], 0, 0],
]


url = 'https://stats.nba.com/stats/teamdashboardbygeneralsplits'

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Access-Control-Request-Headers": "x-nba-stats-origin,x-nba-stats-token",
    "Access-Control-Request-Method": "GET",
    "Connection": "keep-alive",
    "Host": "stats.nba.com",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"

}

params = {
    "DateFrom": "",
    "DateTo": "",
    "GameSegment": "",
    "LastNGames": "0",
    "LeagueID": "00",
    "Location": "",
    "MeasureType": "Base",
    "Month": "0",
    "OpponentTeamID": "0",
    "Outcome": "",
    "PORound": "0",
    "PaceAdjust": "N",
    "PerMode": "PerGame",
    "Period": "0",
    "PlusMinus": "N",
    "Rank": "N",
    "Season": "2020-21",
    "SeasonSegment": "",
    "SeasonType": "Regular Season",
    "ShotClockRange": "",
    "Split": "general",
    "TeamID": "1610612751",
    "VsConference": "",
    "VsDivision": ""
}

r = requests.get(url, params=params, headers=headers)

data = r.json()

overall_stats = data['resultSets'][0]

stat_headers = overall_stats['headers']
stat_values = overall_stats['rowSet'][0]

i = 0
while i < len(stat_headers):
    print(stat_headers[i] + ': ' + str(stat_values[i]))
    i += 1

