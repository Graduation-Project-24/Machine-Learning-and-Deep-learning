from heapq import *
import requests

class Map:
    def __init__(self, grid):
        self.grid = grid
        self.cols = len(grid[0])
        self.rows = len(grid)
        self.graph = {}
        self.full_path = []

    def get_neighbours(self, x, y):
        check_neighbour = lambda x, y: 0 <= x < self.cols and 0 <= y < self.rows
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(self.grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]

    def build_graph(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_neighbours(x, y)

    def find_shortest_path(self, start, goal):
        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while queue:
            cur_cost, cur_node = heappop(queue)
            if cur_node == goal:
                break

            neighbours = self.graph[cur_node]
            for neighbour in neighbours:
                neigh_cost, neigh_node = neighbour
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    priority = new_cost + self.heuristic(neigh_node, goal)
                    heappush(queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node
        return visited

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_directions(self, start, goals):
        car_direction = 'right'
        goals.append(start)
        for goal in goals:
            if goal:
                visited = self.find_shortest_path(start, goal)
                path_head, path_segment = goal, goal
                path = []
                while path_segment:
                    path.append(path_segment)
                    path_segment = visited[path_segment]
                path = path[::-1]
                direction = []

                for i in range(len(path)-1):
                    if car_direction == 'right':
                        if path[i][0] - path[i+1][0] == 1:
                            direction.append('backward')
                            car_direction = 'left'
                        elif path[i][0] - path[i+1][0] == -1:
                            direction.append('forward')
                            car_direction = 'right'
                        elif path[i][1] - path[i+1][1] == 1:
                            direction.append('left')
                            car_direction = 'up'
                        elif path[i][1] - path[i+1][1] == -1:
                            direction.append('right')
                            car_direction = 'down'
                    elif car_direction == 'left':
                        if path[i][0] - path[i+1][0] == 1:
                            direction.append('forward')
                            car_direction = 'left'
                        elif path[i][0] - path[i+1][0] == -1:
                            direction.append('backward')
                            car_direction = 'right'
                        elif path[i][1] - path[i+1][1] == 1:
                            direction.append('right')
                            car_direction = 'up'
                        elif path[i][1] - path[i+1][1] == -1:
                            direction.append('left')
                            car_direction = 'down'
                    elif car_direction == 'up':
                        if path[i][0] - path[i+1][0] == 1:
                            direction.append('left')
                            car_direction = 'left'
                        elif path[i][0] - path[i+1][0] == -1:
                            direction.append('right')
                            car_direction = 'right'
                        elif path[i][1] - path[i+1][1] == 1:
                            direction.append('forward')
                            car_direction = 'up'
                        elif path[i][1] - path[i+1][1] == -1:
                            direction.append('backward')
                            car_direction = 'down'
                    elif car_direction == 'down':
                        if path[i][0] - path[i+1][0] == 1:
                            direction.append('right')
                            car_direction = 'left'
                        elif path[i][0] - path[i+1][0] == -1:
                            direction.append('left')
                            car_direction = 'right'
                        elif path[i][1] - path[i+1][1] == 1:
                            direction.append('backward')
                            car_direction = 'up'
                        elif path[i][1] - path[i+1][1] == -1:
                            direction.append('forward')
                            car_direction = 'down'

                if goal:
                    print('path:', path)
                    print('direction:', direction)
                    self.full_path.append(direction)


                start = path_head

        print('end')
        print('full_path:', self.full_path)

def get_points_from_api():
    try:
        request = requests.get('https://www.smarketp.somee.com/api/Product/GetProductsWithAxies')
        request.raise_for_status()
        full_data = request.json()
        points = [(data['xAxies'], data['yAxies']) for data in full_data]
        return points
    except requests.exceptions.RequestException as e:
        print(f"Error in making the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return []

def main():
    grid = [
        '111111111',
        '111111111',
        '111199111',
        '111199111',
        '111199111',
        '111199111',
        '111111111',
        '111111111',
        '111111111'
    ]
    grid = [[int(char) for char in string] for string in grid]

    map_obj = Map(grid)
    map_obj.build_graph()
    points = get_points_from_api()
    map_obj.find_directions((0, 0), points)

if __name__ == "__main__":
    main()
