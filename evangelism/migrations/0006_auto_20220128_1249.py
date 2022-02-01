# Generated by Django 3.2.9 on 2022-01-28 12:49

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('evangelism', '0005_auto_20220128_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='home_church_phone_numbers',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+254700701209', max_length=128, region=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='minister',
            name='home_church_phone_numbers',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='ministry',
            name='phone_numbers',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='referees',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]