import csv
import requests
import json
from collections import Counter

f = open("oop.csv")
csv_f = csv.reader(f)


class subreddit_author_parser:
    def create_list_authors(self, data_list):
        """ Takes a dictionary list of data and reutnrs it as a list to be parsed easily"""
        twitch_author_list = []
        for author in data_list:
            author_dict = {"name": author[1]}
            twitch_author_list.append(author_dict["name"])
        return twitch_author_list

    def _get_pushshift_author_data(self, user_name):
        """Collects pushshift data from individual users"""
        url = f"https://api.pushshift.io/reddit/search/submission/?author={user_name}&filter=subreddit&limit=1000"
        print(url)
        r = requests.get(url)
        data = json.loads(r.text)
        return data["data"]

    def _collect_author_subreddit_data(self, submission):
        """creates a list of subreddit history to be compared"""
        subreddit_author_data = list()  # list to store data points
        subreddit_signature = submission["subreddit"]

        subreddit_author_data.append((subreddit_signature))

    def compare_subreddit_data(self, new_author_list):
        """Runs through the list created by create_list_authors and finds the most common 100 subreddits users are being active in """
        list_of_authors_subreddits = []
        for user in new_author_list:
            print(user)
            try:
                subreddit_list = self.get_pushshift_author_data(user)
                for individual in subreddit_list:
                    try:
                        list_of_authors_subreddits.append(individual["subreddit"])
                    except KeyError:
                        continue
            except ValueError:
                continue
        return Counter(list_of_authors_subreddits).most_common(100)

    def main(self):
        author_list = self.create_list_authors(csv_f)
        new_author_list = list(set(author_list))
        return self.compare_subreddit_data(new_author_list)


results = subreddit_author_parser()
print(results.main())
