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
        self.game = GoBangLogic()
        self.ai = Gobang_Ai()
        self.game.start_a_game()

    def paintEvent(self, QPaintEvent):
        print('repaint')
        painter = QtGui.QPainter(self)
        self.drawBackground(painter)
        self.drawBoard(painter)

    def keyPressEvent(self, keyPressEvent):
        key = chr(keyPressEvent.key())
        if key=='r' or key=='R':
            self.game = GoBangLogic()
            self.ai = Gobang_Ai()
            self.game.start_a_game()
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

        board = self.game.board
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

    def mousePressEvent(self, QMouseEvent):
        x = QMouseEvent.x()
        y = QMouseEvent.y()

        row = int(round(y / self.step)) - 1
        col = int(round(x / self.step)) - 1
        if self.game.move_a_piece(row, col):
            u, v, ai_score, player_score = self.ai.ai_move(self.game.board, row, col)
            self.game.move_a_piece(u, v)
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameBoard()
    ex.show()
    sys.exit(app.exec_())