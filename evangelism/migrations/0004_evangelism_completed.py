# Generated by Django 3.2.9 on 2022-01-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0003_auto_20220126_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='evangelism',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
