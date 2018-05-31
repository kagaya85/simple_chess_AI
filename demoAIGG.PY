import chess

import sys

import pieceValue as pv

import traceback

import hashTable as ht

import historyHeuristics as hh



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

        self.hashTable = ht.HashTable(1024*1024)

        self.hashTable.CalculateInitHashKey()

        self.historyHeuristics = hh.HistoryHeuristics()



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



    def expand(self, depth,isMax, alpha, beta):

        """

        扩展节点，返回评估值

        """

        val = self.hashTable.SearchHashTable(depth, alpha, beta, isMax)

        if val != 114514:

            return val



        if depth == 0 or self.board.is_game_over():

            val=self.evaluateBoard(self.board.fen())

            self.hashTable.InsertHashTable(depth, val, isMax, ht.HashExact)

            return val



        moveArr = list()

        for move in self.board.legal_moves:

            moveArr.append(move)



        self.historyHeuristics.moveSort(moveArr, moveArr.__len__, True)

        bestMove = moveArr[0]

        eval_is_exact = False

        if isMax:

            current = -9999

            value = -9999

            for index, newMove in enumerate(moveArr):

                self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)

                self.board.push(newMove)

                if (index == 0):

                    current = self.expand(depth - 1,not isMax, alpha,

                                          beta)

                else:

                    value = max(value,

                                self.expand(depth - 1, not isMax, alpha,

                                            alpha + 1))

                    if (value > alpha and value < beta):

                        eval_is_exact = True

                        value = max(value,

                                    self.expand(depth - 1,  not isMax,

                                                alpha, beta))

                        bestMove = moveArr[index]

                self.board.pop()

                self.hashTable.UndoMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)

                current = max(current, value)

                alpha = max(alpha, value)

                if (alpha >= beta):

                    self.hashTable.InsertHashTable(depth, current, isMax, ht.HashAlpha)

                    self.historyHeuristics.InsertHistoryScore(moveArr[index], depth)

                    return current

        else:

            value = 9999

            current = 9999

            for index, newMove in enumerate(self.board.legal_moves):

                self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)

                self.board.push(newMove)

                if (index == 0):

                    current = self.expand(depth - 1, not isMax, alpha, beta)

                else:

                    value = min(value,

                                self.expand(depth - 1,not isMax, beta - 1, beta))

                    if (value > alpha and value < beta):

                        eval_is_exact = True

                        value = min(value, self.expand(depth - 1,not isMax, alpha, beta))

                self.board.pop()

                self.hashTable.UndoMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)

                current = min(current, value)

                beta = min(beta, value)

                if (alpha >= beta):

                    self.hashTable.InsertHashTable(depth, value, isMax, ht.HashBeta)

                    self.historyHeuristics.InsertHistoryScore(moveArr[index], depth)

                    return current

        self.historyHeuristics.InsertHistoryScore(bestMove, depth)

        if eval_is_exact:

            self.hashTable.InsertHashTable(depth, value, isMax, ht.HashExact)



        return current



    def getBestMove(self, isMax):

        """

        用minmax遍历，返回最优移动uci

        """



        moveArr = list()



        for move in self.board.legal_moves:

            moveArr.append(move)



        self.historyHeuristics.moveSort(moveArr, moveArr.__len__, True)

        bestValue = -9999

        for newMove in moveArr:

            self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)

            self.board.push(newMove)

            tempValue = self.expand(self.searchDepth - 1, not isMax, -10000, 10000)

            if bestValue < tempValue:

                bestMove = newMove

                bestValue = tempValue

            self.board.pop()

            self.hashTable.UndoMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)



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

        self.board = chess.Board()

        sys.stderr.write("please input the chess color\n")

        raw_color = sys.stdin.readline()[:-1]

        self.InitColor(raw_color)



        while True:

            if (self.color == 'w'):

                AIMove = self.getBestMove(True)

                AIout = self.board.san(AIMove)

                self.board.push(AIMove)

                print(AIout)



            while True:

                sys.stderr.write("\nplease input moves（eg.a1b2 exit退出）：")

                AnothersideInput = sys.stdin.readline()[:-1]

                if AnothersideInput == 'exit':

                    sys.exit('goodbye^_^\n')

                else:

                    opponentMove = self.board.parse_san(AnothersideInput)

                    self.hashTable.MakeMove(self.board.piece_at(opponentMove.from_square), self.board.piece_at(opponentMove.to_square), opponentMove)

                    self.board.push_san(AnothersideInput)

                    break



            if (self.color == 'b'):

                AIMove = self.getBestMove(True)

                AIout = self.board.san(AIMove)

                self.board.push(AIMove)

                print(AIout)



    def ManualGame(self):

        self.board = chess.Board()

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



        filename = "C:\\Users\\youyaoyin\\OneDrive\\github-space\\chess_ai\\simple_chess_AI\\error.txt"

        file_object = open(filename, 'w')

        file_object.write(traceback.format_exc())

        file_object.close()