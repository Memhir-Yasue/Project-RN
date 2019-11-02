from user_hub.user import User
from user_hub.time_box import summarize_hours_stats

def main():
    # coordinatedflight
    redditor = User("memhir-yasue")
    redditor.validate_user()

    redditor.get_visited_pages()
    redditor.print_subbreddit_visited()
    summarize_hours_stats(redditor.time_stamp_comment)



if __name__ == "__main__":
    main()
