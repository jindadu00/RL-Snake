from Env import *

level = 11
length = 55
width = 40


def co_map(cor):
    mapCor = [width - cor[1] - 1, cor[0]]
    return mapCor


def MapConverter(game_info):
    my_map = Map()
    # current_map = np.zeros([game_info["Map"]["Length"], game_info["Map"]["Width"], level])
    # 在地图上放🐍
    for i in range(len(game_info["Map"]["SnakePosition"])):
        snake_position = game_info["Map"]["SnakePosition"][i]
        for j in range(len(snake_position)):
            position = co_map(snake_position[j])
            my_map.map[position[0]][position[1]][i] = 1
    # 在地图上放星星
    for i in range(len(game_info["Map"]["SugarPosition"])):
        position = co_map(game_info["Map"]["SugarPosition"][i])
        my_map.map[position[0]][position[1]][9] = 1
    # 在地图上放道具
    for i in range(len(game_info["Map"]["PropPosition"])):
        prop_position = game_info["Map"]["PropPosition"]
        for j in range(len(prop_position[i])):
            position = co_map(prop_position[i][j])
            my_map.map[position[0]][position[1]][i + 6] = 1
    # 在地图上放墙
    for i in range(len(game_info["Map"]["WallPosition"])):
        position = co_map(game_info["Map"]["WallPosition"][i])
        my_map.map[position[0]][position[1]][10] = 1
    return my_map


def SnakeConverter(game_info):
    # 生成🐍
    snake_index = 0
    for i in range(len(game_info["Player"])):
        if game_info["Player"][i]["Name"] == "Ubiq073":
            snake_index = i
            break
    my_snake = Snake(snake_index + 1, [], [], True)
    position = game_info["Map"]["SnakePosition"][snake_index]
    my_snake.speed = game_info["Player"][snake_index]["Speed"]
    my_snake.body = []
    for i in range(len(position)):
        my_snake.body.append(Cube(co_map(position[i])))
    return my_snake

def SnakesConverter(game_info):
    snake_list = []
    for i in range(len(game_info)):
        my_snake = Snake(i + 1, [], [], True)
        position = game_info["Map"]["SnakePosition"][i]
        my_snake.speed = game_info["Player"][i]["Speed"]
        my_snake.body = []
        for j in range(len(position)):
            my_snake.body.append(Cube(co_map(position[j])))
        snake_list.append(my_snake)
    return snake_list
