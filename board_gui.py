import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui
from game_logic import *
from gobang_naive_ai import *


class GameBoard(QWidget):
    def __init__(self, board_size=15):
        super().__init__()
        self.title = 'GoBang'
        self.resize(850, 850)
        self.setWindowTitle(self.title)
        self.board_size = board_size
        self.step = min(self.height(), self.width()) / (self.board_size+1)
        self.game = GoBangLogic(width=board_size, height=board_size)
        self.player_score = None
        self.ai_score = None
        self.last_u = None
        self.last_v = None
        self.ai = GobangAi()
        self.game.start_a_game()
        self.score_display_toggle = 0
        # u, v, self.ai_score, self.player_score = self.ai.ai_move(self.game.board, -1, -1)
        # self.game.move_a_piece(u, v)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.drawBackground(painter)
        self.drawBoard(painter)

    def keyPressEvent(self, keyPressEvent):
        key = chr(keyPressEvent.key())
        if key == 'r' or key == 'R':
            self.game = GoBangLogic()
            self.ai = GobangAi()
            self.ai_score = None
            self.player_score = None
            self.last_u = None
            self.last_v = None
            self.game.start_a_game()
        if key == 'd' or key == 'D':
            self.score_display_toggle += 1
            self.score_display_toggle = self.score_display_toggle % 3
        self.update()

    def drawBackground(self, painter):
        painter.setBrush(QtGui.QBrush(QtGui.QColor(128, 128, 128)))
        painter.drawRect(0, 0, self.width(), self.height())

    def drawBoard(self, painter):
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        for i in range(self.board_size):
            painter.drawLine((i+1) * self.step, self.step, (i+1) * self.step, self.board_size * self.step)
            painter.drawLine(self.step, (i+1)*self.step, self.board_size*self.step, (i+1)*self.step)
            painter.drawText((i+1)*self.step-5, self.step-5, str(i+1))
            painter.drawText(self.step-10, (i+1)*self.step+5, chr(ord('A')+i))

        for row, eles in enumerate(self.game.board):
            for col, ele in enumerate(eles):
                if ele == Piece_Empty:
                    continue
                elif ele == Piece_Black:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
                elif ele == Piece_White:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
                painter.drawEllipse((col+0.5) * self.step, (row+0.5) * self.step, self.step, self.step)
                if self.last_u == row and self.last_v == col:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
                    painter.drawEllipse((col + 0.75) * self.step, (row + 0.75) * self.step, self.step / 2, self.step / 2)

        if self.score_display_toggle == 1:
            score_board = self.player_score
            color = (255, 0, 0)
        elif self.score_display_toggle == 2:
            score_board = self.ai_score
            color = (0, 255, 0)
        else:
            score_board = None
        if not score_board:
            return
        for row, line in enumerate(score_board):
            for col, score in enumerate(line):
                if self.game.board[row][col] != Piece_Empty:
                    continue
                alpha = min(255, score / 5000 * 255)
                painter.setBrush(QtGui.QBrush(QtGui.QColor(*color, alpha)))
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
                painter.drawEllipse((col + 0.5) * self.step, (row + 0.5) * self.step, self.step, self.step)
                painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
                painter.drawText((col + 0.8) * self.step, (row + 1) * self.step, '{}'.format(score))

    def mousePressEvent(self, QMouseEvent):
        x = QMouseEvent.x()
        y = QMouseEvent.y()

        row = int(round(y / self.step)) - 1
        col = int(round(x / self.step)) - 1
        if self.game.move_a_piece(row, col):
            self.last_u, self.last_v, self.ai_score, self.player_score = self.ai.ai_move(self.game.board, row, col)
            self.game.move_a_piece(self.last_u, self.last_v)
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameBoard()
    ex.show()
    sys.exit(app.exec_())
