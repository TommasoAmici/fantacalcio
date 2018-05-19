from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from autoslug import AutoSlugField
import uuid


# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)


class League(models.Model):
    """
    Users can create and join leagues to play several competitions.
    """
    access_code = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True)
    teams = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams_of",
        through="Team",
        blank=True
    )

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.name


class Bonus(models.Model):
    """
    Goal, assist, etc.
    The value of each bonus can be customized in each league.
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Performance(models.Model):
    """
    Stores information about a player's performance
    """
    vote = models.PositiveSmallIntegerField(default=6)
    bonuses = models.ManyToManyField(Bonus, blank=True)
    fantavote = models.SmallIntegerField(default=6)
    against_team_irl = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    matchday = models.PositiveSmallIntegerField()


class Role(models.Model):
    """
    Stores roles of a player
    """
    role = models.CharField(max_length=3)
    mantra = models.BooleanField(default=False)

    def __str__(self):
        return self.role


class Season(models.Model):
    """
    Stores information about a player's season
    """
    roles = models.ManyToManyField(
        Role,
        related_name="roles_of",
        blank=True
    )
    team_irl = models.CharField(max_length=100)
    price = models.SmallIntegerField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    performances = models.ManyToManyField(
        Performance,
        related_name="performances_of",
        blank=True
    )


class Player(models.Model):
    """
    Stores information about a player
    """
    name = models.CharField(max_length=100)
    seasons = models.ManyToManyField(Season, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    """
    Stores additional information about User's team.
    A User can have multiple teams in multiple leagues
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="user_of",
        on_delete=models.CASCADE
    )
    league = models.ForeignKey(
        League,
        related_name="league_of",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    founder = models.BooleanField(default=False)
    history = models.TextField(blank=True, null=True)
    players = models.ManyToManyField(
        Player,
        related_name="players_of",
        through="Roster",
        blank=True
    )
    logo = models.ImageField(upload_to="team_logos/", null=True, blank=True)

    class Meta:
        ordering = ("date_joined",)


class Roster(models.Model):
    """
    Stores additional information about instances of Player in a Team
    """
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    price_paid = models.PositiveSmallIntegerField(blank=True)
    date_added = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    date_sold = models.DateField(blank=True, null=True)