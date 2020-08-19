import pygame, sys
import ChessEngine
#from pygame.locals import *
sys.path.append('images')
pygame.init()

Width = Height = 800
Dimension = 8
sq_size = Height // Dimension
max_FPS = 30
Images = ()
#white_color = pygame.Color(255, 255, 255)
#gray_color = pygame.Color(50, 50, 50)
#wK = pygame.image.load("images/wK.png")

def load_images():
	pieces = ["wK", "bK", "wQ", "bQ", "wR", "bR", "wB", "bB", "wN", "bN", "wP", "bP"]
	for piece in pieces:
		#Images["wK"] = pygame.image.load("images/wK.png")
		#Images["wQ"] = pygame.image.load("images/wQ.png")
		#gets tuple item does not support item assignment error ^^
		wR = pygame.image.load("images/wR.png")
		wB = pygame.image.load("images/wB.png")
		wN = pygame.image.load("images/wN.png")
		wP = pygame.image.load("images/wP.png")
		bK = pygame.image.load("images/bK.png")
		bQ = pygame.image.load("images/bQ.png")
		bR = pygame.image.load("images/bR.png")
		bB = pygame.image.load("images/bB.png")
		bN = pygame.image.load("images/bN.png")
		bP = pygame.image.load("images/bP.png")
		#Images[piece] = pygame.image.load("images/" + piece + ".png")
		#Images[piece] =  pygame.transform scale(pygame.image.load("images/" + piece + ".png"), (sq_size, sq_size))
		#idk why this shit doesn't work ^^
	
def main():
	screen = pygame.display.set_mode((Width, Height))
	clock = pygame.time.Clock()
	screen.fill(pygame.Color("black"))
	gs = ChessEngine.GameState()
	print(gs.board)
	load_images()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			drawGameState(screen, gs)		
			clock.tick(max_FPS)
			pygame.display.flip()

def drawGameState(screen, gs):
		draw_board(screen)
		draw_pieces(screen, gs.board)
	
def draw_board(screen):
	#colors = {pygame.Color("white"), pygame.Color("gray")} 
	#this has the issue of pygame.color not being hashable ^
	for r in range(Dimension):
		for c in range(Dimension):
			colour = ((r+c) % 2)
			if colour == 0:
				color = pygame.Color("white")
			else:
				color = pygame.Color("gray")
			pygame.draw.rect(screen, color, pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
			
def draw_pieces(screen, board):
		for r in range(Dimension):
			for c in range(Dimension):
				piece = board(r)(c)
				if piece == "wK":
					screen.blit(pygame.image.load("images/wK.png"), pygame.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
		
		
		
if __name__ == "__main__":
	main()
