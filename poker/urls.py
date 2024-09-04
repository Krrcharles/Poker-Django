# pylint: skip-file
"""
URL configuration for poker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.db.utils import OperationalError
from django.urls import path

import authentication.views
import holdem.views

from holdem.models import Round
from authentication.models import User

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication.views.LoginPage.as_view(), name="login"),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("home/", holdem.views.home, name="home"),
    path("signup/", authentication.views.signup_page, name="signup"),
]


# Code run once at the start of server
print(">> Running poker/urls.py\n")


try:
    if not User.objects.filter(username="admin").exists():
        User.objects.create_user(username="admin", password="admin")
    if not User.objects.filter(username="user").exists():
        User.objects.create_user(username="user", password="user")
    if not User.objects.filter(username="test1").exists():
        User.objects.create_user(username="test1", password="test1")
    if not User.objects.filter(username="test2").exists():
        User.objects.create_user(username="test2", password="test2")
    if not User.objects.filter(username="test3").exists():
        User.objects.create_user(username="test3", password="test3")
    if not User.objects.filter(username="test4").exists():
        User.objects.create_user(username="test4", password="test4")
    for player in User.objects.all():
        if player.username[:4] == "test":
            player.chips = 250 * int(player.username[4])
            player.save()
    #     else:
    #         player.chips = 1000
    #     player.bet = 0
    #     player.total_bet = 0
    #     player.hand = ""
    #     player.action = ""
    #     player.order = -1
    #     player.save()
    # round = Round.objects.latest("id")
    # round.pot = 0
    # round.min_raise = round.blind
    # round.stage = 0
    # round.save()
except OperationalError:
    print(">> Tables not created yet")
    pass
except Round.DoesNotExist:
    print(">> No round in database yet")
    pass
except Exception as e:
    print(">> Error:", e)
    pass
