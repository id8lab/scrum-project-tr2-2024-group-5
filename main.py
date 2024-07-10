import pygame as pg
import random

OBSTACLES = ["main-game contents/Obstacles/Wood.png", "main-game contents/Obstacles/Axe.png",
             "main-game contents/Obstacles/Stone.png"]
VEHICLES = ["main-game contents/Vehicles/roadster1.png", "main-game contents/Vehicles/roadster2.png",
            "main-game contents/Vehicles/roadster3.png", "main-game contents/Vehicles/roadster4.png",
            "main-game contents/Vehicles/supercar1.png", "main-game contents/Vehicles/supercar2.png",
            "main-game contents/Vehicles/supercar3.png", "main-game contents/Vehicles/supercar4.png",
            "main-game contents/Vehicles/SUV1.png", "main-game contents/Vehicles/SUV2.png",
            "main-game contents/Vehicles/SUV3.png", "main-game contents/Vehicles/SUV4.png"]

VEHICLE_SOUNDS = [
    "main-game contents/Audio/motorbike.mp3",
    "main-game contents/Audio/supercar.mp3",
    "main-game contents/Audio/roadster.mp3",
    "main-game contents/Audio/suv.mp3"
]

MOVEMENT_SOUNDS = {
    "w": "main-game contents/Audio/motorbike.mp3",
    "a": "main-game contents/Audio/motorbike.mp3",
    "d": "main-game contents/Audio/motorbike.mp3",
    "s": "main-game contents/Audio/motor stop.mp3"
}

bgm = ["main-game contents/Audio/bgm1.mp3", "main-game contents/Audio/bgm2.mp3",
       "main-game contents/Audio/bgm3.mp3",
       "main-game contents/Audio/bgm4.mp3"]


class Score:
    def __init__(self, font_name='Arial', font_size=50, color=(255, 255, 255), initial_score=0):
        self.score = initial_score
        self.font = pg.font.SysFont(font_name, font_size)
        self.color = color
        self.last_update_time = pg.time.get_ticks()

    def update(self, current_time, increment=1, interval=1000):
        # Increment the score if enough time has passed
        if (current_time - self.last_update_time) >= interval:
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


class Player:
    def __init__(self, image_path, start_pos):
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (150, 150))  # Scale the image to 100x100 pixels
        self.pos = pg.Vector2(start_pos)
        self.health = 3
        self.max_health = 3
        self.heart_image = pg.transform.scale(pg.image.load('main-game contents/Obstacles/heart.png'), (50, 50))  # Load and scale the heart image

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def draw_health(self, screen, x=10, y=70):
        for i in range(self.max_health):
            if i < self.health:
                screen.blit(self.heart_image, (x + i * 55, y))
            else:
                empty_heart_image = pg.Surface((50, 50), pg.SRCALPHA)  # Create an empty surface for the empty heart
                pg.draw.rect(empty_heart_image, (255, 255, 255, 50), empty_heart_image.get_rect(), border_radius=5)  # Draw a transparent rectangle
                screen.blit(empty_heart_image, (x + i * 55, y))

    def get_rect(self):
        return self.image.get_rect(topleft=self.pos)

    def reduce_health(self):
        self.health -= 1
        return self.health


class BackgroundMusic:
    def __init__(self, bgm_paths):
        self.bgm_paths = bgm_paths
        self.current_bgm = None

    def play_random(self):
        bgm_play_track = random.choice(self.bgm_paths)
        print(f"Playing BGM: {bgm_play_track}")
        self.current_bgm = pg.mixer.music.load(bgm_play_track)
        pg.mixer.music.play(-1)  # -1 means loop indefinitely
        pg.mixer.music.set_volume(0.4)  # Adjust volume here

    def stop(self):
        pg.mixer.music.stop()


class MovementSounds:
    def __init__(self, move_sounds_paths):
        self.move_channels = {key: pg.mixer.Channel(i) for i, key in enumerate(move_sounds_paths.keys())}
        self.move_sounds = {key: pg.mixer.Sound(path) for key, path in move_sounds_paths.items()}

        # Set volume for each sound effect
        for sound in self.move_sounds.values():
            sound.set_volume(1)  # Adjust volume here

    def play(self, key):
        if key in self.move_channels:
            self.move_channels[key].play(self.move_sounds[key])

    def stop(self, key):
        if key in self.move_channels:
            self.move_channels[key].stop()

    def stop_all(self):
        for channel in self.move_channels.values():
            channel.stop()


def main():
    # Pygame setup
    pg.init()
    bgm_play_track = random.choice(bgm)
    vehicle_choice = random.choice(VEHICLES)
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
    obstacle_x_pos_1 = 390
    obstacle_x_pos_2 = 900

    # Load the player image
    player = Player(vehicle_choice, (screen.get_width() / 2, screen.get_height() / 2))
    # Load the background game sound
    bgm_play = pg.mixer.Sound(bgm_play_track).play(-1)
    bgm_play.set_volume(0.6)

    # Load obstacle images and scale them down
    obstacle_images = [pg.transform.scale(pg.image.load(obstacle), (50, 50)) for obstacle in OBSTACLES]
    # List to store active obstacles
    obstacles = []
    obstacle_spawn_time = pg.time.get_ticks()

    # Load the mud puddle image and set initial position and spawn time
    mud_puddle_image = pg.image.load('main-game contents/Obstacles/Mud.png').convert_alpha()
    mud_puddle_image = pg.transform.scale(mud_puddle_image, (100, 100))
    mud_puddle_rect = mud_puddle_image.get_rect(midtop=(screen.get_width() // 2, -50))
    mud_puddle_spawn_time = pg.time.get_ticks()

    speed_reduction_factor = 0.2  # Reduce speed by 50%

    bgm_manager = BackgroundMusic(bgm)
    movement_sounds = MovementSounds(MOVEMENT_SOUNDS)
    bgm_manager.play_random()

    def draw_background():
        screen.blit(resized_background, (0, background_road_pos_y1))
        screen.blit(resized_background, (0, background_road_pos_y2))

    def draw_trees():
        screen.blit(tree_props_1, (-500, tree_props_pos_y1))
        screen.blit(tree_props_1, (700, tree_props_pos_y1))
        screen.blit(tree_props_1, (-500, tree_props_pos_y2))
        screen.blit(tree_props_1, (700, tree_props_pos_y2))

    def spawn_obstacle():
        # Generate a random number between 0 and 1
        spawn_chance = random.random()
        if spawn_chance < 0.5:  # Adjust this threshold as needed
            obstacle_image = random.choice(obstacle_images)
            obstacle_rect = obstacle_image.get_rect(midtop=(random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50))
            obstacles.append((obstacle_image, obstacle_rect))

    def spawn_mud_puddle():
        mud_puddle_rect.midtop = (
            random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)  # Random x position within specific range

    # This is where the game runs
    while running:
        # Poll for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    movement_sounds.play("w")
                elif event.key == pg.K_a:
                    movement_sounds.play("a")
                elif event.key == pg.K_s:
                    movement_sounds.play("s")
                elif event.key == pg.K_d:
                    movement_sounds.play("d")
            elif event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    movement_sounds.stop("w")
                elif event.key == pg.K_a:
                    movement_sounds.stop("a")
                elif event.key == pg.K_s:
                    movement_sounds.stop("s")
                elif event.key == pg.K_d:
                    movement_sounds.stop("d")

        # Add the surfaces
        draw_background()
        screen.blit(mud_puddle_image, mud_puddle_rect)
        player.draw(screen)
        draw_trees()
        score.draw(screen)
        current_time = pg.time.get_ticks()
        score.update(current_time, increment=1, interval=500)

        # Spawn obstacles periodically
        if (current_time - obstacle_spawn_time) >= 5000:
            spawn_obstacle()
            obstacle_spawn_time = current_time

        # Move obstacles and detect collisions
        for obstacle_image, obstacle_rect in obstacles:
            obstacle_rect.y += 5
            # If obstacle moves off the screen, reset its position
            if obstacle_rect.top > screen.get_height():
                obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
            screen.blit(obstacle_image, obstacle_rect)
            if obstacle_rect.colliderect(player.get_rect()):
                player.reduce_health()
                print(f"Collision detected! Health: {player.health}")
                if player.health <= 0:
                    running = False
                # Reset the obstacle position to simulate it falling again
                obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)

        # Spawn and move the mud puddle
        if (current_time - mud_puddle_spawn_time) >= 10000:
            spawn_mud_puddle()
            mud_puddle_spawn_time = current_time

        mud_puddle_rect.y += 5  # Move the mud puddle
        if mud_puddle_rect.top > screen.get_height():
            mud_puddle_rect.midtop = (
                random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)  # Reset mud puddle position
        player_slowed = mud_puddle_rect.colliderect(player.get_rect())  # Check for collision with mud puddle

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

        # Player controls
        keys = pg.key.get_pressed()

        if player_slowed:
            speed_modifier = speed_reduction_factor  # Apply the speed reduction factor
        else:
            speed_modifier = 1

        if keys[pg.K_w]:
            player.pos.y -= 400 * dt * speed_modifier
        if keys[pg.K_s]:
            player.pos.y += 200 * dt * speed_modifier
        if keys[pg.K_a]:
            player.pos.x -= 300 * dt * speed_modifier
        if keys[pg.K_d]:
            player.pos.x += 300 * dt * speed_modifier
        if keys[pg.K_l]:
            vehicle_choice = random.choice(VEHICLES)
            player.image = pg.image.load(vehicle_choice).convert_alpha()
            player.image = pg.transform.scale(player.image, (150, 150))  # Scale the image to 150x150 pixels

        # Stop sounds when no movement
        if not (keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]):
            movement_sounds.stop_all()

        # Draw health hearts at the end to ensure they are on top
        player.draw_health(screen)

        # Flip the display to put your work on screen
        pg.display.flip()

        # Limit FPS to 60
        dt = clock.tick(60) / 1000

    # Cleanup
    movement_sounds.stop_all()
    bgm_manager.stop()
    pg.quit()


main()
