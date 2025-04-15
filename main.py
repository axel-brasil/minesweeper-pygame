#!/bin/python3

import pygame
from pygame.locals import *
from random import randint
from collections import deque

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 40
GRID_SIZE = WIDTH // TILE_SIZE
FONT_SIZE = 32

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campo Minato")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

# Draw grid lines
def draw_grid():
    for i in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, "white", (i, 0), (i, HEIGHT))
        pygame.draw.line(screen, "white", (0, i), (WIDTH, i))

# Generate 2D bomb grid
def generate_board():
    board = []
    for y in range(GRID_SIZE):
        row = []
        for x in range(GRID_SIZE):
            cell = '*' if randint(0, 10) == 1 else '0'
            row.append(cell)
        board.append(row)
    return board

# Count adjacent bombs and update numbers
def update_board(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == '*':
                continue
            count = sum(
                board[r + dr][c + dc] == '*'
                for dr, dc in DIRECTIONS
                if 0 <= r + dr < GRID_SIZE and 0 <= c + dc < GRID_SIZE
            )
            board[r][c] = str(count)
    return board

# Reveal 0-zones and adjacent numbers
def reveal_zone(board, x, y, revealed):
    if board[y][x] != '0' or revealed[y][x]:
        return
    queue = deque([(x, y)])
    while queue:
        cx, cy = queue.popleft()
        if revealed[cy][cx]:
            continue
        revealed[cy][cx] = True
        if board[cy][cx] == '0':
            for dx, dy in DIRECTIONS:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if not revealed[ny][nx] and board[ny][nx] != '*':
                        queue.append((nx, ny))
        elif board[cy][cx] != '*':
            revealed[cy][cx] = True

# Draw a single cell
def draw_cell(x, y, value):
    if value == '0':
        return
    text = font.render(value, True, (255, 255, 255))
    rect = text.get_rect(center=(x * TILE_SIZE + 20, y * TILE_SIZE + 20))
    screen.blit(text, rect)

# Handle click
def handle_click(board, revealed, bombs, x, y):
    grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
    if board[grid_y][grid_x] == '*':
        bombs[grid_y][grid_x] = True
        print("BOMBA at:", grid_x, grid_y)
    else:
        if board[grid_y][grid_x] == '0':
            reveal_zone(board, grid_x, grid_y, revealed)
        else:
            revealed[grid_y][grid_x] = True

def main():
    board = update_board(generate_board())
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    bombs = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    running = True
    while running:
        screen.fill("black")
        draw_grid()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                handle_click(board, revealed, bombs, mx, my)

        # Render revealed cells
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if revealed[y][x]:
                    draw_cell(x, y, board[y][x])
                if bombs[y][x]:
                    pygame.draw.rect(screen, "red", (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

