import sys
import numpy as np
import chess
import hashTable as ht


historyTable = np.zeros((81,81))

historyTable[21][31] = 55

print(historyTable[21][31])