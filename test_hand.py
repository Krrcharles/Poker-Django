"""
This module contains unit tests for the Hand and FinalHand classes.
These tests verify the behavior of different hand combinations in a game of Texas Hold'em.
"""

import unittest

from holdem.game.card import Card
from holdem.game.hand import Hand, FinalHandPower


class TestHand(unittest.TestCase):
    """
    # A test case for the Hand & FinalHand classes.
    This test case contains individual test methods to verify the behavior
    of different hand combinations in a game of Texas Hold'em.
    """

    def test_high_card(self):
        """
        # Test method for verifying a high card hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="4", suit="DIAMONDS"),
            Card(value="6", suit="SPADES"),
            Card(value="8", suit="CLUBS"),
            Card(value="10", suit="DIAMONDS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.HIGH_CARD.value)
        self.assertEqual(final_hand.value[0], "ACE")

    def test_one_pair(self):
        """
        # Test method for verifying a one pair hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="2", suit="DIAMONDS"),
            Card(value="6", suit="SPADES"),
            Card(value="8", suit="CLUBS"),
            Card(value="10", suit="DIAMONDS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.ONE_PAIR.value)
        self.assertEqual(final_hand.value[0], "2")

    def test_two_pairs(self):
        """
        # Test method for verifying a two pairs hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="2", suit="DIAMONDS"),
            Card(value="6", suit="SPADES"),
            Card(value="6", suit="CLUBS"),
            Card(value="10", suit="DIAMONDS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.TWO_PAIRS.value)
        self.assertEqual(final_hand.value[0], "6")
        self.assertEqual(final_hand.value[2], "2")

    def test_three_of_a_kind(self):
        """
        # Test method for verifying a three of a kind hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="2", suit="DIAMONDS"),
            Card(value="2", suit="SPADES"),
            Card(value="8", suit="CLUBS"),
            Card(value="10", suit="DIAMONDS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.THREE_OF_A_KIND.value)
        self.assertEqual(final_hand.value[0], "2")

    def test_straight(self):
        """
        # Test method for verifying a straight hand.
        """
        cards = [
            Card(value="ACE", suit="HEARTS"),
            Card(value="2", suit="HEARTS"),
            Card(value="3", suit="DIAMONDS"),
            Card(value="4", suit="SPADES"),
            Card(value="5", suit="CLUBS"),
            Card(value="JACK", suit="DIAMONDS"),
            Card(value="KING", suit="CLUBS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.STRAIGHT.value)
        self.assertEqual(final_hand.value[0], "5")
        self.assertEqual(final_hand.value[-1], "ACE")

    def test_flush(self):
        """
        # Test method for verifying a flush hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="4", suit="HEARTS"),
            Card(value="6", suit="HEARTS"),
            Card(value="8", suit="HEARTS"),
            Card(value="10", suit="HEARTS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="DIAMONDS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.FLUSH.value)
        self.assertEqual(final_hand.value[0], "10")
        self.assertEqual(final_hand.suit, "HEARTS")

    def test_full_house(self):
        """
        # Test method for verifying a full house hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="2", suit="DIAMONDS"),
            Card(value="2", suit="SPADES"),
            Card(value="8", suit="CLUBS"),
            Card(value="8", suit="DIAMONDS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.FULL_HOUSE.value)
        self.assertEqual(final_hand.value[0], "2")
        self.assertEqual(final_hand.value[3], "8")

    def test_four_of_a_kind(self):
        """
        # Test method for verifying four of a kind hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="2", suit="DIAMONDS"),
            Card(value="2", suit="SPADES"),
            Card(value="2", suit="CLUBS"),
            Card(value="10", suit="DIAMONDS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.FOUR_OF_A_KIND.value)
        self.assertEqual(final_hand.value[0], "2")

    def test_straight_flush(self):
        """
        # Test method for verifying a straight flush hand.
        """
        cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="3", suit="HEARTS"),
            Card(value="4", suit="HEARTS"),
            Card(value="5", suit="HEARTS"),
            Card(value="6", suit="HEARTS"),
            Card(value="KING", suit="CLUBS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.STRAIGHT_FLUSH.value)
        self.assertEqual(final_hand.value[0], "6")
        self.assertEqual(final_hand.value[-1], "2")
        self.assertEqual(final_hand.suit, "HEARTS")

    def test_royal_flush(self):
        """
        # Test method for verifying a royal flush hand.
        """
        cards = [
            Card(value="10", suit="HEARTS"),
            Card(value="JACK", suit="HEARTS"),
            Card(value="QUEEN", suit="HEARTS"),
            Card(value="KING", suit="HEARTS"),
            Card(value="ACE", suit="HEARTS"),
            Card(value="9", suit="CLUBS"),
            Card(value="8", suit="CLUBS"),
        ]
        hand = Hand(cards)
        final_hand = hand.final_hand
        self.assertEqual(final_hand.power, FinalHandPower.ROYAL_FLUSH.value)
        self.assertEqual(final_hand.suit, "HEARTS")

    def test_flush_wins_over_straight(self):
        """
        # Test method for verifying that a flush wins over a straight.
        A flush always wins over a straight,
        even if the straight is ACE high while the flush is 10 high.
        """
        community_cards = [
            Card(value="4", suit="HEARTS"),
            Card(value="6", suit="HEARTS"),
            Card(value="10", suit="HEARTS"),
            Card(value="JACK", suit="SPADES"),
            Card(value="QUEEN", suit="CLUBS"),
        ]
        flush_cards = [
            Card(value="2", suit="HEARTS"),
            Card(value="3", suit="HEARTS"),
        ]
        straight_cards = [
            Card(value="KING", suit="DIAMONDS"),
            Card(value="ACE", suit="CLUBS"),
        ]
        flush_final_hand = Hand(community_cards + flush_cards).final_hand
        straight_final_hand = Hand(community_cards + straight_cards).final_hand
        self.assertEqual(flush_final_hand.power, FinalHandPower.FLUSH.value)
        self.assertEqual(straight_final_hand.power, FinalHandPower.STRAIGHT.value)
        self.assertGreater(flush_final_hand, straight_final_hand)

    def test_higher_straight_flush_wins(self):
        """
        # Test method for verifying that a higher straight flush wins.
        higher_straight_flush is 8 high and lower_straight_flush is 7 high.
        """
        community_cards = [
            Card(value="4", suit="HEARTS"),
            Card(value="5", suit="HEARTS"),
            Card(value="6", suit="HEARTS"),
            Card(value="7", suit="HEARTS"),
            Card(value="ACE", suit="DIAMONDS"),
        ]
        higher_straight_flush = [
            Card(value="8", suit="HEARTS"),
            Card(value="7", suit="DIAMONDS"),
        ]
        lower_straight_flush = [
            Card(value="3", suit="HEARTS"),
            Card(value="ACE", suit="HEARTS"),
        ]
        lower_straight_flush_final_hand = Hand(
            community_cards + lower_straight_flush
        ).final_hand
        higher_straight_flush_final_hand = Hand(
            community_cards + higher_straight_flush
        ).final_hand
        self.assertEqual(
            lower_straight_flush_final_hand.power, FinalHandPower.STRAIGHT_FLUSH.value
        )
        self.assertEqual(
            higher_straight_flush_final_hand.power, FinalHandPower.STRAIGHT_FLUSH.value
        )
        self.assertGreater(
            higher_straight_flush_final_hand, lower_straight_flush_final_hand
        )

    def test_equal_full_house(self):
        """
        # Test method for verifying that two full houses are equal.
        A hand is only 5 cards, so having two 3 of a kind doesn't change the hand.
        Here both have a full house (JACKs full of 5s).
        """
        community_cards = [
            Card(value="JACK", suit="HEARTS"),
            Card(value="JACK", suit="DIAMONDS"),
            Card(value="JACK", suit="SPADES"),
            Card(value="5", suit="CLUBS"),
            Card(value="5", suit="DIAMONDS"),
        ]
        first_full_house = [
            Card(value="5", suit="HEARTS"),
            Card(value="ACE", suit="SPADES"),
        ]
        second_full_house = [
            Card(value="2", suit="CLUBS"),
            Card(value="3", suit="CLUBS"),
        ]
        first_full_house_final_hand = Hand(
            community_cards + first_full_house
        ).final_hand
        second_full_house_final_hand = Hand(
            community_cards + second_full_house
        ).final_hand
        self.assertEqual(
            first_full_house_final_hand.power, FinalHandPower.FULL_HOUSE.value
        )
        self.assertEqual(
            second_full_house_final_hand.power, FinalHandPower.FULL_HOUSE.value
        )
        self.assertEqual(first_full_house_final_hand, second_full_house_final_hand)


if __name__ == "__main__":
    unittest.main()
