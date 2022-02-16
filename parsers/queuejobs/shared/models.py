from datetime import datetime

class Match(object):
    def __init__(self, 
        ID: int, 
        API: str, 
        APIleague: int, 
        sportalLeague: int, 
        team1: str, 
        team2: str, 
        status: str, 
        result: str,
        startTime: datetime, 
        endTime: datetime, 
        count: int = 0
    ):
        self.ID = ID
        self.API = API
        self.APIleague = APIleague
        self.sportalLeague = sportalLeague
        self.team1 = team1
        self.team2 = team2
        self.status = status
        self.result = result
        self.startTime = startTime
        self.endTime = endTime
        self.count = count

    def to_dict(self):
        return {
            "ID": self.ID,
            "API": self.API,
            "APIleague": self.APIleague,
            "sportalLeague": self.sportalLeague,
            "team1": self.team1,
            "team2": self.team2,
            "status": self.status,
            "result": self.result,
            "startTime": self.startTime.isoformat(),
            "endTime": self.endTime.isoformat(),
            "count": self.count
        }

class SportalEvent:
    def __init__(self, team1: str, team2: str, date: datetime, status: str, apiID: int, result: str):
        self.team1 = team1
        self.team2 = team2
        self.date = date
        self.status = status
        self.apiID = apiID
        self.result = result

    def to_dict(self):
        return {
            "team1": self.team1,
            "team2": self.team2,
            "date": self.date.isoformat(),
            "status": self.status,
            "apiID": self.apiID,
            "result": self.result
        }

def matchToEvent(match: Match) -> SportalEvent:
    return SportalEvent(match.team1, match.team2, match.startTime, match.status, match.ID, match.result)

def blobToMatch(data) -> Match:
    return Match(
        data["ID"],
        data["API"],
        data["APIleague"],
        data["sportalLeague"],
        data["team1"],
        data["team2"],
        data["status"],
        data.get("result", ""),
        datetime.fromisoformat(data["startTime"]),
        datetime.fromisoformat(data["endTime"]),
        data["count"]
    )