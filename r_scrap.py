import praw
import json
import config


reddit = praw.Reddit(client_id = config.client_id,
                     client_secret=config.client_secret,
                     user_agent = config.user_agent)


# obj_methods = [name for name in dir(obj)]
# print(help(obj.method))

class Sub_scrapper():
    """
    This class is to be used only for gathering subreddit corpuses for the purpose of training an ML model.
    """


class Redditor:
    """
    This class is responsible for conducting all user related operations
    """
    def __init__(self,user):
        self.user = user
        self.__good_to_go = self.validate_user()
        self.visited_pages = {}
        self.pages_info = {}

    def validate_user(self):
        try:
            reddit.redditor(name=self.user).id
            self.__good_to_go = True
        except:
            print("User not found")
            self.__good_to_go = False

    def process_subreddit_visited(self):
        """
        subreddits where user has left a comment
        """
        if (self.__good_to_go == False):
            raise Exception('User was not validated!')

        user = reddit.redditor(name=self.user)
        for comment in user.comments.top('all'):
            # body = comment.body
            sub = comment.subreddit
            if sub.display_name not in self.visited_pages:
                self.visited_pages[sub.display_name] = 1
                self.pages_info[sub.display_name] = sub.public_description
            else:
                self.visited_pages[sub.display_name] += 1
        return self.visited_pages, self.pages_info

    def print_page_info(self):
        info = self.pages_info
        for k, v in info.items():
            print("Subreddit: {0}\n Description: {1}\n\n".format(k,v))

    def top_subreddits(self):
        freq = {}
        for submission in reddit.subreddit('all').top(limit=5000):
            sub_raw = submission.subreddit
            sub = sub_raw.display_name
            if sub not in freq:
                freq[sub] = 1
            else:
                freq[sub] += 1
        return freq


    # def print_pages_count(self):
    #     count_dict = self.visited_pages
    #     for k, v in count_dict.items():
    #         print("Subreddit: {0}\n Description: {1}\n\n".format(k,v))


redditor = Redditor(user='dovahsevobrom')
visited, info = redditor.process_subreddit_visited()
subreddit_freq = redditor.top_subreddits()
sorted_freq = sorted(subreddit_freq.items(), key=lambda x: x[1], reverse=True)
print(sorted_freq)


# print(user)
# for comment in user.comments.top('all'):
#     print(comment.subreddit)
#     print(comment.body,'\n')


# reddit.redditor(name='hfdjshfdsjuf').comments.top('all')
