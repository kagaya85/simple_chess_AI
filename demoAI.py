import chess
import sys
import pieceValue as pv
import traceback
"""
全局参数部分
color: b 黑色（后手） w 白色（先手）
searchDepth: 搜索深度
需添加防止重复走子的代码
"""

class ChessAIDemo:
    color = 'w'
    searchDepth = 4
    board=chess.Board()

    def InitColor(self,color):
        if(color=="white"):
            self.color='w'
        elif(color=="black"):
            self.color='b'
        else:
            self.color='w'

    def InitSearchDepth(self,Depth):
        self.searchDepth=int(Depth)

    def evaluateBoard(self,fenStr) -> float:
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


    def getPieceValue(self,piece, x, y) -> float:
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
            
            if(self.color == 'w'):
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
            
            if(self.color == 'w'):
                return absoluteValue
            else:
                return -absoluteValue


    def expand(self,depth, board, isMax, alpha, beta):
        """
        扩展节点，返回评估值
        """

        if depth == 0:
            return self.evaluateBoard(board.fen())
        if isMax:
            current = self.expand(depth - 1, board, not isMax, alpha, beta)
            value = -9999
            for index, newMove in enumerate(board.legal_moves):
                board.push(newMove)
                if(index == 0):
                    current = self.expand(depth - 1, board, not isMax, alpha, beta)
                else:
                    value = max(value, self.expand(depth - 1, board, not isMax, alpha, alpha + 1))
                    if(value > alpha and value < beta):
                        value = max(value, self.expand(depth - 1, board, not isMax, alpha, beta))
                board.pop()
                current = max(current, value)
                alpha = max(alpha, value)
                if (alpha >= beta):
                    break
        else:
            value = 9999
            current = self.expand(depth - 1, board, not isMax, alpha, beta)
            for index, newMove in enumerate(board.legal_moves):
                board.push(newMove)
                if(index == 0):
                    current = self.expand(depth - 1, board, not isMax, alpha, beta)
                else:
                    value = min(value, self.expand(depth - 1, board, not isMax, beta - 1, beta))
                    if(value > alpha and value < beta):
                        value = min(value, self.expand(depth - 1, board, not isMax, alpha, beta))
                board.pop()
                current = min(current, value)
                beta = min(beta, value)
                if (alpha >= beta):
                    break
        return current


    def getBestMove(self,isMax):
        """
        用minmax遍历，返回最优移动uci
        """

        bestValue = -9999
        for newMove in self.board.legal_moves:
            self.board.push(newMove)
            tempValue = self.expand(self.searchDepth - 1, self.board, not isMax, -10000, 10000)
            if bestValue < tempValue:
                bestMove = newMove
                bestValue = tempValue
            self.board.pop()

        return bestMove


    def replace_tags_board(self,fenStr) -> list:
        fenStr = fenStr.split(" ")[0]
        fenStr = fenStr.replace("2", "11")
        fenStr = fenStr.replace("3", "111")
        fenStr = fenStr.replace("4", "1111")
        fenStr = fenStr.replace("5", "11111")
        fenStr = fenStr.replace("6", "111111")
        fenStr = fenStr.replace("7", "1111111")
        fenStr = fenStr.replace("8", "11111111")
        return fenStr.split('/')


    def is_white_turn(self,fenStr)->bool:
        return fenStr.split(" ")[1] == 'w'


    def GameStart(self):
        self.board = chess.Board()
        sys.stderr.write("please input the chess color\n")
        raw_color=sys.stdin.readline()[:-1]
        self.InitColor(raw_color)
        self.InitSearchDepth(3)
        #while self.board.is_game_over() is False:
        while True:
            if(self.color=='w'):
                AIMove = self.getBestMove(True)
                AIout=self.board.san(AIMove)
                self.board.push(AIMove)
                print(AIout)
                #please delete next two lines during the offical match
                #print("AI:")
                #print(self.board)
                #please delete prior two lines during the offical match
            

            while True:
                sys.stderr.write("\nplease input moves（eg.a1b2 exit退出）：")
                AnothersideInput = sys.stdin.readline()[:-1]
                if  AnothersideInput == 'exit':
                    sys.exit('goodbye^_^\n')
                else:
                    self.board.push_san(AnothersideInput)
                    break
                #AnothersideMove = chess.Move.from_uci(AnothersideInput)

                # the match rule comfirm that the input is legal,so please delete next lines in the formal match
                #if AnothersideMove in self.board.legal_moves:
                #    break
                #else:
                #     sys.stderr.write("input illegal")
                # the match rule comfirm that the input is legal,so please delete prior lines in the formal match

           # print(AnothersideMove)

            #please delete next two lines during the offical match
          #  print("anotherside:")
          #  print(self.board)
            #please delete prior two lines during the offical match

            if(self.color == 'b'):
                AIMove = self.getBestMove(True)
                AIout=self.board.san(AIMove)
                self.board.push(AIMove)
                print(AIout)
                #please delete next two lines during the offical match
               # print("AI:")
                #print(self.board)
                #please delete prior two lines during the offical match
    
    def ManualGame(self):
        self.board = chess.Board()
        sys.stderr.write("please input the chess color\n")
        raw_color=sys.stdin.readline()[:-1]
        self.InitColor(raw_color)
        self.InitSearchDepth(1)
        while self.board.is_game_over() is False:
            if(self.color == 'w'):
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
            if(self.color == 'b'):
                AIMove = self.getBestMove(True)
                self.board.push(AIMove)
                print("AI:")
                print(self.board)
"""
程序入口
"""

if __name__ == '__main__':
   
    try:
        AIDEMO=ChessAIDemo()
        #AIDEMO.GameStart()
        AIDEMO.ManualGame()
    except:

        filename="error.txt"
        file_object=open(filename,'w')
        file_object.write(traceback.format_exc())
        file_object.close()
