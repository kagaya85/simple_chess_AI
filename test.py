import chess
import pieceValue as pv

board = chess.Board()

board.set_fen('r2r4/p1p2kpP/2Qbbq2/4p3/8/2N5/pPPP1PPP/R1B1K2R w KQ - 0 12')

print(board)

# for i in board.legal_moves:
#     print(i)
board.push_uci("h7h8q")
print()
print(board)
print(board.fen())
