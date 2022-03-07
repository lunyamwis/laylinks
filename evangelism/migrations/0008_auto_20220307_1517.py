# Generated by Django 3.2.9 on 2022-03-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("evangelism", "0007_auto_20220301_1205"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evangelism",
            name="completed",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="event",
            field=models.CharField(
                blank=True,
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
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="event_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="event_duration",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="event_location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="event_name",
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="event_purpose",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="evangelism",
            name="field",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PR", "Preacher"),
                    ("P", "Prophecy"),
                    ("M", "Medical"),
                    ("PE", "Personal Evangelism"),
                    ("CH", "Child Evangelism"),
                    ("SO", "Song Evangelism"),
                    ("C", "City Evangelism"),
                    ("D", "Disability Evangelism"),
                    ("S", "Special Classes Evangelism"),
                    ("BS", "Bible Study Evangelism"),
                    ("PU", "Publishing Evangelism"),
                    ("L", "Lay Evangelism"),
                ],
                default="PE",
                max_length=50,
                null=True,
            ),
        ),
    ]