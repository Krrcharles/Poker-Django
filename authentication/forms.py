# pylint: skip-file
"""
This file contains the forms for the authentication app.
"""

from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """
    A form for user login.

    Args:
        forms (type): The base class for all forms.

    Attributes:
        username (CharField): A field for entering the username.
        password (CharField): A field for entering the password.

    """

    username = forms.CharField(max_length=63, label="Username")
    password = forms.CharField(
        max_length=63, widget=forms.PasswordInput, label="Password"
    )


class SignupForm(UserCreationForm):
    """A form for user signup.

    This form extends the UserCreationForm provided by Django to include only the 'username' field.

    Args:
        UserCreationForm (class): The base form class provided by Django for user creation.

    Attributes:
        model (class): The user model to be used for signup.
        fields (tuple): The fields to be included in the form.

    """

    class Meta(UserCreationForm.Meta):
        """Meta class for SignupForm.

        This class extends the Meta class of the UserCreationForm
        to set the model and fields attributes.

        Args:
            UserCreationForm (class): The base form class provided by Django for user creation.

        Attributes:
            model (class): The user model to be used for signup.
            fields (tuple): The fields to be included in the form.

        """

        model = get_user_model()
        fields = ("username",)
