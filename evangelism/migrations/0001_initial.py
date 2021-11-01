# Generated by Django 3.2.6 on 2021-11-01 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evangelism',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field', models.CharField(choices=[('PR', 'Preacher'), ('P', 'Prophecy'), ('M', 'Medical'), ('PE', 'Personal Evangelism'), ('CH', 'Child Evangelism'), ('SO', 'Song Evangelism'), ('C', 'City Evangelism'), ('D', 'Disability Evangelism'), ('S', 'Special Classes Evangelism'), ('BS', 'Bible Study Evangelism'), ('PU', 'Publishing Evangelism'), ('L', 'Lay Evangelism')], default='PE', max_length=50)),
                ('event', models.CharField(choices=[('HE', 'Health Expo'), ('P', 'Personal'), ('PU', 'Public Effort'), ('M', 'Hall Meetings'), ('L', 'Live Streaming'), ('R', 'Recorded Message'), ('MD', 'Printed Material Distribution'), ('S', 'Sermon')], default='P', max_length=50)),
                ('event_name', models.TextField(max_length=1024)),
                ('event_date', models.DateTimeField()),
                ('event_location', models.CharField(max_length=255)),
                ('event_purpose', models.TextField()),
                ('event_duration', models.CharField(max_length=1024)),
                ('sermon_theme', models.TextField()),
                ('sermon_length', models.IntegerField()),
                ('number_attendees', models.IntegerField()),
                ('budget', models.FloatField()),
                ('number_converts', models.IntegerField()),
                ('number_followups', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('conference_name', models.CharField(max_length=255)),
                ('field_name', models.CharField(max_length=255)),
                ('home_church_name', models.TextField()),
                ('home_church_email', models.EmailField(max_length=254)),
                ('home_church_phone_numbers', models.CharField(max_length=200, null=True)),
                ('home_church_location', models.CharField(max_length=50)),
                ('church_elder_first_name', models.CharField(max_length=50)),
                ('church_elder_last_name', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=255)),
                ('baptized', models.BooleanField(default=True)),
                ('position_church', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('phone_numbers', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(choices=[('I', 'Self Supporting'), ('C', 'Supported Church')], default='I', max_length=50)),
                ('conference_name', models.CharField(max_length=255)),
                ('home_church_name', models.TextField()),
                ('home_church_email', models.EmailField(max_length=254)),
                ('home_church_phone_numbers', models.CharField(max_length=200, null=True)),
                ('home_church_location', models.CharField(max_length=50)),
                ('church_elder_first_name', models.CharField(max_length=50)),
                ('church_elder_last_name', models.CharField(max_length=50)),
                ('fields', models.ManyToManyField(to='evangelism.Evangelism')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Minister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('other_names', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('contact_assistant_name', models.CharField(max_length=255)),
                ('contact_assistant_email', models.EmailField(max_length=254)),
                ('conference_name', models.CharField(max_length=255)),
                ('home_church_name', models.TextField()),
                ('home_church_email', models.EmailField(max_length=254)),
                ('home_church_phone_numbers', models.CharField(max_length=200, null=True)),
                ('home_church_location', models.CharField(max_length=50)),
                ('church_elder_first_name', models.CharField(max_length=50)),
                ('church_elder_last_name', models.CharField(max_length=50)),
                ('fields', models.ManyToManyField(to='evangelism.Evangelism')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
