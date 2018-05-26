import sys
import numpy as np
import chess


tableSize = 5
dt = np.dtype([
        ('key', np.uint64),
        ('depth', np.int),
        ('type', np.int),
        ('value', np.int)
        ])

table = np.zeros((2, 1024*1024), dtype = dt)

table[0][1004044]['key'] = 1


print(table[0][1004044]['key'])