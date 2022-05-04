res = ""
max_score = 0

def violentSearchDevelopment(current_map, snake):

    def backtrack(k):
        if k == v:
            score = compute_score(current_map, actions, snake.body[0].coordinates)
            global max_score
            global res
            if score > max_score:
                max_score = score
                res = actions
            return
        if k == 0:
            for i in range(4):
                actions.append(actions_list[i])
                backtrack(k + 1)
                actions.pop()
        else:
            for i in range(4):
                if actions_list[i] != actions[-1]:
                    actions.append(actions_list[i])
                    backtrack(k + 1)
                    actions.pop()

    V = snake.speed
    actions_list = ['w', 'a', 's', 'd']
    for v in range(1, V + 1):
        actions = []
        backtrack(0)
    return res

def get_way(actions, start):
    way = []
    p = start
    for i in range(len(actions)):
        if actions[i] == 'w':
            way.append([p[0] - 1, p[1]])
        elif actions[i] == 's':
            way.append([p[0] + 1, p[1]])
        elif actions[i] == 'a':
            way.append([p[0], p[1] - 1])
        else:
            way.append([p[0], p[1] + 1])
    return way

def compute_score(current_map, actions, start):
    way = get_way(actions, start)
    # 判断边界条件、蛇碰撞、墙碰撞
    for i in range(len(way)):
        p = way[i]
        if p[0] >= current_map.row or p[0] < 0 or p[1] < 0 or p[1] >= current_map.column:
            return 0
        for j in range(6):
            if current_map.map[j][p[0]][p[1]] != 0:
                return 0
        if current_map.map[10][p[0]][p[1]] != 0:
            return 0
    # 统计吃的各种道具数量
    double_star = 1
    star = 1
    strength = 1
    speed = 1
    for i in range(len(way)):
        p = way[i]
        if current_map.map[6][p[0]][p[1]] != 0:
            speed += 1
        if current_map.map[7][p[0]][p[1]] != 0:
            strength += 1
        if current_map.map[8][p[0]][p[1]] != 0:
            double_star += 1
        if current_map.map[9][p[0]][p[1]] != 0:
            star += 1
    return double_star * star * strength * speed
