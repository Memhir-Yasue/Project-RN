def summarize_hours_stats(time_info: dict):
    time_info_sorted = (dict(sorted(time_info.items())))
    for k, v in time_info_sorted.items():
        print(f"{k}: {len(v)}")
    return time_info_sorted


def process_to_edges(time_stamp_to_subreddit: dict) -> list:
    """
    Takes a dictionary from User.time_stamp_to_subreddit, whose value is a list containing subreddit elements.

    Processes it into edges that can be mapped into networkX

    edges are (k,v) or (hour, subreddit)
    :param time_stamp_to_subreddit:
    :return: list
    """
    k_v_tuple_list = list(time_stamp_to_subreddit.items())
    edges = []
    for k_v_pair in k_v_tuple_list:
        hour = k_v_pair[0]
        for subreddit_title in k_v_pair[1]:
            edges.append(tuple([hour, subreddit_title]))
    return edges