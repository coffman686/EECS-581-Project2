from src import main
import pytest

@pytest.fixture
def fresh_game():
    game =  main.GameState()
    print(game)
    return game

def test_new_game(fresh_game):
    assert fresh_game.game_status == fresh_game.game_statuses[0]
    
# # TESTS TO WRITE
#
# - random mine generation 
# - user-input number of mines and mine creation 
# - cell clicking
# - game end 
# - adjacent mine count test 
# - clicked with no empty cell causes recursive clicks
# - flag support 
#     - cant uncover until unflagged
#     - display remaining flag count 
# - mine count reduces correctly 
# - check initial game setup 
