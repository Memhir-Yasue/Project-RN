import praw
import json
import config
from scipy import spatial


reddit = praw.Reddit(client_id = config.client_id,
                     client_secret=config.client_secret,
                     user_agent = config.user_agent)


# obj_methods = [name for name in dir(obj)]
# print(help(obj.method))

class Sub_scrapper:
    """
    For the distant future...
    This class is to be used only for gathering subreddit corpuses for the purpose of training an ML model.
    """

class Redditor:
    """
    This class is responsible for conducting all user/redditor related operations
    """
    def __init__(self,user):
        self.user = user
        self.__good_to_go = self.validate_user()
        self.visited_pages = {}
        self.visited_pages_list = []
        self.pages_info = {}
        self.potential_matches = []

    def validate_user(self):
        try:
            reddit.redditor(name=self.user).id
            return True
        except:
            print("User not found")
            return False

    def process_subreddit_visited(self):
        """
        subreddits where validated user has left a comment
        """
        if (self.__good_to_go == False):
            raise Exception('User was not validated!')

        user = reddit.redditor(name=self.user)
        for comment in user.comments.top('all'):
            # body = comment.body
            sub = comment.subreddit
            # visited_pages_list and visited_pages are both the same.
            #Difference is one keeps track of the frquency and other one is just a list for later use
            if sub.display_name not in self.visited_pages_list:
                print(sub)
                self.visited_pages[sub.display_name] = 1
                self.pages_info[sub.display_name] = sub.public_description
                self.visited_pages_list.append(sub)
            else:
                self.visited_pages[sub.display_name] += 1
        return self.visited_pages_list, self.visited_pages, self.pages_info

    def print_page_info(self):
        """
        prints some basic stats concerning the validated user
        """
        info = self.pages_info
        for k, v in info.items():
            print("Subreddit: {0}\n Description: {1}\n\n".format(k,v))

    def get_potential_matches(self):
        """
        Uses the validated user's visited subreddits to start search for other users
        """
        potential_matches = []
        visited_pages_list = [k for k,v in self.visited_pages.items()]
        # For every subreddit that the validated user has participated in
        for sub in visited_pages_list:
            # for every posts in that subreddit
            for submission in reddit.subreddit(sub).new(limit=10):
                submission.comments.replace_more(limit=1)
                if submission.num_comments > 0:
                    # for every comments in that post get the authors (potentials)
                    for comment in submission.comments:
                        if comment.author not in potential_matches:
                            print(sub,comment.author)
                            potential_matches.append(comment.author)
        self.potential_matches = potential_matches
        return potential_matches

    def process_potential_matches_sub(self):
        """
        # get a set of subbredits where the redditor has left a comment
        """
        potentials_matches_subreddit_list = []
        potential_matches_name_to_sub = {}
        for redditor in self.potential_matches:
            # for dict mapping; for cosign similarity comparison later
            individual_redditors_sub_list = []
            redditor_str = str(redditor)
            user = reddit.redditor(name=redditor_str)
            for comment in user.comments.top(limit=50):
                # body = comment.body
                sub = comment.subreddit

                if sub.display_name not in potentials_matches_subreddit_list:
                    print(sub.display_name)
                    potentials_matches_subreddit_list.append(sub.display_name)

                if sub.display_name not in individual_redditors_sub_list:
                    individual_redditors_sub_list.append(sub.display_name)

            # dict mapping of Redditor: [subreddits]
            if redditor_str not in potential_matches_name_to_sub:
                potential_matches_name_to_sub[redditor_str] = individual_redditors_sub_list

        return potentials_matches_subreddit_list, potential_matches_name_to_sub


    def top_subreddits(self):
        """
        Probably NOT needed
        Process the top 100 subreddits
        """
        freq = {}
        for submission in reddit.subreddit('all').top(limit=100):
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

class Recommender:
    """
    This class concerns pre-processing and implementation of the recommendation 'model'
    """
    def __init__(self,visited_pages_list,all_subreddit_list, redditor_to_subreddit_dict):
        self.visited_pages_list = visited_pages_list
        self.all_subreddit_list = all_subreddit_list
        self.redditor_to_subreddit_dict = redditor_to_subreddit_dict
        self.validated_user_subreddit_vector = []
        # A dict mapping redditors (potential matches) to their respective vectors
        self.redditors_vector_dict = {}
        self.redditors_cosign_similarity = {}

    def vectorization(self):
        """
        Represents the prescence of all subreddits as a vector with 1 indicating a presence.
        """
        validated_user_subreddit_vector = [1 if sub in self.visited_pages_list else 0 for sub in self.all_subreddit_list]
        redditors_to_vector = {}

        for name,visited_subs in self.redditor_to_subreddit_dict.items():
            subreddit_vector = [1 if sub in visited_subs else 0 for sub in self.all_subreddit_list]
            redditors_to_vector[name] = subreddit_vector

        self.validated_user_subreddit_vector = validated_user_subreddit_vector
        self.redditors_vector_dict = redditors_to_vector

        return validated_user_subreddit_vector,self.redditors_vector_dict

    def compute_cosign_similarity(self):
        redditors_cosign_similarity = {}
        for name,sub_vector in self.redditors_vector_dict.items():
            print(name)
            distance = spatial.distance.cosine(self.validated_user_subreddit_vector,sub_vector)
            similarity = 1 - distance
            redditors_cosign_similarity[name] = round(similarity,3)
        self.redditors_cosign_similarity = redditors_cosign_similarity
        return redditors_cosign_similarity

'coordinatedflight'
redditor = Redditor(user='memhir-yasue')
visited_list,visited_dict, info = redditor.process_subreddit_visited()
potential_matches = redditor.get_potential_matches()
pms_list, pms_dict = redditor.process_potential_matches_sub()
for k,v in pms_dict.items():
    print(k,": ",v,"\n\n")
print("{} potential matches and {} subreddits to hot encode".format( len(potential_matches),len(pms_list) ) )
recommender = Recommender(visited_list,pms_list,pms_dict)
val_user_v, r_v_dict = recommender.vectorization()
cosign_similarity = recommender.compute_cosign_similarity()
print(val_user_v)
for k,v in cosign_similarity.items():
    print(k,": ",v,"\n\n")



# sorted_freq = sorted(subreddit_freq.items(), key=lambda x: x[1], reverse=True)
# print(subreddit_freq)


# print(user)
# for comment in user.comments.top('all'):
#     print(comment.subreddit)
#     print(comment.body,'\n')


# reddit.redditor(name='hfdjshfdsjuf').comments.top('all')
