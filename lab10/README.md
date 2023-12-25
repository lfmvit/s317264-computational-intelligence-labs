# Tic-Tac-Toe Reinforcement Learning Player

## Introduction

This code implements a Tic-Tac-Toe player using reinforcement learning. The player uses the Q-learning algorithm to learn optimal strategies through interaction with the game environment. The implementation includes a TicTacToe class representing the game environment and functions for training and playing games.

## Code Structure

### TicTacToe Class

The `TicTacToe` class initializes a Tic-Tac-Toe game with two players, 'X' and 'O'. The class provides methods for making moves, checking the game state, and determining the winner. The game can be configured to use either 'goal_reward' or 'action_penalty' for reinforcement.

### Training Functions

1. **`initialize_Q`**: Given a set of states, this function initializes the Q-values for each possible action.

2. **`moving_average`**: Calculates the moving average of a list.

3. **`train`**: Trains a player (either 'X' or 'O') through reinforcement learning. It takes the number of training games, learning rate (`alpha`), discount factor (`gamma`), and flags for training 'X' and 'O'. The function returns the trained Q-tables and a list of rewards, the method plot the trend of the learning process by calculating the moving average ov the reward of the agent trained, either O or X.

### Playing Functions

1. **`play_games`**: Simulates a given number of games between two players with specified Q-tables and strategies. It returns win statistics and the most common initial winning moves for each player.

### Examples

The code includes examples of training and playing Tic-Tac-Toe games:

1. **Random X vs Random O**: Two players make random moves.

2. **Trained X vs Random O**: Player 'X' is trained against a random player.

3. **Random X vs Trained O**: Player 'O' is trained against a random player.

4. **Trained X vs Trained O (both trained against random)**: Both players are trained against random players.

5. **Retrained X vs Trained O**: Player 'X' is retrained against a trained player.


## Results

The code provides win rates, draw rates, and the most common initial winning moves for each player in different scenarios. The results demonstrate the learning capabilities of the Q-learning algorithm.

| Scenario                                              | X Win Rate | O Win Rate | Draws Rate | Favorite Starting Move of X | Favorite Starting Move of O |
|-------------------------------------------------------|------------|------------|------------|-----------------------------|-----------------------------|
| Random X vs Random O                                  | 61.6%      | 28.4%      | 10.0%      | (1, 1)                      | (1, 1)                      |
| Trained X vs Random O                                 | 94.4%      | 0.0%       | 5.6%       | (2, 2)                      | (1, 1)                      |
| Random X vs Trained O                                 | 1.3%       | 87.1%      | 11.6%      | (2, 0)                      | (1, 1)                      |
| Trained X vs Trained O (both trained against random)  | 0.0%       | 0.0%       | 100.0%     | (2, 2)                      | (0, 0)                      |
| Retrained X vs Trained O                               | 100.0%     | 0.0%       | 0.0%       | (2, 1)                      | (0, 2)                      |



## Notes

- The code includes extensive comments to explain the purpose and functionality of each part.

