from django.shortcuts import render


def home(request):
    """Home page displaying charts and odds tables."""
    return render(request, "polls/home.html")


def about(request):
    """About page with information about BetPoll."""
    return render(request, "polls/about.html")
