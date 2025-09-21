"""
File: test_sweeper.py
Module: test
Function: To run an automated series of unit tests to ensure the source code functions as expected.
Inputs:
    - The rest of the source code.
Outputs:
    - When run with pytest, the test results.
Authors: 
    Delroy Wright
    Jack Bauer
Date: 9/4/2025
NOTE: All code in the file was authored by 1 or more of the authors. No outside sources were used for code
"""
from src import main, classes
import pytest # Our testing library

@pytest.fixture
def fresh_game():
    """Create a new GameManager object for use in later tests."""
    game =  classes.GameManager()
    print(game)
    return game

def test_new_game(fresh_game):
    """When a new game starts, ensure that we initialize to the WELCOME state."""
    assert fresh_game.game_status == classes.GameStatus.WELCOME
    
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
