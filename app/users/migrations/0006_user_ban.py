# Generated by Django 5.0.4 on 2024-06-06 08:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_userresetpassword_used"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ban",
            field=models.BooleanField(default=False),
        ),
    ]
