import praw
import config

reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    user_agent=config.user_agent,
)


class User:
    def __init__(self, user_name):
        self.user_name = user_name
        self.__good_to_go = self.validate_user()
        self.visited_pages = {}

    def validate_user(self):
        try:
            reddit.redditor(name=self.user_name).id
            return True
        except:
            raise Exception("User was not validated!")

    def get_visited_pages(self):
        """
        Goes through the comments of the validated user and returns a dictionary showing the subreddit commented on and the frequency commented on that subreddit

        :return: Dict
        """
        user = reddit.redditor(name=self.user_name)
        for comment in user.comments.top("all"):
            # body = comment.body
            sub = comment.subreddit
            if sub.display_name not in self.visited_pages.keys():
                print(sub)
                self.visited_pages[sub.display_name] = 1
            else:
                self.visited_pages[sub.display_name] += 1

        return self.visited_pages
