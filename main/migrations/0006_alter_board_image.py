# Generated by Django 4.1.3 on 2022-11-22 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_board_members"),
    ]

    operations = [
        migrations.AlterField(
            model_name="board",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
