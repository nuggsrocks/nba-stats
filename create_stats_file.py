def create_stats_file(os, open_file):
    if os.path.isdir('./stats'):
        if os.path.exists('./stats/stats.json'):
            os.remove('./stats/stats.json')

        return open_file('./stats/stats.json', 'x')
    else:
        os.mkdir('stats')

        return open_file('./stats/stats.json', 'x')
