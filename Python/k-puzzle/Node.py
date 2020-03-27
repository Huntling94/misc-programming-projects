import copy

from Board import Board

def manhattan_distance(src: tuple, dest: tuple):
    assert(len(src) == len(dest) == 2)
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

class Node:
    state = None
    parent = None
    action = None
    path_cost = 0
    projected_cost = 0

    def __init__(self, board, parent=None, action=None, path_cost=0):
        if isinstance(board, Board):
            self.state = board
        else:
            self.state = Board(board)
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.projected_cost = self.state.distance_from_goal_state(manhattan_distance)

    def __eq__(self, node):
        if node == None:
            return False
        return (self.path_cost + self.projected_cost) == (node.path_cost + node.projected_cost)

    def _lt__(self, node):
        return (self.path_cost + self.projected_cost) < (node.path_cost + node.projected_cost)
    
    def __gt__(self, node):
        return (self.path_cost + self.projected_cost) > (node.path_cost + node.projected_cost)

    def get_possible_nodes(self):
        possible_nodes = []
        possible_moves = self.state.get_possible_moves()
        cost = self.path_cost+1
        projected_cost = self.state.distance_from_goal_state(manhattan_distance)

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
        ret_str += f"Path Cost: {self.path_cost}, "
        ret_str += f"Projected Cost: {self.projected_cost}\n"
        ret_str += f"Total estimated cost to reach goal: {self.path_cost + self.projected_cost}"
        return ret_str
