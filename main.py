# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
pygame.display.set_caption('Top-Down Race')
clock = pygame.time.Clock()
running = True
dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# Load the player image
player_image = pygame.image.load("Kanata_Tpose.png")
player_image = pygame.transform.scale(player_image, (60, 77))  # Scale the image to desired size

# Get the rect of the image
player_rect = player_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")

    # pygame.draw.circle(screen, "black", player_pos, 60)
    screen.blit(player_image, player_rect.topleft)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= 300 * dt
    if keys[pygame.K_s]:
        player_rect.y += 300 * dt
    if keys[pygame.K_a]:
        player_rect.x -= 300 * dt
    if keys[pygame.K_d]:
        player_rect.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
