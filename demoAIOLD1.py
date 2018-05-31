import chess
import sys
import pieceValue_zyr as pv
import traceback
import hashTable as ht
import historyHeuristics as hh
import numpy as np

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
    def evaluateBoard_zyr(self, movArr, isMax) -> float:
        """
        局面评估
        param:
            color: 己方颜色
        """
        #board = self.replace_tags_board(fenStr)
        totalEval = 0.0

        flexPos = np.zeros(64)

        protectedPos = np.zeros(64)

        threatedPos = np.zeros(64)


        pa = self.board.piece_at


        # for y in range(8):
        #    for x in range(8):
        #        totalEval += self.getPieceValue(board[y][x], x, y)
        
        """
        计算各个棋子的灵活性flexPos
        """
        for move in movArr:
            m = move.uci()
            flexPos[(ord(m[1]) - ord('1')) + 8 * (ord(m[0] )- ord('a'))]+= 1
        
        """
        计算各个棋子的受威胁情况threatedPos
        """
        #for y in range(8):
        #    for x in range(8):
        #        for threated in self.board.attacks(y + x * 8):
        #            threatedPos[threated % 8][threated / 8]+= 1

        """
        计算各个棋子的受威胁情况threatedPos  &&
        计算各个棋子的受保护情况protectedPos
        """
        for pos in range(64):
            y = pos % 8
            x = pos // 8
            pa = self.board.piece_at
            piece = self.board.piece_at(pos)
            if(piece==None):
                continue
            #如果棋子为兵
            if(piece.symbol() == 'P'):
                if(y == 0):
                    if(pa(pos + 9) != None):
                        if(pa(pos + 9).color == piece.color):
                            protectedPos[pos + 9] = 1
                        else:
                            threatedPos[pos + 9] = 1
                elif(y == 7):
                    if(pa(pos + 7) != None):
                        if(pa(pos + 7).color == piece.color):
                            protectedPos[pos + 7] = 1
                        else:
                            threatedPos[pos + 7] = 1
                else:
                    if(pa(pos + 9) != None):
                        if(pa(pos + 9).color == piece.color):
                            protectedPos[pos + 9] = 1
                        else:
                            threatedPos[pos + 9] = 1
                    if(pa(pos + 7) != None):
                        if(pa(pos + 7).color == piece.color):
                            protectedPos[pos + 7] = 1
                        else:
                            threatedPos[pos + 7] = 1
            if(piece.symbol() == 'p'):
                if(y == 0):
                    if(pa(pos - 7) != None):
                        if(pa(pos - 7).color == piece.color):
                            protectedPos[pos - 7] = 1
                        else:
                            threatedPos[pos - 7] = 1
                elif(y == 7):
                    if(pa(pos - 9) != None):
                        if(pa(pos - 9).color == piece.color):
                            protectedPos[pos - 9] = 1
                        else:
                            threatedPos[pos - 9] = 1
                else:
                    if(pa(pos - 9) != None):
                        if(pa(pos - 9).color == piece.color):
                            protectedPos[pos - 9] = 1
                        else:
                            threatedPos[pos - 9] = 1
                    if(pa(pos - 7) != None):
                        if(pa(pos - 7).color == piece.color):
                            protectedPos[pos - 7] = 1
                        else:
                            threatedPos[pos - 7] = 1
            #如果棋子为马
            if(piece.piece_type == 2):
                if(y + 1 <= 7 and x + 2 <= 7):
                    if(pa(pos + 17) != None):
                        if(pa(pos + 17).color == piece.color):
                            protectedPos[pos + 17] = 1
                        else:
                            threatedPos[pos + 17] = 1
                if(y + 1 <= 7 and x - 2 >= 0):
                    if(pa(pos - 15) != None):
                        if(pa(pos - 15).color == piece.color):
                            protectedPos[pos - 15] = 1
                        else:
                            threatedPos[pos - 15] = 1
                if(y - 1 >= 0 and x + 2 <= 7):
                    if(pa(pos + 15) != None):
                        if(pa(pos + 15).color == piece.color):
                            protectedPos[pos + 15] = 1
                        else:
                            threatedPos[pos + 15] = 1
                if(y - 1 >= 0 and x - 2 >= 0):
                    if(pa(pos - 17) != None):
                        if(pa(pos - 17).color == piece.color):
                            protectedPos[pos - 17] = 1
                        else:
                            threatedPos[pos - 17] = 1
                if(y + 2 <= 7 and x + 1 <= 7):
                    if(pa(pos + 10) != None):
                        if(pa(pos + 10).color == piece.color):
                            protectedPos[pos + 10] = 1
                        else:
                            threatedPos[pos + 10] = 1
                if(y + 2 <= 7 and x - 1 >= 0):
                    if(pa(pos - 6) != None):
                        if(pa(pos - 6).color == piece.color):
                            protectedPos[pos - 6] = 1
                        else:
                            threatedPos[pos - 6] = 1
                if(y - 2 >= 0 and x + 1 <= 7):
                    if(pa(pos + 6) != None):
                        if(pa(pos + 6).color == piece.color):
                            protectedPos[pos + 6] = 1
                        else:
                            threatedPos[pos + 6] = 1
                if(y - 2 >= 0 and x - 1 >= 0):
                        if(pa(pos - 10) != None):
                            if(pa(pos - 10).color == piece.color):
                                protectedPos[pos - 10] = 1
                            else:
                                threatedPos[pos - 10] = 1
            #如果棋子为象
            if(piece.piece_type == 3):
                for target_y in range(8):
                    for target_x in range(8):
                        if(target_x + target_y == x + y or target_x - target_y == x - y):
                            if(pa(target_y + target_x * 8) != None):
                                if(pa(target_y + target_x * 8).color == piece.color):
                                    protectedPos[target_y + target_x * 8] = 1
                                else:
                                    threatedPos[target_y + target_x * 8] = 1
            #如果棋子为车
            if(piece.piece_type == 4):
                for target_y in range(8):
                    if(pa(target_y + x * 8) != None):
                        if(pa(target_y + x * 8).color == piece.color):
                            protectedPos[target_y + x * 8] = 1
                        else:
                            threatedPos[target_y + x * 8] = 1
                for target_x in range(8):
                    if(pa(y + target_x * 8) != None):
                        if(pa(y + target_x * 8).color == piece.color):
                            protectedPos[y + target_x * 8] = 1
                        else:
                            threatedPos[y + target_x * 8] = 1
            #如果棋子为皇后
            if(piece.piece_type == 5):
                for target_y in range(8):
                    for target_x in range(8):
                        if(target_x + target_y == x + y or target_x - target_y == x - y or target_x == x or target_y == y):
                            if(pa(target_y + target_x * 8) != None):
                                if(pa(target_y + target_x * 8).color == piece.color):
                                    protectedPos[target_y + target_x * 8] = 1
                                else:
                                    threatedPos[target_y + target_x * 8] = 1
            #如果棋子为王
            if(piece.piece_type == 6):
                if(y + 1 <= 7 and x + 1 <= 7):
                    if(pa(pos + 9) != None):
                        if(pa(pos + 9).color == piece.color):
                            protectedPos[pos + 9] = 1
                        else:
                            threatedPos[pos + 9] = 1
                if(y + 1 <= 7 and x - 1 >= 0):
                    if(pa(pos - 7) != None):
                        if(pa(pos - 7).color == piece.color):
                            protectedPos[pos - 7] = 1
                        else:
                            threatedPos[pos - 7] = 1
                if(y - 1 >= 0 and x + 1 <= 7):
                    if(pa(pos + 7) != None):
                        if(pa(pos + 7).color == piece.color):
                            protectedPos[pos + 7] = 1
                        else:
                            threatedPos[pos + 7] = 1
                if(y - 1 >= 0 and x - 1 >= 0):
                    if(pa(pos - 9) != None):
                        if(pa(pos - 9).color == piece.color):
                            protectedPos[pos - 9] = 1
                        else:
                            threatedPos[pos - 9] = 1
                if(y - 1 >= 0):
                    if(pa(pos - 1) != None):
                        if(pa(pos - 1).color == piece.color):
                            protectedPos[pos - 1] = 1
                        else:
                            threatedPos[pos - 1] = 1
                if(y + 1 <= 7):
                    if(pa(pos + 1) != None):
                        if(pa(pos + 1).color == piece.color):
                            protectedPos[pos + 1] = 1
                        else:
                            threatedPos[pos + 1] = 1
                if(x + 1 <= 7):
                    if(pa(pos + 8) != None):
                        if(pa(pos + 8).color == piece.color):
                            protectedPos[pos + 8] = 1
                        else:
                            threatedPos[pos + 8] = 1
                if(x - 1 >= 0):
                        if(pa(pos - 8) != None):
                            if(pa(pos - 8).color == piece.color):
                                protectedPos[pos - 8] = 1
                            else:
                                threatedPos[pos - 8] = 1
        
        #遍历求估值，默认为执白棋
        for pos in range(64):
            piece = pa(pos)
            if(piece != None):
                sign = 0
                if(piece.color == True):
                    sign = 1
                else:
                    sign = -1
            
                totalEval = totalEval + sign * (pv.baseValue[piece.piece_type-1] + pv.PosVal[piece.piece_type-1][pos] + 0.008 * flexPos[pos] * pv.flexValue[piece.piece_type-1]) 
            
                #如果该棋是白棋
                halfBaseVal = pv.baseValue[piece.piece_type-1] / 8
                if(sign == 1):
                    #轮到白棋走子
                    if(self.board.turn == True):
                        #当前棋子被威胁
                        if(threatedPos[pos] != 0):
                            #如果是王被威胁
                            if(piece.piece_type == 6):
                                totalEval = totalEval - 3
                            else:
                                totalEval = totalEval - 0.005 * halfBaseVal
                        #当前棋子被保护
                        if(protectedPos[pos] != 0):
                            totalEval = totalEval + 0.005 * halfBaseVal
                    #轮到黑棋走子
                    else:
                        #当前棋子被威胁
                        if(threatedPos[pos] != 0):
                            #如果是王被威胁
                            if(piece.piece_type == 6):
                                totalEval = -1200
                            else:
                                totalEval = totalEval - 0.01 * halfBaseVal
                        #当前棋子被保护
                        if(protectedPos[pos] != 0):
                            totalEval = totalEval + 0.01 * halfBaseVal
                #如果该棋是黑棋
                else:
                    #轮到白棋走子
                    if(self.board.turn == True):
                        #当前棋子被威胁
                        if(threatedPos[pos] != 0):
                            #如果是王被威胁
                            if(piece.piece_type == 6):
                                totalEval = 1200
                            else:
                                totalEval = totalEval + 0.01 * halfBaseVal
                        #当前棋子被保护
                        if(protectedPos[pos] != 0):
                            totalEval = totalEval - 0.01 * halfBaseVal
                    #轮到黑棋走子
                    else:
                        #当前棋子被威胁
                        if(threatedPos[pos] != 0):
                            #如果是王被威胁
                            if(piece.piece_type == 6):
                                totalEval = totalEval + 3
                            else:
                                totalEval = totalEval + 0.005 * halfBaseVal
                        #当前棋子被保护
                        if(protectedPos[pos] != 0):
                            totalEval = totalEval - 0.005 * halfBaseVal

        if(self.color == 'b'):
            totalEval = -1 * totalEval

        return totalEval

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

     
        moveArr = list()

        for move in self.board.legal_moves:

            moveArr.append(move)


        if depth == 0: #or self.board.is_game_over():

            val=self.evaluateBoard_zyr(moveArr,isMax)

            return val

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

        bestValue = -10000
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

        filename = "C:\\Users\\youyaoyin\\OneDrive\\github-space\\chess_ai\\simple_chess_AIerror.txt"
        file_object = open(filename, 'w')
        file_object.write(traceback.format_exc())
        file_object.close()
