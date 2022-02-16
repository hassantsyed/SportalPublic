from datetime import datetime, timezone, timedelta
import requests
from . import models
# import models

class NHLParser:
    def __init__(self):
        self.NAME = "NHL"
        self.SPORTAL_LEAGUE = 4
        self.API_LEAGUE = "NHL"
        self.API_URL = "https://statsapi.web.nhl.com/api/v1/schedule?"
        self.API_ID_URL = "https://statsapi.web.nhl.com/api/v1/schedule?gamePk="
        self.EVENT_LENGTH = 150

    
    def getMatchesForTwoDay(self) -> [models.Match]:
        cur = datetime.now()
        curDate = cur.strftime("%Y-%m-%d")
        curNext = datetime.now() + timedelta(days=2)
        curDateNext = curNext.strftime("%Y-%m-%d")
        dateURL = f"startDate={curDate}&endDate={curDateNext}"
        response = requests.get(self.API_URL + dateURL)
        data = response.json()["dates"]
        datas = []
        for dat in data:
            datas += dat["games"]
        results = []
        for m in datas:
            match = self.parseToMatch(m)
            results.append(match)
        return results

    def getMatchByID(self, ID: int) -> models.Match:
        resp = requests.get(self.API_ID_URL + str(ID))
        match = self.parseToMatch(resp.json()["dates"][0]["games"][0])
        return match

    def parseToMatch(self, data):
        team1: str = data["teams"]["home"]["team"]["name"]
        team2: str = data["teams"]["away"]["team"]["name"]
        status: str = None
        result: str = ""
        if data["status"]["abstractGameState"] == "Live":
            status = "ONGOING"
        elif data["status"]["abstractGameState"] == "Final":
            status = "finished"
        elif data["status"]["abstractGameState"]  == "Preview":
            status = "UPCOMING"
        else:
            status = "ONGOING"

        if status == "finished":
            t1Score = data["teams"]["home"]["score"]
            t2Score = data["teams"]["away"]["score"]
            result = f"{t1Score} - {t2Score}"
            if t1Score == t2Score:
                status = "TIE"
            elif t1Score > t2Score:
                status = "TEAM1"
            else:
                status = "TEAM2"
        time = datetime.strptime(data["gameDate"], '%Y-%m-%dT%H:%M:%SZ')
        time = time.replace(tzinfo=timezone.utc)
        time = time.isoformat()
        startTime = datetime.fromisoformat(time)
        return models.Match(
            data["gamePk"], 
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
