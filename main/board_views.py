from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.template import loader

import datetime

from .models import Board, TrelloUser
from .forms import CreateBoard


class BoardListView(View):

    def get(self, request):
        # boards = Board.objects.all()
        user = request.user
        archived_boards = list(user.archive.keys())
        boards = Board.objects.exclude(pk__in=archived_boards)
        context = {
            "boards": boards
        }
        return render(request, "boards/board_index.html", context)


def get_archived(request):
    user = request.user
    archived_boards = list(user.archive.keys())
    boards = Board.objects.filter(pk__in=archived_boards)
    context = {
        "boards": boards
    }
    return render(request, "boards/board_index_complementary.html", context)


class BoardDetailView(View):

    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        members = list(board.members.keys())
        context = {
            "board": board,
            "columns": board.columns.all(),
            "members": members
        }
        user = request.user
        user.favourite[str(datetime.datetime.now())] = str(board.id)
        user.save()
        return render(request, "boards/board_detail.html", context)


def last_seen(request):
    user = request.user
    last_seen_boards = list(user.favourite.items())
    board_ids = []
    for item in last_seen_boards:
        board_ids.append(int(item[1]))
    try:
        boards = Board.objects.filter(pk__in=board_ids[-6:])
    except:
        boards = Board.objects.filter(pk__in=board_ids)
    context = {
        "boards": boards
    }
    return render(request, "boards/board_index_complementary.html", context)


class BoardCreate(View):

    def get(self, request):
        return render(request, "boards/board_form.html", {"form": CreateBoard})

    def post(self, request):
        form = CreateBoard(request.POST, request.FILES)
        if form.is_valid():
            board = Board(
                title=form.cleaned_data['title'],
                creator=request.user,
                image=form.cleaned_data['image']
            )
            board.save()
        return redirect("boards")


class BoardDeleteView(DeleteView):
    model = Board
    success_url = reverse_lazy("boards")


def archive_board(request, **kwargs):
    user = request.user
    board = Board.objects.get(pk=kwargs["pk"])
    try:
        del user.archive[str(board.id)]
    except:
        user.archive[board.id] = board.title
    user.save()
    return redirect("boards")


def preferred_boards(request, **kwargs):
    user = request.user
    board = Board.objects.get(pk=kwargs["pk"])
    try:
        del user.preferred[str(board.id)]
    except:
        user.preferred[board.id] = board.title
    user.save()
    return redirect("boards")


def list_boards_preferred(request):
    user = request.user
    preferred_boards = list(user.preferred.keys())
    boards = Board.objects.filter(pk__in=preferred_boards)
    context = {
        "boards": boards
    }
    return render(request, "boards/board_index_complementary.html", context)


class BoardUpdateView(View):

    def get(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs["pk"])
        template = loader.get_template("boards/board_update.html")
        members = TrelloUser.objects.exclude(pk=request.user.id)
        context = {
            "board": board,
            "members": members
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs["pk"])
        board.title = request.POST["name"]
        participants = request.POST.getlist("members")
        for item in participants:
            board.members[str(item)] = str(TrelloUser.objects.get(username=item).id)
        board.save()
        columns = board.columns.all()
        context = {
            "board": board,
            "columns": columns,
            "members": list(board.members.keys())
        }
        return render(request, "boards/board_detail.html", context)
