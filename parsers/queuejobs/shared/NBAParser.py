from datetime import datetime, timezone, timedelta
import requests
from . import models
# import models

class NBAParser:
    def __init__(self):
        self.NAME = "NBA"
        self.SPORTAL_LEAGUE = 1
        self.API_LEAGUE = 12
        self.API_URL = "https://api-basketball.p.rapidapi.com/games"
        self.PAYLOAD = {"season":"2019-2020","league": self.API_LEAGUE}
        self.HEADERS = {
            'x-rapidapi-host': "api-basketball.p.rapidapi.com",
            'x-rapidapi-key': "7520aba88bmsh850bef9ee546f84p15ccc1jsnf955f50552ed"
        }
        self.EVENT_LENGTH = 150

    
    def getMatchesForTwoDay(self) -> [models.Match]:
        datas = []
        for i in range(2):
            cur = datetime.now() + timedelta(days=i)
            curDate = cur.strftime("%Y-%m-%d")
            self.PAYLOAD["date"] = curDate
            response = requests.get(self.API_URL, headers=self.HEADERS, params=self.PAYLOAD)
            datas += response.json()["response"]
        # data = testData
        results = []
        for m in datas:
            match = self.parseToMatch(m)
            results.append(match)
        return results

    def getMatchByID(self, ID: int) -> models.Match:
        resp = requests.get(self.API_URL, headers = self.HEADERS, params={"id": ID})
        match = self.parseToMatch(resp.json()["response"][0])
        return match

    def parseToMatch(self, data):
        team1: str = data["teams"]["home"]["name"]
        team2: str = data["teams"]["away"]["name"]
        status: str = None
        result: str = ""
        if data["status"]["short"] == "FT" or data["status"]["short"] == "AOT":
            status = "finished"
        elif data["status"]["long"] == "Over Time":
            status = "ONGOING"
        elif data["status"]["short"] is None or data["status"]["short"] == "NS":
            status = "UPCOMING"
        elif data["status"]["short"] == "POST":
            status = "CANCELLED"
        else:
            status = "ONGOING"
        if status == "finished":
            t1Score = data["scores"]["home"]["total"]
            t2Score = data["scores"]["away"]["total"]
            result = f"{t1Score} - {t2Score}"
            if t1Score == t2Score:
                status = "TIE"
            elif t1Score > t2Score:
                status = "TEAM1"
            else:
                status = "TEAM2"
        startTime = datetime.fromisoformat(data["date"])
        return models.Match(
            data["id"], 
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
