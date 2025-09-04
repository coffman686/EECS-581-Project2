# very basic class, feel free to change anything
class GameState:
    game_statuses = ["Starting","Playing","Lose","Win"]

    total_mines = 10
    def __init__(self):
        self.remaining_mine_count = self.total_mines
        self.game_status = self.game_statuses[0]

