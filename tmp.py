import numpy as np


class Cube:
    def __init__(self):
        self.x = 0
        self.y = 0
        # TODO
        self.isHead = False


class Snake:
    def __init__(self):
        self.isDead = False
        self.body = [] # 这是一个Cube的列表
        self.powerTime = 0
        self.speed = 1
        self.speedTime = 0
        self.doubleTime = 0
        self.toGrow = 0

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


def detect_collision(current_map):
    pass


# 刷新道具（随机按照正态分布）、地图缩圈
def resource_refresh(snakes, current_map, current_round):
    pass


class Map:
    def __init__(self):
        self.row = 100
        self.column = 100
        self.level = 3
        self.map = np.zeros([self.row, self.column, self.level])


if __name__ == "__main__":
    while True:
        pass
