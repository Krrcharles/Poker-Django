"""
This module represents a poker game.

It contains the PrintGame class which represents a poker game
and provides methods to watch a round unfold in the terminal.
"""

from holdem.game.hand import Hand
from holdem.game.deck import Deck


class PrintGame:
    """
    Represents a poker game.

    Attributes:
    -----------
        players (int): The number of players in the game.
        deck (Deck): The deck of cards used in the game.
        players_cards (List[List[Card]]): The cards held by each player.
        community_cards (List[Card]): The community cards on the table.
    """

    def __init__(self, players=8, deck_id=None):
        """
        # Initialize a Game object.

        Args:
        -----
            players (int, optional): The number of players in the game. Defaults to 8.
            deck_id (str, optional): The ID of an existing deck. Defaults to None.

        """
        self.players = players
        self.deck = Deck(deck_id=deck_id)
        if deck_id is not None:
            self.deck.shuffle()
        self.players_cards = []
        self.community_cards = []

    def prepare_round(self):
        """
        # Prepare for a new round of the game by dealing cards to players and community.
        """
        self.players_cards = [self.deck.draw(2) for _ in range(self.players)]
        self.community_cards = self.deck.draw(5)

    def play_step(self, step_name, community_cards_drawn, active_players=None):
        """
        # Play a step of the game.

        Args:
        -----
            step_name (str): The name of the step.
            community_cards_drawn (int): The number of community cards to reveal.
            active_players (List[int], optional):
                The indices of active players. Defaults to an empty list.
        """
        if active_players is None:
            active_players = []
        print(">>>", step_name.title(), "<<<")
        print(
            ">> Community cards:",
            [card.unicode for card in self.community_cards][:community_cards_drawn],
        )
        players_hands = [
            Hand(cards + self.community_cards[:community_cards_drawn])
            for cards in [self.players_cards[i] for i in active_players]
        ]
        sorted_indices = sorted(
            range(len(active_players)),
            key=lambda i: players_hands[i].final_hand,
            reverse=True,
        )
        for i in sorted_indices:
            hand = players_hands[i]
            player = active_players[i]
            print(
                f">> Player {player+1}'s hand:",
                hand.final_hand,
                [card.unicode for card in hand.final_hand.cards],
            )
        best_index = sorted_indices[0]
        best_indices = [best_index]
        best_final_hand = players_hands[best_index].final_hand
        for i in range(1, len(sorted_indices)):
            if players_hands[sorted_indices[i]].final_hand == best_final_hand:
                best_indices.append(sorted_indices[i])
            else:
                break
        if len(best_indices) == 1:
            print(
                f">>> Best hand by player {active_players[best_index]+1}:",
                best_final_hand,
                [card.unicode for card in best_final_hand.cards],
            )
        else:
            print(
                ">>> Tie between players",
                ", ".join(active_players[i] + 1 for i in best_indices[:-1]),
                f"and {active_players[best_indices[-1]] + 1}:",
                best_final_hand,
                [card.unicode for card in best_final_hand.cards],
            )
        print()

    def start_game(self):
        """
        # Start the game and determining the winner.
        """
        self.prepare_round()
        print(
            "\n>>>>>>>>> Start <<<<<<<<<\n",
        )
        steps = {"pre-flop": 0, "flop": 3, "turn": 4, "river": 5}
        # a quarter of the players fold between each step
        players = {
            "pre-flop": list(range(self.players)),
            "flop": list(range(self.players // 4 * 3)),
            "turn": list(range(self.players // 2)),
            "river": list(range(self.players // 4)),
        }
        for step_name, community_cards_drawn in steps.items():
            self.play_step(step_name, community_cards_drawn, players[step_name])
        print(">>>>>>>>> End <<<<<<<<<", end="\n\n\n\n")


if __name__ == "__main__":
    game = PrintGame(players=8, deck_id="o9fy1ih84kvx")
    game.start_game()
