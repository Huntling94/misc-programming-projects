import random
import sys
import numpy as np
import math
import copy
import time
from Node import Node
from Board import Board
from queue import PriorityQueue


def generate_puzzle(x: int=3, y: int=3):
    board = []
    for i in range(x*y):
        board.append(i)
    random.shuffle(board)
    return np.reshape(board, (x, y))


def manhattan_distance(src: tuple, dest: tuple):
    assert(len(src) == len(dest) == 2)
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

def a_star(node: Node):
    time_start = time.time()
    pqueue = PriorityQueue(0)
    visited = set()
    pqueue.put(node)
    num_dequeued = 1

    
    cheapest = None
    while not pqueue.empty():
        node = pqueue.get()
        num_dequeued += 1
        if node.state.goal_state():
            print("Done")
            cheapest = node

            break
            if cheapest == None:
                cheapest = node
            elif node.path_cost < cheapest.path_cost:
                cheapest = node
        if node.state.hash() not in visited:
            visited.add(node.state.hash())

        possible_states = node.get_possible_nodes()
        for frontier in possible_states:
            if frontier.state.hash() not in visited:
                pqueue.put(frontier)
                visited.add(frontier.state.hash())
    print(f"Time taken: {round(time.time() - time_start, 2)} seconds", file=sys.stderr)
    print(f"Number of nodes dequeued: {num_dequeued}", file=sys.stderr)
    path = []
    if cheapest == None:
        print("No Path")
        
        return []
    while cheapest.parent != None:
        path.append(cheapest.action)
        cheapest = cheapest.parent
    path.reverse()
    path.append((node.state.num_rows-1, node.state.num_columns-1))
    path.pop(0)
    return path
            

            



    

def bfs(node: Node):
    time_start = time.time()
    possible_states = node.get_possible_nodes()
    queue = []
    visited = set()
    queue.append(node)
    visited.add(node.state.hash())
    #for node in possible_states:
    #    visited.add(node.state.hash())
    #queue.append(possible_states.pop(0))
    
    num_dequeued = 0
    path_costs = []
    ret = None
    while queue:
        node = queue.pop(0)
        num_dequeued += 1
        if node.path_cost not in path_costs:
            path_costs.append(node.path_cost)
            print(f"Level: {node.path_cost}", file=sys.stderr)
        if node.state.goal_state():
            print(f"Visited states: {len(visited)}", file=sys.stderr)
            print(f"Number of nodes dequeued: {num_dequeued}", file=sys.stderr)
            ret = node
            break
        future_states = node.get_possible_nodes()
        for state in future_states:
            if state.state.hash() not in visited:
                queue.append(state)
                visited.add(state.state.hash())
    print(f"Time taken: {round(time.time() - time_start, 2)} seconds", file=sys.stderr)
    path = []
    if ret == None:
       
        return []
    while ret.parent != None:
        path.append(ret.action)
        ret = ret.parent
    path.reverse()
    path.append((node.state.num_rows-1, node.state.num_columns-1))
    path.pop(0)
    return path
                
    print(f"Visited states: {len(visited)}", file=sys.stderr)
    print(f"Number of nodes dequeued: {num_dequeued}", file=sys.stderr)
    print(f"Time taken: {round(time.time() - time_start, 2)} seconds", file=sys.stderr)
    
def print_output(initial_board: Node, path: list):
    board_start = initial_board.state
    print(len(path), path)

    print(f"Initial board state")
    print(board_start)
    for move in path:
        print(f"Apply move: {move}")
        board_start.apply_move(move)
        print(board_start)

def get_correct_position_for_number(number: int, board: Board):
    assert(number >= 0 and number < board.num_columns * board.num_rows)
    if number == 0:
        return (board.num_rows-1, board.num_columns-1)
    return ((number - 1)//board.num_columns, (number-1)%board.num_columns)

def distance_from(src: tuple, dest: tuple, function=manhattan_distance):
    return function(src, dest)

def main():
    num_rows = 3
    num_cols = 3
    node = Node(generate_puzzle(num_rows, num_cols))
    print(node)
    print("Distance from goal state:", node.state.distance_from_goal_state(manhattan_distance))
    path = a_star(node)
    print_output(copy.deepcopy(node), path)
    path = bfs(node)
    print_output(copy.deepcopy(node), path)
    """
    path = bfs(node)
    if path == []:
        print("No Path")
    else:
        print_output(node, path)
    """
    return 0

if __name__ == "__main__":
    sys.exit(main())
