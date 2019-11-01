from user_hub.user import User


def main():
    redditor = User('coordinatedflight')
    redditor.validate_user()
    visited_subs = redditor.get_visited_pages()

    print(visited_subs)

if __name__ == "__main__":
    main()
