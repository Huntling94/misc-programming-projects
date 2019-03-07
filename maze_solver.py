import matplotlib.pyplot as plt
import numpy as np
import math
import queue

class Maze():
    num_grids: int
    num_rowscols: int
    num_blockade: int
    start = (0, 0)
    end: tuple
    maze: np.array
    
    def __init__(self, num_grids: int, percent_blocked: float):
        if percent_blocked > 1:
            percent_blocked / 100
        
        self.maze = random_maze(num_grids, percent_blocked)
        self.num_rowscols = len(self.maze)
        self.num_grids = len(self.maze)**2
        self.num_blockade = np.sum(self.maze)
        self.end = (self.num_rowscols-1, self.num_rowscols-1)
    
    def __len__():
        return len(self.maze)^2
    
    def show_maze(self):
        plt.matshow(self.maze, cmap=plt.cm.gray_r)
        plt.show()
    
    def get_node_index(self, position: tuple) -> int:
        """
        Returns node number of entry

        Arguments:
        position: tuple, (int, int)

        Returns:
        integer, the node number of the entry into the maze
        """
        i, j = position
        return self.num_rowscols*i + j
    
    def is_occupied(self, position: tuple) -> bool:
        """
        Returns whether a particular position in the maze is occupied.
        A position can be occupied by being out of bounds, or blockaded.

        Arguments:
        position: tuple, (int, int)

        Returns:
        True if position is blockaded. False otherwise.
        """
        if position[0] >= self.num_rowscols or position[0] < 0:
            return True
        elif position[1] >= self.num_rowscols or position[1] < 0:
            return True
        else:
            return bool(self.maze[position[0], position[1]])
        
    def possible_paths(self, position: tuple) -> list:
        """
        Returns a list of the immediate possible paths that can be taken
        from the position.

        Arguments:
        position: tuple, (int, int)

        Returns:
        list of possible paths (an empty list means no possible paths).
        """
        paths = []
        i, j = position
        if not self.is_occupied((i+1, j)):
            paths.append((i+1, j))
        if not self.is_occupied((i-1, j)):
            paths.append((i-1, j))
        if not self.is_occupied((i, j+1)):
            paths.append((i, j+1))
        if not self.is_occupied((i, j-1)):
            paths.append((i, j-1))
        return paths
    
    def bfs(self, add_trail: bool=True) -> list:
        """
        Treats each entry as a node, and its immediate accessible path,
        (up, down, left, right) as vertices between nodes. Performs breadth
        first search on this graph until the queue empties without reaching
        end, or until end is reached.

        Arguments:
        add_trail: bool (default True)

        Returns:
        list of the steps to take from start to end if the end can be reached
        otherwise an empty list.
        """
        q = queue.Queue(self.num_grids)
        q.put(self.start)
        visited = {}
        visited[self.start] = 1
        backtrack = [0] * self.num_grids
        failed = True
        while(not q.empty()):
            current = q.get()
            if (current == self.end):
                failed = False
                break
                
            possible = self.possible_paths(current)
            for path in possible:
                if path not in visited:
                    q.put(path)
                    visited[path] = 1
                    backtrack[self.get_node_index(path)] = current
        if failed:
            print(f"No path out of the maze from {self.start} ==> {self.end}")
            return []
                    
        prev = backtrack[self.get_node_index(self.end)]
        track = [self.end]
        
        while prev != self.start:
            track.append(prev)
            i, j = prev
            prev = backtrack[self.get_node_index(prev)]
            
        track.append(self.start)
        track.reverse()
        if add_trail:
            for path in track:
                i, j = path
                self.maze[i][j] = 1
        return track

def random_maze(num_grids: int=100, percent_blocked: float=0.3) -> np.array:
    """
    Creates a random maze with some blockades. It is assumed that the
    start and end positions at the top left and bottom right of the maze
    respectively.

    Arguments:
    num_grids: int, number of entries in the maze (maze is square)
    percent_blocked: float, percent of maze blockaded

    Returns:
    np.array, with entries set to 0 as walkable paths, and 2 as blockades
    """
    while(percent_blocked > 1):
        percent_blocked /= 100
    
    num_blockade = int(num_grids * percent_blocked)
    
    grid_rows = int(math.sqrt(num_grids))
    maze = np.zeros((grid_rows, grid_rows))
    
    potential_blockades = [(x, y) for x in range(grid_rows)
                                  for y in range(grid_rows)]
    np.random.shuffle(potential_blockades)
    for index, tup in enumerate(potential_blockades):
        if (tup == (0, 0) or tup == (grid_rows-1, grid_rows-1)):
            num_blockade += 1
            continue
        if index >= num_blockade:
            break
        maze[tup[0], tup[1]] = 2
    return maze

def main():
    test = Maze(1000, 0.3)
    test.show_maze()
    track = test.bfs()
    if(track):
        test.show_maze()

if __name__ == "__main__":
    main()

