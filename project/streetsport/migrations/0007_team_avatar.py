# Generated by Django 4.2.9 on 2024-04-14 15:45

from django.db import migrations
import sorl.thumbnail.fields
import streetsport.models


class Migration(migrations.Migration):

    dependencies = [
        ("streetsport", "0006_alter_team_lead"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="avatar",
            field=sorl.thumbnail.fields.ImageField(
                blank=True,
                help_text="avatar_field_help",
                null=True,
                upload_to=streetsport.models.Team.get_path_image,
                verbose_name="avatar",
            ),
        ),
    ]
