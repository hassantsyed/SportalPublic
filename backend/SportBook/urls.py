"""SportBook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import privacy

def privacyPolicy(request):
    return HttpResponse(privacy.privacyPolicy)

def version(request):
    return HttpResponse("K8s")

def health(request):
    return HttpResponse(200)

urlpatterns = [
    path("league/", include("League.urls")),
    path("match/", include("Match.urls")),
    path("account/", include("Account.urls")),
    path("pick/", include("Pick.urls")),
    path("participant/", include("Participant.urls")),
    path("crowd/", include("Crowd.urls")),
    path("health/", health, name="health"),
    path('admin/', admin.site.urls),
    path("", include("django_prometheus.urls")),
    path("privacy/", privacyPolicy, name="privacy"),
    path("version/", version, name="version")
]
