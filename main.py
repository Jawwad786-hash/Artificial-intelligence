# ============================================
# 8 Puzzle AI Solver using Python + Pygame
# Interactive AI Project with Hint System
# ============================================
import pygame
import random
import heapq
pygame.init()
# ---------------- WINDOW ----------------
WIDTH = 600
HEIGHT = 780
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8 Puzzle AI Solver")
# ---------------- COLORS ----------------
BG = (15, 15, 25)
TILE = (70, 130, 255)
EMPTY = (35, 35, 50)
TEXT = (255, 255, 255)
BTN = (255, 120, 0)
BTN_HOVER = (255, 160, 50)
GREEN = (0, 220, 120)
RED = (255, 80, 80)
# ---------------- FONTS ----------------
FONT = pygame.font.SysFont("arial", 42, bold=True)
SMALL = pygame.font.SysFont("arial", 24)
MEDIUM = pygame.font.SysFont("arial", 30, bold=True)
# ---------------- SETTINGS ----------------
SIZE = 3
TILE_SIZE = 180
# ---------------- GOAL STATE ----------------
GOAL = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]
# ---------------- INITIAL BOARD ----------------
board = [
    [1,2,3],
    [4,0,6],
    [7,5,8]
]
moves = 0
speed = 300
# ============================================
# BUTTON CLASS
# ============================================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = BTN_HOVER if self.rect.collidepoint(mouse) else BTN
        pygame.draw.rect(WIN, color, self.rect, border_radius=12)
        text = SMALL.render(self.text, True, TEXT)
        WIN.blit(
            text,
            (
                self.rect.x + self.rect.width//2 - text.get_width()//2,
                self.rect.y + self.rect.height//2 - text.get_height()//2
            )
        )
    def clicked(self, pos):
        return self.rect.collidepoint(pos)
# ---------------- BUTTONS ----------------
shuffle_btn = Button(30, 630, 120, 55, "Shuffle")
solve_btn = Button(170, 630, 120, 55, "Solve AI")
reset_btn = Button(310, 630, 120, 55, "Reset")
hint_btn = Button(450, 630, 120, 55, "Hint")
# ============================================
# DRAW BOARD
# ============================================
def draw_board():
    WIN.fill(BG)
    # Title
    title = FONT.render("8 Puzzle AI Solver", True, GREEN)
    WIN.blit(
        title,
        (
            WIDTH//2 - title.get_width()//2,
            20
        )
    )
    # Draw tiles
    for r in range(SIZE):

        for c in range(SIZE):
            value = board[r][c]
            x = c * TILE_SIZE + 25
            y = r * TILE_SIZE + 100
            rect = pygame.Rect(
                x,
                y,
                TILE_SIZE - 10,
                TILE_SIZE - 10
            )
            # Empty tile
            if value == 0:
                pygame.draw.rect(
                    WIN,
                    EMPTY,
                    rect,
                    border_radius=15
                )
            else:
                pygame.draw.rect(
                    WIN,
                    TILE,
                    rect,
                    border_radius=15
                )
                text = FONT.render(str(value), True, TEXT)
                WIN.blit(
                    text,
                    (
                        x + rect.width//2 - text.get_width()//2,
                        y + rect.height//2 - text.get_height()//2
                    )
                )
    # Info
    move_text = MEDIUM.render(f"Moves: {moves}", True, TEXT)
    WIN.blit(move_text, (35, 580))
    # Goal Check
    if board == GOAL:
        win_text = MEDIUM.render("Puzzle Solved!", True, GREEN)
        WIN.blit(
            win_text,
            (
                WIDTH//2 - win_text.get_width()//2,
                580
            )
        )
    # Draw Buttons
    shuffle_btn.draw()
    solve_btn.draw()
    reset_btn.draw()
    hint_btn.draw()
    pygame.display.update()
# ============================================
# FIND EMPTY TILE
# ============================================
def find_zero(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c
# ============================================
# GET NEIGHBORS
# ============================================
def get_neighbors(state):
    neighbors = []
    r, c = find_zero(state)
    directions = [
        (-1,0),
        (1,0),
        (0,-1),
        (0,1)
    ]
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [row[:] for row in state]
            new_state[r][c], new_state[nr][nc] = \
                new_state[nr][nc], new_state[r][c]
            neighbors.append(new_state)
    return neighbors
# ============================================
# MANHATTAN DISTANCE HEURISTIC
# ============================================
def manhattan(state):
    distance = 0
    for r in range(3):
        for c in range(3):
            value = state[r][c]
            if value != 0:
                goal_r = (value - 1) // 3
                goal_c = (value - 1) % 3
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance
# Manhattan Heuristic
# :contentReference[oaicite:0]{index=0}
# ============================================
# CONVERT STATE TO TUPLE
# ============================================
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)
# ============================================
# A* SEARCH ALGORITHM
# ============================================
def solve_puzzle(start):
    pq = []
    heapq.heappush(
        pq,
        (
            0,
            start,
            []
        )
    )
    visited = set()
    while pq:
        cost, current, path = heapq.heappop(pq)
        # Goal Found
        if current == GOAL:
            return path + [current]
        current_tuple = state_to_tuple(current)
        if current_tuple in visited:
            continue
        visited.add(current_tuple)
        for neighbor in get_neighbors(current):
            if state_to_tuple(neighbor) not in visited:
                new_path = path + [current]
                priority = len(new_path) + manhattan(neighbor)

                heapq.heappush(
                    pq,
                    (
                        priority,
                        neighbor,
                        new_path
                    )
                )
    return []
# ============================================
# SHUFFLE BOARD
# ============================================
def shuffle_board():
    global board
    global moves
    for _ in range(50):
        neighbors = get_neighbors(board)
        board = random.choice(neighbors)
    moves = 0
# ============================================
# RESET BOARD
# ============================================
def reset_board():
    global board
    global moves
    board = [
        [1,2,3],
        [4,0,6],
        [7,5,8]
    ]
    moves = 0
# ============================================
# HINT SYSTEM
# ============================================
def show_hint():
    global board
    path = solve_puzzle(board)
    if len(path) > 1:
        board = [row[:] for row in path[1]]
# ============================================
# MOVE TILE
# ============================================
def move_tile(pos):
    global moves
    x, y = pos
    if y < 100 or y > 620:
        return
    c = (x - 25) // TILE_SIZE
    r = (y - 100) // TILE_SIZE
    if not (0 <= r < 3 and 0 <= c < 3):
        return
    zr, zc = find_zero(board)
    # Check adjacency
    if abs(r - zr) + abs(c - zc) == 1:
        board[zr][zc], board[r][c] = \
            board[r][c], board[zr][zc]
        moves += 1
# ============================================
# MAIN LOOP
# ============================================
running = True
while running:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Shuffle
            if shuffle_btn.clicked(pos):
                shuffle_board()
            # Solve AI
            elif solve_btn.clicked(pos):
                path = solve_puzzle(board)
                for step in path:
                    board = [row[:] for row in step]
                    draw_board()
                    pygame.time.delay(speed)
            # Reset
            elif reset_btn.clicked(pos):
                reset_board()
            # Hint
            elif hint_btn.clicked(pos):
                show_hint()
            # Move Tile
            else:
                move_tile(pos)
pygame.quit()
