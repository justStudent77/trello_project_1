from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.template import loader


from .models import Board, Column, Card, CheckList
from .forms import CommentForm, CheckListForm


class CreateChecklist(View):

    def get(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs["pk"])
        column = Column.objects.get(pk=kwargs["column_id"])
        card = Card.objects.get(pk=kwargs["card_id"])
        context = {
            "board": board,
            "column": column,
            "card": card,
            "form": CheckListForm
        }
        return render(request, "checklist/checklist_form.html", context)

    def post(self, request, **kwargs):
        board = Board.objects.get(pk=kwargs["pk"])
        column = Column.objects.get(pk=kwargs["column_id"])
        card = Card.objects.get(pk=kwargs["card_id"])
        form = CheckListForm(request.POST)
        if form.is_valid():
            checklist = CheckList(
                title=form.cleaned_data["title"],
                card=card,
                author=card.column.board.creator
            )
            checklist.save()
        context = {
            "column": column,
            "card": card,
            "board": board,
            "form": CheckListForm
        }
        return HttpResponseRedirect(reverse('card_view', args=(board.id, column.id, card.id)))


class UpdateChecklist(View):

    def get(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs["card_id"])
        column = Column.objects.get(pk=kwargs["column_id"])
        columns = Column.objects.all()
        board = Board.objects.get(pk=kwargs["pk"])
        checklist = CheckList.objects.get(pk=kwargs["checklist_id"])
        template = loader.get_template("checklist/checklist_update.html")
        context = {
            "columns": columns,
            "card": card,
            "column": column,
            "board": board,
            "checklist": checklist,
            "form": CommentForm
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs["card_id"])
        column = Column.objects.get(pk=kwargs["column_id"])
        board = Board.objects.get(pk=kwargs["pk"])
        checklist = CheckList.objects.get(pk=kwargs["checklist_id"])
        checklist.title = request.POST["title"]
        checklist.card = Card.objects.get(title=request.POST["card"])
        checklist.save()
        return HttpResponseRedirect(reverse("card_view", args=(board.id, column.id, card.id)))


def delete_checklist(request, **kwargs):
    column = Column.objects.get(pk=kwargs["column_id"])
    card = Card.objects.get(pk=kwargs["card_id"])
    board = Board.objects.get(pk=kwargs["pk"])
    checklist = CheckList.objects.get(pk=kwargs["checklist_id"])
    checklist.delete()
    return HttpResponseRedirect(reverse("card_view", args=(board.id, column.id, card.id)))
