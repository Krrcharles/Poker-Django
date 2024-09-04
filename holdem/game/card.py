"""
This module defines the Card class, which represents a playing card.
"""

from typing import List


class Card:
    """
    Represents a playing card.

    Attributes:
    -----------
        value (str): The value of the card.
        suit (str): The suit of the card.
        code (str, optional): The code of the card. Defaults to "??"
        image (str, optional): The URL of the card image. Defaults to an empty string.
        name (str): The name of the card, combining value and suit.
        unicode (str): The Unicode representation of the card.
    """

    def __init__(
        self,
        value: str,
        suit: str,
        code: str = "??",
        image: str = "",
    ):
        """
        Args:
        -----
            value (str): The value of the card.
            suit (str): The suit of the card.
            code (str, optional): The code of the card. Defaults to "??"
            image (str, optional): The URL of the card image. Defaults to an empty string.

        Raises:
        -------
            TypeError: If value, suit, code, or image is not a string.
            ValueError: If value is not one of ACE, KING, QUEEN, JACK, 10, 9, 8, 7, 6, 5, 4, 3, 2
                        or if suit is not one of HEARTS, DIAMONDS, CLUBS, SPADES.
        """
        # Checks
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        if not isinstance(suit, str):
            raise TypeError("Suit must be a string")
        if value not in [
            "ACE",
            "KING",
            "QUEEN",
            "JACK",
            "10",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
        ]:
            raise ValueError(
                "Value must be one of ACE, KING, QUEEN, JACK, 10, 9, 8, 7, 6, 5, 4, 3, 2"
            )
        if suit not in ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"]:
            raise ValueError("Suit must be one of HEARTS, DIAMONDS, CLUBS, SPADES")
        if not isinstance(code, str):
            raise TypeError("Code must be a string")
        if not isinstance(image, str):
            raise TypeError("Image must be a string")
        # Init
        self.value = value
        self.suit = suit
        self.code = code
        self.image = image
        self.name = f"{self.value} of {self.suit}"
        value_unicode = {
            "ACE": "Ⓐ",
            "KING": "Ⓚ",
            "QUEEN": "Ⓠ",
            "JACK": "Ⓙ",
            "10": "⑩",
            "9": "⑨",
            "8": "⑧",
            "7": "⑦",
            "6": "⑥",
            "5": "⑤",
            "4": "④",
            "3": "③",
            "2": "②",
        }
        suits_unicode = {
            "HEARTS": "♥",
            "DIAMONDS": "♦",
            "CLUBS": "♣",
            "SPADES": "♠",
        }
        self.unicode = f"{value_unicode[value]} {suits_unicode[suit]}"

    @staticmethod
    def from_deck_of_cards_api(api_dict: dict) -> "Card":
        """
        # Create a Card object from a dictionary obtained from the Deck of Cards API.

        Args:
        -----
            api_dict (dict): Dictionary containing card information.

        Returns:
        --------
            Card: A Card object created from the provided dictionary.

        Raises:
        -------
            TypeError: If api_dict is not a dict.
        """
        # Checks
        if not isinstance(api_dict, dict):
            raise TypeError("api_dict must be a dict")
        # Return
        return Card(
            api_dict["value"], api_dict["suit"], api_dict["code"], api_dict["image"]
        )

    @staticmethod
    def from_code(code: str) -> "Card":
        """
        # Create a Card object from a code.

        Args:
        -----
            code (str): A string representing the code of ONE card.

        Returns:
        --------
            Card: A Card object created from the provided code.

        Raises:
        -------
            TypeError: If code is not a str.
            ValueError: If code does not have a length of 2.
        """
        # Checks
        if not isinstance(code, str):
            raise TypeError("code must be a str")
        if len(code) != 2:
            raise ValueError("code must be a string of length 2")
        # Return
        value_dict = {
            "A": "ACE",
            "K": "KING",
            "Q": "QUEEN",
            "J": "JACK",
            "0": "10",
            "9": "9",
            "8": "8",
            "7": "7",
            "6": "6",
            "5": "5",
            "4": "4",
            "3": "3",
            "2": "2",
        }
        suits_dict = {
            "S": "SPADES",
            "C": "CLUBS",
            "D": "DIAMONDS",
            "H": "HEARTS",
        }
        value, suit = code[0], code[1]
        return Card(
            value_dict[value],
            suits_dict[suit],
            code,
            image=f"https://deckofcardsapi.com/static/img/{code}.png",
        )

    @staticmethod
    def from_code_string(code_string: str) -> List["Card"]:
        """
        # Create multiple Card objects from a string of codes.

        Args:
        -----
            code (str): A string representing multiple codes of multiple cards.

        Returns:
        --------
            List[Card]: Card objects created from the provided string code.

        Raises:
        -------
            TypeError: If code is not a str.
            ValueError: If code does not have a length multiple of 2.
        """
        # Checks
        if not isinstance(code_string, str):
            raise TypeError("code_string must be a str")
        if len(code_string) % 2 != 0:
            raise ValueError(
                "code_string must be a string with a length being a multiple of 2"
            )
        # Return
        codes = [code_string[i : i + 2] for i in range(0, len(code_string), 2)]
        return [Card.from_code(code) for code in codes]

    def __eq__(self, other: "Card") -> bool:
        # Check
        if not isinstance(other, Card):
            return False
        # Return
        return self.value == other.value and self.suit == other.suit

    def __ne__(self, other: "Card") -> bool:
        # Check
        if not isinstance(other, Card):
            return True
        # Return
        return self.value != other.value or self.suit != other.suit

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        ret = f"Card('{self.value}', '{self.suit}'"
        if self.code != "??":
            ret += f", '{self.code}'"
        return ret + ")"
