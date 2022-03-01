# Generated by Django 3.2.9 on 2022-03-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("evangelism", "0006_auto_20220128_1249"),
    ]

    operations = [
        migrations.AddField(
            model_name="evangelism",
            name="is_event",
            field=models.CharField(
                choices=[("S", "Sermon"), ("E", "Event")], default="S", max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="event",
            field=models.CharField(
                choices=[
                    ("HE", "Health Expo"),
                    ("P", "Personal"),
                    ("PU", "Public Effort"),
                    ("M", "Hall Meetings"),
                    ("L", "Live Streaming"),
                    ("R", "Recorded Message"),
                    ("MD", "Printed Material Distribution"),
                ],
                default="P",
                max_length=50,
            ),
        ),
    ]
