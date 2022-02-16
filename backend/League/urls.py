from django.urls import path

from . import views

urlpatterns = [
    path('<str:sport>/', views.leagues, name='leagues'),
]