from .models import Pick
from League.models import League
from Match.models import Match
from Account.models import Account

def getAllPicks(UID):
    # picks = Pick.objects.filter(UID = UID)
    picks = [p.to_dict() for p in Pick.objects.filter(UID = UID)]
    print(picks)
    return picks

def getLeaguePicks(UID, LID):
    picks = [p.to_dict() for p in Pick.objects.filter(UID=UID).filter(LID=LID)]
    return picks

def createPickSelection(UID, MID, selection):
    # check if pick already exists
    match = Match.objects.get(pk=MID)
    u = Account.objects.get(pk=UID)
    p = Pick(LID=match.LID, UID=u, MID=match, pick=selection)
    p.save()
    return p.to_dict()

def upsertPickSelection(UID, MID, selection):
    u = Account.objects.get(pk = UID)
    m = Match.objects.get(pk = MID)
    if selection == -1: #delete pick
        pick = Pick.objects.filter(UID = u, MID = m)
        if not pick: #doesnt exitst
            return 200
        pick = pick[0]
        pick.delete()
        return 200
    elif selection == 0 or selection == 1: #update / create
        selectedTeam = None
        if selection == 0:
            selectedTeam = "TEAM1"
        else:
            selectedTeam = "TEAM2"

        pick = Pick.objects.filter(UID = u, MID = m)
        
        if not pick: #need to create
            print("creating pick")
            pick = Pick(LID=m.LID, UID = u, MID = m, pick = selectedTeam)
        else: #need to update
            print("updating pick")
            pick = pick[0]
            pick.pick = selectedTeam
        
        pick.save()
        return 200
        
    else:
        return 404

def pastPicks(UID, LID):
    pastPs = Pick.objects.filter(LID = LID, UID = UID).exclude(MID__status__in = ["UPCOMING", "ONGOING"])
    return [p.to_dict() for p in pastPs]

def currentPicks(UID, LID):
    curPs = Pick.objects.filter(MID__status__in = ["UPCOMING", "ONGOING"], LID = LID, UID = UID)
    return [p.to_dict() for p in curPs]