from AStarPolicy import *

# 0空地、1道具、2不可走
def transfer_map(current_map):
    map = np.zeros([MAP_ROW, MAP_COLUMN])
    for i in range(MAP_ROW):
        for j in range(MAP_COLUMN):
            for k in range(LEVEL):
                if current_map[i][j][k] == 1:
                    if k in range(0, 6):
                        map[i][j] = 2
                        break
                    if k in range(6, 10):
                        map[i][j] = 1
                    if k == 10:
                        map[i][j] = 2
    return map

# TODO
#  0.低速发育策略
#  1.围杀蛇
#  2.自保&判断下是否自保
#  3.躲避力量强的
def Policy(current_map, snake_list, num):
    map_2d = transfer_map(current_map.map)
    # 发育策略
    return AStar_Policy(map_2d, snake_list[num], row, column, level)
    # 其他策略