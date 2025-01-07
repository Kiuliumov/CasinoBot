import random


class Blackjack:
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_balance = 0
        self.bet = 0
        self.game_over = False
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11
        }

    def reset_deck(self):
        self.deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def calculate_hand_value(self, hand):
        total = sum(self.card_values[card] for card in hand)
        num_aces = hand.count('A')

        # Adjust for Aces being 1 or 11
        while total > 21 and num_aces:
            total -= 10  # Change an Ace from 11 to 1
            num_aces -= 1
        return total

    def start_game(self, bet, balance):
        self.reset_deck()
        self.bet = bet
        self.player_balance = balance
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.game_over = False

    def is_blackjack(self, hand):
        return self.calculate_hand_value(hand) == 21 and len(hand) == 2

    def player_bust(self):
        return self.calculate_hand_value(self.player_hand) > 21

    def dealer_bust(self):
        return self.calculate_hand_value(self.dealer_hand) > 21

    def player_wins(self):
        player_total = self.calculate_hand_value(self.player_hand)
        dealer_total = self.calculate_hand_value(self.dealer_hand)

        if player_total > 21:
            return False
        if dealer_total > 21:
            return True
        return player_total > dealer_total

    def dealer_plays(self):
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())

    def get_hand_string(self, hand):
        return ', '.join(hand)