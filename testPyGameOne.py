import pygame
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

# Screen basis
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen =pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Breakout for... Boosted')


# define variables
cols = 6
rows = 6

# font
font = pygame.font.SysFont('Constantia', 30)

# colors
bg = (234, 218, 184)
#blocks
B_RED = (242, 85, 96)
B_GREEN = (86, 174, 87)
B_BLUE = (69, 177, 232)
# paddle
paddle_col = (142, 135 ,123)
paddle_outline =(100, 100, 100)

# and frames per second
FPS = 60

# in Pong but not in Breakout
def draw_text(text, font, text_coL, x, y):
    img = font.render(text, True, text_coL)
    screen.blit(img, (x, y))


#Brick wall class
class Wall():
    def __init__(self):
        self.width = SCREEN_WIDTH // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        # individual blocks
        block_i = []
        for row in range(rows):
            # reset
            block_row = []
            for col in range(cols):
                # generate rect at x and y positions
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign color based on rules
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                # create a list to store rect and colour data
                block_i = [rect, strength]
                # append to the block row
                block_row.append(block_i)
            # append the row to the list of blocks
            self.blocks.append(block_row)
    
    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign color based on block strength
                if block[1] == 3:
                    block_color = B_BLUE
                elif block[1] == 2:
                    block_color = B_GREEN
                elif block[1] == 1:
                    block_color = B_RED
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg, block[0], 2)    # border blocks


class Paddle():
    def __init__(self):
        # vars
        self.height = 20
        self.width = int(SCREEN_WIDTH / cols)
        self.x = int((SCREEN_WIDTH / 2) - (self.width / 2))
        self.y = SCREEN_HEIGHT -(self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def move(self):
        #reset direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.direction = 1


class Ball():
    def __init__(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2 , self.ball_rad * 2 )
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0
    
    def move(self):

        # collision threshold
        CT = 5
        # collisions with wall
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # check collision
                if self.rect.colliderect(item[0]):
                    # collision from above
                    if abs(self.rect.bottom - item[0].top) < CT and self.speed_y > 0:
                        self.speed_y *= -1
                    # collision from below
                    if abs(self.rect.top - item[0].bottom) < CT and self.speed_y < 0:
                        self.speed_y *= -1
                    # collision from left
                    if abs(self.rect.right - item[0].left) < CT and self.speed_x > 0:
                        self.speed_x *= -1
                    # collision from right
                    if abs(self.rect.left - item[0].right) < CT and self.speed_x < 0:
                        self.speed_x *= -1
                    # reduce block's strength
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] =(0, 0, 0, 0)
                # check if block exists so wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                # increase item count
                item_count +=1
            # increase row count
            row_count +=1
        # after iterating throught all the blocks, check if wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1

                      
        #check for collision with walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        
        #check for collision with top and bottom
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.game_over = -1    
        
        # look for collision with paddle
        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < CT and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

       
# create wall
wall = Wall()
wall.create_wall()

# create paddles
player_paddle = Paddle()

# create ball
ball = Ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

# execution de la boucle principale du programme
run = True
while run:

    fpsClock.tick(FPS)
    screen.fill(bg)
    # draw wall
    wall.draw_wall()
    # draw paddle
    player_paddle.draw()
    player_paddle.move()
    # draw ball
    ball.draw()
    ball.move()
       
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()

