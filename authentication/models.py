"""
This file contains the User model which is used to store the user's information.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """A custom user model for the authentication system.

    This model extends the AbstractUser class provided by Django's authentication framework.

    Attributes:
        id (AutoField): The primary key for the user.
        chips (IntegerField): The number of chips the user has.
        bet (IntegerField): The current bet amount of the user.
        total_bet (IntegerField): The total bet amount of the user.
        hand (CharField): The user's hand in the game.
        action (CharField): The current action of the user.
        last_action (DateTimeField): The timestamp of the user's last action.
        order (IntegerField): The order in which the user plays in the game.
    """

    id = models.AutoField(primary_key=True)
    chips = models.IntegerField(default=1000)
    bet = models.IntegerField(default=0)
    total_bet = models.IntegerField(default=0)
    hand = models.CharField(max_length=4, default="")
    action = models.CharField(max_length=10, default="")
    last_action = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=-1)
