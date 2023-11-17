# Nim Adaptive Strategy

## Overview

This project implements an a fixed rule and an adaptive strategy for playing Nim, a mathematical game of strategy. The game consists of rows with varying objects, and players take turns removing objects to avoid being the one to remove the last object.

Just for the sake of curiosity, I utilized

## Strategies

### Task 2.1 - Fixed Rule Strategy

In lab2_nim, I developed an improved fixed rule method `optimal with misere` starting from the already present `optimal`. This method handles the end game states by adapting it's strategy when there is only 1 row with n > 1 element among all the rows remaining. In this situation in fact, continuing to follow the nimsum strategy it's a terrible blunder. 

By checking how many active rows we have in the end game state, we can ensure the win by takin:
- n element from the longest row if the number of active rows are even
- n-1 elements from the longest row if the number is odd

This strategy achieves 100% win rate againt any of the other strategies if the player who adopts start first, other wise, it wins 99% of the time.

### Task 2.2 - Adaptive Strategy

In lab2_nim_EA, the `adaptive` strategy is represented by an agent with a genotype, adapting based on the current game state. Conditions for move selection include adjusting row and number of objects. The strategy evolves using a genetic algorithm with crossover and mutation.

The adaptive strategy introduces an adaptive approach to the game. The strategy is represented by an agent with a genotype, which includes two parameters: the row adjustment and the number of objects adjustment. The strategy adapts based on the current game state and the agent's genotype.

The adaptive strategy considers the following conditions:

- If the selected row is greater than the first row and the adjusted number of objects is less than zero, choose the move that maximizes the number of objects in the first row.
- If the selected row is greater than the first row, choose the move that maximizes the adjusted number of objects.
- If the adjusted number of objects is less than zero, choose the move that maximizes the number of objects in the first row.
- Otherwise, choose the move that maximizes the adjusted number of objects.
- The strategy evolves over multiple generations using a genetic algorithm, including crossover and mutation, to find an optimal genotype.

Example:  the best genome found is [0, -2]:

The first element (0) represents the weight given to the row.
The second element (-2) represents the weight given to the number of objects in the row.
So, for each possible move, the strategy evaluates the combination of row and objects, and it chooses the move with the maximum value of (row weight + number of objects weight).

In practical terms:

If the row is 0, and there are 3 objects in that row, the value would be 0 + (-2) = -2.
If the row is 1, and there are 4 objects, the value would be 0 + (-2) = -2.
If the row is 2, and there are 5 objects, the value would be 0 + (-2) = -2.
The strategy selects the move with the maximum value. In this case, it prioritizes moves that reduce the number of objects in the row, giving higher importance to the number of objects compared to the row itself.

## Results

| Strategy           | Win Rate | Best Genome | Fitness |
|--------------------|----------|-------------|---------|
| Adaptive vs Optimal| 40%      | [-4, -7]    | 0.57    |
| Adaptive vs Pure Random | 51% | [-1, -2]     | 0.61    |

Considering that the optimal strategy plays with the nimsum, a win rate of 40% is not that bad, on the other hand, the adaptation against the pure random only performs slitgly better than a random vs random situation.

## Collaboration

For this laboratory in Task 1, I collaborated closely with  a course mate Marcello Vitaggio (https://github.com/Kalller/computational-intelligence) to successfully address and rectify the misère bug present in the original optimal method.

I also leveraged chatGTP and python documentation because I'm still learning all the features that python has to offer to handle data with coincise instructions (ex: list comprehensions).



