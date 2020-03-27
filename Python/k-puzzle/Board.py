UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0 , 1)

class Board:
    board = None
    num_rows = 0
    num_columns = 0

    def hash(self):
        ret_str = ""
        for row in self.board:
            for col in row:
                ret_str += str(col)
        return ret_str
    
    def __init__(self, board):
        self.board = board
        self.num_rows = len(board)
        self.num_columns = len(board[0])

    def move(self, position, direction):
        assert(len(position) == 2)
        return position[0] + direction[0], position[1] + direction[1]

    def apply_move(self, position: tuple):
        zero = self.get_zero_position()
        assert(self.is_valid_position(position))
        self.board[zero[0]][zero[1]] = self.get_position(position)
        self.board[position[0]][position[1]] = 0
    
    def get_zero_position(self):
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if self.get_position(i, j) == 0:
                    return (i, j)
    
    def is_valid_position(self, x: int=0, y: int=0):
        if isinstance(x, tuple):
            assert(len(x) == 2)
            return x[0] in range(0, self.num_rows) and x[1] in range(0, self.num_columns)
        return x in range(0, self.num_rows) and y in range(0, self.num_columns)

    def get_position(self, x: int=0, y: int=0):
        if isinstance(x, tuple):
            assert(len(x) == 2)
            if not self.is_valid_position(x[0], x[1]):
                return False
            return self.board[x[0]][x[1]]
        if not self.is_valid_position(x, y):
            return False
        return self.board[x][y]

    def get_number_to_coord(self, number: int):
        assert number >= 0 and number <= self.num_columns * self.num_rows
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if self.get_position(i, j) == number:
                    return (i, j)

    def distance_from_goal_state(self, distance_function):
        distance = 0
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                src = (i, j)
                dest = self.get_correct_position_for_number(self.get_position(i, j))
                distance += distance_function(src, dest)
        return distance

    def get_correct_position_for_number(self, number: int):
        assert(number >= 0 and number < self.num_columns * self.num_rows)
        if number == 0:
            return (self.num_rows-1, self.num_columns-1)
        return ((number - 1)//self.num_columns, (number-1)%self.num_columns)

    def get_possible_moves(self):
        zero_pos = self.get_zero_position()
        moves = [tuple(self.move(zero_pos, LEFT)), tuple(self.move(zero_pos, RIGHT)), tuple(self.move(zero_pos, UP)), tuple(self.move(zero_pos, DOWN))]
        moves = list(filter(lambda x: self.is_valid_position(x) != False, moves))
        return moves

    def goal_state(self):
        cur = 1
        for row in self.board:
            for col in row:
                if col != cur:
                    if cur == self.num_columns * self.num_rows:
                        return True
                    else:
                        return False
                cur += 1    

    def __str__(self):
        str_rep = ""
        for row in self.board:
            for col in row:
                str_rep += f"{col} "
            str_rep += "\n"
        return str_rep

    def __eq__(self, board):
        return self.hash() == board.hash()