from datetime import datetime, timezone, timedelta
import requests
from . import models
# import models

class NFLParser:
    def __init__(self):
        self.NAME = "NFL"
        self.SPORTAL_LEAGUE = 3
        self.API_LEAGUE = "NFL"
        self.API_URL = "https://sportspage-feeds.p.rapidapi.com/games"
        self.API_ID_URL = "https://sportspage-feeds.p.rapidapi.com/gameById"
        self.PAYLOAD = {"league": self.API_LEAGUE}
        self.HEADERS = {
            'x-rapidapi-host': "sportspage-feeds.p.rapidapi.com",
            'x-rapidapi-key': "7520aba88bmsh850bef9ee546f84p15ccc1jsnf955f50552ed"
        }
        self.EVENT_LENGTH = 195

    
    def getMatchesForTwoDay(self) -> [models.Match]:
        datas = []
        for i in range(2):
            cur = datetime.now() + timedelta(days=i)
            curDate = cur.strftime("%Y-%m-%d")
            self.PAYLOAD["date"] = curDate
            response = requests.get(self.API_URL, headers=self.HEADERS, params=self.PAYLOAD)
            datas += response.json()["results"]
        results = []
        for m in datas:
            match = self.parseToMatch(m)
            results.append(match)
        return results

    def getMatchByID(self, ID: int) -> models.Match:
        resp = requests.get(self.API_ID_URL, headers = self.HEADERS, params={"gameId": ID})
        match = self.parseToMatch(resp.json()["results"][0])
        return match

    def parseToMatch(self, data):
        team1: str = data["teams"]["home"]["team"]
        team2: str = data["teams"]["away"]["team"]
        status: str = None
        result: str = ""
        if data["status"] == "in progress":
            status = "ONGOING"
        elif data["status"] == "final":
            status = "finished"
        elif data["status"] == "scheduled":
            status = "UPCOMING"
        else:
            status = "ONGOING"

        if status == "finished":
            t1Score = data["scoreboard"]["score"]["home"]
            t2Score = data["scoreboard"]["score"]["away"]
            result = f"{t1Score} - {t2Score}"
            if t1Score == t2Score:
                status = "TIE"
            elif t1Score > t2Score:
                status = "TEAM1"
            else:
                status = "TEAM2"
        time = datetime.strptime(data["schedule"]["date"], '%Y-%m-%dT%H:%M:%S.%fZ')
        time = time.replace(tzinfo=timezone.utc)
        time = time.isoformat()
        startTime = datetime.fromisoformat(time)
        return models.Match(
            data["gameId"], 
            self.NAME, 
            self.API_LEAGUE, 
            self.SPORTAL_LEAGUE, 
            team1, 
            team2, 
            status,
            result, 
            startTime, 
            startTime + timedelta(minutes=self.EVENT_LENGTH)
        )