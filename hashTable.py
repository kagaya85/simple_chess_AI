import chess
import random as rd
import sys

HashFlags = [HashAlpha, HashBeta, HashExact] = [0, 1, 2]
Pieces = ['p', 'n', 'b', 'q', 'k', 'P', 'N', 'B', 'Q', 'K']
Position = [
            'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 
            'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 
            'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 
            'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'
            ]

class HashNode:
    def __init__(self):
        self.key = 0
        self.depth = 0
        self.flags = 0
        self.value = 0
        self.bestMove = chess.Move.null()


class HashTable:
    def __init__(self, tableSize):
        self._table = []*tableSize
        self._nodeNum = 0
        self.Z = {ps : {i : rd.randint(1, sys.maxsize) for i in Position} for ps in Pieces}
        self.boardKey = 0   # 初始


    def len(self):
        return self._nodeNum


    def newKey(self, key):
        return

    
    def SearchHash(self, depth, alpha, beta):
        return 


    def InsertHash(self, depth, val, key):
        return