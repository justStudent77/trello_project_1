# Generated by Django 4.1.3 on 2022-11-22 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_board_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="board",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]