import copy

from Board import Board

class Node:
    state = None
    parent = None
    action = None
    path_cost = 0

    def __init__(self, board, parent=None, action=None, path_cost=0):
        if isinstance(board, Board):
            self.state = board
        else:
            self.state = Board(board)
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __eq__(self, node):
        if node == None:
            return False
        return self.state == node.state

    def get_possible_nodes(self):
        possible_nodes = []
        possible_moves = self.state.get_possible_moves()
        cost = self.path_cost+1

        for move in possible_moves:
            copy_board = copy.deepcopy(self.state)
            save_move = copy_board.get_zero_position()
            copy_board.apply_move(move)
            

            node = Node(copy_board, self, save_move, cost)
            possible_nodes.append(node)

        return possible_nodes

    def __str__(self):
        ret_str = self.state.__str__()
        ret_str += f"Move from parent: {self.action}\n"
        ret_str += f"Path Cost: {self.path_cost}"
        return ret_str
