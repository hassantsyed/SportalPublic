from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from .controllers import getAllPicks, getLeaguePicks, createPickSelection, upsertPickSelection, pastPicks, currentPicks

import json
import time

# Create your views here.
def leaguePicks(request, UID, LID):
    resp = {"picks": []}
    picks = getLeaguePicks(UID, LID)
    if not picks:
        return JsonResponse(resp)
    resp["picks"] = picks
    return JsonResponse(resp)

def allPicks(request, UID):
    resp = {"picks": []}
    picks = getAllPicks(UID)
    if not picks:
        return JsonResponse(resp)
    resp["picks"] = picks
    return JsonResponse(resp)

def createPick(request, UID, MID):
    selection = request.body.decode("UTF-8")
    print(selection)
    resp = {"pick": None}
    result = createPickSelection(UID, MID, selection)
    if not result:
        return JsonResponse(resp)
    resp["pick"] = result
    return JsonResponse(resp)

def upsertPick(request, UID, MID):
    response = {"status" : 404}
    if request.method == 'POST':
        data = json.loads(request.body)["selection"]
        response["status"] = upsertPickSelection(UID, MID, data)
        return JsonResponse(response)
    else:
        return JsonResponse(response)

def getPastPicks(request, UID, LID):
    response = {"picks": []}
    response["picks"] = pastPicks(UID, LID)
    return JsonResponse(response)

def getCurrentPicks(request, UID, LID):
    response = {"picks": []}
    response["picks"] = currentPicks(UID, LID)
    return JsonResponse(response)