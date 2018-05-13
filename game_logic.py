from global_constans import *
import logging
import utility
class GoBangLogic:
    def __init__(self, width=15, height=15):
        '''
        Init of this class, a typical gobang game usually using 15x15 or 19x19 grid intersections
        :param width: width of grid
        :param height: height of grid
        '''
        self.width = width
        self.height = height
        self.init_board()
        # self.display_board()
        self.movecnt = 0

        self.logicLogger = self.setup_logger('LogicLogger', 'log.log')
        self.moveLogger = self.setup_logger('moveLogger', 'move.log', fmt='%(message)s')
        self.logicLogger.disabled = True
        self.logicLogger.disabled = True

    def setup_logger(self, logger_name, log_file, fmt='%(asctime)s %(name)s %(levelname)s: %(message)s', level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter(fmt)
        fileHandler = logging.FileHandler(log_file)
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler(stream=None)
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)
        l.propagate = False
        return l

    def init_board(self):
        self.board = utility.init_board(self.width, self.height)

    def display_board(self):
        utility.display_board(self.board, self.width, self.height)
        # for i in range(self.width+1):
        #     print(i, '\t', end='')
        # print()
        # for i in range(self.height):
        #     print(i+1, '\t', end='')
        #     for j in range(self.width):
        #         print(Piece_String_Type[self.board[i][j]], '\t', end='')
        #     print(flush=True)

    def start_a_game(self):
        self.init_board()
        self.status = Black_Turn
        self.movecnt = 0
        self.logicLogger.info('New game started')

    def retrieve_five_piece_and_judge(self, row, col, dir='horizontal'):
        '''

        :param dir: horizontal or vertical or slants_down
        :return:
        '''
        if dir == 'horizontal':
            if col + 5 > self.width:
                return False
            five_pieces = [self.board[row][col+i] for i in range(5)]
        elif dir == 'vertical':
            if row + 5 > self.height:
                return False
            five_pieces = [self.board[row+i][col] for i in range(5)]
        elif dir == 'slants_down':
            if row + 5 > self.height or col + 5 > self.width:
                return False
            five_pieces = [self.board[row+i][col+i] for i in range(5)]
        elif dir == 'anti_slants_down':
            if row - 5 > self.height or col + 5 > self.width:
                return False
            five_pieces = [self.board[row-i][col+i] for i in range(5)]
        if len(list(filter(lambda x: x == Piece_Black, five_pieces))) == 5:
            self.status = Black_Win
            self.logicLogger.info('Black win')
            return True
        if len(list(filter(lambda x: x == Piece_White, five_pieces))) == 5:
            self.status = White_Win
            self.logicLogger.info('White win')
            return True
        return False

    def judge(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.retrieve_five_piece_and_judge(row, col, 'horizontal'):
                    return
                if self.retrieve_five_piece_and_judge(row, col, 'vertical'):
                    return
                if self.retrieve_five_piece_and_judge(row, col, 'slants_down'):
                    return
                if self.retrieve_five_piece_and_judge(row, col, 'anti_slants_down'):
                    return

    def switch_turn(self):
        return (self.status+1) % 2
    def move_a_piece(self, row, col):
        if 0<=row and row < self.height and 0<=col and col < self.width:
            if self.status > White_Turn:
                print('Game is over. Try to restart a game')
                self.logicLogger.info('Game is over. Try to restart a game')
                return False
            if self.board[row][col] != Piece_Empty:
                self.logicLogger.warning('Move on an existing piece')
                return False
            self.board[row][col] = Piece_Move[self.status]
            self.moveLogger.info('%d: %d %d', self.movecnt, row, col)
            self.movecnt += 1
            self.display_board()
            self.judge()
            if self.status < Black_Win:
                self.status = self.switch_turn()
            print(Status_Msg[self.status])
            return True
        else:
            self.logicLogger.error('Invalid place to move a piece')
            raise Exception('Invalid place to move a piece.')

def main():
    game = GoBangLogic()
    game.start_a_game()
    # try:
    #     game.move_a_piece(-1, 0)
    # except Exception as exp:
    #     print(exp)
    # game.move_a_piece(7, 7)
    # game.move_a_piece(7, 7)
    # game.move_a_piece(7, 6)
    # game.move_a_piece(6, 6)
    # game.move_a_piece(6, 7)
    # game.move_a_piece(5, 5)
    # game.move_a_piece(5, 7)
    # game.move_a_piece(4, 4)
    # game.move_a_piece(4, 3)
    # game.move_a_piece(3, 3)
    # game.move_a_piece(2, 2)
    #
    # game.start_a_game()
    # game.move_a_piece(7, 8)
    # game.move_a_piece(7, 6)
    # game.move_a_piece(7, 9)
    # game.move_a_piece(7, 5)
    # game.move_a_piece(7, 10)
    # game.move_a_piece(7, 4)
    # game.move_a_piece(7, 11)
    # game.move_a_piece(7, 3)
    # game.move_a_piece(7, 12)
    # game.move_a_piece(7, 2)
    #
    # game.start_a_game()
    # game.move_a_piece(7, 7)
    # game.move_a_piece(7, 6)
    # game.move_a_piece(8, 7)
    # game.move_a_piece(7, 5)
    # game.move_a_piece(9, 7)
    # game.move_a_piece(7, 4)
    # game.move_a_piece(10, 7)
    # game.move_a_piece(7, 3)
    # game.move_a_piece(11, 7)
    # game.move_a_piece(7, 2)

if __name__ == '__main__':
    main()