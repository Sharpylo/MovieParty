# Generated by Django 4.1.5 on 2023-01-29 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movieapp", "0003_alter_movie_cover_image_alter_movie_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="video",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="videos",
                verbose_name="Ссылка на фильм",
            ),
        ),
    ]
