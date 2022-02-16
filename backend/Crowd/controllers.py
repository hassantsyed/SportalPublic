from Crowd.models import Crowd
from Account.models import Account
from Pick.models import Pick

def getMyCrowds(UID):
    a = Account.objects.get(pk = UID)
    data = a.crowd_set.all()
    # data = Crowd.objects.filter(accounts__id = UID)
    return [d.to_dict() for d in data]


def getCurrentCrowdPicks(CID, LID):
    crowd = Crowd.objects.get(pk = CID)
    accounts = crowd.accounts.all()
    accountIds = [a.pk for a in accounts]
    curPs = Pick.objects.filter(MID__status = "UPCOMING", LID = LID, UID__in = accountIds)
    return [p.to_dict() for p in curPs]

def getPastCrowdPicks(CID, LID):
    crowd = Crowd.objects.get(pk = CID)
    accounts = crowd.accounts.all()
    accountIds = [a.pk for a in accounts]
    curPs = Pick.objects.filter(LID = LID, UID__in = accountIds).exclude(MID__status = "UPCOMING")
    res = {pick.MID.pk : {"TEAM1": 0, "TEAM2": 0, "player1": pick.MID.team1.name, "player2": pick.MID.team2.name, "winner": pick.MID.status, "mid": pick.MID.pk, "date": pick.MID.date} for pick in curPs}
    for pick in curPs:
        if pick.MID.pk in res:
            if pick.pick == "TEAM1":
                res[pick.MID.pk]["TEAM1"] += 1
            else:
                res[pick.MID.pk]["TEAM2"] += 1
    #print(list(res.values()))
    return list(res.values())

def makeCrowd(UID, name):
    crowd = Crowd(name = name)
    crowd.save()
    a = Account.objects.get(pk = UID)
    crowd.accounts.add(a)
    crowd.save()
    return crowd.ooid

def insertToCrowd(CID, UID):
    crowd = Crowd.objects.get(pk = CID)
    a = Account.objects.get(pk = UID)
    crowd.accounts.add(a)
    crowd.save()
    return 200

def removeFromCrowd(CID, UID):
    crowd = Crowd.objects.get(pk = CID)
    a = Account.objects.get(pk = UID)
    crowd.accounts.remove(a)
    crowd.save()
    return 200