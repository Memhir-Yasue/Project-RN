from user_hub.user import User


def main():
    # coordinatedflight
    redditor = User("coordinatedflight")
    redditor.validate_user()
    redditor.get_visited_pages()
    redditor.print_subbreddit_visited()
    redditor.print_interacted_under()


if __name__ == "__main__":
    main()
