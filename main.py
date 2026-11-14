import random
import pygame
from player import Player
from cell import Cell
from camera import Camera
from sinner import Sinner
from collectable import Collectable

GAME_WIDTH = 2400
GAME_HEIGHT = 2400
WIDTH = 800
HEIGHT = 800

FPS = 60
GRID_SIZE = 50
CELL_SIZE = GAME_WIDTH // GRID_SIZE
CELL_COLOR = (43, 34, 58)
WALL_COLOR = (247, 240, 232)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hollow Silk Maze")
clock = pygame.time.Clock()

SCALE_X = CELL_SIZE - 10
SCALE_Y = CELL_SIZE - 5
# i should really make an image cache but im too lazy 
player_placeholder = pygame.transform.scale(pygame.image.load("player_image_placeholder.png").convert_alpha(), (SCALE_X, SCALE_Y ))
candy_image = pygame.transform.scale(pygame.image.load("candy_image.png").convert_alpha(), (SCALE_X, SCALE_Y ))
flea_image = pygame.transform.scale(pygame.image.load("flea_image.png").convert_alpha(), (SCALE_X, SCALE_Y ))
gms_image = pygame.transform.scale(pygame.image.load("gms_image.png").convert_alpha(), (SCALE_X, SCALE_Y ))
sinner_image = pygame.transform.scale(pygame.image.load("sinner_image.png").convert_alpha(), (SCALE_X, SCALE_Y))



prob_candy = .04
prob_flea = .006
prob_sin = .006


def get_neighbors(cell, grid):
    # get all adjacent cells 
    neighbors = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] 
    
    for dx, dy in directions:
        nx, ny = cell.x + dx, cell.y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbor = grid[ny][nx]
            if not neighbor.visited:
                neighbors.append(neighbor)
    return neighbors


def remove_walls(current, next_cell):
    # tears down matching walls in two neighboring cells
    dx = current.x - next_cell.x
    dy = current.y - next_cell.y

    if dx == -1: 
        current.walls[1] = False
        next_cell.walls[3] = False
    elif dx == 1: 
        current.walls[3] = False
        next_cell.walls[1] = False
        
    if dy == -1: 
        current.walls[2] = False
        next_cell.walls[0] = False
    elif dy == 1:
        current.walls[0] = False
        next_cell.walls[2] = False


def reset_generation_state():
    # set up maze for generation
    destructables = []
    grid = [[Cell(x, y, CELL_SIZE, CELL_COLOR, WALL_COLOR, destructables) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    stack = []
    current = grid[0][0]
    current.visited = True
    generating = True
    return grid, stack, current, generating, destructables



def generate_item(current, enemies, collectables, grid, destructables):
    x = current.x
    y = current.y
    if random.random() < prob_candy:
        collectables.append(Collectable(x, y, candy_image, CELL_SIZE, "candy", None, collectables))

    elif random.random() < prob_flea:
        collectables.append(Collectable(x, y, flea_image, CELL_SIZE, "flea", None, collectables))
    
    elif random.random() < prob_sin:
        sinner = Sinner(x, y, sinner_image, CELL_SIZE, 5, None, grid)
        enemies.append(sinner)
        destructables.append(sinner)



def generate_maze():
    grid, stack, current, generating, destructables = reset_generation_state()
    enemies = []
    collectables = []

    while generating:
        neighbors = get_neighbors(current, grid)

        if neighbors:
            next_cell = random.choice(neighbors)
            stack.append(current)
            generate_item(current, enemies, collectables, grid, destructables)
            remove_walls(current, next_cell)
            current = next_cell
            current.visited = True

        elif stack:
            current = stack.pop()

        else:
            generating = False

    return grid, enemies, collectables, destructables


def main():
    running = True

    camera = Camera(0, 0, WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT, CELL_SIZE)
    grid, enemies, collectables, destructables = generate_maze()



    def draw(grid, objects, camera):
        screen.fill((0, 0, 0))

        # maze 
        for row in grid:
            for cell in row:
                cell.draw(screen, camera)

        for obj in objects:
            obj.draw(screen, camera)
            if isinstance(obj, Player):
                player.draw_m1(screen, camera)


        pygame.display.flip()

    def update(objects, camera, player, time):
        camera.update(player)

        for obj in objects:
            obj.update(grid, time)
        
        for item in collectables:
            item.collect(player)

        for item in [item for item in collectables if item.collected]:
            collectables.remove(item)
            objects.remove(item)
            

    player = Player(0, 0, player_placeholder, CELL_SIZE, 6, enemies, destructables)

    objs = [player]

    

    for enemy in enemies:
        enemy.set_target(player)

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            elif event.type == pygame.KEYDOWN:
                player.get_inputs(event.key, grid)
        
        draw(grid, objs + collectables + enemies, camera)
        update(objs + collectables + enemies, camera, player, current_time)


        clock.tick(FPS)

main()