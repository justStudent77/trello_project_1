from .models import Board, Column, Card, CheckList
from django import forms


class CreateBoard(forms.Form):
    model = Board
    title = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Board Title"
        })
    )
    image = forms.ImageField()


class CreateColumnForm(forms.Form):
    model = Column
    title = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Column Title"
        })
    )


class CreateCardForm(forms.Form):
    model = Card
    title = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Card Title"
        })
    )
    description = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Description"
        })
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        label='Due date')

    # file = forms.FileField(required=False)


class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )


class CheckListForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter checklist title"
        })
    )


class MarkForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter checklist title"
        })
    )
    colour = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter colour code"
        })
    )