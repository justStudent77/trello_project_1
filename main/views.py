import datetime

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView
from django.template import loader
from django.db.models import Q

from .models import Board, Column, Card, Comment, TrelloUser, CheckList, Mark
from .forms import CreateBoard, CreateColumnForm, CreateCardForm, CommentForm, CheckListForm, MarkForm


# Create your views here.


def about_page(request):
    return render(request, "about.html")


def home(request):
    return render(request, "home.html")


# -----------------------------------------
# Checklists

# ------------------------------------
# Marks

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
