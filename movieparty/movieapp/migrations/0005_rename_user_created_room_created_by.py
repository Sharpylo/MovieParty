# Generated by Django 4.1.5 on 2023-02-19 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movieapp", "0004_room_user_created"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="user_created",
            new_name="created_by",
        ),
    ]