from django.urls import path

from . import views

urlpatterns = [
    path('<int:LID>/', views.leagueMatches, name='LeagueMatches'),
    path('upcoming/<int:LID>', views.upcomingLeagueMatches),
    path('finished/<int:LID>', views.finishedLeagueMatches),
    path('updatematches/<int:LID>/', views.updateMatches, name="UpdateLeagueMatches"),
    path('exists/', views.matchExists),
    path('updateTime/', views.matchUpdate)
]