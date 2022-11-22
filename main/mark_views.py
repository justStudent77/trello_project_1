from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.template import loader

from .models import Board, Column, Card, Mark
from .forms import MarkForm


class CreateMark(View):

    def get(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs["pk"])
        column = Column.objects.get(pk=kwargs["column_id"])
        card = Card.objects.get(pk=kwargs["card_id"])
        context = {
            "board": board,
            "column": column,
            "card": card,
            "form": MarkForm
        }
        return render(request, "mark/mark_form.html", context)

    def post(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs["pk"])
        column = Column.objects.get(pk=kwargs["column_id"])
        card = Card.objects.get(pk=kwargs["card_id"])
        form = MarkForm(request.POST)
        if form.is_valid():
            mark = Mark(
                title=form.cleaned_data["title"],
                card=card,
                colour=form.cleaned_data["colour"],
            )
            mark.save()
        context = {
            "column": column,
            "card": card,
            "board": board,
            "form": MarkForm
        }
        return HttpResponseRedirect(reverse('card_view', args=(board.id, column.id, card.id)))


class UpdateMark(View):

    def get(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs["card_id"])
        column = Column.objects.get(pk=kwargs["column_id"])
        columns = Column.objects.all()
        board = Board.objects.get(pk=kwargs["pk"])
        mark = Mark.objects.get(pk=kwargs["mark_id"])
        template = loader.get_template("mark/mark_update.html")
        context = {
            "columns": columns,
            "card": card,
            "column": column,
            "board": board,
            "mark": mark,
            "form": MarkForm
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs["card_id"])
        column = Column.objects.get(pk=kwargs["column_id"])
        board = Board.objects.get(pk=kwargs["pk"])
        mark = Mark.objects.get(pk=kwargs["mark_id"])
        mark.title = request.POST["title"]
        mark.colour = request.POST["colour"]
        mark.card = Card.objects.get(title=request.POST["card"])
        mark.save()
        return HttpResponseRedirect(reverse("card_view", args=(board.id, column.id, card.id)))


def delete_mark(request, **kwargs):
    column = Column.objects.get(pk=kwargs["column_id"])
    card = Card.objects.get(pk=kwargs["card_id"])
    board = Board.objects.get(pk=kwargs["pk"])
    mark = Mark.objects.get(pk=kwargs["mark_id"])
    mark.delete()
    return HttpResponseRedirect(reverse("card_view", args=(board.id, column.id, card.id)))

