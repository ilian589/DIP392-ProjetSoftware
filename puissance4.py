import pygame
import sys
import numpy as np

ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

def create_board():
    return np.zeros((ROWS, COLUMNS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def display_winner(winner):
    font = pygame.font.SysFont("monospace", 75)
    label = font.render(f"Player {winner} wins!", 1, RED if winner == 1 else YELLOW)
    screen.blit(label, (40, 10))
    pygame.display.update()

def draw_replay_button():
    font = pygame.font.SysFont("monospace", 50)
    label = font.render("Replay", 1, WHITE)
    button_rect = pygame.draw.rect(screen, BLACK, (width//2 - 100, height//2 - 50, 200, 100))
    screen.blit(label, (width//2 - 70, height//2 - 30))
    pygame.display.update()
    return button_rect

pygame.init()

width = COLUMNS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(create_board())
pygame.display.update()

# Main game loop
board = create_board()
game_over = False
turn = 0

while True:

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
              
                if turn == 0:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            draw_board(board)
                            display_winner(1)
                            game_over = True

                else:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            draw_board(board)
                            display_winner(2)
                            game_over = True

                draw_board(board)

                turn += 1
                turn %= 2

    button_rect = draw_replay_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = event.pos
            if button_rect.collidepoint(posx, posy):
                board = create_board()
                draw_board(board)
                game_over = False
                turn = 0
