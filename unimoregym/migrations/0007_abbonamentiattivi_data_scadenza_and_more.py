# Generated by Django 5.0.6 on 2024-06-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("unimoregym", "0006_abbonamentiattivi_qr_abbonamento_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="abbonamentiattivi",
            name="data_scadenza",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="abbonamentiattivi",
            name="utilizzi_rimanenti",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]