import os
import random

class SlotMachine:
    def __init__(self):
        self.symbols = [
            {"symbol": os.path.abspath(os.path.join('src', 'images', 'symbols', '1.png')), "payout": 1.1, "weight": 500},
            {"symbol": os.path.abspath(os.path.join('src', 'images', 'symbols', '2.png')), "payout": 1.5, "weight": 500},
            {"symbol": os.path.abspath(os.path.join('src', 'images', 'symbols', '3.png')), "payout": 5, "weight": 300},
            {"symbol": os.path.abspath(os.path.join('src', 'images', 'symbols', '4.png')), "payout": 10, "weight": 300},
            {"symbol": os.path.abspath(os.path.join('src', 'images', 'symbols', '5.png')), "payout": 15, "weight": 100},
            {"symbol": os.path.abspath(os.path.join('src', 'images', 'symbols', '6.png')), "payout": 20, "weight": 100},
        ]

        self.special_symbol = os.path.abspath(os.path.join('src', 'images', 'symbols', 'jackpot.png'))
        self.jackpot_multiplier = 5000

        self.special_symbol_weight = 1

        self.reel_symbols = []

        for symbol_data in self.symbols:
            self.reel_symbols.extend([symbol_data["symbol"]] * symbol_data["weight"])

        self.reel_symbols.extend([self.special_symbol] * int(self.special_symbol_weight))

    def spin(self):
        """Spin the slot machine and return the result as a 3x3 grid."""
        return [[random.choice(self.reel_symbols) for _ in range(3)] for _ in range(3)]

    def calculate_payout(self, spin_result, bet):
        """Calculate the payout based on the spin result, considering rows, columns, and diagonals."""
        lines = []

        lines.extend(spin_result)

        for col in range(3):
            lines.append([spin_result[row][col] for row in range(3)])

        lines.append([spin_result[i][i] for i in range(3)])
        lines.append([spin_result[i][2 - i] for i in range(3)])

        total_payout = 0
        for line in lines:
            counts = {symbol: line.count(symbol) for symbol in self.reel_symbols}

            for symbol_data in self.symbols:
                symbol = symbol_data["symbol"]
                payout = symbol_data["payout"]

                if counts.get(symbol, 0) == 3:
                    total_payout += payout

            if counts.get(self.special_symbol, 0) > 0:
                total_payout += bet * self.jackpot_multiplier

        return total_payout

    def play(self, bet):
        """Simulate a play on the slot machine."""
        spin_result = self.spin()
        payout = self.calculate_payout(spin_result, bet)
        return spin_result, payout
