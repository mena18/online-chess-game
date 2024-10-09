from django.shortcuts import render

# Create your views here.


def index(request):
    print("hello world")
    print("temp")
    return render(request, "chess/index.html")
