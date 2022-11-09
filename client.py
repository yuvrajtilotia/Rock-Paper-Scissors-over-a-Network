import pygame
from network import Network
import pickle
pygame.font.init()

width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
	def __init__(self, text, x, y, colour):
		self.text = text
		self.x = x
		self.y = y
		self.colour = colour
		self.width = 100
		self.height = 75

	def draw(self, win):
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
		font = pygame.font.SysFont("Cascadia Mono", 40)
		text = font.render(self.text, 1, (255, 255, 255))
		win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

	def click(self, position):
		x1 = position[0]
		y1 = position [1]
		if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
			return True
		else:
			return False

def redrawWindow(win, game, p):
	win.fill((61,176,247))
	if not(game.connected()):
		font = pygame.font.SysFont("Cascadia Mono", 60)
		text = font.render("Waiting for players to join... ", 1, (0, 255, 0))
		win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
	else:
		font = pygame.font.SysFont("Cascadia Mono", 50)
		text = font.render("Your Move", 1, (255, 255, 0))
		win.blit(text, (80, 200))

		text = font.render("Opponent's Move", 1, (255, 255, 0))
		win.blit(text, (380, 200))
		move1 = game.get_player_move(0)
		move2 = game.get_player_move(1)
		if game.bothWent():
			text1 = font.render(move1, 1, (0, 0, 0))
			text2 = font.render(move2, 1, (0, 0, 0))
		else:
			if game.p1Went and p == 0:
				text1 = font.render(move1, 1, (0, 0, 0))
			elif game.p1Went:
				text1 = font.render("Choice Made", 1, (0, 0, 0))
			else:
				text1 = font.render("Making Choice", 1, (0, 0, 0))

			if game.p2Went and p == 1:
				text2 = font.render(move2, 1, (0, 0, 0))
			elif game.p2Went:
				text2 = font.render("Choice Made", 1, (0, 0, 0))
			else:
				text2 = font.render("Making Choice", 1, (0, 0, 0))

		if p == 1:
			win.blit(text2, (100, 350))
			win.blit(text1, (400, 350))
		else:
			win.blit(text1, (100, 350))
			win.blit(text2, (400, 350))

		for btn in btns:
			btn.draw(win)

	pygame.display.update()

btns = [Button("Rock", 50, 450, (0, 0, 255)), Button("Paper", 250, 450, (255, 0, 0)), Button("Scissor", 450, 450, (0, 255, 0))]
def main():
	run = True
	clock = pygame.time.Clock()
	n = Network()
	a = int(n.getP())
	print("You are player ", a ,".")
	while run:
		clock.tick(60)
		try:
			game = n.send("get")
		except:
			run = False
			print("No Game Found")
			break

		if game.bothWent():
			redrawWindow(win, game, a)
			pygame.time.delay(1000)
			try:
				game = n.send("reset")
			except:
				run = False
				print("No Game Found")
				break

			font = pygame.font.SysFont("Cascadia Mono", 70)
			if (game.winner() == 1 and a == 1) or (game.winner() == 0 and a == 0):
				text = font.render("YOU WON !!!", 1, (255, 215, 0))
			elif game.winner() == -1:
				text = font.render("TIED. NO WINNER", 1, (255, 215, 0))
			else:
				text = font.render("YOU LOST !!!", 1, (255, 215, 0))

			win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
			pygame.display.update()
			pygame.time.delay(1000)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				position = pygame.mouse.get_pos()
				for btn in btns:
					if btn.click(position) and game.connected():
						if a == 0:
							if not game.p1Went:
								n.send(btn.text)
						else:
							if not game.p2Went:
								n.send(btn.text)

		redrawWindow(win, game, a)

def menu():
	run = True
	clock = pygame.time.Clock()
	while run:
		clock.tick(60)
		win.fill((61,176,247))
		font = pygame.font.SysFont("Cascadia Mono", 50)
		text = font.render("Click to PLAY !!!", 1, (255, 215, 0))
		win.blit(text, (400, 300))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				run = False

	main()

while True:
	menu()