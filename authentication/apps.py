"""
This file is used to configure the authentication app.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    AppConfig for the 'authentication' app.

    Args:
        AppConfig (type): Base class for application configuration.

    Attributes:
        default_auto_field (str): The name of the auto-created primary key field.
        name (str): The name of the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
