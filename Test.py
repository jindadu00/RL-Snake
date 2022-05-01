import os
import numpy as np
import time
from Env import Map
from Env import Snake
from Env import detect_collision
from Env import render
from Env import resource_refresh
from Env import get_props

if __name__ == "__main__":
    tmp = [1, 2, 3, 4, 5]
    print(tmp.pop())
    mode = os.getenv("mode")
    current_map = Map()
    c = current_map.column
    r = current_map.row
    snake_list = [
        Snake(1, np.array([0, 0]), current_map),
        Snake(2, np.array([0, 20]), current_map),
        Snake(3, np.array([round(r / 3), round(3 * c / 4)]), current_map),
        Snake(4, np.array([round(2 * r / 3), round(c / 4)]), current_map),
        Snake(5, np.array([round(2 * r / 3),
                           round(2 * c / 4)]), current_map),
        Snake(6, np.array([round(2 * r / 3),
                           round(3 * c / 4)]), current_map)
    ]
    if mode == "测试用例1":
        # snake_a = Snake(1, np.array([0, 0]), current_map)
        # snake_b = Snake(1, np.array([0, 20]), current_map)
        for i in range(30):
            render(current_map)
            action = "d"
            snake_list[0].move(action, current_map)
            detect_collision(current_map, snake_list)
            time.sleep(0.1)
    elif mode == "测试用例2":
        snake_list[0].powerTime = 40
        snake_list[1].powerTime = 40
        current_map.map[0][10][9] = 1
        for i in range(30):
            render(current_map)
            action = "d"
            snake_list[0].move(action, current_map)
            detect_collision(current_map, snake_list)
            get_props(current_map, snake_list)
            time.sleep(0.2)
    elif mode == "测试用例3":
        for i in range(30):
            render(current_map)
            action = "a"
            snake_list[2].move(action, current_map)
            detect_collision(current_map, snake_list)
            time.sleep(0.1)
        if snake_list[2].isDead:
            print("测试用例3通过测试")
    elif mode == "测试用例4":
        snake_list[2].powerTime = 40
        # round(r / 3), round(3 * c / 4)
        current_map.map[round(r / 3)][round(3 * c / 4) - 5][9] = 1
        for i in range(30):
            render(current_map)
            action = "a"
            snake_list[2].move(action, current_map)
            detect_collision(current_map, snake_list)
            get_props(current_map, snake_list)
            time.sleep(0.1)
        if snake_list[2].isDead:
            print("测试用例3通过测试")
    # 测试速度药水+双倍星星
    elif mode == "测试用例5":
        print("l")
    # 测试蛇存活时间增长与存活
    elif mode == "测试用例6":
        print("l")
    # 速度快穿墙
    elif mode == "测试用例7":
        # current_map.map[round(r / 3)][round(3 * c / 4) - 5][10] = 1
        for i in range(30):
            render(current_map)
            action = "a"
            snake_list[2].move(action, current_map)
            detect_collision(current_map, snake_list)
            get_props(current_map, snake_list)
            if snake_list[2].isDead:
                print("测试成功")
                break
            time.sleep(0.1)
    # 掉头咬自己长度衰减直到长度小于1死掉
    elif mode == "测试用例8":
        print("l")
    # 速度药水效果（时间与加成速度的值），力量药水，双倍药水的时间
    elif mode == "测试用例9":
        print("l")