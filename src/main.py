from .classes import GameStatus, GameManager

def main():
    ### Initialize
    # Get input, begin the game
    total_mines = int(input("Enter the number of mines: ")) # TODO: Handle better
    manager = GameManager(total_mines)
    manager.game_status = GameStatus.STARTING
    # ... do things to initialize?
    manager.game_status = GameStatus.PLAYING

    ### Main loop
    # Get user input, process that input, output the new grid data
    while manager.game_status == GameStatus.PLAYING:
        # ... get input (where did the user click?)
        # ... process (e.g. check if lost)
        # ... output updates (ex: new grid)
        break
    
    ### End game
    if manager.game_status == GameStatus.WIN:
        pass
    else:
        pass

    manager.game_status = GameStatus.END

if __name__ == "__main__":
    main()
