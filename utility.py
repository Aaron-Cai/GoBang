from global_constans import *
def init_board(width, height):
    return [[0] * width for i in [0] * height]

def display_board(board, width, height):
    for i in range(width+1):
        print(i, '\t', end='')
    print()
    for i in range(height):
        print(i+1, '\t', end='')
        for j in range(width):
            print(Piece_String_Type[board[i][j]], '\t', end='')
        print(flush=True)

def display_board_score(score, width, height):
    for i in range(width+1):
        print(i, '\t', end='')
    print()
    for i, row in enumerate(score):
        print(i+1, '\t', end='')
        for col in row:
            print(col / 1000, '\t', end='')
        print(flush=True)