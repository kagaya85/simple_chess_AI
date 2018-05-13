import chess
import pieceValue as pv

color = 'b'

board = chess.Board()

def evaluateBoard(fenStr) -> float:
    """
    局面评估
    color: 己方颜色
    """
    board = replace_tags_board(fenStr)
    totalEval = 0.0

    for y in range(8):
        for x in range(8):
            tmp = getPieceValue(board[y][x], x, y)
            print(tmp)
            totalEval += tmp

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


print(evaluateBoard('rnbqkbnr/ppppppp1/7p/8/8/P7/1PPPPPPP/RNBQKBNR'))

