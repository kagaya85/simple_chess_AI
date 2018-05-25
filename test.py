import sys
import numpy as np
import chess
import hashTable as ht

def test(array):
    array[0] = 2
    print("test: {}".format(array[0]))
    return


board = chess.Board()
movArr = list()

for move in board.legal_moves:
    movArr.append(move)

print(movArr[0].from_square)