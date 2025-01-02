import pygame
import math
from heapq import heappop, heappush

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 255, 0),
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'PURPLE': (128, 0, 128),
    'ORANGE': (255, 165, 0),
    'GREY': (128, 128, 128),
    'TURQUOISE': (64, 224, 208)
}

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLORS['WHITE']
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLORS['RED']

    def is_open(self):
        return self.color == COLORS['GREEN']

    def is_barrier(self):
        return self.color == COLORS['BLACK']

    def is_start(self):
        return self.color == COLORS['ORANGE']

    def is_end(self):
        return self.color == COLORS['TURQUOISE']

    def reset(self):
        self.color = COLORS['WHITE']

    def make_start(self):
        self.color = COLORS['ORANGE']

    def make_closed(self):
        self.color = COLORS['RED']

    def make_open(self):
        self.color = COLORS['GREEN']

    def make_barrier(self):
        self.color = COLORS['BLACK']

    def make_end(self):
        self.color = COLORS['TURQUOISE']

    def make_path(self):
        self.color = COLORS['PURPLE']

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT
        for dr, dc in directions:
            new_row, new_col = self.row + dr, self.col + dc
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows and not grid[new_row][new_col].is_barrier():
                self.neighbors.append(grid[new_row][new_col])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = []
    heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = set([start])

    while open_set:
        current = heappop(open_set)
        current = current[2]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLORS['GREY'], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, COLORS['GREY'], (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(COLORS['WHITE'])

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()

                    elif not end and spot != start:
                        end = spot
                        end.make_end()

                    elif spot != end and spot != start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)
            except Exception as e:
                print(f"An error occurred: {e}")
                run = False

    pygame.quit()

main(WIN, WIDTH)
