from src.classes import GameStatus, GameManager

def main():
    ### Initialize
    manager = GameManager() 
    manager.change_state(GameStatus.PLAYING)

    ### Main loop
    # Get user input, process that input, output the new grid data
    while manager.should_quit != True:
        # ... get input from frontend (where did the user click?)
        # ... process in backend (e.g. check if lost)
        # ... output updates to frontend (ex: new grid)
        break

if __name__ == "__main__":
    main()
