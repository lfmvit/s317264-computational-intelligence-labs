import random
from game import Game, Move, Player
from collections import defaultdict
from tqdm.auto import tqdm
import numpy as np
from scipy.sparse import lil_matrix
from copy import deepcopy
from itertools import product


CLOCKWISE_ROTATION_90_DEGREES = np.array([4,9,14,19,24,3,8,13,18,23,2,7,12,17,22,1,6,11,16,21,0,5,10,15,20])
CLOCKWISE_ROTATION_180_DEGREES = CLOCKWISE_ROTATION_90_DEGREES[CLOCKWISE_ROTATION_90_DEGREES]
CLOCKWISE_ROTATION_270_DEGREES = CLOCKWISE_ROTATION_180_DEGREES[CLOCKWISE_ROTATION_90_DEGREES]
MIRROR_IMAGE = np.array([4,3,2,1,0,9,8,7,6,5,14,13,12,11,10,19,18,17,16,15,24,23,22,21,20]) 
MIRROR_ROTATION_90_DEGREES = MIRROR_IMAGE[CLOCKWISE_ROTATION_90_DEGREES]
MIRROR_ROTATION_180_DEGREES = MIRROR_IMAGE[CLOCKWISE_ROTATION_180_DEGREES]
MIRROR_ROTATION_270_DEGREES = MIRROR_IMAGE[CLOCKWISE_ROTATION_270_DEGREES]
ALL_SYMMETRIES = [CLOCKWISE_ROTATION_90_DEGREES, CLOCKWISE_ROTATION_180_DEGREES, CLOCKWISE_ROTATION_270_DEGREES, MIRROR_ROTATION_90_DEGREES, MIRROR_ROTATION_180_DEGREES, MIRROR_ROTATION_270_DEGREES, MIRROR_IMAGE]
ALLOWED_SLIDES = [Move.TOP,Move.LEFT,Move.BOTTOM,Move.RIGHT]

class EnhancedGame(Game):
    def __init__(self):
        super().__init__()

    def set_state(self, state):
        board,_ = EnhancedGame.board_from_state(state)
        self._board = board
    
    def set_board(self, board):
        self._board = board
    
    def state_from_board(self,player: int):
        board = self.get_board()
        board = board.flatten()
        Xs = board == 0
        Os = board == 1
        key = tuple(map(tuple, (Xs, Os))), player
        return key

    def board_from_state(state):
        board = np.ones(25, dtype=np.uint8) * -1
        Xs_Os,player = state
        Xs,Os = Xs_Os
        board[list(Xs)] = 0
        board[list(Os)] = 1
        return board.reshape(5,5), player
    
    def move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id not in (0, 1):
            return False
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable = self.take((from_pos[1], from_pos[0]), player_id)
        if acceptable:
            acceptable = self.slide((from_pos[1], from_pos[0]), slide)
            if not acceptable:  # restore previous
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable

    def take(self, from_pos: tuple[int, int], player_id: int) -> bool:
        """Checks that {from_pos} is in the border and marks the cell with {player_id}"""
        row, col = from_pos
        from_border = row in (0, 4) or col in (0, 4)
        if not from_border:
            return False  # the cell is not in the border
        if self._board[from_pos] != player_id and self._board[from_pos] != -1:
            return False  # the cell belongs to the opponent
        self._board[from_pos] = player_id
        return True

    @staticmethod
    def acceptable_slides(from_position: tuple[int, int]):
        """When taking a piece from {from_position} returns the possible moves (slides)"""
        acceptable_slides = [Move.BOTTOM, Move.TOP, Move.LEFT, Move.RIGHT]
        axis_0 = from_position[0]    # axis_0 = 0 means uppermost row
        axis_1 = from_position[1]    # axis_1 = 0 means leftmost column

        if axis_0 == 0:  # can't move upwards if in the top row...
            acceptable_slides.remove(Move.TOP)
        elif axis_0 == 4:
            acceptable_slides.remove(Move.BOTTOM)

        if axis_1 == 0:
            acceptable_slides.remove(Move.LEFT)
        elif axis_1 == 4:
            acceptable_slides.remove(Move.RIGHT)
        return acceptable_slides

    def slide(self, from_pos: tuple[int, int], slide: Move) -> bool:
        '''Slide the other pieces'''
        if slide not in self.acceptable_slides(from_pos):
            return False  # consider raise ValueError('Invalid argument value')
        axis_0, axis_1 = from_pos
        # np.roll performs a rotation of the element of a 1D ndarray
        if slide == Move.RIGHT:
            self._board[axis_0] = np.roll(self._board[axis_0], -1)
        elif slide == Move.LEFT:
            self._board[axis_0] = np.roll(self._board[axis_0], 1)
        elif slide == Move.BOTTOM:
            self._board[:, axis_1] = np.roll(self._board[:, axis_1], -1)
        elif slide == Move.TOP:
            self._board[:, axis_1] = np.roll(self._board[:, axis_1], 1)
        return True
    
    def get_available_moves(self,player: int) -> list[tuple[tuple[int, int], Move]]:
        available_moves = []
        ALL_INDICES = [0,1,2,3,4]
        BORDER_INDICES = [0,4]
        BORDER_CORNERS = list(product(ALL_INDICES, BORDER_INDICES))
        BORDER_EDGES = list(product(BORDER_INDICES, ALL_INDICES))
        EMPTY_POSITIONS = set(BORDER_CORNERS) | set(BORDER_EDGES)
        IDENTICAL_BOARD_SYMMETRIES = []
        original_board = self.get_board().flatten()
        for sym in ALL_SYMMETRIES:
            board = original_board[sym]
            if (original_board == board).all():
                IDENTICAL_BOARD_SYMMETRIES.append(sym)
        
        while EMPTY_POSITIONS:
            row, col = EMPTY_POSITIONS.pop()
            if self._board[row, col] == -1 or self._board[row, col] == player: 
                for move in self.acceptable_slides((row,col)):
                    available_moves.append(((col, row), move))
            else:
                continue
            index = row * 5 + col
            for sym in IDENTICAL_BOARD_SYMMETRIES:
                idx_pos = sym[index]
                pos = idx_pos // 5, idx_pos % 5
                EMPTY_POSITIONS.discard(pos)
        return available_moves
