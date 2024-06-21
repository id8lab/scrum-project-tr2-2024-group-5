import pygame as pg

# pygame setup
pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption('Top-Down Race')
clock = pg.time.Clock()
running = True
dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# Load the player image
player_image = pg.image.load("main-game contents/Vehicles/supercar4.png")
player_image = pg.transform.scale(player_image, (60, 77))  # Scale the image to desired size

# Get the rect of the image
player_rect = player_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")

    # pygame.draw.circle(screen, "black", player_pos, 60)
    screen.blit(player_image, player_rect.topleft)

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        player_rect.y -= 300 * dt
    if keys[pg.K_s]:
        player_rect.y += 300 * dt
    if keys[pg.K_a]:
        player_rect.x -= 300 * dt
    if keys[pg.K_d]:
        player_rect.x += 300 * dt

    # flip() the display to put your work on screen
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pg.quit()
