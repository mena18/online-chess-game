from django.urls import path

from . import views

urlpatterns = [
    path("Weak/", views.computer_random, name="weak_ai"),
    path("Strong/", views.computer_strong, name="Strong_ai"),
    path("Strong/best_move/", views.get_best_move, name="best_move"),
]
