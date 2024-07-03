# Generated by Django 5.0.6 on 2024-06-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("unimoregym", "0005_alter_gymuser_data_nascita"),
    ]

    operations = [
        migrations.AddField(
            model_name="abbonamentiattivi",
            name="qr_abbonamento",
            field=models.ImageField(
                default="default/default_qr.jpg", upload_to="abbonamenti/"
            ),
        ),
        migrations.AddField(
            model_name="gymuser",
            name="profile_image",
            field=models.ImageField(
                default="default/default_user.png", upload_to="profile_images/"
            ),
        ),
    ]