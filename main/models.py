from django.db import models
from users.models import TrelloUser
from django.urls import reverse
from colorfield.fields import ColorField


# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=30, unique=True)
    creator = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)
    members = models.JSONField(default={}, null=True)
    # as soon as we upload an image a file images will be created automatically
    image = models.ImageField(upload_to="", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("boards", args=[self.id])

    def __str__(self):
        return self.title


class Column(models.Model):
    title = models.CharField(max_length=30, unique=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")

    def get_absolute_url(self):
        return reverse("column-update", args=[str(self.board.id), str(self.id)])

    def __str__(self):
        return f"{self.title}"


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cards")
    due_date = models.DateField(null=True)
    file = models.FileField(null=True, blank=True, default=None)

    def get_absolute_url(self):
        return reverse("card-update", args=[str(self.column.id), str(self.id)])

    def __str__(self):
        return f"{self.title}: due {self.due_date}"


class Comment(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, default=None, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True, null=True)


class CheckList(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, default=None, related_name="checklist")


class Mark(models.Model):
    title = models.CharField(max_length=30)
    colour = models.CharField(max_length=15, default=None, null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, default=None, related_name="mark")