class Scoreboard:
    def __init__(self):
        self._scores = {"1": 0, "2": 0}

    @property
    def scores(self):
        return self._scores

    def give_point(self, player_n):
        self._scores[player_n] += 1

    def reset_score(self):
        self._scores["1"] = 0
        self._scores["2"] = 0

    def __str__(self):
        return f"p1: {self._scores['1']}\np2: {self._scores['2']}"
