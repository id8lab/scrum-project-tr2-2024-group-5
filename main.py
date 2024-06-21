import pygame as pg

# pygame setup
pg.init()

screen = pg.display.set_mode((1280, 720))
pg.display.set_caption('Top-Down Race')
clock = pg.time.Clock()
running = True
dt = 0

# Load the game's background
road_background = pg.image.load('main-game contents/Backgrounds/Road_Background.jpg')
resized_background = pg.transform.scale(road_background, (1280, 720))

# Load the player image
player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# player_image = pg.draw.circle(screen, "red", player_pos, 40)  # Placeholder for now


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Add the surfaces
    screen.blit(resized_background, (0, 0))

    pg.draw.circle(screen, "red", player_pos, 40)

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player_pos.y -= 500 * dt
    if keys[pg.K_s]:
        player_pos.y += 100 * dt
    if keys[pg.K_a]:
        player_pos.x -= 300 * dt
    if keys[pg.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pg.quit()
