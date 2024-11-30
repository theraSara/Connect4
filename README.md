# Connect4 Game

This is a Python implementation of the classic Connect4 game. The game is played between a human and an AI where the player can drop red coins and the AI will drop yellow coins. The objective of the game is to get 4 of your coins in a row either horizontally, vertically, or diagonally before the opponent.

<img width="694" alt="image" src="https://github.com/user-attachments/assets/78effefc-6436-4c57-b765-47ea9a5ce0ec">

## Features

- Human vs. AI gameplay.
- AI uses the minimax algorithm with alpha-beta pruning for decision-making.
- Pygame-based graphical interface with visual representation of the board.
- Simple, interactive gameplay where the player can click to drop coins in columns.

## Requirements

- Python 3.x
- Pygame library
- NumPy library

To install the necessary dependencies, run:

```bash
pip install pygame numpy
```


## How to Play

1. The game is started by running the `connect4.py` script.
2. The game opens in a Pygame window, showing a grid where you can drop red coins (as a human player) and yellow coins (as the AI).
3. To drop a coin, click on one of the columns. The coin will fall to the next available row.
4. The first player (human) to get 4 coins in a row wins. If the AI wins, you lose.
5. After the game ends, the winner is displayed, and the game will pause for a few seconds before closing.

## How It Works

The game uses the following components:

- **Game Board**: A 6x7 grid where the game is played.
- **Player Turns**: The game alternates turns between the human and the AI.
- **Minimax Algorithm**: The AI uses the minimax algorithm with alpha-beta pruning to decide on its next move. The algorithm evaluates all possible moves and selects the best one based on the current board state.
- **Win Detection**: The game checks for horizontal, vertical, and diagonal wins after every move.

## Code Breakdown

### Board Functions

- `create_board()`: Creates an empty game board.
- `drop_coin()`: Drops a coin into a specific column.
- `valid_place()`: Checks if a column is valid for placing a coin.
- `next_row()`: Finds the next available row in a column for placing a coin.
- `print_board()`: Prints the current board state to the console.
- `is_win()`: Checks if a player has won by forming a line of 4 coins.

### AI and Minimax Algorithm

- `minimax()`: A recursive function that simulates all possible moves to find the optimal one for the AI.
- `score_position()`: Evaluates the board position based on potential moves and scores them accordingly.
- `pick_best_move()`: Selects the best column for the AI to drop its coin based on the score returned by the minimax algorithm.

### Drawing Functions

- `draw_board()`: Draws the Connect4 board with Pygame, displaying the current state of the game.

## Running the Game

To play the game, simply run the script:

```bash
python main.py
```

Enjoy playing against the AI, and see if you can outsmart it!



