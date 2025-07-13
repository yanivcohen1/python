# from DFS_printTree import printTree, printList
from collections import deque
from typing import List, Optional
class Solution:
    def recursion(self, nums: List[List[int]]) -> List[List[int]]:
        res = []
        def dfs(i, comb):
            if len(comb) == 3:
                res.append(comb[:])
                return
            for j in range(0, 2):
                dfs(i+1, comb + [nums[i][j]])
        dfs(0, [])
        return res

    def loop(self, nums: List[List[int]]) -> List[List[int]]:
        res = []
        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    res.append([nums[0][i],nums[1][j],nums[2][k]])
        return res

res = [[11,12],[21,22],[31,32]]
print(Solution().recursion(res) == Solution().loop(res))

print(Solution().recursion(res))
# [[11, 21, 31], [11, 21, 32], [11, 22, 31], [11, 22, 32],
# [12, 21, 31], [12, 21, 32], [12, 22, 31], [12, 22, 32]]
print(Solution().loop(res))
# [[11, 21, 31], [11, 21, 32], [11, 22, 31], [11, 22, 32],
# [12, 21, 31], [12, 21, 32], [12, 22, 31], [12, 22, 32]]
