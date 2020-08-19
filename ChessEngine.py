class GameState():
	def __init__(self):
		self.board = [
		["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
		["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
		["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
			
		self.whitetomove = True
		self.movelog = []
#gs = GameState()
#print(gs.board)