

import random
from game import Game, Move, Player
from board import Board
from copy import deepcopy

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class MinMaxPlayer(Player):
    def __init__(self, max_depth=3) -> None:
        super().__init__()
        self.max_depth = max_depth
        self.move_cache = {}  # Cache to speed up move calculations

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # Create a Board instance from the game state
        board = Board(game.get_board())
        # Return the best move for the current game state using Minimax with Alpha-Beta Pruning
        return self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)[1]

    def minimax(self, board: 'Board', depth, alpha, beta, maximizingPlayer):
        # Convert the board object to a tuple to use it as a key in the move_cache dictionary
        board_tuple = tuple(map(tuple, board._board))

        if board_tuple in self.move_cache:
            return self.move_cache[board_tuple]

        if depth == 0 or board.check_winner() != -1:
            return board.check_winner(), None

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            for action in board.get_legal_actions(1):  # Assuming player 1 is always the maximizing player
                next_board = deepcopy(board)
                next_board.move(action, 1)  # Always use player 1 index to make the move
                evaluation = self.minimax(next_board, depth - 1, alpha, beta, False)[0]
                if evaluation > maxEval:
                    maxEval = evaluation
                    best_move = action
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            self.move_cache[board_tuple] = (maxEval, best_move)
            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for action in board.get_legal_actions(0):  # Assuming player 0 is always the minimizing player
                next_board = deepcopy(board)
                next_board.move(action, 0)  # Always use player 0 index to make the move
                evaluation = self.minimax(next_board, depth - 1, alpha, beta, True)[0]
                if evaluation < minEval:
                    minEval = evaluation
                    best_move = action
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            self.move_cache[board_tuple] = (minEval, best_move)
            return minEval, best_move

    def __init__(self, max_depth=3) -> None:
        super().__init__()
        self.max_depth = max_depth
        self.move_cache = {}  # Cache to speed up move calculations

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # Create a Board instance from the game state
        board = Board(game.get_board())
        # Return the best move for the current game state using Minimax with Alpha-Beta Pruning
        return self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)[1]

    def minimax(self, board: 'Board', depth, alpha, beta, maximizingPlayer):
        if board in self.move_cache:
            return self.move_cache[board]

        if depth == 0 or board.check_winner() != -1:
            return board.check_winner(), None

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            for action in board.get_legal_actions(1):  # Assuming player 1 is always the maximizing player
                next_board = deepcopy(board)
                next_board.move(action, 1)  # Always use player 1 index to make the move
                evaluation = self.minimax(next_board, depth - 1, alpha, beta, False)[0]
                if evaluation > maxEval:
                    maxEval = evaluation
                    best_move = action
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            self.move_cache[board] = (maxEval, best_move)
            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for action in board.get_legal_actions(0):  # Assuming player 0 is always the minimizing player
                next_board = deepcopy(board)
                next_board.move(action, 0)  # Always use player 0 index to make the move
                evaluation = self.minimax(next_board, depth - 1, alpha, beta, True)[0]
                if evaluation < minEval:
                    minEval = evaluation
                    best_move = action
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            self.move_cache[board] = (minEval, best_move)
            return minEval, best_move

if __name__ == '__main__':
    wins = [0, 0]

    for i in range(100):
        g = Game()
        player1 = RandomPlayer()
        player2 = MinMaxPlayer()
        wins[g.play(player1, player2)] += 1
        print(i)
        
    print(f"My Player won {wins[1]} times")
    print(f"Random Player won {wins[0]} times")
