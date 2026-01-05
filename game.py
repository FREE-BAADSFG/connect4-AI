import numpy as np
import pygame
import sys
import math
import random

# setup
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
R_COUNT = 6
C_COUNT = 7
SQUARE = 100
width = C_COUNT * SQUARE
height = (R_COUNT+1) * SQUARE
RAD = int(SQUARE/2 - 5)

def create_board():
    return np.zeros((R_COUNT,C_COUNT))

def drop_p(board, r, c, p):
    board[r][c] = p

def is_valid(board, c):
    return board[R_COUNT-1][c] == 0

def get_row(board, c):
    for r in range(R_COUNT):
        if board[r][c] == 0: return r

def check_win(board, p):
    for c in range(C_COUNT-3):
        for r in range(R_COUNT):
            if board[r][c] == p and board[r][c+1] == p and board[r][c+2] == p and board[r][c+3] == p: return True
    for c in range(C_COUNT):
        for r in range(R_COUNT-3):
            if board[r][c] == p and board[r+1][c] == p and board[r+2][c] == p and board[r+3][c] == p: return True
    for c in range(C_COUNT-3):
        for r in range(R_COUNT-3):
            if board[r][c] == p and board[r+1][c+1] == p and board[r+2][c+2] == p and board[r+3][c+3] == p: return True
    for c in range(C_COUNT-3):
        for r in range(3, R_COUNT):
            if board[r][c] == p and board[r-1][c+1] == p and board[r-2][c+2] == p and board[r-3][c+3] == p: return True

def get_score(board, p):
    score = 0
    center = [int(i) for i in list(board[:, C_COUNT//2])]
    score += center.count(p) * 3
    return score

def minimax(board, depth, alpha, beta, is_maxing):
    valid = [c for c in range(C_COUNT) if is_valid(board, c)]
    done = check_win(board, 1) or check_win(board, 2) or len(valid) == 0
    if depth == 0 or done:
        if done:
            if check_win(board, 2): return (None, 10000000)
            elif check_win(board, 1): return (None, -10000000)
            else: return (None, 0)
        return (None, get_score(board, 2))
    if is_maxing:
        v = -math.inf
        bc = random.choice(valid)
        for c in valid:
            r = get_row(board, c)
            tmp = board.copy()
            drop_p(tmp, r, c, 2)
            score = minimax(tmp, depth-1, alpha, beta, False)[1]
            if score > v: v = score; bc = c
            alpha = max(alpha, v)
            if alpha >= beta: break
        return bc, v
    else:
        v = math.inf
        bc = random.choice(valid)
        for c in valid:
            r = get_row(board, c)
            tmp = board.copy()
            drop_p(tmp, r, c, 1)
            score = minimax(tmp, depth-1, alpha, beta, True)[1]
            if score < v: v = score; bc = c
            beta = min(beta, v)
            if alpha >= beta: break
        return bc, v

def draw(board):
    for c in range(C_COUNT):
        for r in range(R_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARE, r*SQUARE+SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE+SQUARE/2), int(r*SQUARE+SQUARE+SQUARE/2)), RAD)
    for c in range(C_COUNT):
        for r in range(R_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RAD)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), RAD)
    pygame.display.update()

# INIT
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("C4 Engine")

board = create_board()
draw(board)
game_over = False
turn = 0 

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE/2)), RAD)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
            if turn == 0:
                col = int(math.floor(event.pos[0]/SQUARE))
                if is_valid(board, col):
                    row = get_row(board, col)
                    drop_p(board, row, col, 1)
                    if check_win(board, 1): game_over = True
                    turn = 1
                    draw(board)

    if turn == 1 and not game_over:				
        col, _ = minimax(board, 5, -math.inf, math.inf, True)
        if is_valid(board, col):
            row = get_row(board, col)
            drop_p(board, row, col, 2)
            if check_win(board, 2): game_over = True
            draw(board)
            turn = 0

    if game_over:
        pygame.time.wait(3000)