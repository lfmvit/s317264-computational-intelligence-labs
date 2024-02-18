# Quixo

### Overview
Quixo is a strategy board game that can be played by two players. The game is played on a 5x5 grid with 25 movable cubes. The cubes can be moved by players to make a line of five cubes of their color, either horizontally, vertically, or diagonally, while simultaneously trying to prevent their opponent from achieving the same.

The game starts with all cubes placed face-up, with the white cubes representing player 0 and the black cubes representing player 1. The players take turns to move a cube from the border of the board to an empty cell, and then push the line of cubes either horizontally or vertically. A cube can only be pushed from a border cell, and once moved, it cannot be moved again until the end of the game.



This report presents an analysis and evaluation of an agent **MinMaxFragger** that utilizes a minmax approach to play the game of Quixo.


## Implementation

## Classes
## RandomPlayer

**RandomPlayer** is a player that randomly selects moves, it's not been modified.. It initializes a random position and selects a move in a random direction (top, bottom, left, or right). This player demonstrates no strategic thinking and only depends on chance. As a result, **RandomPlayer** performs poorly and is not a viable choice for competitive play.

## NoobPlayer

 **NoobPlayer** operates by searching through available moves and boards for a winning move. If it doesn't find one, it makes a random move. Although it performs better than **RandomPlayer**, it still lacks the strategic depth required for competitive play.

## MinMaxFragger

**MinMaxFragger** is the main agent a player that uses the minimax algorithm to find the best move. It has a set depth for its search tree, which limits its ability to explore all possible moves. The depth of the search tree affects the player's performance, with higher depths generally resulting in better moves. However, deeper searches also require more computation time. **MinMaxFragger** demonstrates a superior strategic approach compared to **RandomPlayer** and **NoobPlayer**. It evaluates each move based on its potential to lead to a win or prevent a loss.

## EnhancedGame

The **EnhancedGame** class extends the basic Game class, adding more features and functionality for the Quixo game. It includes methods for setting the game state from a state tuple, getting the game state as a tuple, and performing moves with border checks, rotations, and reflections. The state_from_board() method creates a hashable representation of the game state.

In the EnhancedGame class, symmetries are utilized to recognize equivalent game states. These equivalent game states have indistinguishable properties but contrast only in the orientation or mirroring of the board. By recognizing these equivalent states, the EnhancedGame class can diminish the quantity of evaluations it needs to execute and enhance the efficiency of its move evaluation and decision-making process.

Here's how symmetries are employed in the EnhancedGame class, that are of course used by `MinMaxFragger` agent when it calls the method "get_availables_moves()"

### Identifying Equivalent Board States:

1. The `EnhancedGame` class first identifies equivalent board states. Two board states are considered equivalent if one can be obtained from the other by applying a symmetry (rotation or reflection) operation.

2. By identifying such equivalent states, the class can group them together and consider them as a single state. This reduces the number of unique states that need to be evaluated, thus improving performance.

### Optimizing Evaluations:

1. During the game, when evaluating possible moves for the current player, the class can exploit the identified symmetries. It checks whether a given move results in an equivalent state to a previously evaluated state, thereby avoiding the need to re-evaluate the same state multiple times.
2. For instance, suppose the game reaches a state where Player 0 occupies cells (1,1) and (1,2), and Player 1 occupies cells (1,4) and (2,4). When evaluating possible moves for Player 1, the class can identify that this state is equivalent to the state where Player 0 occupies cells (4,4) and (4,3) and Player 1 occupies cells (4,1) and (3,1) after applying a 180-degree rotation. It can then avoid re-evaluating this state, which significantly reduces computational effort, not necessarely in terms of number of operations, but mainly in the potential benefit of evaluating states are actually differrent in terms of points of the evaluation.



## Main Algorithm - Methods and Attributes


The MinMaxFragger agent employs the Minimax algorithm with Alpha-Beta Pruning to make decisions regarding which move to make. The agent considers the possible future states of the game based on a specified depth and selects the best move that maximizes its evaluation score, which is based on the current board state and player strategy.

It takes the current player and a depth parameter as input to initialize the player's strategy.

The agent's primary method is `make_move`, which takes the current game state (`quixo_game`) as input and returns the best move that the agent should make. 

The agent uses the `minimax` method (alpha beta pruning) to calculate the best move, considering possible future game states.here are two parameters, evaluation_prev_node and max_eval (or min_eval), that are used to track the maximum or minimum value found so far depending on the player's turn. These values help prune the search tree by stopping the evaluation of branches when they are unlikely to produce better results than already found.

The `evaluate` method is used to evaluate the current state of the board.

### Evaluation Function

The evaluation function of the MinMaxFragger agent considers various factors of the board state to determine its value. These factors include the number of tiles for each player in each row, column, and diagonal, with different weights applied based on the strategic importance of each factor.

Additionally, the evaluation function takes into account if a row or column has more of the agent's tiles than the opponent's tiles, adjusting the evaluation score accordingly. The evaluation function also considers the edge rows and columns more important than the middle ones, reflecting their strategic value in the game this kind of heuristic rule was designed by playing the game live, it follows a natural way of playing the game "optimally" from a human perspective, it performs good agaist the NoobPlayer, but it may not be the absolute optimal evaluation statistically speaking.

### Results
Based of various batch of 100 games each played, with a depth of 2 for the minmax search, starting either first or second, the MinMax agent is able to outclass the NoobPlayer 99% of the times and RandomPlayer 100% of the time, most likely due to the fact that the random agent does not capitalize even in winning positions. Each batch of games runs very fast even on bad hardware, confirming the fact that the minmax approach addresses very well the game of Quixo.


### Failed Experiment
The first implementation of the Quixo agent relied of RL, following the approach of the Lab10 of Loris Vitale s317264 (https://github.com/lfmvit/s317264-computational-intelligence-labs/tree/main/lab10), making also use of the paper "Quixo Is Solved" (https://www.researchgate.net/publication/362416260_Quixo_is_Solved). 

Ideally, as stated in the paper, it is possible to completely solve Quixo, by evaluating al the possible state using smart optimization techinques to represent the states. After various attempts and lot of time spent reading the paper we realized that the premises of the paper were not actually feasible, the amount of RAM needed far exceeds the theoretical 16GB calulated by the authors due to instrinc overhead of the data structures used and memory alignement performed internally during memory management in the execution environment.

We then tried to create a simpler agent using MonteCarlo approach, but the performances against the RandomPlayer were really bad, after that, we decided to start from fresh and go for Minmax that revealed to be much simpler and powerfull for the game of Quixo.



### Collaborations and External Sources

The project it's been designed and developed in pair by Marcello Vitaggio (s318904) and Loris Fabrizio Mario Vitale (s317264).

The main agent algorithm it's ispired by the pyrazn's one, although heavily revisitated (github repo: https://github.com/poyrazn/quixo/blob/master/players/aiplayer.py)

The idea of the exploitation of symmetries it's been ispired by a review done on Lab10 of Beatrice Occhiena s314971 (https://github.com/beatrice-occhiena/Computational_intelligence/tree/main/Labs/Lab_10) who tried a similar approach in a context of RL for TicTacToe.


