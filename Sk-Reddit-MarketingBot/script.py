import requests
import json
import csv
import datetime


class pushshift_parser:

    sub_stats = {}

    def __init__(self, subreddit, before_date, after_date):
        self.subreddit = subreddit
        self.before_date = before_date
        self.after_date = after_date

    def get_pushshift_data(self):
        url = f"https://api.pushshift.io/reddit/search/submission/?size=1000&after={self.after_date}&before={self.before_date}&subreddit={self.subreddit}"
        print(url)
        r = requests.get(url)
        data = json.loads(r.text)
        return data["data"]

    def collect_subreddit_Data(self, submission):
        sub_data = list()  # list to store data points
        author = submission["author"]
        sub_id = submission["id"]

        sub_data.append((sub_id, author))
        self.substats[sub_id] = sub_data

    def gather_all_posts(self, data):
        sub_count = 0
        while len(data) > 0:
            for submission in data:
                self.collect_subreddit_data(submission)
                sub_count += 1
            # Calls getPushshiftData() with the created date of the last sub
            print(len(data))
            date = str(datetime.datetime.fromtimestamp(data[-1]["created_utc"]))
            print(date)
            self.after_date = data[-1]["created_utc"]
            data = self.get_pushshift_data()
        print(len(data))
        print(str(len(self.subStats)) + " submissions have added to list")
        return self.subStats

    def main(self):
        data = self.get_pushshift_data()
        return self.gather_all_posts(data)


Twitch = pushshift_parser("Twitch", "1590624704", "1587840400")

collection = Twitch.main()


def update_subreddit_file(collection):
    upload_count = 0
    print("input filename of submission file, please add .csv")
    filename = input()
    file = filename
    with open(file, "w", newline="", encoding="utf-8") as file:
        a = csv.writer(file, delimiter=",")
        headers = ["Post ID", "Author"]
        a.writerow(headers)
        for sub in collection:
            a.writerow(collection[sub][0])
            upload_count += 1

        print(str(upload_count) + " submissions have been uploaded")


update_subreddit_file(collection)
