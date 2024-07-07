# Generated by Django 4.2.13 on 2024-07-07 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0010_alter_image__order_alter_image_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="place",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="places.place",
            ),
        ),
    ]
