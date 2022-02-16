from django.urls import path

from . import views

urlpatterns = [
    path('<int:UID>/', views.myCrowds),
    path('current/<uuid:CID>/<int:LID>/', views.currentCrowdPicks),
    path('past/<uuid:CID>/<int:LID>/', views.pastCrowdPicks),
    path('create/<int:UID>/', views.createCrowd),
    path('add/<uuid:CID>/<int:UID>/', views.addToCrowd),
    path('exit/<uuid:CID>/<int:UID>/', views.leaveCrowd),
]