# Generated by Django 4.2.13 on 2024-07-07 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0006_alter_place_description_long_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="place",
            old_name="description_long",
            new_name="long_description",
        ),
        migrations.RenameField(
            model_name="place",
            old_name="description_short",
            new_name="short_description",
        ),
    ]
