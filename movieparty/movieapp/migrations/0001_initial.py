# Generated by Django 4.1.5 on 2023-02-14 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=50, verbose_name="Название страны"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Жанр")),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=50, verbose_name="Наименование фильма"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "year",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Год выпуска"
                    ),
                ),
                (
                    "cover_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="covers/",
                        verbose_name="Изображение обложки",
                    ),
                ),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="videos/",
                        verbose_name="Файл фильма",
                    ),
                ),
                (
                    "trailer",
                    models.TextField(blank=True, null=True, verbose_name="Трейлер"),
                ),
                (
                    "link_movie",
                    models.TextField(
                        blank=True, null=True, verbose_name="Ссылка на фильм"
                    ),
                ),
                (
                    "country",
                    models.ManyToManyField(
                        related_name="movies",
                        to="movieapp.country",
                        verbose_name="Страны",
                    ),
                ),
                (
                    "genre",
                    models.ManyToManyField(
                        related_name="movies", to="movieapp.genre", verbose_name="Жанры"
                    ),
                ),
            ],
            options={
                "verbose_name": "Фильм",
                "verbose_name_plural": "Фильмы",
            },
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Имя комнаты")),
                (
                    "password",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Пароль для комнаты",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время обновления"
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время начала фильма"
                    ),
                ),
                (
                    "end_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время конца фильма"
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movieapp.movie",
                        verbose_name="Название фильма",
                    ),
                ),
            ],
        ),
    ]
