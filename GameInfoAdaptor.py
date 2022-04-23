import numpy as np
from AStarPolicy import Policy
from Env import Cube
from Env import render

level = 11
length = 55
width = 40

class Snake:
    def __init__(self, position, speed, id):
        self.toGrow = 0
        self.id = id
        self.isDead = False
        self.body = []
        self.speed = speed
        for i in range(len(position)):
            self.body.append(Cube(position[i]))

    def move(self, action, current_map):
        if self.isDead:
            return
        # 先把身体的每个部分都看作尾部
        for body in self.body:
            body.isHead = False
        # 获取动作
        for act in action:
            # 获取头部位置
            head_pos = (self.body[0]).coordinates
            if act == 'w':
                # 向上走
                if head_pos[0] == 0:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos.copy()
                    new_head_pos[0] -= 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if act == 'a':
                # 向上走
                if head_pos[1] == 0:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos.copy()
                    new_head_pos[1] -= 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if act == 'd':
                # 向右走
                if head_pos[1] == width - 1:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos.copy()
                    new_head_pos[1] += 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if act == 's':
                # 向下走
                if head_pos[0] == length - 1:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos.copy()
                    new_head_pos[0] += 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if self.toGrow > 0:
                # 如果有toGrow，尾巴增长
                self.toGrow -= 1
            else:
                # 否则尾巴推近
                tail_pos = self.body.pop()
                current_map[tail_pos.coordinates[0],
                                tail_pos.coordinates[1], self.id - 1] -= 1

# 地图转换
def convert(game_info):
    global length
    length = game_info["Map"]["Length"]
    global width
    width = game_info["Map"]["Width"]
    current_map = np.zeros([game_info["Map"]["Length"], game_info["Map"]["Width"], level])
    # 在地图上放🐍
    for i in range(len(game_info["Map"]["SnakePosition"])):
        snake_position = game_info["Map"]["SnakePosition"][i]
        for j in range(len(snake_position)):
            current_map[snake_position[j][0]][snake_position[j][1]][i] = 1
    # 在地图上放星星
    for i in range(len(game_info["Map"]["SugarPosition"])):
        current_map[game_info["Map"]["SugarPosition"][i][0]][game_info["Map"]["SugarPosition"][i][1]][9] = 1
    # 在地图上放道具
    for i in range(len(game_info["Map"]["PropPosition"])):
        prop_position = game_info["Map"]["PropPosition"]
        for j in range(len(prop_position)):
            current_map[prop_position[i][j][0]][prop_position[i][j][1]][i + 6] = 1
    # 在地图上放墙
    for i in range(len(game_info["Map"]["WallPosition"])):
        current_map[game_info["Map"]["WallPosition"][i][0]][game_info["Map"]["WallPosition"][i][1]][10] = 1
    # 生成🐍
    snake_index = 0
    for i in range(len(game_info["Player"])):
        if game_info["Player"][i]["Name"] == "Ubiq073":
            snake_index = i
            break
    my_snake = Snake(game_info["Map"]["SnakePosition"][snake_index], game_info["Player"][snake_index]["Speed"], snake_index + 1)
    return current_map, my_snake

def my_policy(game_info):
    current_map, snake = convert(game_info)
    actions = ""
    for _ in range(snake.speed):
        tmp = Policy(current_map, snake)
        actions += tmp
        snake.move(tmp, current_map)

    converted_actions = ""
    for i in range(len(actions)):
        a = actions[i]
        if a == 'w':
            converted_actions += 'a'
        if a == 'a':
            converted_actions += 's'
        if a == 's':
            converted_actions += 'd'
        if a == 'd':
            converted_actions += 'w'
    return converted_actions
