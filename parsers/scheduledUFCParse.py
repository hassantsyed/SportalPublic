import parser
import time
import requests
from datetime import datetime
import random

production = True
devURL = "http://localhost:8000/match/updatematches/2/"
prodURL = "http://sportal.live/match/updatematches/2/"
updateURL = None
if production:
    updateURL = prodURL
else:
    updateURL = devURL

run = True
firstDate = None
idAttempt = 0

while (run):
    modifier = random.randint(0,60)
    data = parser.parse(parser.all_ids()[idAttempt])
    date = datetime.strptime(data["date"], "%Y-%m-%d")
    if firstDate is None:
        firstDate = date
    if firstDate != date:
        idAttempt += 1
        print("different date")
        continue
    if data["matches"][0]["winner"] == "player1":
        run = False
    else:
        for m1, m2 in zip(data["matches"], data["matches"][1:]):
            if m2["winner"] != "pending":
                m1["winner"] = "ongoing"
                break
    # print(data)
    resp = requests.post(updateURL, json = data)
    print(resp)
    print(resp.status_code)
    print(run)
    time.sleep(600 + modifier)
