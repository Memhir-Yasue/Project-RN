import praw
import config


reddit = praw.Reddit(client_id = config.client_id,
                     client_secret=config.client_secret,
                     user_agent = config.user_agent)



class Sub_Scrapper():
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

    def validate_user(self):
        try:
            reddit.redditor(name=self.user).id
            self.__good_to_go = True
        except:
            print("User not found")
            self.__good_to_go = False

    def subreddit_visited(self):
        """
        subreddits where user has left a comment
        """
        if (self.__good_to_go == False):
            raise Exception('User was not validated!')

        visited_pages = {}
        user = reddit.redditor(name=self.user)
        for comment in user.comments.top('all'):
            # body = comment.body
            sub = comment.subreddit
            if sub.display_name not in visited_pages:
                visited_pages[sub.display_name] = 1
            else:
                visited_pages[sub.display_name] += 1
        return visited_pages






redditor = Redditor(user='memhir-yasue')
print(redditor.subreddit_visited())

# user = reddit.redditor(name='memhir-yasue')
# user_comments = [comment for comment in user.comments.top('all')]
# print([comment.subreddit for comment in user_comments])

# print(user)
# for comment in user.comments.top('all'):
#     print(comment.subreddit)
#     print(comment.body,'\n')


# reddit.redditor(name='hfdjshfdsjuf').comments.top('all')


# obj_methods = [name for name in dir(obj)]
# print(help(obj.method))
