import pygame
import time
import math

# define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Ball(pygame.sprite.Sprite):
    
    def __init__(self, x, y, radius, speed, direction, color, surface):
        super(Ball, self).__init__()

        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = math.radians(direction)
        self.color = color
        self.surface = surface

        self.calculateDeltas()

    def drawBall(self):
        self.checkCollision()
        self.x += self.deltaX
        self.y += self.deltaY
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

    def calculateDeltas(self):
        self.deltaX = int(self.speed * math.cos(self.direction))
        self.deltaY = int(self.speed * math.sin(self.direction))

    def checkCollision(self):
        if self.x + 8 >= self.surface.get_width() - 5 - self.speed:
            self.direction = math.pi - self.direction
            self.calculateDeltas()
        elif self.x - 8 <= 5 + self.speed:
            self.direction = math.pi - self.direction
            self.calculateDeltas()
        elif self.y - 8 <= 5 + self.speed:
            self.direction = 2 * math.pi - self.direction
            self.calculateDeltas()
        elif self.y + 8 >= self.surface.get_height() - 50 - self.speed:
            self.direction = 2 * math.pi - self.direction
            self.calculateDeltas()

class Bar(pygame.sprite.Sprite):

    def __init__(self, x, y, length, width, speed, color, surface):
        super(Bar, self).__init__()

        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.speed = speed
        self.color = color
        self.surface = surface

    def drawBar(self):
        pygame.draw.rect(self.surface, self.color, [self.x, self.y, self.length, self.width])


# initiate the board
height = 600
width = 800

pygame.init()
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('TilePong')
clock = pygame.time.Clock()

# draw background that won't be updated
surface.fill(BLACK)
pygame.draw.rect(surface, WHITE, [5, 5, width - 10, height - 10])
pygame.draw.rect(surface, BLUE, [5, height - 5 - 30, width - 10, 30])

# initiate the moving bar
myBar = Bar(width/2, height - 50, width / 5, 10, 8, RED, surface)
barChange = 0

# initiate the ball
# myBall = Ball(width/2, height - 49 - myBar.width, 8, 10, -38, GREEN, surface)
myBall = Ball(width/2, height - 150 - myBar.width, 8, 20, -5, GREEN, surface)
ballChange = 0

while True:

    # paint the line white that the bar moves
    pygame.draw.rect(surface, WHITE, [5, height - 50, width - 10, myBar.width])

    # remove previous ball and draw the ball on the next position
    pygame.draw.circle(surface, WHITE, (myBall.x, myBall.y), myBall.radius)
    myBall.drawBall()

    for event in pygame.event.get():
        # if page is closed, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # check if key down is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                barChange = -myBar.speed
            if event.key == pygame.K_RIGHT:
                barChange = myBar.speed

        # if the key is unpressed, stop the motion
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                barChange = 0

    # if going to be out of surface, do not update
    if not(myBar.x < 14 and barChange < 0) and not (myBar.x > width - myBar.length - 15 and barChange > 0):
        myBar.x += barChange 

    # draw the updated the bar
    myBar.drawBar()
    pygame.display.update()
    clock.tick(360)


