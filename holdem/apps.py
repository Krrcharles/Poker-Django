"""
This file is used to configure the app name for the holdem app.
"""

from django.apps import AppConfig


class HoldemConfig(AppConfig):
    """
    Configuration class for the 'holdem' app.

    Args:
        AppConfig: The base configuration class provided by Django.

    Attributes:
        default_auto_field (str): The default auto field for the app's models.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "holdem"
