# simple_chess_AI

### 基于剪枝搜索的国际象棋AI

## 改进方向

* 评估函数优化———根据走子动态改变局面评价
* 评估参数优化
* 优先搜索策略（扩展排序）
* 优化局面评估参数，加入新的评估策略
* 动态调整递归层数可能有更好的结果

## 正在进行

* 正在调整输入输出符合规则 5/20
* HashTable（调试）5/23
* 历史启发(调试) 5/26
* 空着搜索 5/24 (效果未知)
* 优化写法减少不必要的对象重新赋值 5/24

## 目前已知的bug

* 还不支持输入.进行重新走子 5/20
* 应避免重复三回的走法

## 已完成

* alpha-beta剪枝优化 5/6
* 加入PVS优化 5/13
* 改成面对对象实现方式，手动调试请使用ManualGame，比赛对弈请使用GameStart 5/20
* 加入置换表 5/26
* 历史启发类 5/26
* HashTable类 5/23