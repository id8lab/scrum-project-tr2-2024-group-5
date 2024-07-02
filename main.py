import pygame as pg
import random


class Score:
    def __init__(self, font_name='Arial', font_size=50, color=(255, 255, 255), initial_score=0):
        self.score = initial_score
        self.font = pg.font.SysFont(font_name, font_size)
        self.color = color
        self.last_update_time = pg.time.get_ticks()

    def update(self, current_time, increment=1, interval=1000):
        # Increment the score if enough time has passed
        if current_time - self.last_update_time >= interval:
            self.score += increment
            self.last_update_time = current_time

    def draw(self, screen, x=10, y=10):
        # Render the score as a surface
        score_surface = self.font.render(f'Score: {self.score}', True, self.color)
        # Draw the score on the screen at position (x, y)
        screen.blit(score_surface, (x, y))

    def reset(self):
        self.score = 0
        self.last_update_time = pg.time.get_ticks()


def main():
    # Pygame setup
    pg.init()
    bgm = ["main-game contents/Audio/bgm1.mp3", "main-game contents/Audio/bgm2.mp3",
           "main-game contents/Audio/bgm3.mp3",
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
    score = Score()
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

    # This is where the game runs
    while running:
        # Poll for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Add the surfaces
        draw_background()
        screen.blit(player_image, player_pos)
        draw_trees()
        score.draw(screen)
        current_time = pg.time.get_ticks()
        score.update(current_time, increment=1, interval=500)

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


main()
