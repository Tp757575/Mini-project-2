import pygame
import random
from queue import Queue

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 30
TILE_SIZE = 20
WINDOW_SIZE = GRID_SIZE * TILE_SIZE
COLORS = {
    "obstacle": (169, 169, 169),
    "open": (34, 139, 34),
    "start": (0, 0, 255),  # Blue
    "goal": (255, 0, 0),   # Red
    "path": (255, 255, 0), # Yellow
    "border": (0, 0, 0),   # Black border
}

# --- Function Descriptions ---

# Generate a grid with random clusters of obstacles
def generate_random_grid(size, clusters=10, cluster_size=20):
   
    grid = [[0] * size for _ in range(size)]
    for _ in range(clusters):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        for _ in range(cluster_size):
            grid[y][x] = 1
            x, y = max(0, min(size - 1, x + random.choice([-1, 1, 0]))), max(0, min(size - 1, y + random.choice([-1, 1, 0])))
    return grid

# Create a clear path between two points
def create_clear_path(grid, start, goal):
   
    x, y = start
    gx, gy = goal
    grid[y][x] = grid[gy][gx] = 0  # Clear start and goal
    while (x, y) != (gx, gy):
        x += (gx > x) - (gx < x)  # Move horizontally toward goal
        y += (gy > y) - (gy < y)  # Move vertically toward goal
        grid[y][x] = 0

# BFS algorithm to find a path
def bfs(map_grid, start, goal, visualize=None):
  
    frontier = Queue()
    frontier.put(start)
    parent = {start: None}
    reached = {start}

    while not frontier.empty():
        current = frontier.get()
        if visualize:
            visualize(current)  # Visualize exploration

        if current == goal:
            # Reconstruct the path from goal to start
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Return path from start to goal

        # Explore all neighbors (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[1] < len(map_grid) and 0 <= neighbor[0] < len(map_grid[0]) 
                    and map_grid[neighbor[1]][neighbor[0]] == 0 
                    and neighbor not in reached):
                frontier.put(neighbor)
                reached.add(neighbor)
                parent[neighbor] = current
    return None

# Draw the grid, start, goal, and path
def draw_map(screen, map_grid, start, goal, path=None):
   
    screen.fill((255, 255, 255))  # Clean (white) screen to work out from
    for y, row in enumerate(map_grid): 
        for x, tile in enumerate(row):
            color = COLORS["obstacle"] if tile else COLORS["open"]
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    draw_tile(screen, start, COLORS["start"], is_special=True)  # Highlight start
    draw_tile(screen, goal, COLORS["goal"], is_special=True)    # Highlight goal
    if path:
        for y, x in path:
            draw_tile(screen, (y, x), COLORS["path"])
    pygame.display.flip()

# Helper to draw a single tile
def draw_tile(screen, pos, color, is_special=False):
   
    x, y = pos
    rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    if is_special:  # Add a border for special tiles (start and goal)
        pygame.draw.rect(screen, COLORS["border"], rect)  # Outer border
        inner_rect = (x * TILE_SIZE + 2, y * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4)
        pygame.draw.rect(screen, color, inner_rect)  # Inner fill
    else:
        pygame.draw.rect(screen, color, rect)  # Normal tile fill

# --- Main Code ---

# Generate grid and random start/goal points
map_grid = generate_random_grid(GRID_SIZE)
start, goal = None, None
while not start or not goal or map_grid[start[1]][start[0]] or map_grid[goal[1]][goal[0]] or abs(start[0] - goal[0]) + abs(start[1] - goal[1]) < 5:
    start = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    goal = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
create_clear_path(map_grid, start, goal)

# Initialize screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("BFS Pathfinding")

# BFS and visualization
path = bfs(map_grid, start, goal, visualize=lambda pos: draw_tile(screen, pos, COLORS["path"]) or pygame.display.flip() or pygame.time.delay(20))

# Main loop
running = True
while running:
    draw_map(screen, map_grid, start, goal, path)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
