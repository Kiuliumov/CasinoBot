import random

class Roulette:
    def __init__(self):
        self.red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

    def spin(self):
        result = random.randint(0, 36)
        if result == 0:
            color = "green"
        elif result in self.red_numbers:
            color = "red"
        else:
            color = "black"

        return result, color
