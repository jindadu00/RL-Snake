from ast import Pass
from pickle import FALSE
import numpy as np


# myinit
class Cube:

    def __init__(self, coordinates, isHead=True):
        self.coordinates = coordinates
        # coordinates  -->  np.array([x,y])
        # 屏幕左上角为[0,0],
        # 右上角为[0,current_map.column-1],
        # 左下角为[current_map.row-1,0],
        # 右下角为[current_map.row-1,current_map.column-1],
        # TODO
        self.isHead = isHead


class Map:

    def __init__(self):
        """
        self.level: [0, 5], indicating snake 1, 2, 3, 4, 5, 6; 
                    [6, 9], indicating speed, strength, double star, star;
                    [10], indicating wall cell;
        """
        self.row = 100
        self.column = 100
        self.level = 11
        self.map = np.zeros([self.row, self.column, self.level])


class Snake:

    def __init__(self, id):
        self.isDead = False
        self.body = []  # 这是一个Cube的列表
        self.powerTime = 0
        self.speed = 1
        self.speedTime = 0
        self.doubleTime = 0
        self.toGrow = 0
        self.id = id  #1~6蛇的编号
        self.score = 0

    def eat_star(self, num):
        if self.doubleTime > 0:
            self.toGrow += num * 2
        else:
            self.toGrow += num

    def eat_power_prop(self):
        self.powerTime += 5

    def eat_speed_prop(self):
        self.speed += 1
        self.speedTime += 5

    def eat_double_prop(self):
        self.doubleTime += 5

    # action是行动列表，比如"左,右,左"这种，就用['a', 'd', 'a']表示
    # 改current_map中自己的位置
    def move(self, action, current_map):
        # TODO
        # 先把身体的每个部分都看作尾部
        for body in self.body:
            body.isHead = False
        # 获取动作
        for act in action:
            # 获取头部位置
            head_pos = (self.body[0]).coordinates
            if act == 'a':
                # 向左走
                if head_pos[0] == 0:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos[0].copy()
                    new_head_pos[0] -= 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map.map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if act == 'w':
                # 向上走
                if head_pos[1] == 0:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos[0].copy()
                    new_head_pos[1] -= 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map.map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if act == 'd':
                # 向右走
                if head_pos[1] == current_map.column - 1:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos[0].copy()
                    new_head_pos[1] += 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map.map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if act == 's':
                # 向下走
                if head_pos[0] == current_map.row - 1:
                    # 碰到墙
                    self.isDead = True
                    return
                else:
                    # 没碰到墙
                    new_head_pos = head_pos[0].copy()
                    new_head_pos[0] += 1
                    self.body.insert(0, Cube(new_head_pos))
                    current_map.map[new_head_pos[0], new_head_pos[1],
                                    self.id - 1] += 1

            if self.toGrow > 0:
                # 如果有toGrow，尾巴增长
                self.toGrow -= 1
            else:
                # 否则尾巴推近
                tail_pos = self.body.pop()
                current_map.map[tail_pos[0], tail_pos[1], self.id - 1] -= 1

    def reduce_length(self, current_map):
        # TODO
        pass

    def reduce_props(self):
        if self.doubleTime > 0:
            self.doubleTime -= 1
        if self.speedTime > 0:
            self.speedTime -= 1
            if self.speedTime == 0:
                self.speed = 1
        if self.powerTime > 0:
            self.powerTime -= 1


def gen_head_matrix(snakes, current_map):
    """
    return:
        np.array(W, H, L)
    """
    head_matrix = np.zeros_like(current_map.map[:, :, :6])
    for i, snake in enumerate(snakes):
        if snake.isDead:
            continue
        for cube in snake.body:
            if cube.isHead:
                head_matrix[cube.coordinate[0], cube.coordinate[1]] = 1

    return head_matrix


def passive_killing(snake_A, snake_B, head_matrix, next_head_matrix):
    """
    adding B's score in passive killing.
    """
    powered_A, powered_B = snake_A.powerTime > 0, snake_B.powerTime > 0

    if powered_A:
        # TODO:
        pass
    else:
        # A passively killed by B
        snake_A.isDead = True
        # B get pts
        snake_B.score += 1.5 * 1


def active_killing(snake_A, snake_B, head_matrix, next_head_matrix):
    """
    only adds A's score in active killing
    input:
        head_matrix: [W, H, 2], layer 0 indicating A, layer 1 indicating B
        next_head_matrix: [W, H, 2], layer 0 indicating A, layer 1 indicating B
    """
    powered_A, powered_B = snake_A.powerTime > 0, snake_B.powerTime > 0
    len_A, len_B = len(snake_A.body), len(snake_B.body)
    if not powered_A and not powered_B:
        if len_A == len_B:
            snake_A.isDead = True
            snake_B.isDead = True
        elif len_A > len_B:
            snake_B.isDead = True
            snake_A.score += 1.5 * 2
        else:
            snake_A.is_Dead = True
    elif powered_A and not powered_B:
        snake_B.isDead = True
        snake_A.score = 1.5 * 2
    elif powered_B and not powered_A:
        snake_A.isDead = True
    else:
        overlap_inds_xy = np.where(np.sum(head_matrix, axis=2) == 2)
        if overlap_inds_xy[0].shape > 0:
            next_head_matrix = next_head_matrix * 0

        # eye_mat = np.ones_like(next_head_matrix)
        # eye_mat[overlap_inds[0], overlap_inds[1], :] = 0
        # next_head_matrix = next_head_matrix * eye_mat


def update_body(snakes, snakes_matrix):
    for i, snake in enumerate(snakes):
        snake_matrix = snakes_matrix[:, :, i]
        snake.body = [
            cell for cell in snake.body
            if snake_matrix[cell.coordinate[0], cell.coordinate[0]]
        ]


def detect_collision(current_map, snakes):
    """
    correcting collision relation.
    input:
        current_map: np.array(W, H, L)
    """
    # init snakes_tail_matrix, head_matrix where snakes_matrix = tail_matrix + head_matrix
    snakes_matrix = current_map.map[:, :, 0:6]
    head_maxtrix = gen_head_matrix(snakes, current_map)
    tail_matrix = snakes_matrix - head_maxtrix
    next_head_matrix = head_maxtrix.copy()

    # hit conditions records
    # 0: head hit tail
    # 1: head hit head
    hit_records = np.zeros((6, 6, 2))
    for i, snake in snakes:
        if snake.isDead:
            continue
        # judge head hit head
        snake_i_head = np.repeat(head_maxtrix[:, :, i:i + 1],
                                 repeats=6,
                                 axis=2)
        hh_idxs = np.unique(np.where(snake_i_head == head_maxtrix)[2])
        # judge head hit tail
        ht_idxs = np.unique(np.where(snake_i_head == tail_matrix)[2])
        # record
        hit_records[i, hh_idxs, 0] = 1
        hit_records[i, ht_idxs, 1] = 1
        hit_records[i, i, :] = 0
    #TODO: suicide

    # handle hit between snakes
    for idx_A in hit_records.shape[0]:
        for idx_B in hit_records.shape[1]:
            hh_hit, ht_hit = hit_records[idx_A,
                                         idx_B, :][0], hit_records[idx_A,
                                                                   idx_B, :][1]
            if hh_hit == 0 and ht_hit == 0:
                continue
            elif hh_hit == 0 and ht_hit == 1:
                passive_killing(snakes[idx_A], snakes[idx_B],
                                head_maxtrix[:, :, [idx_A, idx_B]],
                                next_head_matrix[:, :, [idx_A, idx_B]])
            elif hh_hit == 1 and ht_hit == 0:
                # active killing
                active_killing(snakes[idx_A], snakes[idx_B],
                               head_maxtrix[:, :, [idx_A, idx_B]],
                               next_head_matrix[:, :, [idx_A, idx_B]])
            else:
                # TODO:
                pass

    # handle hit between snake and wall
    wall = np.repeat(current_map.map[:, :, -1:], repeats=6, axis=2)
    hit_wall_idxs = np.unique(
        np.where((wall == snakes_matrix) & (snakes_matrix == 1))[0])
    for snake_idx in hit_wall_idxs:
        snakes[snake_idx].isDead = True

    # declibe length < 1 's snakes
    snakes_matrix = tail_matrix + next_head_matrix
    zero_len_idx = np.unique(np.where(snakes_matrix.sum(axis=(0, 1)) == 0)[0])
    for snake_idx in zero_len_idx:
        snakes[snake_idx].isDead = True

    # update maps and snakes' body
    current_map.map[:, :, 0:6] = snakes_matrix
    update_body(snakes, snakes_matrix)


def get_props(current_map):
    pass


def sample_action():
    pass


def render():

    pass


def reset():
    pass


# 刷新道具（随机按照正态分布）、地图缩圈
def resource_refresh(snakes, current_map, current_round):
    global wall_flag
    if wall_flag == False:
        map_size = current_map.column * current_map.row
        empty_space = map_size - np.sum(current_map)
        if empty_space < 400:
            wall_flag = True
            #在第一次空区域小于400的时候，触发墙壁刷新停止机制

    elif current_round < 100:
        pass
    else:
        if current_round % 5 == 0:
            wall_refresh(current_map, current_round)

        else:
            pass

    #刷新星星
    N_star = 200 + current_round
    R_star = 100 + min(current_round * 10, 200)
    N_curstar = current_map[:, :, 9].sum()
    for i in range(R_star):
        if N_curstar >= N_star:
            break
        else:
            [newstar_posx, newstar_posy] = genpos_normal()  #返回服从正态分布的坐标

            if 1 in current_map[newstar_posx, newstar_posy, :]:
                continue
            else:
                current_map[newstar_posx, newstar_posy, 9] = 1
                N_curstar += 1
    #刷新速度、力量、双倍道具
    if current_round == 1:
        N_props = [50, 50, 50]
    else:
        N_props = [60 + int(current_round * 0.2), 40, 50]

    R_props = 10 + min(current_round * 10, 100)
    #速度
    N_curspeed = current_map[:, :, 6].sum()
    for i in range(R_props):
        if N_curspeed >= N_props[0]:
            break
        else:
            [newspeed_posx, newspeed_posy] = genpos_normal()
            if 1 in current_map[newspeed_posx, newspeed_posy, :]:
                continue
            else:
                current_map[newspeed_posx, newspeed_posy, 6] = 1
                N_curspeed += 1
    #力量
    N_curstrength = current_map[:, :, 7].sum()
    for i in range(R_props):
        if N_curstrength >= N_props[1]:
            break
        else:
            [newstrength_posx, newstrength_posy] = genpos_normal()
            if 1 in current_map[newstrength_posx, newstrength_posy, :]:
                continue
            else:
                current_map[newstrength_posx, newstrength_posy, 7] = 1
                N_curstrength += 1

    #双倍
    N_curdouble = current_map[:, :, 8].sum()
    for i in range(R_props):
        if N_curdouble >= N_props[2]:
            break
        else:
            [newdouble_posx, newdouble_posy] = genpos_normal()
            if 1 in current_map[newdouble_posx, newdouble_posy, :]:
                continue
            else:
                current_map[newdouble_posx, newdouble_posy, 8] = 1
                N_curdouble += 1


def wall_refresh(current_map, current_round):
    global wall_refresh_times
    toupdatewall_index = np.where(current_map.sum(axis=3) == 0)

    for i in range(np.size(toupdatewall_index[0])):
        rowflag = (toupdatewall_index[0][i] < wall_refresh_times) or ...
        (toupdatewall_index[0][i] >= current_map.row - wall_refresh_times)

        colflag = (toupdatewall_index[1][i] < wall_refresh_times) or ...
        (toupdatewall_index[1][i] >= current_map.column - wall_refresh_times)

        if rowflag and colflag:
            current_map[toupdatewall_index[0][i], toupdatewall_index[1][i],
                        10] = 1
        else:
            continue
    wall_refresh_times += 1


def genpos_normal(current_map):
    center = [current_map.column / 2, current_map.row / 2]
    x = np.random.normal(0, 10, 1)
    y = np.random.normal(0, 10, 1)
    if x < -center[0]:
        x = -center[0]
    elif x >= center[0] - 1:
        x = -center[0] - 1

    if y < -center[1]:
        y = -center[1]
    elif y >= center[1] - 1:
        y = -center[1] - 1
    return [round(x) + center[0], round(y) + center[1]]


if __name__ == "__main__":
    current_map = Map()
    snake_list = [Snake(1), Snake(2), Snake(3), Snake(4), Snake(5), Snake(6)]
    wall_flag = FALSE
    wall_refresh_times = 0

    while True:
        reset()

        for snake in snake_list:
            snake.reduce_props()

        for snake in snake_list:
            snake.move()

        detect_collision()

        for snake in snake_list:
            snake.reduce_length()

        get_props()

        resource_refresh()

        render()
