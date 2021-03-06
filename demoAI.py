import chess
import sys
import pieceValue as pv
import traceback
import hashTable as ht
import historyHeuristics as hh
import time

class ChessAIDemo:
    def __init__(self, initdepth = 3, color = 'w'):
        """
        初始化搜索深度以及AI执棋颜色
        初始化置换表
            param：
                depth: 搜索深度
                color: 执棋颜色(白先黑后)
        """
        self.color = color
        self.initDepth = int(initdepth)
        self.searchDepth = int(initdepth)
        self.board = chess.Board()
        self.hashTable = ht.HashTable()
        self.hashTable.CalculateInitHashKey()
        self.historyHeuristics = hh.HistoryHeuristics()
        self.startTime = 0
        self.timeOver = True
        self.timeLimit = 3

    def InitColor(self, color):
        if (color == "white"):
            self.color = 'w'
        elif (color == "black"):
            self.color = 'b'
        else:
            self.color = 'w'

    def evaluateBoard(self) -> float:
        """
        局面评估
        param:
            color: 己方颜色
        """
        totalEval = 0.0

        for square in chess.SQUARES:
            totalEval += self.getPieceValue(square)

        return totalEval

    def getPieceValue(self, square) -> float:
        """
        根据棋子的类型以及位置返回评估值
        """
        
        piece = self.board.piece_at(square)
        if piece == None:
            return 0
        
        x = chess.square_file(square)
        y = chess.square_rank(square)

        absoluteValue = 0
        if piece.color == False:  # black
            if piece.piece_type == chess.PAWN:
                absoluteValue = 10 + pv.pawnEvalBlack[y][x]
            elif piece.piece_type == chess.ROOK:
                absoluteValue = 50 + pv.rookEvalBlack[y][x]
            elif piece.piece_type == chess.KNIGHT:
                absoluteValue = 40 + pv.knightEval[y][x]
            elif piece.piece_type == chess.BISHOP:
                absoluteValue = 30 + pv.bishopEvalBlack[y][x]
            elif piece.piece_type == chess.QUEEN:
                absoluteValue = 90 + pv.queenEval[y][x]
            elif piece.piece_type == chess.KING:
                absoluteValue = 900 + pv.kingEvalBlack[y][x]

            if (self.color == 'w'):
                return -absoluteValue
            else:
                return absoluteValue
        else:  # white
            if piece.piece_type == chess.PAWN:
                absoluteValue = 10 + pv.pawnEvalWhite[y][x]
            elif piece.piece_type == chess.ROOK:
                absoluteValue = 50 + pv.rookEvalWhite[y][x]
            elif piece.piece_type == chess.KNIGHT:
                absoluteValue = 40 + pv.knightEval[y][x]
            elif piece.piece_type == chess.BISHOP:
                absoluteValue = 30 + pv.bishopEvalWhite[y][x]
            elif piece.piece_type == chess.QUEEN:
                absoluteValue = 90 + pv.queenEval[y][x]
            elif piece.piece_type == chess.KING:
                absoluteValue = 900 + pv.kingEvalWhite[y][x]

            if (self.color == 'w'):
                return absoluteValue
            else:
                return -absoluteValue

    def expand(self, depth, isMax, alpha, beta):
        """
        扩展节点，返回评估值
        """
        # val = self.hashTable.SearchHashTable(depth, alpha, beta, isMax)
        # if val != 114514:
        #     return val

        if int(time.time()) - self.startTime >= self.timeLimit:
            self.timeOver = True
            depth = 0
        else:
            self.timeOver = False

        if depth == 0 or self.board.is_game_over():
            val = self.evaluateBoard()
            self.hashTable.InsertHashTable(depth, val, isMax, ht.HashExact)
            return val
        #make NUll move
       # if(depth>=2):
        #     self.board.push(chess.Move.null())
       #     val_null=self.expand(depth-2,not isMax,beta - 1, beta)
        #    self.board.pop()
        #    if(val_null>=beta):
        #        return beta
        #unmakenullmove
        """
        change generator to list
        """
        moveArr = list()
        for move in self.board.legal_moves:
            moveArr.append(move)
        
        self.historyHeuristics.moveSort(moveArr, moveArr.__len__, True)

        eval_is_exact = False
        bestMove = moveArr[0]
        if isMax:
            value = -9999

            for index, newMove in enumerate(moveArr):
                self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
                self.board.push(newMove)

                if (index == 0):
                    value = self.expand(depth - 1, not isMax, alpha, beta)
                else:
                    value = max(value, self.expand(depth - 1, not isMax, alpha, alpha + 1))
                    if (value > alpha and value < beta):
                        value = max(value, self.expand(depth - 1,not isMax, alpha, beta))
                        eval_is_exact = True
                        bestMove = moveArr[index]

                self.board.pop()
                self.hashTable.UndoMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
                alpha = max(alpha, value)

                if (alpha >= beta):
                    self.hashTable.InsertHashTable(depth, value, isMax, ht.HashAlpha)
                    self.historyHeuristics.InsertHistoryScore(moveArr[index], depth)
                    return alpha   # alpha 剪枝
        else:   # isMin
            value = 9999

            for index, newMove in enumerate(moveArr):
                self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
                self.board.push(newMove)

                if (index == 0):
                    value = self.expand(depth - 1, not isMax, alpha, beta)
                else:
                    value = min(value, self.expand(depth - 1, not isMax, beta - 1, beta))
                    if (value > alpha and value < beta):
                        value = min(value, self.expand(depth - 1,not isMax, alpha, beta))
                        eval_is_exact = True
                        bestMove = moveArr[index]

                self.board.pop()
                self.hashTable.UndoMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
                beta = min(beta, value)

                if (alpha >= beta):
                    self.hashTable.InsertHashTable(depth, value, isMax, ht.HashBeta)
                    self.historyHeuristics.InsertHistoryScore(moveArr[index], depth)
                    return beta   # beta 剪枝


        self.historyHeuristics.InsertHistoryScore(bestMove, depth)
        if eval_is_exact:
            self.hashTable.InsertHashTable(depth, value, isMax, ht.HashExact)

        return value  # def end

    def expandEx(self, depth, isMax, alpha, beta):
        val = self.hashTable.SearchHashTable(depth, alpha, beta, isMax)
        if val != 114514:
            return val

        if int(time.time()) - self.startTime >= self.timeLimit:
            self.timeOver = True
            depth = 0
        else:
            self.timeOver = False

        if depth == 0 or self.board.is_game_over():
            val = self.evaluateBoard()
            self.hashTable.InsertHashTable(depth, val, isMax, ht.HashExact)
            return val
        #make NUll move
        # if(depth>=2):
        #     self.board.push(chess.Move.null())
        #     val_null=self.expand(depth-2,not isMax,beta - 1, beta)
        #    self.board.pop()
        #    if(val_null>=beta):
        #        return beta
        #unmakenullmove
        """
        change generator to list
        """
        moveArr = list()
        for move in self.board.legal_moves:
            moveArr.append(move)
        
        self.historyHeuristics.moveSort(moveArr, moveArr.__len__, True)

        eval_is_exact = False
        bestMove = chess.Move.null()
        a = alpha
        b = beta
        for index, newMove in enumerate(moveArr):
            self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
            self.board.push(newMove)
            t = -self.expandEx(depth-1, not isMax, -b, -a)
            if t > a and t < beta and index > 0:
                a = -self.expandEx(depth-1, not isMax, -beta, -t)
                eval_is_exact = True
                bestMove = newMove
            self.board.pop()
            self.hashTable.UndoMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)

            if a < t:
                eval_is_exact = True
                a = t

            if a >= beta:
                self.hashTable.InsertHashTable(depth, a, isMax, ht.HashAlpha)
                self.historyHeuristics.InsertHistoryScore(newMove, depth)
                return a

            b = a + 1    

        self.historyHeuristics.InsertHistoryScore(bestMove, depth)

        if eval_is_exact:
            self.hashTable.InsertHashTable(depth, a, isMax, ht.HashExact)
        else:
            self.hashTable.InsertHashTable(depth, a, isMax, ht.HashBeta)

        return a

    def getBestMove(self, isMax):
        """
        返回最优移动mov
        """
        if(self.timeOver == False):     # 上次最后一次搜索没有超时，则递归层数+1
            self.searchDepth = self.searchDepth + 1

        moveArr = list()
        for move in self.board.legal_moves:
            moveArr.append(move)
        
        self.historyHeuristics.moveSort(moveArr, moveArr.__len__, True)
        bestValue = -9999
        #bestMove = chess.Move.null()
        for newMove in moveArr:
            self.startTime = int(time.time())
            self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
            self.board.push(newMove)
            tempValue = self.expandEx(self.searchDepth -1, not isMax, -10000, 10000)
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
        sys.stderr.write("Link Start!\n")
        raw_color = sys.stdin.readline()[:-1]
        self.InitColor(raw_color)

        while True:
            if (self.color == 'w'):
                AIMove = self.getBestMove(True)
                AIout = self.board.san(AIMove)
                self.board.push(AIMove)
                print(AIout)

            sys.stderr.write("当前搜索层数：{}层\n".format(self.searchDepth))
            AnothersideInput = sys.stdin.readline()[:-1]
            opponentMove = self.board.parse_san(AnothersideInput)
            self.hashTable.MakeMove(self.board.piece_at(opponentMove.from_square), self.board.piece_at(opponentMove.to_square), opponentMove)
            self.board.push_san(AnothersideInput)

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
                print("AI:当前搜索层数：{}层".format(self.searchDepth))
                print(self.board)

            while True:
                playerInput = input("\nplease input moves（eg.a1b2 exit退出）：")
                if playerInput == 'exit':
                    sys.exit('goodbye^_^\n')
                playerMove = self.board.parse_uci(playerInput)
                if playerMove in self.board.legal_moves:
                    break
                else:
                    print("input illegal")
            self.hashTable.MakeMove(self.board.piece_at(playerMove.from_square), self.board.piece_at(playerMove.to_square), playerMove)
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
        # AIDEMO.ManualGame()

    except:
        filename = "error.txt"
        file_object = open(filename, 'w')
        file_object.write(traceback.format_exc())
        file_object.close()
