from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from .controllers import create

# Create your views here.
def createParticipant(request, name):
    resp = {"code": 200}
    resp["code"] = create(name)
    return JsonResponse(resp)