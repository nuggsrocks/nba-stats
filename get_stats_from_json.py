def get_stats_from_json(file_path, pandas):
    try:
        return pandas.read_json(file_path)
    except:
        pass

