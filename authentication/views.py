"""
This file contains the views for the authentication app. 
"""

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings


from . import forms


class LoginPage(View):
    """
    A view for handling the login page.

    Args:
        View (type): The base class for all views.

    Returns:
        type: The response returned by the view.
    """

    form_class = forms.LoginForm
    template_name = "authentication/login.html"

    def get(self, request):
        """
        Handle GET requests to the login page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        """
        Handle POST requests to the login page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        form = self.form_class(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            message = "Incorrect username or password"
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )


def logout_user(request):
    """
    Logs out the user and redirects to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect response to the login page.
    """
    logout(request)
    return redirect("login")


def signup_page(request):
    """
    Render the signup page and handle the signup form submission.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    return render(request, "authentication/signup.html", context={"form": form})
