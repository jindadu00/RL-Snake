longest_way = []
current_way = []

def my_get_longest_way(map_2d, x, y, row, col):
    global longest_way
    global current_way

    current_way.append([x, y])
    map_2d[x][y] = -1
    if len(current_way) > len(longest_way):
        longest_way = current_way.copy()

    if x >= 0 and map_2d[x - 1][y] != 2 and map_2d[x - 1][y] != -1:
        my_get_longest_way(map_2d, x - 1, y, row, col)
    if x < row and map_2d[x + 1][y] != 2 and map_2d[x + 1][y] != -1:
        my_get_longest_way(map_2d, x + 1, y, row, col)
    if y >= 0 and map_2d[x][y - 1] != 2 and map_2d[x][y - 1] != -1:
        my_get_longest_way(map_2d, x, y - 1, row, col)
    if y < col and map_2d[x][y + 1] != 2 and map_2d[x][y + 1] != -1:
        my_get_longest_way(map_2d, x - 1, y, row, col)

def get_operate(index):
    if longest_way[index - 1][0] < longest_way[index][0]:
        return 's'
    if longest_way[index - 1][0] > longest_way[index][0]:
        return 'w'
    if longest_way[index - 1][1] < longest_way[index][1]:
        return 'd'
    return 'a'

def get_longest_way(map_2d, x, y, row, col):
    my_get_longest_way(map_2d, x, y, row, col)
    return longest_way

def get_longest_way_options(map_2d, x, y, row, col):
    my_get_longest_way(map_2d, x, y, row, col)
    res = ""
    for i in range(1, len(longest_way)):
        res += get_operate(i)
    return longest_way, res
