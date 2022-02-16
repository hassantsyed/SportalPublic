from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from League.controllers import getSportLeagues

def leagues(request, sport):
    response = {"leagues": []}
    sport = sport.upper()
    leagues = getSportLeagues(sport)
    if not leagues:
        return JsonResponse(response)
    response["leagues"] = leagues 
    return JsonResponse(response)