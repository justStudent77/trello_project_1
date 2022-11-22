from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.template import loader

from .models import Board, Column, Card, Comment
from .forms import CreateCardForm, CommentForm


class CreateCardView(View):

    def get(self, request, **kwargs):
        column = Column.objects.get(pk=kwargs["column_id"])
        board = Board.objects.get(pk=kwargs["pk"])
        context = {
            "board": board,
            "column": column,
            "form": CreateCardForm
        }
        return render(request, "cards/card_form.html", context)

    def post(self, request, pk, column_id):
        column = Column.objects.get(pk=column_id)
        board = Board.objects.get(pk=pk)
        form = CreateCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = Card(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                column=column,
                due_date=form.cleaned_data['due_date']
            )
            card.save()
        context = {
            "column": column,
            "cards": column.cards.all(),
            "board": board,
            "form": CreateCardForm
        }
        return render(request, "columns/column_detail.html", context)


class CardDetailView(View):

    def get(self, request, pk, column_id, card_id):
        board = Board.objects.get(pk=pk)
        column = Column.objects.get(pk=column_id)
        card = Card.objects.get(pk=card_id)
        comments = Comment.objects.filter(card=card)
        checklist = card.checklist.all()
        marks = card.mark.all()
        form = CommentForm()
        context = {
            "card": card,
            "column": column,
            "card_title": card.title,
            "card_description": card.description,
            "board": board,
            "comments": comments,
            "checklists": checklist,
            "marks": marks,
            "form": form
        }
        return render(request, "cards/card_detail.html", context)

    def post(self, request, pk, column_id, card_id):
        board = Board.objects.get(pk=pk)
        column = Column.objects.get(pk=column_id)
        card = Card.objects.get(pk=card_id)
        form = CommentForm(request.POST)
        marks = card.mark.all()
        if form.is_valid():
            comment = Comment(
                author=request.user,
                body=form.cleaned_data["body"],
                card=card
            )
            comment.save()
        comments = Comment.objects.filter(card=card)
        context = {
            "card": card,
            "column": column,
            "card_title": card.title,
            "card_description": card.description,
            "board": board,
            "comments": comments,
            "marks": marks,
            "form": form
        }
        return render(request, "cards/card_detail.html", context)


def delete_card(request, **kwargs):
    column = Column.objects.get(pk=kwargs["column_id"])
    card = Card.objects.get(pk=kwargs["card_id"])
    card.delete()
    board = Board.objects.get(pk=kwargs["pk"])
    context = {
        "column": column,
        "cards": column.cards.all(),
        "board": board,
        "form": CreateCardForm
    }
    return render(request, "columns/column_detail.html", context)


class UpdateCard(View):

    def get(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs["card_id"])
        column = Column.objects.get(pk=kwargs["column_id"])
        columns = Column.objects.all()
        board = Board.objects.get(pk=kwargs["pk"])
        template = loader.get_template("cards/card_update.html")
        context = {
            "columns": columns,
            "card": card,
            "column": column,
            "board": board,
            "form": CommentForm
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, **kwargs):
        card = Card.objects.get(pk=kwargs["card_id"])
        column = Column.objects.get(pk=kwargs["column_id"])
        board = Board.objects.get(pk=kwargs["pk"])
        card.title = request.POST["title"]
        card.column = Column.objects.get(title=request.POST["column"])
        card.description = request.POST["description"]
        card.due_date = request.POST["due_date"]
        card.save()
        return HttpResponseRedirect(reverse('card_view', args=(board.id, column.id, card.id)))

