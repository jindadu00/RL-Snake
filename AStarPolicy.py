"""
Copyrights: 2021 @TheJunhan
Date: 2022-04-16 21:02:05
LastEditor: TheJunhan
LastEditTime: 2022-04-16 21:04:10
"""
import numpy as np

MAP_ROW = 40
MAP_COLUMN = 55
LEVEL = 11


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


# 找到到尾巴的最长路径
def longest_tail_path(map, snake_head, snake_tail):
    direction = []
    longest = 0
    if snake_head[0] - 1 >= 0 and map[snake_head[0] - 1][snake_head[1]] != 2:
        can, tmp = tailBFS(map, [snake_head[0] - 1, snake_head[1]], snake_tail)
        if can and tmp > longest:
            longest = tmp
            direction = [snake_head[0] - 1, snake_head[1]]
    if snake_head[0] + 1 < MAP_ROW and map[snake_head[0] +
                                           1][snake_head[1]] != 2:
        can, tmp = tailBFS(map, [snake_head[0] + 1, snake_head[1]], snake_tail)
        if can and tmp > longest:
            longest = tmp
            direction = [snake_head[0] + 1, snake_head[1]]
    if snake_head[1] - 1 >= 0 and map[snake_head[0]][snake_head[1] - 1] != 2:
        can, tmp = tailBFS(map, [snake_head[0], snake_head[1] - 1], snake_tail)
        if can and tmp > longest:
            longest = tmp
            direction = [snake_head[0], snake_head[1] - 1]
    if snake_head[1] + 1 < MAP_COLUMN and map[snake_head[0]][snake_head[1] +
                                                             1] != 2:
        can, tmp = tailBFS(map, [snake_head[0], snake_head[1] + 1], snake_tail)
        if can and tmp > longest:
            direction = [snake_head[0], snake_head[1] + 1]
    return direction


# 模拟蛇去吃道具
def explore(map, path, snake):
    explore_map = map.copy()
    explore_path = path.copy()
    explore_path.reverse()
    new_head = explore_path[0]
    # 不能忘了，这时候蛇的长度已经加一了
    if len(snake.body) < len(explore_path):
        new_tail = explore_path[len(snake.body)]
        for i in range(len(snake.body) + 1):
            explore_map[explore_path[i][0]][explore_path[i][1]] = 2
        for i in range(len(snake.body)):
            explore_map[snake.body[i].coordinates[0]][
                snake.body[i].coordinates[1]] = 0
    else:
        new_tail = snake.body[len(snake.body) - len(explore_path)].coordinates
        for i in range(len(explore_path)):
            explore_map[explore_path[i][0]][explore_path[i][1]] = 2
        for i in range(
                len(snake.body) - len(explore_path) + 1, len(snake.body)):
            explore_map[snake.body[i].coordinates[0]][
                snake.body[i].coordinates[1]] = 0
    return tailBFS(explore_map, new_head, new_tail)


def hash_xy(x, y):
    return x * 100 + y


# 找道具，返回能否找到和道具的路径
def BFS(map, snake_head):
    bfs_map = map.copy()
    queue = [snake_head]
    jump_history = {}
    end_position = []
    path = []
    bfs_map[snake_head[0]][snake_head[1]] = -1
    flag = 0

    def judge_neighbor(x, y, last_position):
        nonlocal jump_history
        if map[x][y] == 1:
            jump_history[hash_xy(x, y)] = last_position
            return [[x, y], 1]
        elif map[x][y] == 0:
            map[x][y] = -1
            queue.append([x, y])
            jump_history[hash_xy(x, y)] = last_position
        return [[], 0]

    while len(queue) > 0:
        current_position = queue.pop(0)
        # 把他的邻居加进来
        if current_position[0] - 1 >= 0:
            end_position, flag = judge_neighbor(
                current_position[0] - 1, current_position[1],
                [current_position[0], current_position[1]])
        if flag == 1:
            break
        if current_position[0] + 1 < MAP_ROW:
            end_position, flag = judge_neighbor(
                current_position[0] + 1, current_position[1],
                [current_position[0], current_position[1]])
        if flag == 1:
            break
        if current_position[1] - 1 >= 0:
            end_position, flag = judge_neighbor(
                current_position[0], current_position[1] - 1,
                [current_position[0], current_position[1]])
        if flag == 1:
            break
        if current_position[1] + 1 < MAP_COLUMN:
            end_position, flag = judge_neighbor(
                current_position[0], current_position[1] + 1,
                [current_position[0], current_position[1]])
        if flag == 1:
            break
    tmp = end_position
    if flag == 1:
        while tmp[0] != snake_head[0] or tmp[1] != snake_head[1]:
            path.append(tmp)
            tmp = jump_history[hash_xy(tmp[0], tmp[1])]
        path.append(snake_head)
    path.reverse()
    return [path, flag]


# 看看自己能不能找到尾巴
def tailBFS(map, snake_head, snake_tail):
    if snake_head[0] == snake_tail[0] and snake_tail[1] == snake_head[1]:
        return [True, 0]
    bfs_map = map.copy()
    queue = [snake_head]
    length = 0

    def judge_neighbor(current, dst):
        nonlocal queue
        if current[0] == dst[0] and current[1] == dst[1]:
            return True
        if bfs_map[current[0]][current[1]] != -1 and bfs_map[current[0]][
                current[1]] != 2:
            queue.append(current)
            bfs_map[current[0]][current[1]] = -1
        return False

    while len(queue) > 0:
        current_position = queue.pop(0)
        if current_position[0] - 1 >= 0:
            if judge_neighbor([current_position[0] - 1, current_position[1]],
                              snake_tail):
                return [True, length]
        if current_position[0] + 1 < MAP_ROW:
            if judge_neighbor([current_position[0] + 1, current_position[1]],
                              snake_tail):
                return [True, length]
        if current_position[1] - 1 >= 0:
            if judge_neighbor([current_position[0], current_position[1] - 1],
                              snake_tail):
                return [True, length]
        if current_position[1] + 1 < MAP_COLUMN:
            if judge_neighbor([current_position[0], current_position[1] + 1],
                              snake_tail):
                return [True, length]
    return [False, 0]


# 散步哈 TODO
def wander(map, snake_head):
    if snake_head[0] - 1 >= 0 and map[snake_head[0] - 1][snake_head[1]] != 2:
        return 'w'
    if snake_head[0] + 1 < MAP_ROW and map[snake_head[0] +
                                           1][snake_head[1]] != 2:
        return 's'
    if snake_head[1] - 1 >= 0 and map[snake_head[0]][snake_head[1] - 1] != 2:
        return 'a'
    if snake_head[1] + 1 < MAP_COLUMN and map[snake_head[0]][snake_head[1] +
                                                             1] != 2:
        return 'd'
    return 'w'


def get_operate(map, snake_head, path):
    if len(path) < 2:
        return wander(map, snake_head)
    if path[0] < snake_head[0]:
        return 'w'
    if path[0] > snake_head[0]:
        return 's'
    if path[1] < snake_head[1]:
        return 'a'
    if path[1] > snake_head[1]:
        return 'd'
    return wander(map, snake_head)


# 这个函数只走一步，按照snake的speed数量进行多次调用
def Policy(current_map, snake):
    global MAP_ROW
    MAP_ROW = current_map.row
    global MAP_COLUMN
    MAP_COLUMN = current_map.column
    global LEVEL
    LEVEL = current_map.level
    map = transfer_map(current_map.map)
    snake_head = snake.body[0].coordinates
    snake_tail = snake.body[len(snake.body) - 1].coordinates
    # 如果速度大于长度，则wander
    if snake.speed > len(snake.body):
        return wander(map, snake_head)
    # 在BFS过程中找到的第一个食物路径进行判断
    # map = [[0, 1, 0], [0, 2, 0], [0, 2, 0]]
    # snake_head = [2, 1]
    # snake_tail = [2, 1]
    food_path, food_flag = BFS(map, snake_head)
    tail_flag = tailBFS(map, snake_head, snake_tail)
    if food_flag == 1:
        virtual_tail_flag = explore(map, food_path, snake)
        if virtual_tail_flag:
            print("蛇可以去吃食物")
            if len(food_path) < 2:
                return wander(map, snake_head)
            return get_operate(map, snake_head, food_path[1])
        else:
            longest_direction = longest_tail_path(map, snake_head, snake_tail)
            print("蛇该去追尾巴")
            return get_operate(map, snake_head, longest_direction)
    elif tail_flag:
        print("找不到食物了，直接追尾巴")
        longest_direction = longest_tail_path(map, snake_head, snake_tail)
        return get_operate(map, snake_head, longest_direction)
    else:
        # 目前就是哪里不撞走哪里
        return wander(map, snake_head)
