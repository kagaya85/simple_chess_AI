import chess
import numpy as np


class HistoryHeuristic:
    """
    历史启发记录
    """

    def __init__(self):
        self.historyTable = np.zeros((81, 81))

    def ResetHistoryTable(self):
        self.historyTable = np.zeros((81, 81))

    def GetHistoryScore(self, move):
        return self.historyTable[move.from_square][move.to_square]

    def InsertHistoryScore(self, move, depth):
        self.historyTable[move.from_square][move.to_square] += 2 << depth

    def moveSort(self, moveArr, len, direction) -> list:
        """
        对合法行动数组排序
        
        param:
            moveArr: 所有合法行为数组
            len: the length of moveArr
            direction: 排序方向 (true: 按历史得分从大到小 按历史得分false:从小到大)
        """
        moveArr.sort(self.valureCmp)

        return

    def valureCmp(self, mov1, mov2) -> bool:
        """
        mov1 < mov2 return Ture
        """
        if (self.historyTable[mov1.from_square][mov1.to_square] <
                self.historyTable[mov2.from_square][mov2.to_square]):
            return True
        else:
            return False
