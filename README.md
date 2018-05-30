# simple_chess_AI

`基于剪枝搜索的国际象棋AI————stableVersion稳定版本`

## 改进方向

* 评估函数优化———根据走子动态改变局面评价
* 评估参数优化
* 优先搜索策略（扩展排序）
* 优化局面评估参数，加入新的评估策略
* 动态调整递归层数可能有更好的结果

## 正在进行

* 正在调整输入输出符合规则 5/20
* 优化写法减少不必要的对象重新赋值 5/24

## 目前已知的bug

* 还不支持输入.进行重新走子 5/20

## 已完成

* alpha-beta剪枝优化 5/6
* 加入PVS优化 5/13
* 改成面对对象实现方式，手动调试请使用ManualGame，比赛对弈请使用GameStart 5/20
* 加入置换表 5/26
* 修复了HashTable左右横跳的bug(大概) 5/28
* **由于master版出现了不可预知的问题，因此回档到之前表现较好的版本，建立新分支stableVersion维护** 5/30
* 避免了重复三回的走法 5/30