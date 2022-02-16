from bs4 import BeautifulSoup
import requests
from datetime import datetime

eventsURL = "http://www.ufcstats.com/event-details/"

statsURL = "http://www.ufcstats.com/statistics/events/completed"

def parse_finished(eventID):
    reqURL = eventsURL + eventID
    data = requests.get(reqURL).text
    soup = BeautifulSoup(data, 'html.parser')
    matches = []
    rows = soup.findAll("tr")[1:]
    for r in rows:
        winner = r.find_all(class_ = "b-fight-details__table-col b-fight-details__table-col_style_align-top")
        print(winner)
        fight = r.find_all(class_="b-fight-details__table-col l-page_align_left")[0]
        fighters = fight.find_all(class_="b-link b-link_style_black")
        cur_match = {}
        for i in range(len(fighters)):
            cur_match[f"player{i+1}"] = fighters[i].text.strip()
        matches.append(cur_match)
    return matches

# returns list of fights... [{player1 : ..., player2: ....}, ...]
# ordered from main event to first
def parse_upcoming(eventID):
    reqURL = eventsURL + eventID
    data = requests.get(reqURL).text
    soup = BeautifulSoup(data, 'html.parser')
    matches = []
    rows = soup.findAll("tr")[1:]
    for r in rows:
        winner = r.find_all(class_ = "b-flag b-flag_style_green")
        print(winner)
        fight = r.find_all(class_="b-fight-details__table-col l-page_align_left")[0]
        fighters = fight.find_all(class_="b-link b-link_style_black")
        cur_match = {}
        for i in range(len(fighters)):
            cur_match[f"player{i+1}"] = fighters[i].text.strip()
        matches.append(cur_match)
    return matches

def parse(eventID):
    reqURL = eventsURL + eventID
    data = requests.get(reqURL).text
    soup = BeautifulSoup(data, 'html.parser')
    result = {}
    matches = []
    rows = soup.findAll("tr")[1:]
    for idx, r in enumerate(rows):
        cur_match = {}
        fight = r.find_all(class_="b-fight-details__table-col l-page_align_left")[0]
        method = r.find_all(class_="b-fight-details__table-col l-page_align_left")[-1]
        fighters = fight.find_all(class_="b-link b-link_style_black")
        winner = r.find_all(class_ = "b-flag b-flag_style_green")
        draw = r.find_all(class_ = "b-flag b-flag_style_bordered")
        if len(winner) > 0:
            cur_match["winner"] = "player1"
        elif len(draw) > 0:
            cur_match["winner"] = "draw"
        else:
            cur_match["winner"] = "pending"
        for i in range(len(fighters)):
            cur_match[f"player{i+1}"] = fighters[i].text.strip()
        cur_match["order"] = idx
        if cur_match["winner"] != "pending":
            match_res = method.find_all(class_="b-fight-details__table-text")[0].text.strip()
            if "DEC" in match_res:
                match_res = "DEC"
            cur_match["result"] = match_res
        matches.append(cur_match)
    result["matches"] = matches
    dirtyDate = soup.find_all(class_="b-list__box-list-item")[0].text
    dirtyDate = dirtyDate.strip()
    dirty = dirtyDate.splitlines()
    date = dirty[-1].strip()
    cleanedDate = datetime.strptime(date, "%B %d, %Y")
    result["date"] = f"{cleanedDate.year}-{cleanedDate.month}-{cleanedDate.day}"

    return result
    #return result

def last_completed_id():
    data = requests.get(statsURL).text
    soup = BeautifulSoup(data, 'html.parser')
    events = soup.find_all(class_="b-link b-link_style_black")
    latest = events[0].get("href").split("/")[-1]
    #print(latest)
    return latest

def upcoming_id():
    data = requests.get(statsURL).text
    soup = BeautifulSoup(data, 'html.parser')
    event = soup.find(class_="b-link b-link_style_white")
    last = event.get("href").split("/")[-1]
    # print(last)
    return last

def all_ids():
    data = requests.get(statsURL).text
    soup = BeautifulSoup(data, "html.parser")
    events = soup.find_all(class_ = "b-link")
    events = [e.get("href").split("/")[-1] for e in events]
    return events

