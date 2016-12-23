import pygame
import time
import math
import random

# define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (145,7,7)
GREY = (56,56,56)
BLUE = (135,181,255)

# COLOR1 = (181,23,101)
# COLOR2 = (74,211,114)
# COLOR3 = (110,141,231)

COLOR1 = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
COLOR2 = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
COLOR3 = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))

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
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.score = 0

        self.calculateDeltas()

    def drawBall(self, barX, barLength, barY):
        self.checkCollision(barX, barLength, barY)
        self.x += self.deltaX
        self.y += self.deltaY
        self.rect.x = self.x
        self.rect.y = self.y
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.radius)

    def calculateDeltas(self):
        self.deltaX = self.speed * math.cos(self.direction)
        self.deltaY = self.speed * math.sin(self.direction)

    def checkCollision(self, barX, barLength, barY):
        if self.x + self.radius >= self.surface.get_width() - 5 - self.speed / 2:
            self.direction = math.pi - self.direction
            self.calculateDeltas()
        elif self.x - self.radius <= 5 + self.speed / 2:
            self.direction = math.pi - self.direction
            self.calculateDeltas()
        elif self.y - self.radius <= 5 + self.speed:
            self.direction = 2 * math.pi - self.direction
            self.calculateDeltas()
        elif self.y + self.radius >= barY and self.y + self.radius < barY + 5 and self.x >= barX and self.x <= barX + barLength:
            degree = 210 + int(120 * (self.x - barX) / barLength)
            self.direction = math.radians(degree)
            self.calculateDeltas()
        elif self.y + self.radius >= barY + 100:
            gameQuit("YOU LOST", surface)

    def checkTileCollision(self, tileList):
        tileHits = pygame.sprite.spritecollide(self, tileList, True)
        for tile in tileHits:
            self.tileDirectionChange(tile)
            self.score += 1  
            pygame.draw.rect(self.surface, WHITE, [tile.x, tile.y, tile.length, tile.width])
            if self.score >= 40:
                gameQuit("YOU WON", surface)

    def tileDirectionChange(self, tile):
        if self.y + self.radius < tile.y + 1:                   # tile up hit
            self.direction = 2 * math.pi - self.direction
            self.calculateDeltas()
        elif self.y - self.radius >= tile.y + 9:                # tile down hit
            self.direction = 2 * math.pi - self.direction
            self.calculateDeltas()
        elif self.x + self.radius < tile.x + 1:                 # tile left hit
            self.direction = math.pi - self.direction
            self.calculateDeltas()
        elif self.x - self.radius > tile.x + tile.length - 1:   # tile right hit
            self.direction = math.pi - self.direction
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

        self.rect = pygame.Rect(x, y, length, width)

    def drawBar(self):
        pygame.draw.rect(self.surface, self.color, [self.x, self.y, self.length, self.width])

class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, length, width, color, surface):
        super(Tile, self).__init__()

        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.color = color
        self.surface = surface
        self.rect = pygame.Rect(x - 3, y - 3, length + 6, width + 6)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, [self.x, self.y, self.length, self.width])

def putText(text, x, y, size, color, bg, surface):
    font = pygame.font.Font('freesansbold.ttf', size)
    textSurface = font.render(text, True, BLACK, BLUE)
    textRect = textSurface.get_rect()
    textRect.x = x
    textRect.y = y
    surface.blit(textSurface, textRect)

def gameQuit(text, surface):
    gameEnded = True
    # # pygame.draw.rect(surface, WHITE, [0, 0, surface.get_width(), surface.get_height()])
    # surface.fill((255,255,255))
    # putText(text, surface.get_width() - 100, surface.get_height() / 2 - 50, 78, COLOR1, WHITE, surface)
    # pygame.time.wait(5000)
    pygame.quit()
    quit()


# initiate the board
height = 600
width = 800

pygame.init()
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('TilePong')
clock = pygame.time.Clock()
gameEnded = False

# draw background that won't be updated
surface.fill(BLACK)
pygame.draw.rect(surface, WHITE, [5, 5, width - 10, height - 10])
pygame.draw.rect(surface, BLUE, [5, height - 5 - 30, width - 10, 30])

#initiate tiles and draw them, hardcoded to have 5x8 tiles
tileList = pygame.sprite.Group()
colorList = {0:COLOR1, 1:COLOR2, 2:COLOR3}
for i in range(5):
    y = (i + 1) * 10 + i * 20 + 5
    for j in range(8):
        x = (j + 1) * 6 + j * 92 + 5
        tile = Tile(x, y, 92, 20, colorList[(i * 8 + j) % 3], surface)
        tileList.add(tile)
        tile.draw()

# initiate the moving bar
myBar = Bar(width/2, height - 50, width / 5, 10, 8, RED, surface)
barChange = 0

# initiate the ball
ballRadius = 6
myBall = Ball(width/2, height - 49 - myBar.width, ballRadius, 10, -38, GREY, surface)
ballChange = 0

# main game loop
while not gameEnded:

    # paint the line white that the bar moves
    pygame.draw.rect(surface, WHITE, [5, height - 50, width - 10, myBar.width])

    # remove previous ball and draw the ball on the next position
    pygame.draw.circle(surface, WHITE, (int(myBall.x), int(myBall.y)), myBall.radius)
    myBall.drawBall(myBar.x, myBar.length, myBar.y)

    # process tile hits
    myBall.checkTileCollision(tileList)

    # render scoreboard (TILE NUMBER) as text
    text = "TILES: " + str(myBall.score)
    putText(text, 50, height - 30, 22, BLACK, BLUE, surface)

    for event in pygame.event.get():
        # if page is closed, quit the game
        if event.type == pygame.QUIT:
            gameQuit("YOU LOST", surface)

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
    clock.tick(720)

pygame.draw.rect(surface, WHITE, [0, 0, surface.get_width(), surface.get_height()])