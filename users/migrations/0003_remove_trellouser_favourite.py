# Generated by Django 4.1.3 on 2022-11-21 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_trellouser_preferred"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trellouser",
            name="favourite",
        ),
    ]
