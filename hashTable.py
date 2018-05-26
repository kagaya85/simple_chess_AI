import chess
import sys
import random
import numpy as np

HashFlags = [HashAlpha, HashBeta, HashExact] = [0, 1, 2]
Color = [True, False]

class HashTable:
    def __init__(self, tableSize = 1024*1024):
        self.tableSize = tableSize
        dt = np.dtype([
        ('key', np.uint64),
        ('depth', np.int),
        ('type', np.int),
        ('value', np.int)
        ])
        self._table = np.zeros((2,tableSize), dtype = dt)    
        self.hashKeyMap = [[[rand64() for k in chess.SQUARES] for piecesType in range(7)] for i in Color]
        self.hashKey64 = 0  # 初始
        self.hashIndexMap = [[[rand32() for k in chess.SQUARES] for piecesType in range(7)] for i in Color]
        self.hashIndex32 = 0
        return


    def CalculateInitHashKey(self):
        """
        计算初始hashKey64,hashIndex32
        """

        board = chess.BaseBoard()
 
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if(piece != None):
                self.hashKey64 = self.hashKey64 ^ self.hashKeyMap[piece.color][piece.piece_type][square]
                self.hashIndex32 = self.hashIndex32 ^ self.hashIndexMap[piece.color][piece.piece_type][square]
                
        return


    def MakeMove(self, from_piece, to_piece, move):
        """
        计算移动后的hashKey64,
        
        ps: 请在push之前执行

        param：
            from_piece: 要移动的棋子
            to_piece: 目标位置的敌方棋子
            move: 将要执行的移动
        """

        self.hashKey64 = self.hashKey64 ^ self.hashKeyMap[from_piece.color][from_piece.piece_type][move.from_square]
        self.hashIndex32 = self.hashIndex32 ^ self.hashIndexMap[from_piece.color][from_piece.piece_type][move.from_square]
        
        self.hashKey64 = self.hashKey64 ^ self.hashKeyMap[from_piece.color][from_piece.piece_type][move.to_square]
        self.hashIndex32 = self.hashIndex32 ^ self.hashIndexMap[from_piece.color][from_piece.piece_type][move.to_square]
        
        if to_piece:
            self.hashKey64 = self.hashKey64 ^ self.hashKeyMap[to_piece.color][to_piece.piece_type][move.to_square]
            self.hashIndex32 = self.hashIndex32 ^ self.hashIndexMap[to_piece.color][to_piece.piece_type][move.to_square]
            
        return


    def UndoMove(self, from_piece, to_piece, move):
        """
        恢复移动前的hashKey64,
        
        ps: 请在pop后执行
        
        param：
            from_piece: 要移动的棋子
            to_piece: 目标位置的敌方棋子
            move: 要恢复执行的移动
        """

        self.hashKey64 = self.hashKey64 ^ self.hashKeyMap[from_piece.color][from_piece.piece_type][move.from_square]
        self.hashIndex32 = self.hashIndex32 ^ self.hashIndexMap[from_piece.color][from_piece.piece_type][move.from_square]
        
        self.hashKey64 = self.hashKey64 ^ self.hashKeyMap[from_piece.color][from_piece.piece_type][move.to_square]
        self.hashIndex32 = self.hashIndex32 ^ self.hashIndexMap[from_piece.color][from_piece.piece_type][move.to_square]
        
        if to_piece:
            self.hashKey64 = self.hashKey64 ^ self.hashKeyMap[to_piece.color][to_piece.piece_type][move.to_square]
            self.hashIndex32 = self.hashIndex32 ^ self.hashIndexMap[to_piece.color][to_piece.piece_type][move.to_square]
            
        return


    def SearchHashTable(self, depth, alpha, beta, isMax):
        """
        Search item in HashTable
        """

        self.hashIndex32 = self.hashIndex32 % self.tableSize
        p = self._table[isMax][self.hashIndex32]        

        if p['depth'] >= depth and p['key'] == self.hashKey64:
            if p['type'] == HashExact:
                return p['value']
            elif p['type'] == HashAlpha:
                if p['value'] >= beta:
                    return p['value']
            elif p['type'] == HashBeta:
                if p['value'] <= alpha:    
                    return p['value']

        return 114514


    def InsertHashTable(self, depth, value, isMax, types):
        """
        Insert item into HashTable
        """
        
        self.hashIndex32 = self.hashIndex32 % self.tableSize
        
        self._table[isMax][self.hashIndex32]['key'] = self.hashKey64
        self._table[isMax][self.hashIndex32]['depth'] = depth
        self._table[isMax][self.hashIndex32]['value'] = value
        self._table[isMax][self.hashIndex32]['type'] = types

        return


def rand64():
    return random.randint(0, 0xFFFF_FFFF_FFFF_FFFF)


def rand32():
    return random.randint(0, 0xFFFF_FFFF)    