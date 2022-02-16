from Match.models import Match
from Participant.models import Participant
from League.models import League

from datetime import datetime
#from Match.loaders import defaultLoader

def getAllLeagueMatches(LID):
    res = [m.to_dict() for m in Match.objects.filter(LID = LID)]
    return res


def getUpcomingMatches(LID):
    matches = Match.objects.filter(LID = LID, status__in = ["UPCOMING", "ONGOING"])
    res = [m.to_dict() for m in matches] #Match.objects.filter(LID = LID, status = "UPCOMING")]
    return res

def getFinishedMatches(LID):
    matches = Match.objects.filter(LID = LID).exclude(status__in = ["UPCOMING", "ONGOING"])
    res = [m.to_dict() for m in matches] #Match.objects.filter(LID = LID).exclude(status = "UPCOMING")
    return res

def updateLeagueMatches(LID, data):
    matchLoader = {2: ufcMatchLoader}
    return matchLoader.get(LID, defaultLoader)(LID, data)

def ufcMatchLoader(LID, data):
    resolved_states = ["TEAM1", "TEAM2", "TIE"]
    date = datetime.strptime(data["date"], "%Y-%m-%d")
    for match in data["matches"]:
        p1, _ = Participant.objects.get_or_create(name = match["player1"])
        p2, _ = Participant.objects.get_or_create(name = match["player2"])
        if match["winner"] == "pending":
            m = createOrGetMatch(LID, p1, p2, date)
            m.order = match["order"]
            m.save()
        elif match["winner"] == "player1":
            m = getMatch(LID, p1, p2, date)
            if not m:
                print(f"Match was unable to be found: {p1.name} v. {p2.name}")
                continue
            if m.status in resolved_states:
                continue
            if not m:
                print("no match found")
                continue
            if p1.name == m.team1.name:
                m.status = "TEAM1"
            else:
                m.status = "TEAM2"
            m.result = match.get("result", "")
            m.save()
        elif match["winner"] == "draw":
            m = getMatch(LID, p1, p2, date)
            if m.status in resolved_states:
                continue
            if not m:
                print("no match found draw")
                continue
            m.status = "TIE"
            m.result = match.get("result", "")
            m.save()
        elif match["winner"] == "ongoing":
            m = getMatch(LID, p1, p2, date)
            if m.status in resolved_states:
                continue
            if not m:
                print("no match found")
                continue
            m.status = "ONGOING"
            m.save()
        else:
            print("unsuported.")
            continue
    return 200

def championLeagueLoader(LID, matches):
    raise Exception("not yet implemented")

def checkAPIMatchExistence(match):
    try:
        p1 = Participant.objects.get(name = match["team1"])
        p2 = Participant.objects.get(name = match["team2"])
        if p2 is None or p1 is None:
            return False
        if getAPIMatch(p1, p2, match["apiID"]) is None:
            return False
        return True
    except Exception as ex:
        print(ex)
        return False

def getAPIMatch(p1, p2, apiID):
    match1 = Match.objects.filter(team1 = p1, team2 = p2, apiID=apiID)
    match2 = Match.objects.filter(team1 = p2, team2 = p1, apiID=apiID)
    if match1:
        return match1[0]
    if match2:
        return match2[0]
    return None

def updateAPIMatch(match):
    try:
        p1 = Participant.objects.get(name = match["team1"])
        p2 = Participant.objects.get(name = match["team2"])
        if p2 is None or p1 is None:
            return False
        oldMatch = getAPIMatch(p1, p2, match["apiID"])
        if oldMatch is None:
            return False
        oldMatch.date = datetime.fromisoformat(match["updated_date"])
        oldMatch.save()
        return True
    except Exception:
        return False

def getMatch(LID, p1, p2, date):
    match1 = Match.objects.filter(team1 = p1, team2 = p2, date = date)
    match2 = Match.objects.filter(team1 = p2, team2 = p1, date = date)
    if match1:
        return match1[0]
    if match2:
        return match2[0]
    return None
    

def createOrGetMatch(LID, p1, p2, date, status = "UPCOMING"):
    match = getMatch(LID, p1, p2, date)
    
    if not match:
        match = Match(LID = League.objects.get(pk=LID),
            team1 = p1, 
            team2 = p2, 
            date = date,
            status = status)
        match.save()
    return match

def defaultLoader(LID, data):
    resolved_states = ["TEAM1", "TEAM2", "TIE"]
    for match in data['matches']:
        t1, _ = Participant.objects.get_or_create(name = match["team1"])
        t2, _ = Participant.objects.get_or_create(name = match["team2"])
        startTime = datetime.fromisoformat(match["date"])
        if match["status"] == "UPCOMING":
            m = createOrGetMatch(LID, t1, t2, startTime)
            m.apiID = match["apiID"]
            m.save()
        elif match["status"] in resolved_states:
            m = getMatch(LID, t1, t2, startTime)
            if not m or m.status in resolved_states or m.status == "CANCELLED":
                print("Match could not be found or was already resolved.")
                continue
            m.status = match["status"]
            m.result = match.get("result", "")
            m.save()
        elif match["status"] == "CANCELLED":
            m = getMatch(LID, t1, t2, startTime)
            if not m or m.status in resolved_states:
                print("Match could not be found or already resolved.")
                continue
            m.staus = match["status"]
            m.save()
        elif match["status"] == "ONGOING":
            m = getMatch(LID, t1, t2, startTime)
            if not m or m.status in resolved_states:
                print("Match could not be found or resolved.")
                continue
            m.status = match["status"]
            m.save()
        else:
            print(f"Unsupported {match}")
            continue
    return 200