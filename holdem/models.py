"""
This file contains the Round model which is used to store the current state of the game.
"""

from django.db import models
from authentication.models import User

# Unused import
# from poker import settings


class Round(models.Model):
    """Represents a round of the Texas Hold'em game.

    Attributes:
        id (AutoField): The primary key for the round.
        community_cards (CharField): The community cards for the round.
        players (ManyToManyField): The players participating in the round.
        player_to_play (IntegerField): The id of the player currently playing.
        stage (IntegerField): The stage of the round.
        pot (IntegerField): The current pot amount.
        blind (IntegerField): The blind amount for the round.
        min_raise (IntegerField): The minimum raise amount for the round.
        winners_name (CharField): The names of the winners of the round.
        winner_hand (CharField): The winning hand for the round.
    """

    id = models.AutoField(primary_key=True)
    community_cards = models.CharField(max_length=10, default="")
    players = models.ManyToManyField(User)
    player_to_play = models.IntegerField(default=0)
    stage = models.IntegerField(default=0)
    pot = models.IntegerField(default=0)
    blind = models.IntegerField(default=25)
    min_raise = models.IntegerField(default=25)
    winners_name = models.CharField(max_length=1500, default="")
    winner_hand = models.CharField(max_length=50, default="")
