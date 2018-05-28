import sys
import numpy as np
import chess

L = np.zeros((10), dtype = np.int) 

# L[3] = 3
# L[4] = 4
# L[5] = 5

for i in L:
    print("{}  id:{}".format(L[i], id(L[i])))