# Generated by Django 4.2.9 on 2024-04-13 19:09

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_rating"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="inst_link",
        ),
        migrations.AlterField(
            model_name="user",
            name="tg_link",
            field=models.CharField(
                blank=True,
                help_text="tg_link_field_help",
                max_length=44,
                null=True,
                validators=[users.validators.TgLinkValidator()],
                verbose_name="tg_link",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={
                    "unique": "A user with that username already exists."
                },
                help_text="username_field_help",
                max_length=150,
                unique=True,
                validators=[users.validators.UsernameValidator()],
                verbose_name="username",
            ),
        ),
    ]
