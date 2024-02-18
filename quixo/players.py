
import random
from game import Game, Move, Player
from collections import defaultdict
from tqdm.auto import tqdm
import numpy as np
import pickle
from copy import deepcopy
from itertools import product
from enhanced_game import EnhancedGame

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

"noob player is like your average teamate when you are solo queuing in ranked, it sucks, but it can capitalize on a immediate win if he sees it"
class NoobPlayer(Player):
    def __init__(self,player) -> None:
        super().__init__()
        self.player = player

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        g = EnhancedGame()
        moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
        l = [0,1,2,3,4]
        l2 = [0,4]
        p1 = list(product(l, l2))
        p2 = list(product(l2, l))
        positions = list(set(p1) | set(p2))
        for pos in positions:
            for move in moves:
                g.set_board(game.get_board())
                ok = g.move(pos,move,self.player)
                if not ok:
                    continue
                if g.check_winner() == self.player:
                    return pos,move
        from_pos = random.choice(positions)
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move



class MinMaxFragger(Player):
    def __init__(self, player: int, depth: int):
        self.player = player
        self.depth = depth
        self.board = EnhancedGame()
        self.initial_val = float('inf') if player == 0 else float('-inf')

    def make_move(self, quixo_game: Game) -> tuple[tuple[int, int], Move]:
        self.board.set_board(quixo_game.get_board())
        _, move = self.minimax(deepcopy(self.board), depth=self.depth, maximizing_player = self.player, evaluation_prev_node = self.initial_val)
        return move

    def minimax(self, quixo_game: EnhancedGame, depth: int, maximizing_player: int, evaluation_prev_node: float):
        if depth == 0 or quixo_game.check_winner() != -1:
            return self.evaluate(quixo_game), None

        possible_moves = quixo_game.get_available_moves(maximizing_player)

        if maximizing_player == 0:
            max_eval = float('-inf')
            best_move = None
            for tile,move in possible_moves:
                if max_eval == float('inf'):
                    return max_eval, best_move
                if max_eval >= evaluation_prev_node:
                    return max_eval, best_move
                
                new_game = deepcopy(quixo_game)
                ok = new_game.move(tile,move,0)
                if not ok:
                    print(tile, move)
                    continue
                evaluation, _ = self.minimax(new_game, depth - 1, 1, max_eval)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = tile,move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for tile,move in possible_moves:
                if min_eval == float('-inf'):
                    return min_eval, best_move
                if min_eval <= evaluation_prev_node:
                    return min_eval, best_move
                
                new_game = deepcopy(quixo_game)
                ok = new_game.move(tile,move,1)
                if not ok:
                    print(tile, move)
                    continue
                evaluation, _ = self.minimax(new_game, depth - 1, 0, min_eval)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = tile,move
            return min_eval, best_move

    def evaluate(self, quixo_game: EnhancedGame) -> float:
        # Check for a winner and return appropriate values
        winner = quixo_game.check_winner()
        if winner == 1:
            return float('-inf')
        elif winner == 0:
            return float('inf')
        
        # Initialize lists for tracking row and column scores
        row_scores = []
        col_scores = []

        # Calculate scores for rows and columns
        for i in range(quixo_game._board.shape[0]):
            x_r = sum([1 for j in range(quixo_game._board.shape[1]) if quixo_game._board[i,j] == 0])
            o_r = sum([1 for j in range(quixo_game._board.shape[1]) if quixo_game._board[i,j] == 1])
            row_scores.extend([x_r, o_r])

            x_c = sum([1 for j in range(quixo_game._board.shape[1]) if quixo_game._board[j,i] == 0])
            o_c = sum([1 for j in range(quixo_game._board.shape[1]) if quixo_game._board[j,i] == 1])
            col_scores.extend([x_c, o_c])

        # Calculate scores for diagonals
        x_d1 = sum([1 for i in range(quixo_game._board.shape[0]) if quixo_game._board[i,i] == 0])
        o_d1 = sum([1 for i in range(quixo_game._board.shape[0]) if quixo_game._board[i,i] == 1])
        
        x_d2 = sum([1 for i in range(quixo_game._board.shape[0]) if quixo_game._board[i, -(i+1)] == 0])
        o_d2 = sum([1 for i in range(quixo_game._board.shape[0]) if quixo_game._board[i, -(i+1)] == 1])

        # Initialize the evaluation value
        evaluation = 0

        # Calculate scores for rows and columns
        for i in range(len(row_scores)):
            val = row_scores[i] / 4 - col_scores[i] / 4
            
            if row_scores[i] > col_scores[i]:
                val += row_scores[i]*0.1
            elif row_scores[i] < col_scores[i]:
                val -= col_scores[i]*0.1

            if i<2 or i>=len(row_scores)-2:
                val *= 1.5
            
            evaluation += val

        # Calculate scores for diagonals
        val_d1 = x_d1 / 4 - o_d1 / 4
        if x_d1 > o_d1:
            val_d1 += x_d1*0.1
        elif x_d1 < o_d1:
            val_d1 -= o_d1*0.1
        
        evaluation += val_d1

        val_d2 = x_d2 / 4 - o_d2 / 4
        if x_d2 > o_d2:
            val_d2 += x_d2*0.1
        elif x_d2 < o_d2:
            val_d2 -= o_d2*0.1
        
        evaluation += val_d2

        # Return the final evaluation value
        return evaluation
