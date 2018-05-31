import chess
import sys
import pieceValue as pv
import traceback
import hashTable as ht
import historyHeuristics as hh
import numpy as np

class ChessAIDemo:
    def __init__(self, depth = 4, color = 'w'):
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
        self.hashCheck = 0
        self.hashHit = 0
        self.valueCheck = 0
        self.enablestalement=True

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
        color: 己方颜色
        """
        totalEval = 0.0

        for square in chess.SQUARES:   
            totalEval+=self.getPieceValue(square)

        return totalEval

    def getPieceValue(self, square) -> float:
        """
        根据棋子的类型以及位置返回评估值
        """
        piece = self.board.piece_at(square)
        if piece == None:
            return 0
        
        x = chess.square_file(square)
        y = 7 - chess.square_rank(square)
        absoluteValue = 0
        if piece.color == False:  # black
            if piece.piece_type == chess.PAWN:
                absoluteValue = 15 + pv.pawnEvalBlack[y][x]
            elif piece.piece_type == chess.ROOK:
                absoluteValue = 50 + pv.rookEvalBlack[y][x]
            elif piece.piece_type == chess.KNIGHT:
                absoluteValue = 40 + pv.knightEval[y][x]
            elif piece.piece_type == chess.BISHOP:
                absoluteValue = 30 + pv.bishopEvalBlack[y][x]
            elif piece.piece_type == chess.QUEEN:
                absoluteValue = 90 + pv.queenEval[y][x]
            elif piece.piece_type == chess.KING:
                absoluteValue = 1000 + pv.kingEvalBlack[y][x]

            if (self.color == 'w'):
                return -absoluteValue
                
            else:
                return  absoluteValue
        
        else:  # white
            if piece.piece_type == chess.PAWN:
                absoluteValue = 15 + pv.pawnEvalWhite[y][x]
            elif piece.piece_type == chess.ROOK:
                absoluteValue = 50 + pv.rookEvalWhite[y][x]
            elif piece.piece_type == chess.KNIGHT:
                absoluteValue = 40 + pv.knightEval[y][x]
            elif piece.piece_type == chess.BISHOP:
                absoluteValue = 30 + pv.bishopEvalWhite[y][x]
            elif piece.piece_type == chess.QUEEN:
                absoluteValue = 90 + pv.queenEval[y][x]
            elif piece.piece_type == chess.KING:
                absoluteValue = 1000 + pv.kingEvalWhite[y][x]

            if (self.color == 'w'):
                return  absoluteValue
              
            else:
                return  -absoluteValue
        
        return 0
              


    def expand(self, depth,isMax, alpha, beta):
        """

        扩展节点，返回评估值

        """

        val = self.hashTable.SearchHashTable(depth, alpha, beta, isMax)
        self.hashCheck += 1
        
        if val != 114514:
            self.hashHit += 1
            return val

        if depth == 0:
            val = self.evaluateBoard()
            self.valueCheck += 1
            self.hashTable.InsertHashTable(depth, val, isMax, ht.HashExact)
            return val
        

        moveArr = list()
        for move in self.board.legal_moves:
            moveArr.append(move)

        if(len(moveArr) == 0):
            '''
            if(self.board.is_stalemate()):
                if(isMax):
                    return -1000
                else:
                    return 1000
            else:
                '''

            if(isMax):
                return -9999
            else:
                if(self.board.is_stalemate()):
                    return -9999
                return 9999

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
                    current = self.expand(depth - 1,not isMax, alpha, beta)

                else:
                    value = max(value, self.expand(depth - 1, not isMax, alpha, alpha + 1))
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
                    value = min(value, self.expand(depth - 1,not isMax, beta - 1, beta))
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
        if(self.hashCheck > 0):
            if(self.hashCheck < 5000 and self.searchDepth < 6):
               self.searchDepth += 1
            elif(self.hashCheck > 60000):
                self.searchDepth -= 1

        self.hashCheck = 0
        self.hashHit = 0
        self.valueCheck = 0
        moveArr = list()
        for move in self.board.legal_moves:
            moveArr.append(move)

        self.historyHeuristics.moveSort(moveArr, moveArr.__len__, True)
        bestValue = -10000
        lastValue = -10000
        count=0
        bestMove=chess.Move.null()
        for newMove in moveArr:
            self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
            self.board.push(newMove)
            tempValue = self.expand(self.searchDepth - 1, not isMax, -10000, 10000)

            if(self.board.can_claim_threefold_repetition()):
                pass
            elif bestValue < tempValue and (bestValue==-10000):
                bestValue=tempValue
                lastValue=tempValue
                bestMove=newMove
                count=0
                # lastmove=newMove
            elif bestValue!=-10000 and (bestValue==lastValue) and bestValue < tempValue :
                lastValue=bestValue
                bestValue=tempValue
                # lastmove=bestMove
                count=0
                bestMove=newMove
            elif bestValue!=-10000 and (bestValue==lastValue) and bestValue > tempValue :
                lastValue=tempValue
                # lastmove=newMove
            elif bestValue > tempValue and lastValue > tempValue:
                pass
            elif bestValue > tempValue and lastValue < tempValue:
                lastValue=tempValue
                # lastmove=newMove
            elif bestValue < tempValue and lastValue < tempValue:
                lastValue=bestValue
                bestValue=tempValue
                count=0
                # lastmove=bestMove
                bestMove=newMove
            elif bestValue == tempValue:
                count+=1
            else:
                pass

            self.board.pop()
            self.hashTable.UndoMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)

        if count >= 4 and self.searchDepth == 3:
            self.searchDepth += 1
            bestMove=self.getBestMove(isMax)

        if bestMove == chess.Move.null():
            self.hashTable.enable=False
            self.searchDepth+=1
            bestMove=self.getBestMove(isMax)
        '''
        self.board.push(bestMove)
        if(self.board.is_stalemate() and self.enablestalement==True):
            self.enablestalement=False
            self.board.pop()
            self.searchDepth =7
            bestMove=self.getBestMove(isMax)
            self.searchDepth =4
        else:
            self.board.pop()
        '''
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
        # count=0
        while True:
            if (self.color == 'w'):
                #if(count!=0):
                AIMove = self.getBestMove(True)
                AIout = self.board.san(AIMove)
                self.board.push(AIMove)
                print(AIout)
                sys.stderr.write("当前搜索{}层，评估局面{}种，哈希表搜索{}次，命中{}次\n".format(self.searchDepth, self.valueCheck, self.hashCheck, self.hashHit))
                
                #else:
                   # newMove=self.board.parse_san('e4')
                   # self.hashTable.MakeMove(self.board.piece_at(newMove.from_square), self.board.piece_at(newMove.to_square), newMove)
                   # self.board.push(newMove)
                   # print('e4')

            while True:
                AnothersideInput = sys.stdin.readline()[:-1]
                if AnothersideInput == 'exit':
                    sys.exit('goodbye^_^\n')
                elif AnothersideInput == '.':
                    self.board.pop()
                    self.searchDepth+=1
                    break
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
                sys.stderr.write("当前搜索{}层，评估局面{}种，哈希表搜索{}次，命中{}次\n".format(self.searchDepth, self.valueCheck, self.hashCheck, self.hashHit))
            self.enablestalement==True

            # count+=1 
            self.hashTable.enable=True


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

        filename = "\\error.txt"
        file_object = open(filename, 'w')
        file_object.write(traceback.format_exc())
        file_object.close()
