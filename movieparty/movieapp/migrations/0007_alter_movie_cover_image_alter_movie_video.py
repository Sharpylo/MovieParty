# Generated by Django 4.1.5 on 2023-01-30 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movieapp", "0006_alter_movie_cover_image_alter_movie_video"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="cover_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="covers/",
                verbose_name="Изображение обложки",
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="video",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="videos/",
                verbose_name="Ссылка на фильм",
            ),
        ),
    ]
