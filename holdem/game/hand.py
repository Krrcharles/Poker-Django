"""
This module contains classes for representing poker hands and their powers.

Classes:
- FinalHandPower: Enumeration representing the power of a final hand in poker.
- FinalHand: Represents the final hand in a poker game.
- Hand: Represents a hand in a poker game.

"""

from typing import List, Optional
from enum import Enum

from holdem.game.card import Card


class FinalHandPower(Enum):
    """
    Enumeration representing the power of a final hand in poker.
    """

    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9


class FinalHand:
    """
    # Represents the final hand in a poker game.

    Attributes:
    -----------
        cards (List[Card]): List of Card objects
        power (int): Power of the final hand (value of FinalHandPower)
        value (List[str]):
            List of strings representing the values of the cards.
            Ordered from highest to lowest card value.
        suit (Optional[str]): String representing the suit of the hand (None if not relevant)
        name (str): Name of the hand (based on its power and value)
    """

    def __init__(self, cards: List[Card], hand_power: FinalHandPower, suit: str = None):
        """
        Args:
        -----
            cards (List[Card]): List of cards forming the hand.
            hand_power (FinalHandPower): Power of the hand.
            suit (str, optional): Suit of the hand for flush or straight flush. Defaults to None.

        Raises:
        -------
            TypeError: If input types are incorrect.
        """
        # Checks
        if not isinstance(cards, list):
            raise TypeError("Cards must be a list")
        if not all(isinstance(card, Card) for card in cards):
            raise TypeError("All cards must be Card objects")
        if not isinstance(hand_power, FinalHandPower):
            raise TypeError("Hand power must be a FinalHandPower object")
        if suit is not None and not isinstance(suit, str):
            raise TypeError("Suit must be a string (or None)")
        # Init
        self.cards = cards
        self.power = hand_power.value
        self.value = [card.value for card in cards]
        self.suit = suit

    @property
    def name(self) -> str:
        """
        # Getter for the name of the hand.

        Returns:
            str: name of the hand
        """
        # if len(self.cards) != 5:
        #     print(f">>> {len(self.cards)} card hand <<<")
        #     print("   HAND: " + ", ".join([str(card) for card in self.cards]))
        match self.power:
            case FinalHandPower.HIGH_CARD.value:
                fh_str = f"High card ({self.value[0]})"
            case FinalHandPower.ONE_PAIR.value:
                fh_str = f"One Pair ({self.value[0]}s)"
            case FinalHandPower.TWO_PAIRS.value:
                fh_str = f"Two pairs ({self.value[0]}s and {self.value[2]}s)"
            case FinalHandPower.THREE_OF_A_KIND.value:
                fh_str = f"Three of a kind ({self.value[0]}s)"
            case FinalHandPower.STRAIGHT.value:
                fh_str = f"Straight ({self.value[4]} to {self.value[0]})"
            case FinalHandPower.FLUSH.value:
                fh_str = f"Flush (in {self.suit}, {self.value[0]} high)"
            case FinalHandPower.FULL_HOUSE.value:
                fh_str = f"Full house ({self.value[0]}s full of {self.value[3]}s)"
            case FinalHandPower.FOUR_OF_A_KIND.value:
                fh_str = f"Four of a kind ({self.value[0]}s)"
            case FinalHandPower.STRAIGHT_FLUSH.value:
                fh_str = f"Straight flush (in {self.suit}, {self.value[4]} to {self.value[0]})"
            case FinalHandPower.ROYAL_FLUSH.value:
                fh_str = f"Royal flush! (in {self.suit})"
            case _:
                fh_str = "Unknown hand"
        return fh_str

    def compare(self, other: "FinalHand") -> int:
        """
        # Compare the power of this hand with another.

        Args:
        -----
            other (FinalHand): Other hand to compare with.

        Returns:
        --------
            int: 1 if this hand is stronger, -1 if other hand is stronger, 0 if equal.

        Raises:
        -------
            TypeError: If input type is incorrect.
        """
        # Checks
        if not isinstance(other, FinalHand):
            raise TypeError("Other must be a FinalHand")
        # Return
        if self.power > other.power:
            return 1
        if self.power < other.power:
            return -1
        num_values = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "JACK": 11,
            "QUEEN": 12,
            "KING": 13,
            "ACE": 14,
        }
        for i in range(min(len(self.value), len(other.value))):
            if num_values[self.value[i]] > num_values[other.value[i]]:
                return 1
            if num_values[self.value[i]] < num_values[other.value[i]]:
                return -1
        return 0

    def __ge__(self, other) -> bool:
        # Check
        if not isinstance(other, FinalHand):
            raise TypeError("Other must be a FinalHand")
        # Return
        return self.compare(other) >= 0

    def __gt__(self, other) -> bool:
        # Check
        if not isinstance(other, FinalHand):
            raise TypeError("Other must be a FinalHand")
        # Return
        return self.compare(other) > 0

    def __le__(self, other) -> bool:
        # Check
        if not isinstance(other, FinalHand):
            raise TypeError("Other must be a FinalHand")
        # Return
        return self.compare(other) <= 0

    def __lt__(self, other) -> bool:
        # Check
        if not isinstance(other, FinalHand):
            raise TypeError("Other must be a FinalHand")
        # Return
        return self.compare(other) < 0

    def __eq__(self, other) -> bool:
        # Check
        if not isinstance(other, FinalHand):
            return False
        # Return
        return self.compare(other) == 0

    def __ne__(self, other) -> bool:
        # Check
        if not isinstance(other, FinalHand):
            return True
        # Return
        return self.compare(other) != 0

    def __str__(self) -> str:
        return self.name


class Hand:
    """
    # Represents a hand in a poker game.

    Attributes:
    -----------
        cards (List[Card]): List of Card objects forming the hand.
        sep_suits (dict): Dictionary with suits as keys and lists of cards as values.
        sep_values (dict): Dictionary with values as keys and lists of cards as values.
        final_hand (FinalHand): Final hand detected from the given cards.
    """

    SUITS = {"CLUBS": 0, "DIAMONDS": 1, "HEARTS": 2, "SPADES": 3}
    NUM_VALUES = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "JACK": 11,
        "QUEEN": 12,
        "KING": 13,
        "ACE": 14,
        "STRAIGHT_OFFSET": 4,
    }

    def __init__(self, cards: List[Card]):
        """
        Args:
        -----
            cards (List[Card]): List of cards forming the hand.

        Raises:
        -------
            TypeError: If input types are incorrect.
            ValueError: If the number of cards is invalid.
        """
        # Checks
        if not isinstance(cards, list):
            raise TypeError("Cards must be a list")
        if not all(isinstance(card, Card) for card in cards):
            raise TypeError("All cards must be Card objects")
        if 0 > len(cards) > 7:
            raise ValueError("A hand can't have more than 7 cards or less than 1.")
        # Init
        self.cards = sorted(
            cards,
            key=lambda card: self.NUM_VALUES[card.value] + self.SUITS[card.suit] / 4,
            reverse=True,
        )
        self.sep_suits = self.separate_by_suits()
        self.sep_values = self.separate_values()
        self.final_hand = self.detect_final_hand()

    def separate_by_suits(self) -> dict:
        """
        # Separate the cards in the hand by suits.

        Returns:
        --------
            dict: Dictionary with suits as keys and lists of cards as values.
        """
        suits: dict = {}
        for card in self.cards:
            if card.suit in suits:
                suits[card.suit].append(card)
            else:
                suits[card.suit] = [card]
        return suits

    def separate_values(self) -> dict:
        """
        # Separate the cards in the hand by values.

        Returns:
        --------
            dict: Dictionary with values as keys and lists of cards as values.
        """
        values: dict = {}
        for card in self.cards:
            if card.value in values:
                values[card.value].append(card)
            else:
                values[card.value] = [card]
        return values

    def detect_royal_flush(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains a royal flush.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing a royal flush if it is detected, None otherwise.
        """
        if len(self.cards) < 5:
            return None
        for suit, cards in self.sep_suits.items():
            if len(cards) >= 5:
                num_values = [self.NUM_VALUES[card.value] for card in cards]
                for i in range(len(num_values) - 4):
                    if (
                        num_values[i] == self.NUM_VALUES["ACE"]
                        and num_values[i + 4] == self.NUM_VALUES["10"]
                    ):
                        return FinalHand(
                            cards[i : i + 5], FinalHandPower.ROYAL_FLUSH, suit
                        )
        return None

    def detect_straight_flush(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains a straight flush.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing a straight flush if it is detected, None otherwise.
        """
        if len(self.cards) < 5:
            return None
        for suit, cards in self.sep_suits.items():
            if len(cards) >= 5:
                num_values = [self.NUM_VALUES[card.value] for card in cards]
                for i in range(len(num_values) - 4):
                    if (
                        num_values[i] - num_values[i + 4]
                        == self.NUM_VALUES["STRAIGHT_OFFSET"]
                    ):
                        return FinalHand(
                            cards[i : i + 5], FinalHandPower.STRAIGHT_FLUSH, suit
                        )
                if (
                    num_values[-4] == self.NUM_VALUES["5"]
                    and num_values[-1] == self.NUM_VALUES["2"]
                    and num_values[0] == self.NUM_VALUES["ACE"]
                ):
                    return FinalHand(
                        cards[-4:] + [cards[0]], FinalHandPower.STRAIGHT_FLUSH, suit
                    )
        return None

    def detect_four_of_a_kind(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains a four of a kind.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing a four of a kind if it is detected, None otherwise.
        """
        if len(self.cards) < 4:
            return None
        for quad_value, cards in self.sep_values.items():
            if len(cards) == 4:
                if quad_value == self.cards[0].value and len(self.cards) > 4:
                    other_high_card_list = [self.cards[4]]
                else:
                    other_high_card_list = [self.cards[0]]
                return FinalHand(
                    cards + other_high_card_list, FinalHandPower.FOUR_OF_A_KIND
                )
        return None

    def detect_full_house(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains a full house.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing a full house if it is detected, None otherwise.
        """
        if len(self.cards) < 5:
            return None
        for trips_value, cards in self.sep_values.items():
            if len(cards) == 3:
                for full_value, cards2 in self.sep_values.items():
                    if len(cards2) >= 2 and full_value != trips_value:
                        return FinalHand(cards + cards2, FinalHandPower.FULL_HOUSE)
        return None

    def detect_flush(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains a flush.

        Returns:
        --------
            Optional[FinalHand]: Final hand representing a flush if it is detected, None otherwise.
        """
        if len(self.cards) < 5:
            return None
        for suit, cards in self.sep_suits.items():
            if len(cards) >= 5:
                return FinalHand(cards[:5], FinalHandPower.FLUSH, suit)
        return None

    def detect_straight(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains a straight.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing a straight if it is detected, None otherwise.
        """
        if len(self.cards) < 5:
            return None
        unique_value_cards = [cards[0] for cards in self.sep_values.values()]
        unique_num_values = [self.NUM_VALUES[card.value] for card in unique_value_cards]
        if len(unique_num_values) >= 5:
            for i in range(len(unique_num_values) - 4):
                if (
                    unique_num_values[i] - unique_num_values[i + 4]
                    == self.NUM_VALUES["STRAIGHT_OFFSET"]
                ):
                    return FinalHand(
                        unique_value_cards[i : i + 5],
                        FinalHandPower.STRAIGHT,
                    )
            if (
                unique_num_values[-4] == self.NUM_VALUES["5"]
                and unique_num_values[-1] == self.NUM_VALUES["2"]
                and unique_num_values[0] == self.NUM_VALUES["ACE"]
            ):
                return FinalHand(
                    unique_value_cards[-4:] + [unique_value_cards[0]],
                    FinalHandPower.STRAIGHT,
                )
        return None

    def detect_three_of_a_kind(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains a three of a kind.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing a three of a kind if it is detected, None otherwise.
        """
        if len(self.cards) < 3:
            return None
        for trips_value, cards in self.sep_values.items():
            if len(cards) == 3:
                other_high_card_list = []
                if len(self.cards) == 4:
                    if trips_value == self.cards[0].value:
                        other_high_card_list = [self.cards[3]]
                    else:
                        other_high_card_list = [self.cards[0]]
                elif len(self.cards) >= 5:
                    if trips_value == self.cards[0].value:
                        other_high_card_list = self.cards[3:5]
                    elif trips_value == self.cards[1].value:
                        other_high_card_list = [self.cards[0], self.cards[4]]
                    else:
                        other_high_card_list = self.cards[0:2]
                return FinalHand(
                    cards + other_high_card_list, FinalHandPower.THREE_OF_A_KIND
                )
        return None

    def detect_two_pairs(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains two pairs.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing two pairs if it is detected, None otherwise.
        """
        if len(self.cards) < 4:
            return None

        pair_values = [
            value for value, cards in self.sep_values.items() if len(cards) == 2
        ]
        if len(pair_values) < 2:
            return None

        first_pair_value, second_pair_value = pair_values[:2]
        first_pair_cards = self.sep_values[first_pair_value]
        second_pair_cards = self.sep_values[second_pair_value]

        if first_pair_value != self.cards[0].value:
            other_high_card = self.cards[0]
        elif second_pair_value != self.cards[2].value:
            other_high_card = self.cards[2]
        elif len(self.cards) >= 5:
            other_high_card = self.cards[4]
        else:
            return FinalHand(
                first_pair_cards + second_pair_cards, FinalHandPower.TWO_PAIRS
            )
        return FinalHand(
            first_pair_cards + second_pair_cards + [other_high_card],
            FinalHandPower.TWO_PAIRS,
        )

    def detect_one_pair(self) -> Optional[FinalHand]:
        """
        # Detect if the hand contains one pair.

        Returns:
        --------
            Optional[FinalHand]:
                Final hand representing one pair if it is detected, None otherwise.
        """
        for pair_value, cards in self.sep_values.items():
            if len(cards) == 2:
                length = min(5, len(self.cards))
                if pair_value == self.cards[0].value:
                    other_high_card_list = self.cards[2:length]
                elif pair_value == self.cards[1].value:
                    other_high_card_list = [self.cards[0]] + self.cards[3:length]
                elif pair_value == self.cards[2].value:
                    other_high_card_list = self.cards[0:2] + self.cards[4:length]
                else:
                    other_high_card_list = self.cards[0:3]
                return FinalHand(cards + other_high_card_list, FinalHandPower.ONE_PAIR)
        return None

    def detect_high_card(self) -> FinalHand:
        """
        # 'Detect' if the hand contains a high card.
        (This is the default case if no other hand is detected.)

        Returns:
        --------
            FinalHand: Final hand representing the high card hand.
        """
        length = min(5, len(self.cards))
        return FinalHand(self.cards[:length], FinalHandPower.HIGH_CARD)

    def detect_final_hand(self) -> FinalHand:
        """
        # Detect the final hand from the given hand, using all detect_ methods.

        Returns:
        --------
            FinalHand: Final hand detected from the hand.
        """
        final_hand = None
        detection_methods = [
            self.detect_royal_flush,
            self.detect_straight_flush,
            self.detect_four_of_a_kind,
            self.detect_full_house,
            self.detect_flush,
            self.detect_straight,
            self.detect_three_of_a_kind,
            self.detect_two_pairs,
            self.detect_one_pair,
        ]

        for detect_method in detection_methods:
            if (final_hand := detect_method()) is not None:
                return final_hand

        return self.detect_high_card()

    def __str__(self) -> str:
        return (
            ", ".join([str(card) for card in self.cards])
            + f"\nFinal hand: {self.final_hand}"
        )
