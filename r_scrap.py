import praw
import config


reddit = praw.Reddit(client_id = config.client_id,
                     client_secret=config.client_secret,
                     user_agent = config.user_agent)

class Redditor:
    def __init__(self,user):
        self.user = user

    def validate_user(self):
        try:
            reddit.redditor(name=self.user).id
            print("User Exists")
            return True
        except:
            print("User not found")
            return False

    # def search_user(self,user):
    #     if(validate_user(user)):
    #         print("Welcome!")


redditor = Redditor(user='randomredditordss')
redditor.validate_user()

# user = reddit.redditor(name='hfdjhfjd')
# print(user)
# for comment in user.comments.top('all'):
#     print(comment.subreddit)
#     print(comment.body,'\n')


# reddit.redditor(name='hfdjshfdsjuf').comments.top('all')


# obj_methods = [name for name in dir(obj)]
# print(help(obj.method))
