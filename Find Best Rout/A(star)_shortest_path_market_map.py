import pygame as pg
from heapq import *


def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_neighbours(x, y):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]#, [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.circle(sc, pg.Color('red'), *get_circle(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


# def heuristic(a, b):
#    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited


cols, rows = 14, 18
TILE = 44


pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# set grid
grid = ['77771999999144',
        '99991999999144',
        '77771111111144',
        '44411111111114',
        '44111111111114',
        '44119911119914',
        '11119911119914',
        '11119911119914',
        '44119911119914',
        '44119911119914',
        '44119911119914',
        '44119911119914',
        '44111111111114',
        '44111111111114',
        '44111111111114',
        '79999711111111',
        '79999711111111',
        '79999719999999']
grid = [[int(char) for char in string ] for string in grid]
# adjacency dict
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

start = (0, 7)
goal = start
queue = []
heappush(queue, (0, start))
visited = {start: None}

bg = pg.image.load('img\mapp.jpg').convert()
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))
while True:
    # fill screen
    sc.blit(bg, (0, 0))

    # bfs, get path to mouse click
    mouse_pos = get_click_mouse_pos()
    if mouse_pos:
        visited = dijkstra(start, mouse_pos, graph)
        goal = mouse_pos

    # print the shortest path in console
    path_head1, path_segment1 = goal, goal
    path1 = []
    while path_segment1:
        path1.append(path_segment1)
        path_segment1 = visited[path_segment1]

    # print('shortest path:', path1[::-1])
    # get the dircetion of the shortest path (up, down, left, right)
    path_head, path_segment = goal, goal
    path = []
    while path_segment:
        path.append(path_segment)
        path_segment = visited[path_segment]
    path = path[::-1]
    # print('path:', path)
    direction = []
    for i in range(len(path)-1):
        if path[i][0] - path[i+1][0] == 1:
            direction.append('left')
        elif path[i][0] - path[i+1][0] == -1:
            direction.append('right')
        elif path[i][1] - path[i+1][1] == 1:
            direction.append('up')
        elif path[i][1] - path[i+1][1] == -1:
            direction.append('down')
    # print('direction:', direction)

    # print the shortest path and path and directions when the mouse is clicked
    if mouse_pos:
        print('shortest path:', path1[::-1])
        print('path:', path)
        print('direction:', direction)

    

    # draw path
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.circle(sc, pg.Color('blue'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(sc, pg.Color('green'), *get_circle(*start))
    pg.draw.circle(sc, pg.Color('white'), *get_circle(*path_head))

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(30)

    # make the start of the path the end of the previous path
    start = path_head

    