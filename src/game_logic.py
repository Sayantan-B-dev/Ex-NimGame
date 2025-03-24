import random

class GameLogic:
    def __init__(self, num_piles=5, max_pile_size=10):
        self.num_piles = num_piles
        self.max_pile_size = max_pile_size
        self.initial_piles = [random.randint(1, max_pile_size) for _ in range(num_piles)]
        self.piles = self.initial_piles.copy()
        self.current_player = 0  # 0 for Player 1, 1 for Player 2

    def reset(self, randomize=False):
        if randomize:
            self.initial_piles = [random.randint(1, self.max_pile_size) for _ in range(self.num_piles)]
        self.piles = self.initial_piles.copy()
        self.current_player = 0

    def make_move(self, pile, number):
        if 0 < number <= self.piles[pile]:
            self.piles[pile] -= number
            self.current_player = 1 - self.current_player
            return True
        return False

    def is_game_over(self):
        return all(p == 0 for p in self.piles)

    def get_piles(self):
        return self.piles.copy()

    def get_current_player(self):
        return self.current_player

    def make_ai_move(self):
        non_empty_piles = [i for i, p in enumerate(self.piles) if p > 0]
        if non_empty_piles:
            pile = random.choice(non_empty_piles)
            number = random.randint(1, self.piles[pile])
            self.make_move(pile, number)