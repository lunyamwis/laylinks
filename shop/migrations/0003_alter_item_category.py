# Generated by Django 3.2.9 on 2021-11-29 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('B', 'Book'), ('O', 'Outfit')], max_length=2),
        ),
    ]
