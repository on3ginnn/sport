# Generated by Django 4.2.9 on 2024-04-13 20:26

from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_auto_20240413_2024"),
    ]

    operations = [
        UnaccentExtension()
    ]