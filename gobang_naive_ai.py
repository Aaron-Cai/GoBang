from global_constans import *
from game_logic import GoBangLogic
import utility

class Gobang_Ai:
    def __init__(self, choose=Piece_White, width=15, height=15):
        self.choose = choose
        self.width=width
        self.height=height
        self.init_winning_array()

    def init_winning_array(self):
        self.winning_array = []
        for row in range(self.height):
            for col in range(self.width-4):
                board = utility.init_board(self.width, self.height)
                for i in range(5):
                    board[row][col+i] = True
                self.winning_array.append(board)
        for row in range(self.height-4):
            for col in range(self.width):
                board = utility.init_board(self.width, self.height)
                for i in range(5):
                    board[row+i][col] = True
                self.winning_array.append(board)
        for row in range(self.height-4):
            for col in range(self.width-4):
                board = utility.init_board(self.width, self.height)
                for i in range(5):
                    board[row+i][col+i] = True
                self.winning_array.append(board)
        for row in range(self.height-4):
            for col in range(4, self.width):
                board = utility.init_board(self.width, self.height)
                for i in range(5):
                    board[row+i][col-i] = True
                self.winning_array.append(board)
        self.my_winning_cnt = [0] * len(self.winning_array)
        self.opp_winning_cnt = [0] * len(self.winning_array)

    def ai_move(self, current_board, last_r, last_c):
        # analyze board situation
        if last_r == -1 and last_c == -1:
            return int(self.height/2), int(self.width/2), None, None
        for k in range(len(self.winning_array)):
            if self.winning_array[k][last_r][last_c]:
                self.opp_winning_cnt[k]+=1
                self.my_winning_cnt[k]=0
        # find a best move
        my_score = [[0] * self.width for i in [0] * self.height]
        opp_score = [[0] * self.width for i in [0] * self.height]
        my_score_get = [0, 220, 420, 2100, 20000]
        opp_score_get = [0, 200, 400, 2000, 10000]
        max_score = 0
        u, v = -1, -1
        for row in range(self.height):
            for col in range(self.width):
                if current_board[row][col] == Piece_Empty:
                    for k in range(len(self.winning_array)):
                        if self.winning_array[k][row][col]:
                            my_score[row][col] += my_score_get[self.my_winning_cnt[k]]
                            opp_score[row][col] += opp_score_get[self.opp_winning_cnt[k]]
                    if opp_score[row][col] > max_score:
                        max_score = opp_score[row][col]
                        u, v = row, col
                    elif opp_score[row][col] == max_score:
                        if my_score[row][col] > opp_score[u][v]:
                            u, v = row, col
                    if my_score[row][col] > max_score:
                        max_score = my_score[row][col]
                        u, v = row, col
                    elif my_score[row][col] == max_score:
                        if opp_score[row][col] > my_score[u][v]:
                            u, v = row, col
        return u, v, my_score, opp_score

def main():
    game = GoBangLogic()
    game.start_a_game()
    ai = Gobang_Ai()
    # ai_black = Gobang_Ai()
    # ai_white = Gobang_Ai()
    # u, v = -1, -1
    # while game.status != Black_Win and game.status != White_Win:
    #     u, v, _, _ = ai_black.ai_move(game.board, u, v)
    #     game.move_a_piece(u, v)
    #     u, v, _, _ = ai_white.ai_move(game.board, u, v)
    #     game.move_a_piece(u, v)

    game.move_a_piece(7, 7)
    u, v ,ai_score, player_score = ai.ai_move(game.board, 7, 7)
    utility.display_board_score(ai_score, 15, 15)
    utility.display_board_score(player_score, 15, 15)
    game.move_a_piece(u, v)
    print('====================================================\n')

    game.move_a_piece(6, 7)
    u, v, ai_score, player_score = ai.ai_move(game.board, 6, 7)
    utility.display_board_score(ai_score, 15, 15)
    utility.display_board_score(player_score, 15, 15)
    game.move_a_piece(u, v)
    print('====================================================\n')





if __name__ == '__main__':
    main()
