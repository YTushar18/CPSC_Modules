import random
from collections import deque

def generate_maze(width, height):
    maze = [['#' for _ in range(width)] for _ in range(height)]

    for i in range(1, height, 2):
        for j in range(1, width, 2):
            maze[i][j] = ' '

    for i in range(1, height, 2):
        for j in range(2, width-1, 2):
            if random.randint(0, 1) == 1:
                maze[i][j] = ' '

    for i in range(2, height-1, 2):
        for j in range(1, width, 2):
            if random.randint(0, 1) == 1:
                maze[i][j] = ' '

    maze[0][1] = 'S'
    maze[height-1][width-2] = 'G'

    return maze

# Function to print the maze
def print_maze(maze):
    for row in maze:
        print(' '.join(row))

# Function to find the shortest path using Breadth-First Search
def bfs(maze):
    start = None
    goal = None

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'G':
                goal = (i, j)

    queue = deque([(start, [])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path + [(x, y)]
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '#' and (new_x, new_y) not in visited:
                queue.append(((new_x, new_y), path + [(x, y)]))

    return None

# Function to generate and print a new maze
def regenerate_maze(cols, rows):
    maze = generate_maze(cols, rows)
    print("\nRandom Maze:")
    print_maze(maze)
    return maze

def visualize_path(path, maze):
    for i, (x, y) in enumerate(path):
            if maze[x][y] == ' ':
                # maze[x][y] = str(i % 10)
                maze[x][y] = str(i)
    print("\nShortest Path:")
    print_maze(maze)
    print(f"\nShortest path length: {len(path)} steps")



def control_function():
    while True:
        rows = int(input("Enter the number of rows: "))
        cols = int(input("Enter the number of columns: "))
        maze = regenerate_maze(cols, rows)

        path = bfs(maze)

        if path:
            visualize_path(path, maze)
        else:
            print("\nNo path found!")

        choice = input("\nDo you want to regenerate the maze? (y/n): ")
        if choice.lower() != 'y':
            break

if __name__ == "__main__":
    control_function()