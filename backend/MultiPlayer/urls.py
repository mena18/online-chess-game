from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("multiPlayer/<str:room_name>/", views.room, name="room"),
    path("AiGame/Weak/", views.computer_random, name="weak_ai"),
    path("AiGame/Strong/", views.computer_strong, name="Strong_ai"),
    path("AiGame/Strong/best_move/", views.get_best_move, name="best_move"),
]
