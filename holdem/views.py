# pylint: disable=W0622, E1101
# W0622: Redefining built-in 'round'
#   => Irrelevant as round() will never be used here (there are no floats)
# E1101: Class 'Round' has no 'objects' member
#   => This is a false positive, as the objects function is provided by Django.

"""
This module contains the views for the Texas Hold'em game.

It includes the following views:
- home: Renders the home page of the game and handles user actions.
"""

from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User
from holdem.models import Round
from holdem.game.game import (
    Stage,
    prepare_round,
    next_player,
    next_stage_check,
    check_action,
    do_action,
    resolve_round,
)


@login_required
def home(request):
    """
    # Renders the home page of the Texas Hold'em game and handles user actions.

    This view handles the following actions:
    - Updating the last action of the user.
    - Checking for AFK players and handling their actions.
    - Adding the user to the round if not already added.
    - Starting the round if there are enough players.
    - Checking if the round is finished or needs to move to the next stage.
    - Resolving the round and updating the stage.
    - Handling the user's action and updating the round accordingly.

    Args:
    -----
        request: The HTTP request object.

    Returns:
    --------
        The rendered home page template with the appropriate context.
    """
    user = request.user
    user.last_action = datetime.now()
    user.save()

    if Round.objects.all().exists():
        round = Round.objects.latest("id")
    else:
        round = Round()
        round.save()

    error_message = ""

    if round.player_to_play != 0:
        afk = User.objects.get(id=round.player_to_play)
        if (
            afk.last_action.timestamp() - datetime.now().timestamp()
            > timedelta(seconds=120).total_seconds()
        ):
            print(f"{afk.username} has been away for too long so he was ejected.")
            afk.action = "fold"
            afk.order = -1
            afk.bet = 0
            next_player(round)
            round.players.remove(afk)
            afk.save()
            round.save()

    if user not in round.players.all():
        # Add the user to the round and save the changes.
        round.players.add(user)
        round.save()
        user.action = "spectator"
        user.hand = ""
        user.save()

    if round.stage == Stage.WAITING.value:
        # If there are enough players in the round, start the round.
        if round.players.count() >= 2:
            prepare_round(round)

    if Stage.PRE_FLOP.value <= round.stage <= Stage.RIVER.value:
        next_stage_check(round)

    if round.stage >= Stage.SHOWDOWN.value:
        resolve_round(round)
        redirect("home")
        players = round.players.all()
        round = Round()
        round.save()
        round.players.set(players)
        round.save()

    # Traitement de l'action de l'utilisateur
    if request.method == "POST" and round.player_to_play == user.id:
        action = request.POST.get("action")
        check, error_message = check_action(round, user, action)
        if check:
            print(f"Action '{action}' by {user.username} at stage {round.stage}")
            do_action(round, user, action)
            next_player(round)
            return redirect("home")
        print(f"'{action}' is not a valid action in this context: {error_message}")

    # * CONTEXT
    previous_round = Round.objects.filter(id__lt=round.id).order_by("-id").first()
    if previous_round is not None and previous_round.winners_name == "":
        # Happens when a new round was created without finishing the previous one
        previous_round = None

    opponents = list(
        list(round.players.filter(order__gt=user.order).order_by("order"))
        + list(round.players.filter(order__lt=user.order).order_by("order"))
    )
    # Remove the user from the list of opponents if it ended up there
    opponents = [opponent for opponent in opponents if opponent.id != user.id]

    current_raise = max(player.bet for player in round.players.all())
    call_value = min(current_raise, user.chips + user.bet)

    players = round.players.filter(order__gte=0).order_by("order")
    if len(players) > 0:
        dealer_id = players[0].id
    else:
        dealer_id = 0

    context = {
        "user": user,
        "round": round,
        "previous_round": previous_round,
        "call_value": call_value,
        "call_difference": call_value - user.bet,
        "max_raise_by": max(user.chips - current_raise, 0),
        "opponents": opponents,
        "dealer_id": dealer_id,
        "error": error_message,
    }

    return render(request, "holdem/home.html", context=context)
