def summarize_hours_stats(time_info: dict):
    time_info_sorted = (dict(sorted(time_info.items())))
    for k, v in time_info_sorted.items():
        print(f"{k}: {len(v)}")
    return time_info_sorted
