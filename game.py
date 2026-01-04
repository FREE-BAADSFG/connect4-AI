import numpy as np
import pygame
import sys
import math
import random

# setup stuff
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
R_COUNT = 6
C_COUNT = 7

def create_board():
	return np.zeros((R_COUNT,C_COUNT))

def drop_piece(board, r, c, piece):
	board[r][c] = piece

def is_valid(board, c):
	return board[R_COUNT-1][c] == 0

def get_next_row(board, c):
	for r in range(R_COUNT):
		if board[r][c] == 0:
			return r

def check_win(board, p):
	# horizontal
	for c in range(C_COUNT-3):
		for r in range(R_COUNT):
			if board[r][c] == p and board[r][c+1] == p and board[r][c+2] == p and board[r][c+3] == p:
				return True
	# vertical
	for c in range(C_COUNT):
		for r in range(R_COUNT-3):
			if board[r][c] == p and board[r+1][c] == p and board[r+2][c] == p and board[r+3][c] == p:
				return True
	# diag 1
	for c in range(C_COUNT-3):
		for r in range(R_COUNT-3):
			if board[r][c] == p and board[r+1][c+1] == p and board[r+2][c+2] == p and board[r+3][c+3] == p:
				return True
	# diag 2
	for c in range(C_COUNT-3):
		for r in range(3, R_COUNT):
			if board[r][c] == p and board[r-1][c+1] == p and board[r-2][c+2] == p and board[r-3][c+3] == p:
				return True

def score_window(window, p):
	score = 0
	opp = 1 if p == 2 else 2
	if window.count(p) == 4: score += 100
	elif window.count(p) == 3 and window.count(0) == 1: score += 5
	elif window.count(p) == 2 and window.count(0) == 2: score += 2
	if window.count(opp) == 3 and window.count(0) == 1: score -= 4
	return score

def get_score(board, p):
	score = 0
	# center
	center = [int(i) for i in list(board[:, C_COUNT//2])]
	score += center.count(p) * 3
	# rows/cols/diags - condensed logic
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
		val = -math.inf
		best_c = random.choice(valid)
		for c in valid:
			r = get_next_row(board, c)
			temp = board.copy()
			drop_piece(temp, r, c, 2)
			new_score = minimax(temp, depth-1, alpha, beta, False)[1]
			if new_score > val:
				val = new_score
				best_c = c
			alpha = max(alpha, val)
			if alpha >= beta: break
		return best_c, val
	else:
		val = math.inf
		best_c = random.choice(valid)
		for c in valid:
			r = get_next_row(board, c)
			temp = board.copy()
			drop_piece(temp, r, c, 1)
			new_score = minimax(temp, depth-1, alpha, beta, True)[1]
			if new_score < val:
				val = new_score
				best_c = c
			beta = min(beta, val)
			if alpha >= beta: break
		return best_c, val