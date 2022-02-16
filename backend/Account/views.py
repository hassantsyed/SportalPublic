from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from .controllers import createAccount, getAccount
from django.views.decorators.http import require_POST
import json

# Create your views here.
def create(request, GID):
    resp = {"account": 200}
    resp["account"] = createAccount(GID)
    return JsonResponse(resp)

@require_POST
def get(request):
    user = json.loads(request.body)
    resp = {"account": None}
    try:
        gid = user["GID"]
        resp["account"] = getAccount(gid)
    except Exception as ex:
        print(ex)
    return JsonResponse(resp)