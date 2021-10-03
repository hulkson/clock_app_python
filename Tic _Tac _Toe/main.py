import pygame
import sys
import numpy as np

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH
SCREEN_COLOR = (255, 255, 255)
LINE_COLOR = (49, 49, 49)
BOARD_ROW = 3
BOARD_COLS = 3
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLS
LINE_WIDTH = SQUARE_SIZE // 10
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = SQUARE_SIZE // 10
CIRCLE_COLOR = (30, 171, 157)
CROSS_WIDTH = SQUARE_SIZE // 10
CROSS_COLOR = (66, 66, 66)
SPACE = SQUARE_SIZE // 4

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(SCREEN_COLOR)
pygame.display.set_caption('TIC TAC TOE')
# pygame.draw.line(screen, LINE_COLOR, (10, 10), (300, 300), 10)

# board
board = np.zeros((BOARD_ROW, BOARD_COLS))
# print(board)


def draw_lines():
    # horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (SCREEN_WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * 2), (SCREEN_WIDTH, SQUARE_SIZE * 2), LINE_WIDTH)

    # vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, SCREEN_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * 2, 0), (SQUARE_SIZE * 2, SCREEN_HEIGHT), LINE_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    # return board[row][col] == 0 -> shorter way
    if board[row][col] == 0:
        return True
    else:
        return False


def is_board_full():
    for row in range(BOARD_ROW):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


def draw_icon():
    for row in range(BOARD_ROW):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)

            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE +SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)


def check_win(player):
    # check vertical win
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # check horizontal win
    for row in range(BOARD_ROW):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # check left-cross win
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_left_winning_cross(player)
        return True

    # check right-cross win
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_right_winning_cross(player)
        return True

    return False


def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE / 2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (posX, SQUARE_SIZE // 10), (posX, SCREEN_HEIGHT - SQUARE_SIZE // 10), SQUARE_SIZE // 10)


def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE / 2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (SQUARE_SIZE // 10, posY), (SCREEN_WIDTH - SQUARE_SIZE // 10, posY), SQUARE_SIZE // 10)

def draw_left_winning_cross(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (SQUARE_SIZE // 10, SCREEN_HEIGHT - SQUARE_SIZE // 10), (SCREEN_WIDTH - SQUARE_SIZE // 10, SQUARE_SIZE // 10), SQUARE_SIZE // 10)

def draw_right_winning_cross(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (SQUARE_SIZE // 10, SQUARE_SIZE // 10), (SCREEN_WIDTH - SQUARE_SIZE // 10, SCREEN_HEIGHT -SQUARE_SIZE // 10), SQUARE_SIZE // 10)

def restart_game():
    screen.fill(SCREEN_COLOR)
    draw_lines()
    for row in range(BOARD_ROW):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()

game_over = False
player = 1

# mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1
                # if player == 1:
                #     mark_square(clicked_row, clicked_col, 1)
                #     if check_win(player):
                #         game_over = True
                #     player = 2
                # elif player == 2:
                #     mark_square(clicked_row, clicked_col, 2)
                #     if check_win(player):
                #         game_over = True
                #     player = 1
                draw_icon()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    pygame.display.update()
