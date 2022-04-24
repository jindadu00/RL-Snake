import numpy as np
from AStarPolicy import Policy
from Env import *
from Converter import *

level = 11
length = 55
width = 40

def my_policy(game_info, Num_):
    current_map = MapConverter(game_info)
    render(current_map)
    actions = ""
    if game_info["Player"][Num_]["IsDead"]:
        return "w"
    my_snake = SnakeConverter(game_info)
    for _ in range(my_snake.speed):
        tmp = Policy(current_map, my_snake)
        actions += tmp
        my_snake.move(tmp, current_map)
    return actions
