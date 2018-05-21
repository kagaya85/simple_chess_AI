import chess
import sys
import pieceValue as pv

"""
全局参数部分
color: b 黑色（后手） w 白色（先手）
searchDepth: 搜索深度
需添加防止重复走子的代码
"""

color = 'w'
searchDepth = 4


def evaluateBoard(fenStr) -> float:
    """
    局面评估
    color: 己方颜色
    """
    board = replace_tags_board(fenStr)
    totalEval = 0.0

    for y in range(8):
        for x in range(8):
            totalEval += getPieceValue(board[y][x], x, y)

    return totalEval


def getPieceValue(piece, x, y) -> float:
    """
    根据棋子的类型以及位置返回评估值
    """
    global color

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
        
        if(color == 'w'):
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
        
        if(color == 'w'):
            return absoluteValue
        else:
            return -absoluteValue


def expand(depth, board, isMax, alpha, beta):
    """
    扩展节点，返回评估值
    """

    # 此处查询置换表中是否存在，存在则直接返回

    if depth == 0:
        value = evaluateBoard(board.fen()) 
        # 存入置换表
        return value
    if isMax:
        value = -9999
        for index, newMove in enumerate(board.legal_moves):
            # 产生 hashkey
            board.push(newMove)
            if(index == 0):
                current = expand(depth - 1, board, not isMax, alpha, beta)
            else:
                value = max(value, expand(depth - 1, board, not isMax, alpha, alpha + 1))
                if(value > alpha and value < beta):
                    value = max(value, expand(depth - 1, board, not isMax, alpha, beta))
            board.pop()
            # 复原 hashkey
            current = max(current, value)
            alpha = max(alpha, value)
            if (alpha >= beta):
                break
    else:
        value = 9999
        for index, newMove in enumerate(board.legal_moves):
            board.push(newMove)
            if(index == 0):
                current = expand(depth - 1, board, not isMax, alpha, beta)
            else:
                value = min(value, expand(depth - 1, board, not isMax, beta - 1, beta))
                if(value > alpha and value < beta):
                    value = min(value, expand(depth - 1, board, not isMax, alpha, beta))
            board.pop()
            current = min(current, value)
            beta = min(beta, value)
            if (alpha >= beta):
                break
    return current


def getBestMove(depth, board, isMax):
    """
    用minmax遍历，返回最优移动uci
    """

    bestValue = -9999
    for newMove in board.legal_moves:
        board.push(newMove)
        tempValue = expand(depth - 1, board, not isMax, -10000, 10000)
        if bestValue < tempValue:
            bestMove = newMove
            bestValue = tempValue
        board.pop()

    return bestMove


def replace_tags_board(fenStr) -> list:
    fenStr = fenStr.split(" ")[0]
    fenStr = fenStr.replace("2", "11")
    fenStr = fenStr.replace("3", "111")
    fenStr = fenStr.replace("4", "1111")
    fenStr = fenStr.replace("5", "11111")
    fenStr = fenStr.replace("6", "111111")
    fenStr = fenStr.replace("7", "1111111")
    fenStr = fenStr.replace("8", "11111111")
    return fenStr.split('/')


def is_white_turn(fenStr):
    return fenStr.split(" ")[1] == 'w'


"""
程序入口
"""

if __name__ == '__main__':
    board = chess.Board()

    while board.is_game_over() is False:
        if(color == 'w'):
            AIMove = getBestMove(searchDepth, board, True)
            board.push(AIMove)
            print("AI:")
            print(board)

        while True:
            playerInput = input("\nplease input moves（eg.a1b2 exit退出）：")
            if playerInput == 'exit':
                sys.exit('goodbye^_^\n')
            playerMove = chess.Move.from_uci(playerInput)
            if playerMove in board.legal_moves:
                break
            else:
                print("input illegal")
        board.push(playerMove)
        print("Player:")
        print(board)

        if(color == 'b'):
            AIMove = getBestMove(searchDepth, board, True)
            board.push(AIMove)
            print("AI:")
            print(board)
