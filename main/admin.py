from django.contrib import admin
from .models import Board, Card, Column
# Register your models here.

admin.site.register(Board)
admin.site.register(Card)
admin.site.register(Column)