import chess
import sys
import pieceValue as pv


def evaluateBoard(fenStr) -> float:
    """
    局面评估
    """
    board = replace_tags_board(fenStr)
    board.reverse()
    totalEval = 0.0

    for y in range(8):
        for x in range(8):
            totalEval += getPieceValue(board[y][x], x, y)

    return totalEval


def getPieceValue(piece, x, y) -> float:
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
            absoluteValue = 900 + pv.bishopEvalBlack[y][x]
        return -absoluteValue
    else:   # white
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
            absoluteValue = 900 + pv.bishopEvalWhite[y][x]
        return absoluteValue


def expand(depth, board, isMax, alpha, beta):
    """
    扩展节点，返回评估值
    """

    if depth == 0:
        return -evaluateBoard(board.fen())
    if isMax:
        bestValue = -9999
        for newMove in board.legal_moves:
            board.push(newMove)
            bestValue = max(bestValue, expand(depth - 1, board, ~isMax, alpha, beta))
            board.pop()
            alpha = max(alpha, bestValue)
            if(alpha >= beta):
                return bestValue
    else:
        bestValue = 9999
        for newMove in board.legal_moves:
            board.push(newMove)
            bestValue = min(bestValue, expand(depth - 1, board, ~isMax, alpha, beta))
            board.pop()
            beta = min(beta, bestValue)
            if(alpha >= beta):
                return bestValue

    return bestValue


def getBestMove(depth, board, isMax):
    """
    用minmax遍历，返回最优移动uci
    """

    bestValue = -9999
    for newMove in board.legal_moves:
        board.push(newMove)
        tempValue = expand(depth - 1, board, ~isMax, -10000, 10000)
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


board = chess.Board()
depth = 3

while board.is_game_over() is False:
    while True:
        playerInput = input("请输入起始结束位置（eg.a1b2 exit退出）：")
        if playerInput is 'exit':
            sys.exit('goodbye^_^')
        playerMove = chess.Move.from_uci(playerInput)
        if playerMove in board.legal_moves:
            break
    board.push(playerMove)
    print(board)
    print('\n')
    AIMove = getBestMove(depth, board, True)
    board.push(AIMove)
    print(board)
