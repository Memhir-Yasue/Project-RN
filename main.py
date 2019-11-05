from user_hub.user import User
from user_hub import time_box

def main():
    # coordinatedflight
    redditor = User("memhir-yasue")
    redditor.validate_user()
    redditor.get_visited_pages()
    visited, t_stamp, t_stamp_subreddit = redditor.return_user_attributes()
    time_box.summarize_hours_stats(t_stamp)

    edges = time_box.process_to_edges(t_stamp_subreddit)
    print(edges)


if __name__ == "__main__":
    main()
