from AStarPolicy import *
from LongestWay import *
from ViolentSearchPolicy import *

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

def long_to_wall(wall_thick, position, long_distance):
    return position[0] - wall_thick >= long_distance and position[1] - wall_thick >= long_distance
# TODO
#  0.低速发育策略
#  1.围杀蛇
#  2.自保&判断下是否自保
#  3.躲避力量强的
def Policy(current_map, snake_list, num):
    map_2d = transfer_map(current_map.map)
    my_snake = snake_list[num]
    # 发育策略
    if my_snake.speed <= 5:
        return violentSearchDevelopment(current_map, snake_list[num])
    # 绕远路
    else:
        longest_way, longest_way_actions = get_longest_way_options(map_2d, x, y, row, col)
        wall_thick = 0
        for i in range(0, int(current_map.row / 2)):
            if current_map.map[10][i][i] == 1:
                wall_thick += 1
            else:
                break
        # 找最后一个食物，看看离墙远不远，顺便找到离墙距离不超过5的最近的点
        food_index = -1
        last_index = 1
        for i in range(len(longest_way)):
            p = longest_way[i]
            if long_to_wall(wall_thick, p, 5):
                last_index = i + 1
                if map_2d[p[0]][p[1]] == 1:
                    food_index = i + 1
        # 走到最后一个食物那里
        res = ""
        if food_index != -1:
            for i in range(food_index):
                res += longest_way_actions[i]
        else:
            for i in range(last_index):
                res += longest_way_actions[i]
        return res