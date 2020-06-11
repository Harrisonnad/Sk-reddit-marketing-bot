import datetime
import requests
import json
import csv


def getPushshiftData(after, before, sub):
    url = (
        "https://api.pushshift.io/reddit/search/submission/?size=1000&after="
        + str(after)
        + "&before="
        + str(before)
        + "&subreddit="
        + str(sub)
    )
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data["data"]


def collectSubData(subm):
    subData = list()  # list to store data points
    author = subm["author"]
    sub_id = subm["id"]

    subData.append((sub_id, author))
    subStats[sub_id] = subData


# Subreddit to query
sub = "Twitch"
# before and after dates
before = "1590624704"  # October 1st
after = "1577840400"  # January 1st
query = "Screenshot"

subCount = 0
subStats = {}

data = getPushshiftData(after, before, sub)
# Will run until all posts have been gathered
# from the 'after' date up until before date
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount += 1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]["created_utc"])))
    after = data[-1]["created_utc"]
    data = getPushshiftData(after, before, sub)

print(len(data))
print(str(len(subStats)) + " submissions have added to list")


def updateSubs_file():
    upload_count = 0
    print("input filename of submission file, please add .csv")
    filename = input()
    file = filename
    with open(file, "w", newline="", encoding="utf-8") as file:
        a = csv.writer(file, delimiter=",")
        headers = ["Post ID", "Author"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count += 1

        print(str(upload_count) + " submissions have been uploaded")


updateSubs_file()
