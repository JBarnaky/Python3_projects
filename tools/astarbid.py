import pygame
from heapq import heappop, heappush

# Constants
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Bi-directional A* Path Finding Algorithm")

COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
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
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows:
                neighbor = grid[new_row][new_col]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)

    def __lt__(self, other):
        return False  # Required for heapq comparison

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, forward=True):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def bidirectional_a_star(draw, grid, start, end):
    count = 0
    open_set_start = []  # Priority queue for start
    open_set_end = []    # Priority queue for end
    heappush(open_set_start, (0, count, start))
    heappush(open_set_end, (0, count, end))

    came_from_start = {}
    came_from_end = {}

    g_score_start = {spot: float('inf') for row in grid for spot in row}
    g_score_start[start] = 0

    f_score_start = {spot: float('inf') for row in grid for spot in row}
    f_score_start[start] = h(start.get_pos(), end.get_pos())

    g_score_end = {spot: float('inf') for row in grid for spot in row}
    g_score_end[end] = 0

    f_score_end = {spot: float('inf') for row in grid for spot in row}
    f_score_end[end] = h(end.get_pos(), start.get_pos())

    open_set_hash_start = {start}
    open_set_hash_end = {end}

    while open_set_start and open_set_end:
        # Process forward search
        current_start = heappop(open_set_start)[2]
        open_set_hash_start.remove(current_start)

        if current_start in open_set_hash_end:
            reconstruct_path(came_from_start, current_start, draw)
            reconstruct_path(came_from_end, current_start, draw, forward=False)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current_start.neighbors:
            temp_g_score = g_score_start[current_start] + 1
            if temp_g_score < g_score_start[neighbor]:
                came_from_start[neighbor] = current_start
                g_score_start[neighbor] = temp_g_score
                f_score_start[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash_start:
                    count += 1
                    heappush(open_set_start, (f_score_start[neighbor], count, neighbor))
                    open_set_hash_start.add(neighbor)
                    if neighbor != start and neighbor != end:
                        neighbor.make_open()

        draw()

        if current_start != start and current_start != end:
            current_start.make_closed()

        # Process backward search
        current_end = heappop(open_set_end)[2]
        open_set_hash_end.remove(current_end)

        if current_end in open_set_hash_start:
            reconstruct_path(came_from_end, current_end, draw, forward=False)
            reconstruct_path(came_from_start, current_end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current_end.neighbors:
            temp_g_score = g_score_end[current_end] + 1
            if temp_g_score < g_score_end[neighbor]:
                came_from_end[neighbor] = current_end
                g_score_end[neighbor] = temp_g_score
                f_score_end[neighbor] = temp_g_score + h(neighbor.get_pos(), start.get_pos())
                if neighbor not in open_set_hash_end:
                    count += 1
                    heappush(open_set_end, (f_score_end[neighbor], count, neighbor))
                    open_set_hash_end.add(neighbor)
                    if neighbor != start and neighbor != end:
                        neighbor.make_open()

        draw()

        if current_end != start and current_end != end:
            current_end.make_closed()

    return False

def make_grid(rows, width):
    gap = width // rows
    return [[Spot(i, j, gap, rows) for j in range(rows)] for i in range(rows)]

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLORS['GREY'], (0, i * gap), (width, i * gap))
        pygame.draw.line(win, COLORS['GREY'], (i * gap, 0), (i * gap, width))

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
    return y // gap, x // gap

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start, end = None, None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif pygame.mouse.get_pressed()[0]:  # Left click
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
            elif pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bidirectional_a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start, end = None, None
                    grid = make_grid(ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
