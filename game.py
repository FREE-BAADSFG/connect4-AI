import numpy as np
import pygame
import sys
import math
import random

# colors and stuff
blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
white = (255,255,255)

rows = 6
cols = 7
sq = 100
width = cols * sq
height = (rows+1) * sq
rad = int(sq/2 - 5)

# logic functions
def make_board():
    return np.zeros((rows,cols))

def drop(b, r, c, p):
    b[r][c] = p

def is_ok(b, c):
    return b[rows-1][c] == 0

def find_row(b, c):
    for r in range(rows):
        if b[r][c] == 0: return r

def win_check(b, p):
    # horizontal check
    for c in range(cols-3):
        for r in range(rows):
            if b[r][c] == p and b[r][c+1] == p and b[r][c+2] == p and b[r][c+3] == p: return True
    # vertical check
    for c in range(cols):
        for r in range(rows-3):
            if b[r][c] == p and b[r+1][c] == p and b[r+2][c] == p and b[r+3][c] == p: return True
    # diag 1
    for c in range(cols-3):
        for r in range(rows-3):
            if b[r][c] == p and b[r+1][c+1] == p and b[r+2][c+2] == p and b[r+3][c+3] == p: return True
    # diag 2
    for c in range(cols-3):
        for r in range(3, rows):
            if b[r][c] == p and b[r-1][c+1] == p and b[r-2][c+2] == p and b[r-3][c+3] == p: return True

def get_val(b, p):
    s = 0
    mid = [int(i) for i in list(b[:, cols//2])]
    s += mid.count(p) * 3
    return s

# AI part
def bot(b, d, a, bt, max_p):
    moves = [c for c in range(cols) if is_ok(b, c)]
    over = win_check(b, 1) or win_check(b, 2) or len(moves) == 0
    
    if d == 0 or over:
        if over:
            if win_check(b, 2): return (None, 10000000)
            elif win_check(b, 1): return (None, -10000000)
            else: return (None, 0)
        return (None, get_val(b, 2))

    if max_p:
        v = -math.inf
        best = random.choice(moves)
        for c in moves:
            r = find_row(b, c)
            copy = b.copy()
            drop(copy, r, c, 2)
            score = bot(copy, d-1, a, bt, False)[1]
            if score > v:
                v = score
                best = c
            a = max(a, v)
            if a >= bt: break
        return best, v
    else:
        v = math.inf
        best = random.choice(moves)
        for c in moves:
            r = find_row(b, c)
            copy = b.copy()
            drop(copy, r, c, 1)
            score = bot(copy, d-1, a, bt, True)[1]
            if score < v:
                v = score
                best = c
            bt = min(bt, v)
            if a >= bt: break
        return best, v

def render(b):
    for c in range(cols):
        for r in range(rows):
            pygame.draw.rect(win, blue, (c*sq, r*sq+sq, sq, sq))
            pygame.draw.circle(win, black, (int(c*sq+sq/2), int(r*sq+sq+sq/2)), rad)
    for c in range(cols):
        for r in range(rows):      
            if b[r][c] == 1:
                pygame.draw.circle(win, red, (int(c*sq+sq/2), height-int(r*sq+sq/2)), rad)
            elif b[r][c] == 2: 
                pygame.draw.circle(win, yellow, (int(c*sq+sq/2), height-int(r*sq+sq/2)), rad)
    pygame.display.update()

# main part
pygame.init()
win = pygame.display.set_mode((width, height))
fnt = pygame.font.SysFont("arial", 40)

def start():
    b = make_board()
    render(b)
    over = False
    turn = 0 

    while not over:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()

            if e.type == pygame.MOUSEMOTION:
                pygame.draw.rect(win, black, (0,0, width, sq))
                if turn == 0:
                    pygame.draw.circle(win, red, (e.pos[0], int(sq/2)), rad)
                pygame.display.update()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    c = int(math.floor(e.pos[0]/sq))
                    if is_ok(b, c):
                        r = find_row(b, c)
                        drop(b, r, c, 1)
                        if win_check(b, 1):
                            res = "Nice. You actually won."
                            over = True
                        turn = 1
                        render(b)

        if turn == 1 and not over:				
            c, _ = bot(b, 5, -math.inf, math.inf, True)
            if is_ok(b, c):
                r = find_row(b, c)
                drop(b, r, c, 2)
                if win_check(b, 2):
                    res = "The bot won lol"
                    over = True
                render(b)
                turn = 0

        if over:
            pygame.draw.rect(win, black, (0,0, width, sq))
            t = fnt.render(res, 1, white)
            win.blit(t, (20, 20))
            pygame.display.update()
            
            # loop for reset
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_r: start()
                        if e.key == pygame.K_q: sys.exit()

start()