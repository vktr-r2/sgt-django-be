# Generated by Django 5.0.6 on 2024-06-04 03:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("call_caddy", "0001_initial"),
        ("grounds_crew", "0001_initial"),
        ("rough_draft", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MatchResult",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_score", models.IntegerField()),
                ("place", models.IntegerField()),
                ("winner_picked", models.BooleanField(default=False)),
                ("cuts_missed", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "tournament_id",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="call_caddy.tournament"),
                ),
                ("user_id", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="grounds_crew.user")),
            ],
        ),
        migrations.CreateModel(
            name="Score",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.IntegerField(blank=True, null=True)),
                ("round", models.IntegerField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "match_picks_id",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="rough_draft.matchpick"),
                ),
            ],
        ),
    ]
