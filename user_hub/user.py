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
        self.interacted_under = {}

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
            subreddit = comment.subreddit
            submission = comment.submission
            if subreddit.display_name not in self.visited_pages.keys():
                print(subreddit)
                self.visited_pages[subreddit.display_name] = 1
            else:
                self.visited_pages[subreddit.display_name] += 1
            if submission.author is not None:
                if submission.author.name not in self.interacted_under.keys():
                    self.interacted_under[submission.author.name] = 1
                else:
                    self.interacted_under[submission.author.name] += 1

    def print_subbreddit_visited(self):
        print(self.visited_pages)

    def print_interacted_under(self):
        print(self.interacted_under)
