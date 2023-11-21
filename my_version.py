from random import randint
from time import sleep

class Conway:
    def __init__(self, chunk_width=10, chunk_height=10):
        self.board = Board(chunk_width, chunk_height)
        for x in range(-1, 3):
            for y in range(-1, 3):
                self.board.add_chunk(x, y)
        
        # draw a glider
        self.board.set_chunk(1, -1, int_matrix_to_cell_matrix([ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
        self.board.set_chunk(1, 0,  int_matrix_to_cell_matrix([ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 1, 0, 1, 1, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
        self.board.set_chunk(1, 1,  int_matrix_to_cell_matrix([ [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
        self.board.set_chunk(1, 2,  int_matrix_to_cell_matrix([ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
        
    def iterate_chunks(self):
        new_chunks = []
        for c in self.board.get_chunks():
            new_chunks.append((c['x'], c['y'], c['chunk'].iterate(self.board)))
        for c in new_chunks:
            self.board.set_chunk(c[0], c[1], c[2])
    
    def print_chunks(self):
        whole_board = self.board.combine_all_chunks()
        print('┌' + '─' * len(whole_board[0]) * len(Cell.EMPTY)  + '┐')
        for i, row in enumerate(whole_board):
            print('│', end='')
            
            for cell in row:
                print(cell.get_state_letter(), end='')
            
            print('│', end='')
            print()
        print('└' + '─' * len(whole_board[0]) * len(Cell.EMPTY) + '┘')
        
def int_matrix_to_cell_matrix(matrix):
    return [[Cell(x) for x in row] for row in matrix]


class Board:
    def __init__(self, chunk_width, chunk_height):
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.chunks = []

    def add_chunk(self, x, y):
        self.chunks.append({
            'chunk': Chunk(x, y, Chunk.empty_chunk(self.chunk_width, self.chunk_height)),
            'x': x,
            'y': y,
        })
    def set_chunk(self, x, y, new_contents):
        for c in self.chunks:
            if c['x'] == x and c['y'] == y:
                c['chunk'].set_contents(new_contents)
    def get_chunk_size(self):
        return self.chunk_width, self.chunk_height
    def get_chunks(self):
        return self.chunks
    def combine_all_chunks(self):
        min_x, max_x, min_y, max_y = self.get_bounds()
        whole = Chunk.empty_chunk((max_x - min_x + 1) * self.chunk_width, (max_y - min_y + 1) * self.chunk_height)
        for c in self.chunks:
            for x in range(self.chunk_width):
                for y in range(self.chunk_height):
                    whole[(c['x'] - min_x) * self.chunk_width + x][(c['y'] - min_y) * self.chunk_height + y] = c['chunk'].get_cell(x, y)
        return whole
    def get_bounds(self):
        # requires chunk at (0, 0)
        min_x, max_x, min_y, max_y = [0]*4
        for c in self.chunks:
            min_x = min(min_x, c['x'])
            max_x = max(max_x, c['x'])
            min_y = min(min_y, c['y'])
            max_y = max(max_y, c['y'])
        return min_x, max_x, min_y, max_y
    def get_chunk_at(self, x, y):
        for c in self.chunks:
            if c['x'] == x and c['y'] == y:
                return c['chunk']
        return Chunk(x, y, Chunk.empty_chunk(self.chunk_width, self.chunk_height))

class Chunk:
    B = [3]
    S = [2, 3]
    def __init__(self, x, y, contents=None, width=None, height=None):
        self.x = x
        self.y = y
        self.width = len(contents)
        self.height = len(contents[0])
        self.contents = contents

    def get_contents(self):
        return self.contents
    def get_cell(self, x, y):
        return self.contents[x][y]
    def set_contents(self, new_contents):
        self.contents = new_contents
    def clear_contents(self): # technically unnecessary, but a nice addition
        self.contents = Chunk.empty_chunk(self.width, self.height)
    def set_random_contents(self):
        self.contents = Chunk.random_chunk(self.width, self.height)
    
    def iterate(self, board):
        new_state = Chunk.empty_chunk(self.width, self.height)
        for x in range(len(self.contents)):
            for y in range(len(self.contents[x])):
                neighbours = [self.get_value(*coord, board).get_state() for coord in Chunk.neighbour_coords(x, y)]
                total = sum(neighbours)
                if self.contents[x][y].get_state():
                    new_state[x][y] = Cell(1) if total in Chunk.S else Cell(0)
                else:
                    new_state[x][y] = Cell(1) if total in Chunk.B else Cell(0)
        return new_state

    def get_value(self, x, y, board):
        # clumsily written but it works
        if x < 0:
            if y < 0:
                return board.get_chunk_at(self.x - 1, self.y - 1).get_cell(-1, -1)
            if y >= self.height:
                return board.get_chunk_at(self.x - 1, self.y + 1).get_cell(-1, 0)
            return board.get_chunk_at(self.x - 1, self.y).get_cell(-1, y)
        if x >= self.width:
            if y < 0:
                return board.get_chunk_at(self.x + 1, self.y - 1).get_cell(0, -1)
            elif y >= self.height:
                return board.get_chunk_at(self.x + 1, self.y + 1).get_cell(0, 0)
            return board.get_chunk_at(self.x + 1, self.y).get_cell(0, y)
        if y < 0:
            return board.get_chunk_at(self.x, self.y - 1).get_cell(x, -1)
        if y >= self.height:
            return board.get_chunk_at(self.x, self.y + 1).get_cell(x, 0)
        return self.contents[x][y]

    @staticmethod
    def empty_chunk(width, height):
        return [[Cell(0) for i in range(height)] for j in range(width)]
    @staticmethod
    def random_chunk(width, height):
        return [[Cell(randint(0, 1)) for i in range(height)] for j in range(width)]
    @staticmethod
    def neighbour_coords(x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j and i == 0:
                    continue
                yield (x + i, y + j)

class Cell:
    FILLED = '██'
    EMPTY = '  '
    def __init__(self, state:int):
        self.state = state
    def set_state(self, new_state):
        self.state = new_state
    def get_state(self):
        return self.state
    def get_state_letter(self):
        # use unicode block
        return Cell.FILLED if self.state else Cell.EMPTY
    def toggle_state(self):
        self.state = 1 - self.state


if __name__ == '__main__':
    conway = Conway()
    conway.print_chunks()
    while True:
        conway.iterate_chunks()
        conway.print_chunks()
        sleep(0.2)