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

table = np.zeros((2,10), dtype = dt)

table[0][1]['key'] = 1

print(id(table[0][1]))
print(id(table[0][2]))
print(id(table[0][3]))
print(id(table[0][4]))
print(id(table[0]))
print(id(table[1]))

print(table)