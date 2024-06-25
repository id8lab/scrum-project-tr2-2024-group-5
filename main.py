import pygame as pg
import random

# Pygame setup
pg.init()
bgm = ["main-game contents/Audio/bgm1.mp3", "main-game contents/Audio/bgm2.mp3", "main-game contents/Audio/bgm3.mp3",
       "main-game contents/Audio/bgm4.mp3"]
bgm_play_track = random.randint(0, 3)

screen = pg.display.set_mode((1280, 720))
pg.display.set_caption('Top-Down Race')
clock = pg.time.Clock()
running = True
dt = 0

# Load the game's background
road_background = pg.image.load('main-game contents/Backgrounds/Road_Background.jpg')
resized_background = pg.transform.scale(road_background, (1290, 723))

# Load the tree props
tree_props_1 = pg.image.load('main-game contents/Backgrounds/Bunch_of_Trees1.png')

# Initial positions
background_road_pos_y1 = 0
background_road_pos_y2 = -723
tree_props_pos_y1 = 0
tree_props_pos_y2 = -723

# Load the player image
player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_image = pg.image.load("main-game contents/Vehicles/supercar4.png")
player_image = pg.transform.scale(player_image, (200, 200))  # Scale the image to desired size

# Load the background game sound
bgm_play = pg.mixer.Sound(bgm[bgm_play_track]).play(-1)
bgm_play.set_volume(0.6)


def draw_background():
    screen.blit(resized_background, (0, background_road_pos_y1))
    screen.blit(resized_background, (0, background_road_pos_y2))


def draw_trees():
    screen.blit(tree_props_1, (-500, tree_props_pos_y1))
    screen.blit(tree_props_1, (700, tree_props_pos_y1))
    screen.blit(tree_props_1, (-500, tree_props_pos_y2))
    screen.blit(tree_props_1, (700, tree_props_pos_y2))


while running:
    # Poll for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Add the surfaces
    draw_background()
    draw_trees()
    screen.blit(player_image, player_pos)

    # Update positions for scrolling effect
    scroll_speed = 18  # Increase this value to make it faster
    background_road_pos_y1 += scroll_speed
    background_road_pos_y2 += scroll_speed
    tree_props_pos_y1 += scroll_speed
    tree_props_pos_y2 += scroll_speed

    # Reset positions once off-screen to create continuous loop
    if background_road_pos_y1 >= 723:
        background_road_pos_y1 = -723
    if background_road_pos_y2 >= 723:
        background_road_pos_y2 = -723
    if tree_props_pos_y1 >= 723:
        tree_props_pos_y1 = -723
    if tree_props_pos_y2 >= 723:
        tree_props_pos_y2 = -723

    # Player movement
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player_pos.y -= 400 * dt
    if keys[pg.K_s]:
        player_pos.y += 200 * dt
    if keys[pg.K_a]:
        player_pos.x -= 300 * dt
    if keys[pg.K_d]:
        player_pos.x += 300 * dt

    # Flip the display to put your work on screen
    pg.display.flip()

    # Limit FPS to 60
    dt = clock.tick(60) / 1000

pg.quit()
