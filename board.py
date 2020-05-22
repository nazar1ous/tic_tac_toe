from task_3_tic_tac_toe.btree import LinkedBinaryTree
from task_3_tic_tac_toe.btnode import BNode
from copy import deepcopy
import random as rd


class InvalidMovement(Exception):
    """Represent a invalid move exception"""
    pass


class Board:
    """Represent a board"""
    movement_symbols = ['X', 'O']

    def __init__(self, board=None):
        """Initialize the board"""
        if board is not None:
            self._board = board
        else:
            self._board = [[None for i in range(3)] for j in range(3)]
        self._last_move_position = None
        self._last_move_symbol = None
        self._result = None

    def last_move_position(self):
        """Get last move position"""
        return self._last_move_position

    def last_move_symbol(self):
        """Get last move symbol"""
        return self._last_move_symbol

    def __str__(self):
        """Return string representation of a board"""
        str_value = ''
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j] is None:
                    str_value += '-'
                else:
                    str_value += self._board[i][j]
                str_value += ' '
            str_value = str_value[:-1] + '\n'
        return str_value[:-1]

    def make_movement(self, symbol, position):
        """Make move"""
        if self.is_valid(position):
            self._board[position[0]][position[1]] = symbol
            self._last_move_position = position
            self._last_move_symbol = symbol
        else:
            raise InvalidMovement

    def is_valid(self, position):
        """Check whether the position is valid"""
        i, j = position
        if 0 <= i < 3 and 0 <= j < 3:
            if self._board[i][j] is None:
                return True
            else:
                return False
        else:
            return False

    def is_win(self):
        """Check whether the current state of the board has winning combination,
        if it has, return the winning symbol"""
        for i in range(len(self._board)):
            value = self._board[i][0]
            coin = 0
            for j in range(1, len(self._board[0])):
                if value == self._board[i][j] and value is not None:
                    coin += 1
            if coin == 2:
                return value
        for j in range(len(self._board[0])):
            value = self._board[0][j]
            coin = 0
            for i in range(1, len(self._board)):
                if value == self._board[i][j] and value is not None:
                    coin += 1
            if coin == 2:
                return value

        if self._board[0][0] == self._board[1][1] == self._board[2][2]\
                and self._board[0][0] is not None:
            return self._board[0][0]
        if self._board[2][0] == self._board[1][1] == self._board[0][2]\
                and self._board[1][1] is not None:
            return self._board[2][0]

        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j] is None:
                    return False
        return 'tie'

    def possible_moves(self):
        """Get two possible moves from the current state of a board"""
        moves = []
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j] is None:
                    moves.append((i, j))
        rd.shuffle(moves)
        return moves[:2]

    @staticmethod
    def another_symbol(symbol):
        """Get another symbol of a board"""
        symbols = ['X', 'O']
        if symbol == 'O':
            return 'X'
        else:
            return 'O'

    def graph_from_state(self, maximize_symbol='X'):
        """Return a graph representation of a board"""

        # implementing minmax idea
        def minmax(node):
            n_board = node.data
            moves = n_board.possible_moves()
            boards = [deepcopy(n_board) for i in range(len(moves))]
            if n_board.last_move_symbol() == maximize_symbol:
                move_symbol = Board.another_symbol(maximize_symbol)
            else:
                move_symbol = maximize_symbol
            for i in range(len(boards)):
                _board = boards[i]
                move = moves[i]
                _board.make_movement(move_symbol, move)

                if _board.is_win() == 'tie':
                    b_res = 0
                elif _board.is_win() == maximize_symbol:
                    b_res = 1
                elif _board.is_win() == Board.another_symbol(maximize_symbol):
                    b_res = -1
                else:
                    b_res = minmax(BNode(_board))
                if move_symbol != maximize_symbol:
                    b_res = -1 * b_res
                _board._result = b_res
            if len(boards) == 1:
                LinkedBinaryTree.add_children(node, boards[0])
                return boards[0]._result
            else:
                board1, board2 = boards

                if board1._result <= board2._result:
                    LinkedBinaryTree.add_children(node, board1, board2)
                else:
                    LinkedBinaryTree.add_children(node, board2, board1)
                if move_symbol != maximize_symbol:
                    return min(board1._result, board1._result)
                else:
                    return max(board1._result, board2._result)
        board = Board(deepcopy(self._board))
        node = BNode(board)
        tree = LinkedBinaryTree(node)
        minmax(node)
        return tree

    def make_decision(self):
        """Make the most preferable decision from two moves"""
        max_symbol = Board.another_symbol(self._last_move_symbol)
        max_tree = self.graph_from_state(max_symbol)
        return max_tree._root.right.data._last_move_position



