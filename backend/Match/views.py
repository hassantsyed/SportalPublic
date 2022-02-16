from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_POST

from .models import Match
from .controllers import getAllLeagueMatches, updateLeagueMatches, getUpcomingMatches, getFinishedMatches, checkAPIMatchExistence, updateAPIMatch

from datetime import datetime
import json


# Create your views here.
def leagueMatches(request, LID):
    response = {"matches": []}
    allMatches = getAllLeagueMatches(LID)
    if not allMatches:
        return JsonResponse(response)
    response["matches"] = allMatches
    return JsonResponse(response)

def upcomingLeagueMatches(request, LID):
    response = {"matches": []}
    response["matches"] = getUpcomingMatches(LID)
    return JsonResponse(response)

def finishedLeagueMatches(request, LID):
    response = {"matches": []}
    response["matches"] = getFinishedMatches(LID)
    return JsonResponse(response)

def updateMatches(request, LID):
    response = {"status" : 404}
    if request.method == 'POST':
        data = json.loads(request.body)
        response["status"] = updateLeagueMatches(LID, data)
        return JsonResponse(response)
    else:
        return JsonResponse(response)

@require_POST
def matchExists(request):
    match = json.loads(request.body)
    if checkAPIMatchExistence(match):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=300)

@require_POST
def matchUpdate(request):
    match = json.loads(request.body)
    if updateAPIMatch(match):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=300)