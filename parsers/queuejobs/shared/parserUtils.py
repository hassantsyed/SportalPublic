import requests
from datetime import datetime, timedelta
from typing import Dict, List
from . import NBAParser, NFLParser, NHLParser
from . import models
# import models
# import NBAParser, NFLParser, NHLParser

AZURE_SA_CON_STR = ""
startQ = ""
endQ = ""
SPORTAL_LEAGUE = 1
production = True
devURL = f"http://localhost:8000/match/updatematches/"
prodURL = f"http://sportal.live/match/updatematches/"
updateURL = None
if production:
    updateURL = prodURL
else:
    updateURL = devURL

def submitEvents(matches: List[models.Match], sportalLeague: int) -> int:
    submitURL = updateURL + str(sportalLeague) + "/"
    events = [models.matchToEvent(m).to_dict() for m in matches]
    try:
        resp = requests.post(submitURL, json={"matches": events})
    except Exception as ex:
        print(ex)
        return 400
    return resp.status_code

def matchToParsers(match: models.Match):
    parsers = {1: NBAParser.NBAParser, 3: NFLParser.NFLParser, 4: NHLParser.NHLParser}
    return parsers[match.sportalLeague]()

def exists(match: models.Match) -> bool:
    checkURL = None
    if production:
        checkURL = "http://sportal.live/match/exists/"
    else:
        checkURL = "http://localhost:8000/match/exists/"
    event = models.matchToEvent(match).to_dict()
    try:
        resp = requests.post(checkURL, json=event)
        if resp.status_code == 200:
            return True
    except Exception:
        return False
    return False

def updateMatchTime(oldMatch: models.Match, newMatch: models.Match):
    checkURL = None
    if production:
        checkURL = "http://sportal.live/match/updateTime/"
    else:
        checkURL = "http://localhost:8000/match/updateTime/"
    event = models.matchToEvent(oldMatch).to_dict()
    event["updated_date"] = newMatch.startTime.isoformat()
    try:
        resp = requests.post(checkURL, json=event)
        if resp.status_code == 200:
            return True
    except Exception:
        return False
    return False
