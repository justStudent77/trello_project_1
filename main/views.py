from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from .models import Board, TrelloUser


def about_page(request):
    return render(request, "about.html")


def home(request):
    return render(request, "home.html")


class SearchBoardResultView(ListView):
    model = Board
    template_name = "boards/search_board_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Board.objects.filter(
            Q(title__icontains=query) | Q(id__icontains=query)
        )
        return object_list


class SearchUserResultsView(ListView):
    model = TrelloUser
    template_name = "boards/search_user_results.html"

    def get_queryset(self):
        query = self.request.GET.get("user_query")
        object_list = TrelloUser.objects.filter(Q(username__icontains=query))
        return object_list


def get_user_board(request, **kwargs):
    user = TrelloUser.objects.get(username=kwargs["user_id"])
    context = {
        "user": user
    }
    return render(request, "users/user_profile.html", context)
