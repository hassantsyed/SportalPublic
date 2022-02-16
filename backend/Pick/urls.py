from django.urls import path

from . import views

urlpatterns = [
    path('<int:UID>/', views.allPicks, name='allPicks'),
    path('<int:UID>/<int:LID>/', views.leaguePicks, name='leaguePicks'),
    path('create/<int:UID>/<int:MID>/', views.createPick, name='createPick'),
    path('upsert/<int:UID>/<int:MID>/', views.upsertPick),
    path('past/<int:UID>/<int:LID>/', views.getPastPicks),
    path('current/<int:UID>/<int:LID>/', views.getCurrentPicks)
]