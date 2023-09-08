import numpy as np
import random
import pygame
import sys
import math

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROWS = 6
COLUMNS = 7

HUMAN = 0
AI = 1

EMPTY = 0
HUMAN_COIN = 1
AI_COIN = 2

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

def drop_coin(board, row, col, coin):
    board[row][col] = coin

def valid_place(board, col):
    return board[ROWS - 1][col] == 0

def next_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def is_win(board, coin):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == coin and board[r][c + 1] == coin and board[r][c + 2] == coin and board[r][
                c + 3] == coin:
                return True

    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == coin and board[r + 1][c] == coin and board[r + 2][c] == coin and board[r + 3][
                c] == coin:
                return True

    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == coin and board[r + 1][c + 1] == coin and board[r + 2][c + 2] == coin and board[r + 3][
                c + 3] == coin:
                return True

    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == coin and board[r - 1][c + 1] == coin and board[r - 2][c + 2] == coin and board[r - 3][
                c + 3] == coin:
                return True


def evaluate_window(window, coin):
    score = 0
    player = HUMAN_COIN
    if coin == HUMAN_COIN:
        player = AI_COIN
    if window.count(coin) == 4:
        score += 100
    elif window.count(coin) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(coin) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(player) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def score_position(board, coin):
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    center_count = center_array.count(coin)
    score += center_count * 3

    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, coin)

    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, coin)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, coin)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, coin)

    return score


def is_terminal_node(board):
    return is_win(board, HUMAN_COIN) or is_win(board, AI_COIN) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maxPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if is_win(board, AI_COIN):
                return (None, 100000000000)
            elif is_win(board, HUMAN_COIN):
                return (None, -10000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_COIN))
    if maxPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_row(board, col)
            b_copy = board.copy()
            drop_coin(b_copy, row, col, AI_COIN)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_row(board, col)
            b_copy = board.copy()
            drop_coin(b_copy, row, col, HUMAN_COIN)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if valid_place(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, coin):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = next_row(board, col)
        temp_board = board.copy()
        drop_coin(temp_board, row, col, coin)
        score = score_position(temp_board, coin)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == HUMAN_COIN:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_COIN:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(HUMAN, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == HUMAN:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            if turn == HUMAN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if valid_place(board, col):
                    row = next_row(board, col)
                    drop_coin(board, row, col, HUMAN_COIN)
                    if is_win(board, HUMAN_COIN):
                        label = myfont.render("YOU WON!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)

    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        if valid_place(board, col):
            row = next_row(board, col)
            drop_coin(board, row, col, AI_COIN)
            if is_win(board, AI_COIN):
                label = myfont.render("COMPUTER WON!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
