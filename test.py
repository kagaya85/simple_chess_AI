import sys
import numpy as np
import chess

class HashItem:
    def __init__(self):
        self.key = 0
        self.depth = 0
        self.flags = 0
        self.value = 0

table = [[HashItem()] * 3, [HashItem()] * 3]




print(table[0][1].key)
