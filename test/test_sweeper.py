from src import main, classes
import pytest

@pytest.fixture
def fresh_game():
    game =  main.GameManager(10)
    print(game)
    return game

def test_new_game(fresh_game):
    assert fresh_game.game_status == classes.GameStatus.STARTING # TODO: We don't want a new game to immediately END
    
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
