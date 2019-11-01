from user_hub.user import User
from user_hub.neighborhood import Neighborhood


def main():
    # coordinatedflight
    redditor = User('memhir-yasue')
    redditor.validate_user()
    redditor.get_visited_pages()
    redditor.print_subbreddit_visited()
    redditor.print_interacted_with()

if __name__ == "__main__":
    main()
