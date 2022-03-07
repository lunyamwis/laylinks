# Generated by Django 2.0.1 on 2018-01-16 16:35

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("link", models.URLField()),
                ("description", models.TextField()),
                ("language", models.CharField(blank=True, max_length=5)),
                ("copyright", models.CharField(blank=True, max_length=255)),
                (
                    "managing_editor",
                    models.EmailField(
                        blank=True,
                        help_text="Email address for person responsible for editorial content.",
                        max_length=254,
                    ),
                ),
                (
                    "web_master",
                    models.EmailField(
                        blank=True,
                        help_text="Email address for person responsible for technical issues.",
                        max_length=254,
                    ),
                ),
                ("pub_date", models.DateTimeField(blank=True, null=True)),
                ("last_build_date", models.DateTimeField(blank=True, null=True)),
                ("generator", models.CharField(blank=True, max_length=255)),
                (
                    "ttl",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="The number of minutes a channel can be cached before \
                        refreshing.",
                        null=True,
                        verbose_name="TTL",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="podcast/channel/"
                    ),
                ),
                ("subtitle", models.CharField(blank=True, max_length=255)),
                ("summary", models.TextField(blank=True)),
                ("redirect", models.URLField(blank=True)),
                ("keywords", models.CharField(blank=True, max_length=255)),
                (
                    "itunes",
                    models.URLField(blank=True, verbose_name="iTunes Store URL"),
                ),
                (
                    "block",
                    models.BooleanField(
                        default=False, help_text="Block this podcast on iTunes."
                    ),
                ),
                ("explicit", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("link", models.URLField()),
                ("description", models.TextField(help_text="The item synopsis.")),
                ("pud_date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "author",
                    models.EmailField(
                        blank=True,
                        help_text="Email address of the author of the item.",
                        max_length=254,
                    ),
                ),
                ("enclosure", models.FileField(upload_to="podcasts/items/")),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="podcast.Channel",
                    ),
                ),
            ],
        ),
    ]