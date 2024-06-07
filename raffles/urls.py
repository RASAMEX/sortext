"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('raffle/<int:raffle_id>/', views.raffle_details, name='raffle_details'),
    path('create-raffle/', views.create_raffle, name='create_raffle'),
    path('draw/<int:id>/', views.draw_raffle, name='draw_raffle'),
    path('raffle/<int:raffle_id>/update_participants/', views.update_participants, name='update_participants'),
]