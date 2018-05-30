import chess
import sys
import pieceValue as pv
import traceback
# import hashTable as ht


class ChessAIDemo:
    def __init__(self, depth = 3, color = 'w'):
        """
        初始化搜索深度以及AI执棋颜色
        初始化置换表
            param：
                depth: 搜索深度
                color: 执棋颜色(白先黑后)
        """
        self.color = color
        self.searchDepth = int(depth)
        self.board = chess.Board()
        # self.hashTable = ht.HashTable(1024*1024)
        # self.hashTable.CalculateInitHashKey()

    def InitColor(self, color):
        if (color == "white"):
            self.color = 'w'
        elif (color == "black"):
            self.color = 'b'
        else:
            self.color = 'w'

    def evaluateBoard(self, fenStr) -> float:
        """
        局面评估
        color: 己方颜色
        """
        board = self.replace_tags_board(fenStr)
        totalEval = 0.0

        for y in range(8):
            for x in range(8):
                totalEval += self.getPieceValue(board[y][x], x, y)

        return totalEval

    def getPieceValue(self, piece, x, y) -> float:
        """
        根据棋子的类型以及位置返回评估值
        """

        if piece == 1:
            return 0

        absoluteValue = 0
        if piece.islower():  # black
            if piece == 'p':
                absoluteValue = 10 + pv.pawnEvalBlack[y][x]
            elif piece == 'r':
                absoluteValue = 50 + pv.rookEvalBlack[y][x]
            elif piece == 'n':
                absoluteValue = 30 + pv.knightEval[y][x]
            elif piece == 'b':
                absoluteValue = 30 + pv.bishopEvalBlack[y][x]
            elif piece == 'q':
                absoluteValue = 90 + pv.queenEval[y][x]
            elif piece == 'k':
                absoluteValue = 900 + pv.kingEvalBlack[y][x]

            if (self.color == 'w'):
                return -absoluteValue
            else:
                return absoluteValue
        else:  # white
            if piece == 'P':
                absoluteValue = 10 + pv.pawnEvalWhite[y][x]
            elif piece == 'R':
                absoluteValue = 50 + pv.rookEvalWhite[y][x]
            elif piece == 'N':
                absoluteValue = 30 + pv.knightEval[y][x]
            elif piece == 'B':
                absoluteValue = 30 + pv.bishopEvalWhite[y][x]
            elif piece == 'Q':
                absoluteValue = 90 + pv.queenEval[y][x]
            elif piece == 'K':
                absoluteValue = 900 + pv.kingEvalWhite[y][x]

            if (self.color == 'w'):
                return absoluteValue
            else:
                return -absoluteValue

    def expand(self, depth, isMax, alpha, beta):
        """
        扩展节点，返回评估值
        """

        if depth == 0:
            return self.evaluateBoard(self.board.fen())

        if isMax:
            current = -9999
            value = -9999
            for index, newMove in enumerate(self.board.legal_moves):
                self.board.push(newMove)
                if (index == 0):
                    current = self.expand(depth - 1, not isMax, alpha,
                                          beta)
                else:
                    value = max(value,
                                self.expand(depth - 1, not isMax, alpha,
                                            alpha + 1))
                    if (value > alpha and value < beta):
                        value = max(value,
                                    self.expand(depth - 1, not isMax,
                                                alpha, beta))
                self.board.pop()
                current = max(current, value)
                alpha = max(alpha, value)
                if (alpha >= beta):
                    break
        else:
            value = 9999
            current = 9999
            for index, newMove in enumerate(self.board.legal_moves):
                self.board.push(newMove)
                if (index == 0):
                    current = self.expand(depth - 1, not isMax, alpha, beta)
                else:
                    value = min(value,
                                self.expand(depth - 1, not isMax, beta - 1, beta))
                    if (value > alpha and value < beta):
                        value = min(value, self.expand(depth - 1, not isMax, alpha, beta))
                self.board.pop()
                current = min(current, value)
                beta = min(beta, value)
                if (alpha >= beta):
                    break
        return current

    def getBestMove(self, isMax):
        """
        用minmax遍历，返回最优移动uci
        """

        bestValue = -9999
        for newMove in self.board.legal_moves:
            self.board.push(newMove)
            tempValue = self.expand(self.searchDepth - 1, not isMax, -10000, 10000)
            if bestValue < tempValue:
                bestMove = newMove
                bestValue = tempValue
            self.board.pop()

        return bestMove

    def replace_tags_board(self, fenStr) -> list:
        fenStr = fenStr.split(" ")[0]
        fenStr = fenStr.replace("2", "11")
        fenStr = fenStr.replace("3", "111")
        fenStr = fenStr.replace("4", "1111")
        fenStr = fenStr.replace("5", "11111")
        fenStr = fenStr.replace("6", "111111")
        fenStr = fenStr.replace("7", "1111111")
        fenStr = fenStr.replace("8", "11111111")
        return fenStr.split('/')

    def is_white_turn(self, fenStr) -> bool:
        return fenStr.split(" ")[1] == 'w'

    def GameStart(self):
        sys.stderr.write("Link Start!\n")
        raw_color = sys.stdin.readline()[:-1]
        self.InitColor(raw_color)

        while True:
            if (self.color == 'w'):
                AIMove = self.getBestMove(True)
                AIout = self.board.san(AIMove)
                self.board.push(AIMove)
                print(AIout)

            while True:
                sys.stderr.write("当前搜索层数：{}层\n".format(self.searchDepth))
                AnothersideInput = sys.stdin.readline()[:-1]
                if AnothersideInput == 'exit':
                    sys.exit('goodbye^_^\n')
                else:
                    self.board.push_san(AnothersideInput)
                    break

            if (self.color == 'b'):
                AIMove = self.getBestMove(True)
                AIout = self.board.san(AIMove)
                self.board.push(AIMove)
                print(AIout)

    def ManualGame(self):
        sys.stderr.write("please input the chess color\n")
        raw_color = sys.stdin.readline()[:-1]
        self.InitColor(raw_color)
        while self.board.is_game_over() is False:
            if (self.color == 'w'):
                AIMove = self.getBestMove(True)
                self.board.push(AIMove)
                print("AI:")
                print(self.board)

            while True:
                playerInput = input("\nplease input moves（eg.a1b2 exit退出）：")
                if playerInput == 'exit':
                    sys.exit('goodbye^_^\n')
                playerMove = chess.Move.from_uci(playerInput)
                if playerMove in self.board.legal_moves:
                    break
                else:
                    print("input illegal")
            self.board.push(playerMove)

            print("Player:")
            print(self.board)

            if (self.color == 'b'):
                AIMove = self.getBestMove(True)
                self.board.push(AIMove)
                print("AI:")
                print(self.board)


"""
程序入口
"""

if __name__ == '__main__':

    try:
        AIDEMO = ChessAIDemo()
        AIDEMO.GameStart()
        #AIDEMO.ManualGame()
    except:

        filename = "error.txt"
        file_object = open(filename, 'w')
        file_object.write(traceback.format_exc())
        file_object.close()
