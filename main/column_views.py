from django.shortcuts import render, HttpResponse
from django.views import View
from django.template import loader


from .models import Board, Column
from .forms import CreateColumnForm, CreateCardForm


class CreateColumnView(View):

    def get(self, request, pk):
        board = Board.objects.get(pk=pk)
        return render(request, "columns/column_form.html", {"form": CreateColumnForm})

    def post(self, request, pk):
        board = Board.objects.get(pk=pk)
        form = CreateColumnForm(request.POST)
        if form.is_valid():
            column = Column(
                title=form.cleaned_data["title"],
                board=board
            )
            column.save()
        context = {
            "board": board,
            "columns": board.columns.all(),
            "members": list(board.members.keys())
        }
        return render(request, "boards/board_detail.html", context)


class ColumnDetailView(View):

    def get(self, request, **kwargs):
        column = Column.objects.get(pk=kwargs["column_id"])
        board = Board.objects.get(pk=kwargs["pk"])
        context = {
            "column": column,
            "cards": column.cards.all(),
            "board": board,
            "form": CreateCardForm
        }
        return render(request, "columns/column_detail.html", context)


def delete_column(request, **kwargs):
    column = Column.objects.get(pk=kwargs["column_id"])
    column.delete()
    board = Board.objects.get(pk=kwargs["pk"])
    context = {
        "board": board,
        "columns": board.columns.all()
    }
    return render(request, "boards/board_detail.html", context)


class ColumnUpdateView(View):

    def get(self, request, **kwargs):
        column = Column.objects.get(pk=kwargs["column_id"])
        board = Board.objects.get(pk=kwargs["pk"])
        template = loader.get_template("columns/column_update.html")
        context = {
            "column": column,
            "board": board
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        column = Column.objects.get(pk=kwargs["column_id"])
        board = Board.objects.get(pk=kwargs["pk"])
        column.title = request.POST["title"]
        column.board = Board.objects.get(title=request.POST["board"])
        column.save()
        context = {
            "column": column,
            "cards": column.cards.all(),
            "board": board
        }
        return render(request, "columns/column_detail.html", context)
