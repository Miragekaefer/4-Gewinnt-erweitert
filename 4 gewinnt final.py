import numpy as np
import pygame
import sys
import math

BLUE = (0,50,200)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 7
COLUMN_COUNT = 11

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def set_advanced_move(board,row,col,piece):
		board[row][col] = piece

def print_board(board):
	print(np.flip(board, 0))

def check_and_shift_0(board, col, piece):
    for row in range(ROW_COUNT):
        while board[row][0] != 0:
            for col in range(COLUMN_COUNT):
                if board[row][col+1] == 0:
                    board[row][col+1] = board[row][col]
                    board[row][col] = 0
                    break
                board[row][10] = 0
                
def check_and_shift_10(board, col, piece):
    for row in range(ROW_COUNT):
        while board[row][10] != 0:
            for col in reversed(range(COLUMN_COUNT+1)):
                if board[row][col-1] == 0:
                    board[row][col-1] = board[row][col]
                    board[row][col] = 0
                    break
                board[row][0] = 0                
                                
            		
def check_and_drop(board): #funktiniert !!! # aber nur halb gecheckt / kind of genau das gegenteil von dem code hierrüber der steine hochfallen lässt aber wieso hat der code darüber die ganze zeile immer gelöscht ???
    for col in range(1,COLUMN_COUNT-1):
        for row in reversed(range(ROW_COUNT-1)):
            while board[row+1][col] != 0 and board[row,col] == 0:
                board[row][col] == 0
                board[row][col] = board[row+1][col]
                board[row+1][col] = 0
                break                

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(1,COLUMN_COUNT-1):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r*SQUARESIZE+SQUARESIZE), SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(1,COLUMN_COUNT-1):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def start_screen():
    screen.fill(BLACK)
    
    button_rect = pygame.Rect(150,200,200,50)
    pygame.draw.rect(screen,RED,button_rect)
    start_text = pygame.font.SysFont(None,36).render("Start Game",True,BLACK)
    
    text_rect = start_text.get_rect(center=button_rect.center)
    
    screen.blit(start_text,text_rect)
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return
        pygame.display.update()
    
    

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100
#######################################################################
width = (COLUMN_COUNT) * SQUARESIZE 
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
#draw_board(board)
#pygame.display.update()

start_screen()

draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			pygame.draw.rect(screen,BLACK,(0,0,SQUARESIZE,height))
			pygame.draw.rect(screen,BLACK,(1000,0,SQUARESIZE,height))
			posx = event.pos[0]
			posy = event.pos[1]
			if SQUARESIZE <= posx <= width - SQUARESIZE:			
				if turn == 0:
					pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
				else: 
					pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
			else:
				if 0 <= posx <= 100:
					if turn == 0:
						pygame.draw.circle(screen, RED, (int(SQUARESIZE)/2, posy), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (int(SQUARESIZE)/2, posy), RADIUS)
				else:
					if turn == 0:
						pygame.draw.circle(screen, RED, (1050, posy), RADIUS)  #MagicNr.
					else: 
						pygame.draw.circle(screen, YELLOW, (1050, posy), RADIUS) #MagicNr.
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			print(event.pos)
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			posy = abs(height - event.pos[1]) ###
			col=int(math.floor(posx/SQUARESIZE))
   
			if col == 0:
				set_advanced_move(board,int(math.floor(posy/SQUARESIZE)),col,1 if turn == 0 else 2)
				check_and_shift_0(board,col,1 if turn == 0 else 2)
				check_and_drop(board)
			elif col == 10:
				set_advanced_move(board,int(math.floor(posy/SQUARESIZE)),col,1 if turn == 0 else 2)
				check_and_shift_10(board,col,1 if turn == 0 else 2)
				check_and_drop(board)
				#check_and_shift_10(board,col,1 if turn == 0 else 2)
				#row = int(event.pos[1] / SQUARESIZE)
			else:
				if is_valid_location(board,col):
					row = get_next_open_row(board,col)
				else:
					continue


				if is_valid_location(board, col):
					drop_piece(board,row,col,1 if turn == 0 else 2)



			if winning_move(board, 1):
				label = myfont.render("Player 1 wins!!", 1, RED)
				screen.blit(label, (40,10))
				game_over = True
			else:
				if winning_move(board, 2):
					label = myfont.render("Player 2 wins!!", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True

			#check_and_drop(board)

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)