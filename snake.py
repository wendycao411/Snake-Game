import pygame, sys, random
from pygame.math import Vector2

class Fruit:
	def randomize(self):
		new_x = random.randint(0, h_cells -1)
		new_y = random.randint(0,v_cells - 1)
		self.pos = Vector2(new_x, new_y)

	def __init__(self):
		self.randomize()

	def draw(self):
		fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
		screen.blit(apple_image, fruit_rect)

class Snake:
	def __init__(self):
		self.body = [Vector2(7,10), Vector2(6,10), Vector2 (5,10)]
		self.direction = Vector2(1,0)
		self.add_block = False

	def get_head_direction(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(-1,0):
			return head_right
		if head_relation == Vector2(1,0):
			return head_left
		if head_relation == Vector2(0,-1):
			return head_down
		else:
			return head_up

	def get_tail_direction(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(-1,0):
			return tail_right
		if tail_relation == Vector2(1,0):
			return tail_left
		if tail_relation == Vector2(0,-1):
			return tail_down
		else:
			return tail_up


	def draw(self):
		for index, block in enumerate(self.body):
			block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
			if index == 0:
				screen.blit(self.get_head_direction(), block_rect)
			elif index == len(self.body) -1:
				screen.blit(self.get_tail_direction(), block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(body_vertical, block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(body_horizontal, block_rect)
				elif previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
					screen.blit(body_tl, block_rect)
				elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
					screen.blit(body_tr, block_rect)
				elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
					screen.blit(body_bl, block_rect)
				else:
					screen.blit(body_br, block_rect)
	
	def move(self):
		if self.add_block:
			self.add_block = False
		else:
			self.body.pop()
		head = self.body[0] + self.direction
		self.body.insert(0, head)	
	
	def grow(self):
		self.add_block = True


#global vars
h_cells = 15
v_cells = 12
cell_size = 40
display_width = h_cells * cell_size
display_height = v_cells * cell_size
apple = Fruit()
snake = Snake()
game_over = False

		
def check_collisions():
	global game_over
	#snake eating fruit
	if apple.pos == snake.body[0]:
		#move the apple
		apple.randomize()
		#grow the snake
		snake.grow()
	#snake hitting wall
	if not 0 <= snake.body[0].x < h_cells or not 0 <= snake.body[0].y < v_cells:
		game_over = True
	#snake hitting self
	for block in snake.body[1:]:
		if snake.body[0] == block:
			game_over = True

def reset():
	global game_over
	game_over = False
	snake.__init__()
	apple.randomize()


#pygame setup
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#Load the images
apple_image = pygame.image.load("Graphics/apple.png").convert_alpha() 
head_up = pygame.image.load("Graphics/head_up.png").convert_alpha() 
head_down = pygame.image.load("Graphics/head_down.png").convert_alpha() 
head_left = pygame.image.load("Graphics/head_left.png").convert_alpha() 
head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()

tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha() 
tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha() 
tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha() 
tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()

body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha() 
body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()
body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha() 
body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()
body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()



#game loop
while True:
	#event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE and not game_over:
			snake.move()
			check_collisions()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				reset()
			if event.key == pygame.K_UP and snake.direction.y != 1:
				snake.direction = Vector2(0,-1)
			if event.key == pygame.K_DOWN and snake.direction.y != -1:
				snake.direction = Vector2(0,1)
			if event.key == pygame.K_RIGHT and snake.direction.x != -1:
				snake.direction = Vector2(1,0)
			if event.key == pygame.K_LEFT and snake.direction.x != 1:
				snake.direction = Vector2(-1,0)


	#draw stuff here
	screen.fill((92, 219, 132))
	apple.draw()
	snake.draw()
	if game_over:
		font = pygame.font.Font('freesansbold.ttf', 32)
		text = font.render('GAME OVER', True, (255,0,0))
		text_rect = text.get_rect()
		text_rect.center = (h_cells * cell_size / 2, v_cells * cell_size / 2)
		screen.blit(text, text_rect)
		#reset directions
		reset_text = font.render("press r to restart", True, (0,0,255))
		reset_rect = reset_text.get_rect()
		reset_rect.center = (h_cells * cell_size / 2, v_cells * 2 / 3 * cell_size)
		screen.blit(reset_text, reset_rect)
		#draw score here
		score = len(snake.body) - 3
		score_text = font.render("Score: " + str(score), True, (0,0,255))
		score_rect = score_text.get_rect()
		score_rect.center = (h_cells * cell_size / 2, v_cells * 5 / 6 * cell_size)
		screen.blit(score_text, score_rect)

	#these should be the last 2 lines of the loop
	pygame.display.update()
	clock.tick(60)
