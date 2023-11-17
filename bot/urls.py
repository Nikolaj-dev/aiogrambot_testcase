from django.urls import path
from . import views


urlpatterns = [
    path('currency/', views.get_currency),
    path('register/', views.register),
    path('history/', views.history),
    path('subscribe/', views.subscribe),
    path('unsubscribe/', views.unsubscribe),
]
