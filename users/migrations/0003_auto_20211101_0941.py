# Generated by Django 3.2.6 on 2021-11-01 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211101_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='baptized',
        ),
        migrations.RemoveField(
            model_name='user',
            name='category',
        ),
        migrations.RemoveField(
            model_name='user',
            name='church_elder_first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='church_elder_last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='conference_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contact_assistant_email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contact_assistant_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='field_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='home_church_email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='home_church_location',
        ),
        migrations.RemoveField(
            model_name='user',
            name='home_church_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='home_church_phone_numbers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.RemoveField(
            model_name='user',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_numbers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='position_church',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
