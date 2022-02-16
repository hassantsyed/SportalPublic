from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .controllers import getMyCrowds, getCurrentCrowdPicks, getPastCrowdPicks, makeCrowd, insertToCrowd, removeFromCrowd

import json

# Create your views here.
def myCrowds(request, UID):
    response = {"crowds": []}
    response["crowds"] = getMyCrowds(UID)
    return JsonResponse(response)

def currentCrowdPicks(request, CID, LID):
    response = {"crowds": []}
    response["crowds"] = getCurrentCrowdPicks(CID, LID)
    return JsonResponse(response)

def pastCrowdPicks(request, CID, LID):
    response = {"crowds": []}
    response["crowds"] = getPastCrowdPicks(CID, LID)
    return JsonResponse(response)

@require_POST
def createCrowd(request, UID):
    response = {"status": 200}
    data = json.loads(request.body)
    response["uuid"] = makeCrowd(UID, data["name"])
    return JsonResponse(response)

def addToCrowd(request, CID, UID):
    response = {"status": 200}
    response["status"] = insertToCrowd(CID, UID)
    return JsonResponse(response)

def leaveCrowd(request, CID, UID):
    response = {"status": 200}
    response["status"] = removeFromCrowd(CID, UID)
    return JsonResponse(response)