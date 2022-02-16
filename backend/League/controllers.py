from League.models import League

def getSportLeagues(sportName):
    allLeagues = [l.to_dict() for l in League.objects.filter(sportName=sportName)]
    return allLeagues