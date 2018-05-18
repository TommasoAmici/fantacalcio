# Generated by Django 2.0.5 on 2018-05-18 20:25

import autoslug.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='founded', to=settings.AUTH_USER_MODEL)),
                ('teams', models.ManyToManyField(blank=True, related_name='leagues', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=6, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('fantavote', models.IntegerField(default=6)),
                ('against_team_irl', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('matchday', models.IntegerField()),
                ('bonuses', models.ManyToManyField(blank=True, to='main.Bonus')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=3)),
                ('mantra', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_paid', models.IntegerField(blank=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('date_sold', models.DateField(blank=True, null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_irl', models.CharField(max_length=100)),
                ('price', models.IntegerField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('performances', models.ManyToManyField(blank=True, to='main.Performance')),
                ('roles', models.ManyToManyField(blank=True, to='main.Role')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='seasons',
            field=models.ManyToManyField(blank=True, to='main.Season'),
        ),
    ]
