import numpy as np
import pygame
import sys
import math

# Constants
ROWS = 6
COLS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PLAYER = 1
AI = 2
EMPTY = 0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)
font = pygame.font.SysFont("monospace", 75)
pygame.display.set_caption("Connect 4")

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_move(board, col):
    return board[ROWS - 1][col] == EMPTY

def get_next_open_row(board, col):
    for row in range(ROWS):
        if board[row][col] == EMPTY:
            return row

def is_winning_move(board, piece):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Check positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    # Check negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    return False

def draw_board(board):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, (row + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (col * SQUARESIZE + SQUARESIZE // 2, (row + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
    
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == PLAYER:
                pygame.draw.circle(screen, RED, (col * SQUARESIZE + SQUARESIZE // 2, HEIGHT - (row * SQUARESIZE + SQUARESIZE // 2)), RADIUS)
            elif board[row][col] == AI:
                pygame.draw.circle(screen, YELLOW, (col * SQUARESIZE + SQUARESIZE // 2, HEIGHT - (row * SQUARESIZE + SQUARESIZE // 2)), RADIUS)

    pygame.display.update()

def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_moves = get_valid_moves(board)
    is_terminal = is_winning_move(board, PLAYER) or is_winning_move(board, AI) or len(valid_moves) == 0

    if depth == 0 or is_terminal:
        if is_terminal:
            if is_winning_move(board, AI):
                return None, 1000000
            elif is_winning_move(board, PLAYER):
                return None, -1000000
            else:  # Draw
                return None, 0
        else:
            return None, score_position(board, AI)

    if maximizingPlayer:
        value = float('-inf')
        best_col = np.random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI)
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = float('inf')
        best_col = np.random.choice(valid_moves)
        for col in valid_moves:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER)
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def score_position(board, piece):
    # Simplified scoring logic for this example
    return 0

def main():
    board = create_board()
    game_over = False
    turn = np.random.choice([PLAYER, AI])
    draw_board(board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, SQUARESIZE // 2), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = posx // SQUARESIZE

                    if is_valid_move(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER)

                        if is_winning_move(board, PLAYER):
                            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                            label = font.render("PLAYER WINS!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn = AI
                        draw_board(board)

        if turn == AI and not game_over:
            col, _ = minimax(board, 5, float('-inf'), float('inf'), True)

            if is_valid_move(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI)

                if is_winning_move(board, AI):
                    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                    label = font.render("AI WINS!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn = PLAYER
                draw_board(board)

        if game_over:
            pygame.time.wait(3000)

if __name__ == "__main__":
    main()
