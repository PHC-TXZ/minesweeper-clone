# Author: Vijay Karthikeyan                     Date: 2025/06/17

# Import necessary modules
import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors using RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)    
BLACK = (0, 0, 0)         

# Game settings
game_width = 10
game_height = 10
num_mines = 12
grid_size = 32
border = 16
top_border = 100

# Calculate display size
display_width = game_width * grid_size + border * 2
display_height = game_height * grid_size + border * 2 + top_border

# Create the game window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Minesweeper")

# Load images
flag = pygame.image.load("flag.jpg")
empty = pygame.image.load("empty.jpg")
grid_image = pygame.image.load("grid.jpg")
grid1 = pygame.image.load("grid1.jpg")
grid2 = pygame.image.load("grid2.jpg")
grid3 = pygame.image.load("grid3.jpg")
grid4 = pygame.image.load("grid4.jpg")
grid5 = pygame.image.load("grid5.jpg")
grid6 = pygame.image.load("grid6.jpg")
grid7 = pygame.image.load("grid7.jpg")
grid8 = pygame.image.load("grid8.jpg")
mine = pygame.image.load("mine.jpg")
mineClicked = pygame.image.load("minetripped.jpg")
noMine = pygame.image.load("noMine.jpg")

# Global variables to store game state
grid = []
mines = []

# Function to draw text on the screen
def drawText(text, size, y_offset=0):
    font = pygame.font.SysFont("Comic Sans MS", size, True)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (display_width // 2, display_height // 2 + y_offset)
    gameDisplay.blit(text_surface, text_rect)

# Class representing each cell in the grid
class Grid:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        self.rect = pygame.Rect(border + self.x * grid_size,
                                top_border + self.y * grid_size,
                                grid_size, grid_size)

    def draw(self):
        if self.mineFalse:
            gameDisplay.blit(noMine, self.rect)
        else:
            if self.clicked:
                if self.value == -1:
                    if self.mineClicked:
                        gameDisplay.blit(mineClicked, self.rect)
                    else:
                        gameDisplay.blit(mine, self.rect)
                else:
                    self.draw_number()
            else:
                if self.flag:
                    gameDisplay.blit(flag, self.rect)
                else:
                    gameDisplay.blit(grid_image, self.rect)

    def draw_number(self):
        if self.value == 0:
            gameDisplay.blit(empty, self.rect)
        elif self.value == 1:
            gameDisplay.blit(grid1, self.rect)
        elif self.value == 2:
            gameDisplay.blit(grid2, self.rect)
        elif self.value == 3:
            gameDisplay.blit(grid3, self.rect)
        elif self.value == 4:
            gameDisplay.blit(grid4, self.rect)
        elif self.value == 5:
            gameDisplay.blit(grid5, self.rect)
        elif self.value == 6:
            gameDisplay.blit(grid6, self.rect)
        elif self.value == 7:
            gameDisplay.blit(grid7, self.rect)
        elif self.value == 8:
            gameDisplay.blit(grid8, self.rect)

    def revealGrid(self):
        if self.clicked or self.flag:
            return
        self.clicked = True
        if self.value == 0:
            for dx in range(-1, 2):
                nx = self.x + dx
                for dy in range(-1, 2):
                    ny = self.y + dy
                    if 0 <= nx < game_width and 0 <= ny < game_height:
                        if not grid[ny][nx].clicked:
                            grid[ny][nx].revealGrid()
        elif self.value == -1:
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].mineClicked = True

    def updateValue(self):
        if self.value != -1:
            count = 0
            for dx in range(-1, 2):
                nx = self.x + dx
                if 0 <= nx < game_width:
                    for dy in range(-1, 2):
                        ny = self.y + dy
                        if 0 <= ny < game_height:
                            if grid[ny][nx].value == -1:
                                count += 1
            self.value = count

# Function to generate the grid with mines and values
def generate_grid():
    global grid
    grid = []
    for y in range(game_height):
        row = []
        for x in range(game_width):
            if [x, y] in mines:
                row.append(Grid(x, y, -1))
            else:
                row.append(Grid(x, y, 0))
        grid.append(row)
    for row in grid:
        for cell in row:
            cell.updateValue()

# Function to randomly generate mine positions
def generate_mines():
    global mines
    mines = []
    while len(mines) < num_mines:
        x = random.randint(0, game_width - 1)
        y = random.randint(0, game_height - 1)
        if [x, y] not in mines:
            mines.append([x, y])

# Main game loop
def gameLoop():
    gameState = "Playing"
    mineLeft = num_mines

    generate_mines()
    generate_grid()

    while gameState != "Exit":
        gameDisplay.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "Exit"
            if gameState in ["Game Over", "Win"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    gameLoop()
                    return
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for row in grid:
                        for cell in row:
                            if cell.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    if not cell.flag:
                                        cell.revealGrid()
                                        if cell.value == -1:
                                            gameState = "Game Over"
                                            cell.mineClicked = True
                                elif event.button == 3:
                                    if not cell.clicked:
                                        if cell.flag:
                                            cell.flag = False
                                            mineLeft += 1
                                        else:
                                            cell.flag = True
                                            mineLeft -= 1

        # Check win condition
        won = True
        for row in grid:
            for cell in row:
                cell.draw()
                if cell.value != -1 and not cell.clicked:
                    won = False
        if won and gameState == "Playing":
            gameState = "Win"

        # Draw UI text
        if gameState == "Game Over":
            drawText("Game Over!", 50)
            drawText("Press R to restart", 35, 50)
            for row in grid:
                for cell in row:
                    if cell.flag and cell.value != -1:
                        cell.mineFalse = True
        elif gameState == "Win":
            drawText("You WON!", 50)
            drawText("Press R to restart", 35, 50)

        # Draw mines left
        mines_text = pygame.font.SysFont("Comic Sans MS", 50).render(str(mineLeft), True, BLACK)
        gameDisplay.blit(mines_text, (display_width - border - 50, border))

        pygame.display.update()

    pygame.quit()
    quit()

# Start the game
if __name__ == "__main__":
    gameLoop()
