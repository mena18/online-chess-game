from django.shortcuts import render
from django.http import JsonResponse

import os
from dotenv import load_dotenv
from stockfish import Stockfish

load_dotenv()

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
ENGINE = Stockfish(
    path=STOCKFISH_PATH,
    depth=18,
    parameters={"Threads": 2, "Minimum Thinking Time": 30},
)


def computer_random(request):
    return render(request, "computerplayer/computer_random.html")


def computer_strong(request):
    return render(request, "computerplayer/computer_strong.html")


def get_best_move(request):
    fen = request.GET.get("fen", "")
    ENGINE.set_fen_position(fen)
    move = ENGINE.get_best_move()
    print(move)
    data = {
        "source": move[:2],  # "e2"
        "target": move[2:],  # "e4"
    }
    return JsonResponse(data)
