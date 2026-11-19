import random
import pygame
from player import Player
from cell import Cell
from camera import Camera
from sinner import Sinner
from collectable import Collectable
from display import Display
from gms import GMS

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
pygame.mixer.init()

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


uwa_song = pygame.mixer.Sound("uwa.mp3")
morning_dance_song = pygame.mixer.Sound("morning_dance.mp3")



prob_candy = .04
prob_flea = .006
prob_sin = .04


def get_neighbors(cell, grid):
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
    destructables = []
    grid = [[Cell(x, y, CELL_SIZE, CELL_COLOR, WALL_COLOR, destructables) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    stack = []
    current = grid[0][0]
    current.visited = True
    generating = True
    return grid, stack, current, generating, destructables



def generate_item(current, enemies, collectables, grid, destructables, summon, player_pos):
    x = current.x
    y = current.y
    if not summon and random.random() < prob_candy:
        collectables.append(Collectable(x, y, candy_image, CELL_SIZE, "candy", None, collectables))

    elif not summon and random.random() < prob_flea:
        collectables.append(Collectable(x, y, flea_image, CELL_SIZE, "flea", None, collectables))
    
    elif random.random() < prob_sin and abs(x - player_pos[0]) + abs(y - player_pos[1]) >= 10:
        sinner = Sinner(x, y, sinner_image, CELL_SIZE, 3, None, grid)
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
            generate_item(current, enemies, collectables, grid, destructables, False, tuple([0, 0]))
            remove_walls(current, next_cell)
            current = next_cell
            current.visited = True

        elif stack:
            current = stack.pop()

        else:
            generating = False

    open_walls(grid, 256)
    return grid, enemies, collectables, destructables

def open_walls(grid, amount):
    for i in range(amount):
        x = random.randrange(len(grid))
        y = random.randrange(len(grid[0]))
        current = grid[y][x]
        options = []

        if y > 0 and current.walls[0]: options.append((0, -1))
        if x < len(grid) - 1 and current.walls[1]: options.append((1, 0))
        if y < len(grid[0]) - 1 and current.walls[2]: options.append((0, 1))
        if x > 0 and current.walls[3]: options.append((-1, 0))

        if options:
            dx, dy = random.choice(options)
            next_cell = grid[y + dy][x + dx]
            remove_walls(current, next_cell)

def main():

        
    bg_channel = pygame.mixer.Channel(0)
    bg_channel.set_volume(0.3)

    running = True

    camera = Camera(0, 0, WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT, CELL_SIZE)
    grid, enemies, collectables, destructables = generate_maze()
    debug = False
    death = False

    def draw(grid, objects, camera, display):
        screen.fill((0, 0, 0))

        # maze 
        for row in grid:
            for cell in row:
                cell.draw(screen, camera)

        for obj in objects:
            obj.draw(screen, camera)
            if isinstance(obj, Player):
                player.draw_m1(screen, camera)

            if isinstance(obj, Sinner) and debug:
                if obj.state == "pursuit":
                    obj.draw_path(screen, camera)
                obj.debug_draw(screen, camera)

        display.draw(screen)

        pygame.display.flip()

    def update(objects, camera, player, time, display):
        nonlocal death
        camera.update(player)
        display.update()

        for obj in objects:
            obj.update(grid, time)
            if isinstance(obj, Sinner):
                if obj.end_game():
                    death = True
        if len(enemies) <= 33:
            for i in range(random.randint(15, 40)):
                x = random.randrange(len(grid))
                y = random.randrange(len(grid[0]))
                generate_item(grid[x][y], enemies, collectables, grid, destructables, False, tuple([0, 0]))
                for enemy in enemies:
                    if enemy.global_target == None:
                        enemy.set_target(player)


        
        for item in collectables:
            item.collect(player)

        for item in [item for item in collectables if item.collected]:
            collectables.remove(item)
            objects.remove(item)
            

    player = Player(0, 0, player_placeholder, CELL_SIZE, 6, enemies, destructables, 3)

    objs = [player]

    for enemy in enemies:
        enemy.set_target(player)

    display = Display(None, player, WIDTH, HEIGHT)

    bg_channel.play(uwa_song, loops=-1)
    new_last_player_move = "up"
    last_player_move = "up"
    boss = GMS(len(grid) - 5, len(grid[0]) - 5, gms_image, CELL_SIZE, 999, player, grid)
    enemies.append(boss)
    destructables.append(boss)

    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or death:
                running = False
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    debug = not debug
                
                new_last_player_move = player.get_inputs(event.key, grid)

        boss.data_intake(new_last_player_move, last_player_move)
        last_player_move = new_last_player_move


        draw(grid, objs + collectables + enemies, camera, display)
        update(objs + collectables + enemies, camera, player, current_time, display)


        clock.tick(FPS)

main()