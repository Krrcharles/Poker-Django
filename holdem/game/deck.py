"""
This module represents a deck of cards using the Deck of Cards API.

It provides a Deck class that allows creating a new deck,
drawing cards from the deck and shuffling the deck.

Example usage:
--------------
    deck = Deck(deck_id="o9fy1ih84kvx")
    deck.shuffle()
    cards = deck.draw(5)
    print(cards)
"""

from time import sleep
from typing import List, Optional
import requests

from holdem.game.card import Card
from holdem.game.hand import Hand


class DeckError(Exception):
    """Base class for exceptions in this module."""


class Deck:
    """
    Represents a deck of cards using the Deck of Cards API.

    Attributes:
    -----------
        deck_id (str): The ID of the deck.
    """

    def __init__(self, deck_id: Optional[str] = None):
        """
        Initialize a Deck object. If no deck_id is provided, a new deck is created in the API.

        Args:
        -----
            deck_id (Optional[str]): The ID of an existing deck. Defaults to None.

        Raises:
        -------
            TypeError: If deck_id is not a string or None.
        """
        # Checks
        if deck_id is not None and not isinstance(deck_id, str):
            raise TypeError("Deck ID must be a string (or None)")
        # Init
        self.deck_id = deck_id
        if self.deck_id is None:
            self.new_deck()
        # else:
        #     print(f"> Using existing deck: '{self.deck_id}'\n")

    def new_deck(self):
        """
        Create a new deck of cards.

        Raises:
        -------
            DeckError: If the new deck request is not successful.
        """
        try:
            response = requests.get(
                "https://deckofcardsapi.com/api/deck/new/shuffle", timeout=10
            )
            data = response.json()
            if not data["success"]:
                raise DeckError("API says the new deck request was not successful.")
        except Exception as e:
            raise DeckError(e) from e
        # print("> New deck:", data)
        self.deck_id = data["deck_id"]

    def draw(self, count: int) -> List[Card]:
        """
        Draw a specified number of cards from the deck.

        Args:
        -----
            count (int): The number of cards to draw.

        Returns:
        --------
            List[Card]: A list of Card objects representing the drawn cards.

        Raises:
        -------
            TypeError: If count is not an integer.
            ValueError: If no deck exists or count is not between 1 and 52.
            DeckError: If draw request is not successful.
        """
        # Checks
        if not isinstance(count, int):
            raise TypeError("Count must be an integer")
        if self.deck_id is None:
            raise ValueError("No deck exists")
        if count == 0:
            return []
        if not 1 <= count <= 52:
            raise ValueError("Count must be between 0 and 52")
        # Request
        try:
            response = requests.get(
                f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count={count}",
                timeout=10,
            )
            data = response.json()
            if not data["success"]:
                raise DeckError(
                    f"API says the draw ({count}) request was not successful."
                )
        except Exception as e:
            raise DeckError(e) from e
        cards = [Card.from_deck_of_cards_api(card_dict) for card_dict in data["cards"]]
        # print(
        #     f"> Draw ({count}):", ", ".join([card.unicode for card in cards]), cards
        # )
        return cards

    def shuffle(self):
        """
        Shuffle the deck.

        Raises:
        -------
            ValueError: If no deck exists.
            DeckError: If the shuffle request is not successful.
        """
        # Checks
        if self.deck_id is None:
            raise ValueError("No deck exists")
        # Request
        try:
            response = requests.get(
                f"https://deckofcardsapi.com/api/deck/{self.deck_id}/shuffle/",
                timeout=10,
            )
            data = response.json()
            if not data["success"]:
                raise DeckError("API says the shuffle request was not successful.")
        except Exception as e:
            raise DeckError(e) from e

    def __str__(self) -> str:
        return f"Deck with ID: {self.deck_id}"

    def __repr__(self) -> str:
        return f"Deck('{self.deck_id}')"


if __name__ == "__main__":
    deck = Deck(deck_id="o9fy1ih84kvx")

    STEPS = 30
    COUNT = 7
    for step in range(1, STEPS + 1):
        print(f">>> Step {step}/{STEPS} <<<")
        hand = Hand(deck.draw(COUNT))
        print(hand)
        deck.shuffle()
        print()  # Empty line
        sleep(5)
