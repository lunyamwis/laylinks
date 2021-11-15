# Generated by Django 3.2.6 on 2021-11-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0005_ministry_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evangelism',
            name='budget',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evangelism',
            name='number_attendees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evangelism',
            name='number_converts',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evangelism',
            name='number_followups',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evangelism',
            name='sermon_length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='evangelism',
            name='sermon_theme',
            field=models.TextField(blank=True, null=True),
        ),
    ]
