from django.urls import path

from . import views

urlpatterns = [
    # path('create/<str:GID>/', views.create, name='create'),
    path('', views.get, name="get")
]   