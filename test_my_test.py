def tests_winning_in_Tic_Tac_Toe(agent: VisionAgent):
    agent.tools.webbrowser.open_new("https://playtictactoe.org/")

    # Start to automate individual steps
    time.sleep(5)

    agent.act("""
Everytime you make a move, wait 2 seconds before you continue.
You are playing a Tic Tac Toe game as player X. Follow these strategic rules:

1. First Move Strategy:
    - Always take the center if available
    - If center is taken, take a corner

2. Winning Strategy (in priority order):
    a) Win: Complete any line with two X's
    b) Block: Stop opponent's two-in-a-row
    c) Fork: Create multiple winning paths
    d) Defense: Take opposite corner if opponent has corner, or side middle if they have two corners

3. Game Flow:
    - After each move, wait for opponent's move
    - Verify the opponent's move is complete before proceeding
    - If you lose click in the center of the board to reset the game.

4. Error Handling:
    - If any popups appear, close them immediately
    - If the game freezes, refresh the page
    """)

