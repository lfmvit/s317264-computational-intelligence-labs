# Quixo
computational intelligence's exam - 2023-24

### Overview

This report presents an analysis and evaluation of an agent **MinMaxFragger** that utilizes a minmax approach to play the game of Quixo.


## Implementation

### Classes
### RandomPlayer

**RandomPlayer** is a player that randomly selects moves, it's not been modified.. It initializes a random position and selects a move in a random direction (top, bottom, left, or right). This player demonstrates no strategic thinking and only depends on chance. As a result, **RandomPlayer** performs poorly and is not a viable choice for competitive play.

## NoobPlayer

 **NoobPlayer** operates by searching through available moves and boards for a winning move. If it doesn't find one, it makes a random move. Although it performs better than **RandomPlayer**, it still lacks the strategic depth required for competitive play.

## MinMaxFragger

**MinMaxFragger** is the main agent a player that uses the minimax algorithm to find the best move. It has a set depth for its search tree, which limits its ability to explore all possible moves. The depth of the search tree affects the player's performance, with higher depths generally resulting in better moves. However, deeper searches also require more computation time. **MinMaxFragger** demonstrates a superior strategic approach compared to **RandomPlayer** and **NoobPlayer**. It evaluates each move based on its potential to lead to a win or prevent a loss.

## EnhancedGame

The **EnhancedGame** class extends the basic Game class, adding more features and functionality for the Quixo game. It includes methods for setting the game state from a state tuple, getting the game state as a tuple, and performing moves with border checks, rotations, and reflections. The state_from_board() method creates a hashable representation of the game state.

In the EnhancedGame class, symmetries are utilized to recognize equivalent game states. These equivalent game states have indistinguishable properties but contrast only in the orientation or mirroring of the board. By recognizing these equivalent states, the EnhancedGame class can diminish the quantity of evaluations it needs to execute and enhance the efficiency of its move evaluation and decision-making process.

Here's how symmetries are employed in the EnhancedGame class, that are of course used by minmaxagent trough the method "get_availables_moves()"
### Identifying Equivalent Board States:

1. The `EnhancedGame` class first identifies equivalent board states. Two board states are considered equivalent if one can be obtained from the other by applying a symmetry (rotation or reflection) operation.

2. By identifying such equivalent states, the class can group them together and consider them as a single state. This reduces the number of unique states that need to be evaluated, thus improving performance.

### Optimizing Evaluations:

1. During the game, when evaluating possible moves for the current player, the class can exploit the identified symmetries. It checks whether a given move results in an equivalent state to a previously evaluated state, thereby avoiding the need to re-evaluate the same state multiple times.
2. For instance, suppose the game reaches a state where Player 0 occupies cells (1,1) and (1,2), and Player 1 occupies cells (1,4) and (2,4). When evaluating possible moves for Player 1, the class can identify that this state is equivalent to the state where Player 0 occupies cells (4,4) and (4,3) and Player 1 occupies cells (4,1) and (3,1) after applying a 180-degree rotation. It can then avoid re-evaluating this state, which significantly reduces computational effort, not necessarely in terms of number of operations, but mainly in the potential value of the states evaluated, focusing on states that are actually different.



## Main Algorithm - Methods and Attributes


The MinMaxFragger agent employs the Minimax algorithm with Alpha-Beta Pruning to make decisions regarding which move to make. The agent considers the possible future states of the game based on a specified depth and selects the best move that maximizes its evaluation score, which is based on the current board state and player strategy.

It takes the current player and a depth parameter as input to initialize the player's strategy.

The agent's primary method is `make_move`, which takes the current game state (`quixo_game`) as input and returns the best move that the agent should make. The agent uses the `minimax` method to calculate the best move, considering possible future game states. The `evaluate` method is used to evaluate the current state of the board.

### Evaluation Function

The evaluation function of the MinMaxFragger agent considers various factors of the board state to determine its value. These factors include the number of tiles for each player in each row, column, and diagonal, with different weights applied based on the strategic importance of each factor.

Additionally, the evaluation function takes into account if a row or column has more of the agent's tiles than the opponent's tiles, adjusting the evaluation score accordingly. The evaluation function also considers the edge rows and columns more important than the middle ones, reflecting their strategic value in the game this kind of heuristic rule was designed by playing the game live, it follows a natural way of playing the game optimally from a human perspective, it performs good agaist the NoobPlayer, but it may not be the absolute optimal strategy.


### Conclusions

### Failed Experiments

### Notes

### Collaborations and External Sources


