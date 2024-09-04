# pylint: disable=W0622
# W0622: Redefining built-in 'round'
#   => Irrelevant as round() will never be used here (there are no floats)

"""
This module contains the implementation of a Texas Hold'em game.

It includes functions for preparing a round, placing bets,
moving to the next player's turn, moving to the next stage of the round,
filtering players based on their last action, checking the validity of an action,
and resolving the round to determine the winners and distribute the pot.

The module also defines an enumeration 'Stage'
representing the different stages of a round in Texas Hold'em.

Classes:
- Stage: Enumeration representing different stages of a round in Texas Hold'em.

Functions:
- deal_cards: Deal cards to players and community cards for a round.
- prepare_round: Prepare a new round of Texas Hold'em.
- bet: Place a bet in the current round.
- next_player: Move to the next player's turn in the round.
- next_stage: Move to the next stage of the round.
- filter_players: Filter the active players and the players that can bet.
- check_action: Check the validity of an action.
- resolve_round: Determine the winners of the round and distribute the pot.

Constants:
- DECK_ID: The ID of the deck used for dealing cards.

```mermaid
---
title: Texas Hold'em
---
classDiagram
direction LR
User "2..10" <-- "*" Round : is played by
class User{
    int id
    str name
    str password
    int chips
    int bet
    int total_bet
    str hand
    str action
    date last_action
    int order
}
class Round{
    int id
    str community_cards
    List[User] players
    int player_to_play
    int stage
    int pot
    int blind
    int min_raise
    str winners_name
    str winner_hand
}
```
"""

from enum import Enum
from typing import List, Dict, Set, Tuple
from datetime import datetime
from authentication.models import User
from holdem.game.deck import Deck, DeckError
from holdem.game.card import Card
from holdem.game.hand import Hand, FinalHand

# from authentication.models import User

DECK_ID = "o9fy1ih84kvx"


class Stage(Enum):
    """
    # Enumeration representing different stages of a round in Texas Hold'em.
    """

    WAITING = 0
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    SHOWDOWN = 5
    FINISHED_EARLY = 6


def deal_cards(round, test=False):
    """
    # Deal cards to players and community cards for a round.

    Args:
    -----
        - round (Round): The round object representing the current round.
        - test (bool, optional): A flag indicating whether to use a test deck. Defaults to False.
    """
    if not test:
        try:
            deck = Deck(deck_id=DECK_ID)
            deck.shuffle()
        except DeckError:
            print("Using a new deck")
            deck = Deck()
        round.community_cards = "".join([card.code for card in deck.draw(5)])
        for player in list(round.players.all()):
            player.action = ""
            player.hand = "".join([card.code for card in deck.draw(2)])
            player.save()
    else:
        round.community_cards = "3H4H5H6H7H"
        for player in list(round.players.all()):
            player.action = ""
            player.hand = "2D2S"
            player.save()
    round.save()


def prepare_round(round):
    """
    # Prepare a new round of Texas Hold'em.

    - Shifts the dealer position.
    - Deals cards to players.
    - Sets blinds.
    - Determines the player to play first.

    Args:
    -----
        round (Round): The round object to prepare.
    """
    round.stage = Stage.PRE_FLOP.value
    round.save()

    players = list(round.players.filter(order__gte=0).order_by("order")) + list(
        round.players.filter(order__lt=0)
    )
    for i, player in enumerate(players):
        player.order = (i + 1) % len(players)
        player.save()

    # Deal the cards
    deal_cards(round, test=False)

    # Set the blinds
    round_players = list(round.players.order_by("order"))
    if round.players.count() == 2:
        # In a two player game, the dealer is the small blind and the other player is the big blind
        # The dealer is the one who starts in the pre-flop
        sb = round_players[0]
        bb = round_players[1]
        if sb.bet == 0:
            pay_blind(round, player=sb, blind=round.blind, action="small blind")
        if bb.bet == 0:
            pay_blind(round, player=bb, blind=round.blind * 2, action="big blind")
        if sb.chips > 0:
            round.player_to_play = sb.id
        else:
            if bb.chips > 0:
                round.player_to_play = bb.id
            else:
                # Rare case where the players are all-in by the blinds
                round.stage = Stage.SHOWDOWN.value
                return
        round.save()
    else:
        sb = round_players[1]
        bb = round_players[2]
        if sb.bet == 0:
            pay_blind(round, player=sb, blind=round.blind, action="small blind")
        if bb.bet == 0:
            pay_blind(round, player=bb, blind=round.blind * 2, action="big blind")

        for i in [0] + list(range(3, round.players.count())):
            player = list(round.players.order_by("order"))[i]
            player.action = ""
            player.save()

        first = list(round.players.order_by("order"))[3 % round.players.count()]
        round.player_to_play = first.id
    round.save()


def pay_blind(round, player, blind: int, action: str):
    """
    # Place a blind in the current round.

    - Updates player's action, bet, and chips.
    - Updates the round's pot.

    Args:
    -----
        - round (Round): The current round object.
        - player (Player): The player placing the blind.
        - blind (int): The amount of chips bet by the player due to the blind.
        - action (str): The action taken by the player, "call" or "x", where x is the raise value.
    Raises:
    -------
        TypeError: If action/bet is the not the expected type.
    """
    # Checks
    if not isinstance(blind, int):
        raise TypeError("blind must be an int")
    if not isinstance(action, str):
        raise TypeError("action must be a string")
    # Return
    player.action = action
    blind = min(blind, player.chips)
    player.bet += blind
    player.total_bet += blind
    player.chips -= blind
    player.save()
    round.pot += blind
    round.save()


def next_player(round):
    """
    # Move to the next player's turn in the round.

    Args:
    -----
        round (Round): The current round of the game.
    """
    n = round.players.filter(order__gte=0).count()
    ordered_players = list(round.players.filter(order__gte=0).order_by("order"))
    for i, player in enumerate(ordered_players):
        if player.id == round.player_to_play:
            next_p = ordered_players[(i + 1) % n]
            for j in range(2, round.players.count()):
                if next_p.action in ["fold", "spectator"] or next_p.chips == 0:
                    next_p = ordered_players[(i + j) % n]
                else:
                    break
            print(
                "player_to_play BEFORE next_player():",
                round.players.get(id=round.player_to_play).username,
            )
            round.player_to_play = next_p.id
            round.save()
            print(
                "player_to_play AFTER next_player():",
                round.players.get(id=round.player_to_play).username,
            )
            return
    # Should never happen : if the user that is the player_to_play is removed,
    #   player_to_play should have been updated before
    raise ValueError("Player to play not found in the round's players")


def next_stage(round):
    """
    # Move to the next stage of the round.

    Args:
    -----
        round (Round): The current round of the game.
    """
    round.stage += 1
    for player in list(round.players.all()):
        player.bet = 0
        player.save()
    betting_players = filter_players(round)[1]
    for player in betting_players:
        player.action = ""
        player.save()
    if round.stage < Stage.SHOWDOWN.value:
        round.player_to_play = list(round.players.order_by("order"))[0].id
    round.min_raise = round.blind
    round.save()
    next_player(round)


def next_stage_check(round):
    """
    # Checks if the round should go to the next stage, and makes it do so if true.

    Args:
    -----
        round (Round): The current round of the game.
    """
    active_players, betting_players = filter_players(round)
    if len(betting_players) < 2:
        # If there are <2 players able to bet, the round is finished
        if len(active_players) <= 1:
            # If there is only 1 active player (or less), the round is finished early
            round.stage = Stage.FINISHED_EARLY.value
        else:
            # Else a showdown is necessary
            round.stage = Stage.SHOWDOWN.value
        round.save()
    else:
        # If all players have same bet, go to next stage
        bets = set(player.bet for player in betting_players)
        if len(bets) == 1:
            actions = {player.action for player in betting_players}
            if bets.pop() == 0:
                # Need to check if all bets are 0 because everyone checked,
                # not because of the reset due to moving to the stage
                if "" not in actions:
                    print("actions", actions, "=> next stage")
                    next_stage(round)
            else:
                # Big blind plays again even if everyone called
                if "big blind" not in actions:
                    print("actions", actions, "=> next stage")
                    next_stage(round)


def filter_players(round):
    """
    # Filter the players based on if they are active and if they can bet.

    Args:
    -----
        round (Round): The current round of the game.

    Returns:
    --------
    Tuple[QuerySet, QuerySet]:
        - QuerySet: The active players (players who have not folded or become spectators).
        - QuerySet: The betting players (active players who have chips greater than 0).
    """
    active_players = round.players.exclude(action__in=["fold", "spectator"])
    betting_players = active_players.filter(chips__gt=0)
    return active_players, betting_players


def check_action(round, user, action: str) -> Tuple[bool, str]:
    """
    # Checks that the action is possible.

    Args:
    -----
        - round_ (Round): the round being played
        - user (Player): the player taking the action
        - action (str): the action taken by the player

    Returns:
    --------
    Tuple[bool, str]:
        - bool: If the action is valid
        - str: An error message if the action is invalid
    Raises:
    -------
        TypeError: If action is not a string
    """
    # Checks
    if not isinstance(action, str):
        raise TypeError("action must be an integer or a string")

    # Initialize return values
    check = True
    message = ""

    # If the action is an integer, it represents a raise amount
    if action.isdigit():
        # Convert the action to an integer
        raise_amount = int(action)
        call_value = max(player.bet for player in round.players.all())
        user_cost = call_value + raise_amount - user.bet

        # Verify that the raise amount is at least the minimum raise
        # except if the raise makes the player all-in
        if raise_amount < round.min_raise and user_cost != user.chips:
            check = False
            message = "Raise must be at least " + str(round.min_raise)

        # Verify that the player has enough chips to make the raise
        if user_cost > user.chips:
            check = False
            message = "You don't have enough chips"

    # If the action is not valid, set check to False and generate an error message
    # else:
    # check = False
    # message = "Invalid action"

    # Return the results of the check
    return check, message


def do_action(round, user, action: str):
    """
    # Perform an action for a user in a round of the game.

    Args:
    -----
        - round (Round): The current round of the game.
        - user (User): The user performing the action.
        - action (str): The action to be performed.
            If it's digits, it represents the amount to raise.

    Raises:
    -------
        TypeError: If action is not a string
    """
    user.action = action
    user.last_action = datetime.now()
    user.save()
    print("user.total_bet BEFORE:", user.total_bet)
    if action == "call":
        max_bet = max(players.bet for players in round.players.all())
        amount_to_call = min(max_bet - user.bet, user.chips)
        print("call: amount_to_call", amount_to_call)
        user.bet += amount_to_call
        user.total_bet += amount_to_call
        user.chips -= amount_to_call
        round.pot += amount_to_call

    # raise case
    if action.isdigit():
        print("raise")
        max_bet = max(players.bet for players in round.players.all())
        amount_to_call = max_bet - user.bet
        delta = amount_to_call + int(action)
        user.bet += delta
        user.total_bet += delta
        user.chips -= delta
        round.pot += delta
        round.min_raise = int(action)
    print("user.total_bet AFTER:", user.total_bet)
    round.save()
    user.save()


def calculate_pots(round) -> Tuple[Dict[int, List[int]], int, int]:
    """
    # Calculate the pots and the number of active players.

    Args:
    -----
        round (Round): The current round of the game.

    Returns:
    --------
    Tuple[Dict[int, List[int]], int, int]:
        - final_bets (Dict[int, List[int]]):
            A dictionary where the keys are the total_bets made by players and
            the values are sets of indices of players who participated in that bet.
        - n_active_players (int): The number of active players in the round.
        - last_active_index (int): The index of the last active player in the round.
    """
    final_bets: dict = {}
    n_active_players: int = 0

    players = list(round.players.all())
    for index, player in enumerate(players):
        if player.action not in ["fold", "spectator"]:
            # => player is active
            n_active_players += 1
            last_active_index = index  # useful for edge case
            print(
                "player.username:",
                player.username,
                "player.total_bet:",
                player.total_bet,
                "player.bet:",
                player.bet,
            )
            if player.total_bet not in final_bets:
                final_bets[player.total_bet] = {index}
            else:
                final_bets[player.total_bet].add(index)

    enum_players = list(enumerate(players))
    for p in list(User.objects.filter(total_bet__gt=0).all()):
        if p.id not in [player.id for player in players]:
            enum_players.append((-p.total_bet, p))

    for value, indices in final_bets.items():
        for index, player in enum_players:
            if player.total_bet >= value:
                indices.add(index)
    for index, player in enum_players:
        if index < 0:
            player.total_bet = 0
            player.save()
    print(
        "final_bets with usernames",
        {k: {players[index].username for index in v} for k, v in final_bets.items()},
        "n_active_players",
        n_active_players,
    )
    return final_bets, n_active_players, last_active_index


def distribute_chips(
    round,
    distributed_chips,
    pot,
    indices,
    player_final_hands,
):
    """
    # Distributes chips to the winning players based on their final hands.

    Args:
    -----
        - round (Round): The current round of the game.
        - distributed_chips (int): The total number of chips already distributed.
        - pot (int): The total number of chips to distribute.
        - indices (list): The indices of the players participating in the round.
        - player_final_hands (list): The final hands of the players.

    Returns:
    --------
    Tuple[int, Set[int]]:
        - distributed_chips (int): The updated total number of distributed chips.
        - winners (set): The indices of the winning players.
    """

    winners = set()
    best_final_hand = max(
        player_final_hands[index]
        for index in indices
        if index >= 0 and list(round.players.all())[index].action != "fold"
    )
    winning_indices = [
        index
        for index in indices
        if (
            index >= 0
            and list(round.players.all())[index].action != "fold"
            and player_final_hands[index] == best_final_hand
        )
    ]
    for win_index in winning_indices:
        win_player = list(round.players.all())[win_index]
        chips_won = pot // len(winning_indices)
        print(win_player.username, "won", chips_won, "chips")
        win_player.chips += chips_won
        distributed_chips += chips_won
        winners.add(win_index)
        win_player.save()
    round.winner_hand = best_final_hand.name
    round.save()
    return distributed_chips, winners


def distribute_pots(
    round,
    player_final_hands: List[FinalHand],
    final_bets: Dict[int, List[int]],
    n_active_players: int,
    last_active_index: int,
) -> Set[int]:
    """
    # Distributes pots to the winners based on the final bets and player hands.

    Args:
    -----
        - round (Round): The current round of the game.
        - player_final_hands (List[FinalHand]): The final hands of all players.
        - final_bets (Dict[int, List[int]]):
            The dictionary where the keys are the total_bets made by players and
            the values are sets of indices of players who participated in that bet.
        - n_active_players (int): The number of active players in the round.
        - last_active_index (int):
            The index of the last active player.
            Used to avoid doing another for when n_active_players==1.

    Returns:
    --------
        Set[int]: The indices of the winners.
    """
    winners = set()
    if n_active_players > 1:
        # Multiple active players: determine the winners
        distributed_chips = 0
        if len(final_bets) > 1:
            # Multiple pots: need to distribute the chips in the right order
            final_bets = sorted(final_bets.items(), key=lambda item: item[0])
            previous_pot_value = 0
            for value, indices in final_bets:
                current_pot_value: int = 0
                for index in indices:
                    if index >= 0:
                        current_pot_value += max(
                            min(list(round.players.all())[index].total_bet, value)
                            - previous_pot_value,
                            0,
                        )
                    else:
                        current_pot_value += max(-index - previous_pot_value, 0)
                print("current_pot_value", current_pot_value)
                distributed_chips, new_winners = distribute_chips(
                    round,
                    distributed_chips,
                    current_pot_value,
                    indices,
                    player_final_hands,
                )
                winners = winners.union(new_winners)
                previous_pot_value = value
        else:
            # Only 1 pot: distribute the chips
            indices = list(final_bets.values())[0]
            distributed_chips, winners = distribute_chips(
                round,
                distributed_chips,
                round.pot,
                indices,
                player_final_hands,
            )

        # If there are remaining chips, give them to the winners
        while distributed_chips < round.pot:
            for index in winners:
                player = list(round.players.all())[index]
                player.chips += 1
                player.save()
                distributed_chips += 1
                print(player.username, "won", 1, "additional chip due to rounding")
                if distributed_chips == round.pot:
                    break
    else:
        if n_active_players == 1:
            # Only 1 active player: the winner
            winner = list(round.players.all())[last_active_index]
            winner.chips += round.pot
            print(winner.username, "won", round.pot, "chips (by default)")
            winners.add(last_active_index)
            winner.save()
        # else:
        #    #! No active players ???
        #    pass
    return winners


def resolve_round(round):
    """
    # Determine the winners of the round & distribute the pot.
    A player can only win the amount of chips he has contributed to the pot from each other player.

    - Determines the winners.
    - Distributes the pot among the winners, considering each player's contribution to the pot.
    - Resets the players' bets after distributing the pot.
    - Updates the round object with the winners and the best hand.

    Args:
    -----
        round (Round): The current round of the game.
    """
    # Determine the final hands
    community_cards: List[Card] = Card.from_code_string(round.community_cards)
    player_final_hands: List[FinalHand] = []
    for player in list(round.players.all()):
        hand = Hand(Card.from_code_string(player.hand) + community_cards)
        player_final_hands.append(hand.final_hand)

    # Separate the different pots
    final_bets, n_active_players, last_active_index = calculate_pots(round)

    # Distribute the chips
    winners = distribute_pots(
        round, player_final_hands, final_bets, n_active_players, last_active_index
    )

    # Reset the players' bets
    for player in list(round.players.all()):
        player.bet = 0
        player.total_bet = 0
        player.save()

    # Set the winners and the best hand
    winners_name_list = []
    for index, player in enumerate(list(round.players.all())):
        if index in winners:
            winners_name_list.append(player.username)
    round.winners_name = ", ".join(winners_name_list)
    round.save()
