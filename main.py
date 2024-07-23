import pygame as pg
import random

PLAYER_SIZE_Y = 160
PLAYER_SIZE_X = 80

# Define constants
OBSTACLES = ["main-game contents/Obstacles/Wood.png", "main-game contents/Obstacles/crate.png",
             "main-game contents/Obstacles/Stone.png"]
VEHICLES = ["main-game contents/Vehicles/roadster1.png", "main-game contents/Vehicles/roadster2.png",
            "main-game contents/Vehicles/roadster3.png", "main-game contents/Vehicles/roadster4.png",
            "main-game contents/Vehicles/supercar1.png", "main-game contents/Vehicles/supercar2.png",
            "main-game contents/Vehicles/supercar3.png", "main-game contents/Vehicles/supercar4.png",
            "main-game contents/Vehicles/SUV1.png", "main-game contents/Vehicles/SUV2.png",
            "main-game contents/Vehicles/SUV3.png", "main-game contents/Vehicles/SUV4.png",
            "main-game contents/Vehicles/motorbike1.png", "main-game contents/Vehicles/motorbike2.png",
            "main-game contents/Vehicles/motorbike3.png", "main-game contents/Vehicles/motorbike4.png"
            ]

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
BGM = ["main-game contents/Audio/bgm1.mp3", "main-game contents/Audio/bgm2.mp3",
       "main-game contents/Audio/bgm3.mp3", "main-game contents/Audio/bgm4.mp3"]


# Define classes
class Score:
    def __init__(self, font_name='Arial', font_size=50, color=(255, 255, 255), initial_score=0):
        self.score = initial_score
        self.font = pg.font.SysFont(font_name, font_size)
        self.color = color
        self.last_update_time = pg.time.get_ticks()

    def update(self, current_time, increment=1, interval=1000):
        if (current_time - self.last_update_time) >= interval:
            self.score += increment
            self.last_update_time = current_time

    def draw(self, screen, x=10, y=10):
        score_surface = self.font.render(f'Score: {self.score}', True, self.color)
        screen.blit(score_surface, (x, y))

    def reset(self):
        self.score = 0
        self.last_update_time = pg.time.get_ticks()


class Player:
    def __init__(self, image_path, start_pos):
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        self.pos = pg.Vector2(start_pos)
        self.health = 3
        self.max_health = 3
        self.heart_image = pg.transform.scale(pg.image.load('main-game contents/Obstacles/heart.png'), (50, 50))

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def draw_health(self, screen, x=10, y=70):
        for i in range(self.max_health):
            if i < self.health:
                screen.blit(self.heart_image, (x + i * 55, y))
            else:
                empty_heart_image = pg.Surface((50, 50), pg.SRCALPHA)
                pg.draw.rect(empty_heart_image, (255, 255, 255, 50), empty_heart_image.get_rect(), border_radius=5)
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
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.4)

    def stop(self):
        pg.mixer.music.stop()


class MovementSounds:
    def __init__(self, move_sounds_paths):
        self.move_channels = {key: pg.mixer.Channel(i) for i, key in enumerate(move_sounds_paths.keys())}
        self.move_sounds = {key: pg.mixer.Sound(path) for key, path in move_sounds_paths.items()}
        for sound in self.move_sounds.values():
            sound.set_volume(1)

    def play(self, key):
        if key in self.move_channels:
            self.move_channels[key].play(self.move_sounds[key])

    def stop(self, key):
        if key in self.move_channels:
            self.move_channels[key].stop()

    def stop_all(self):
        for channel in self.move_channels.values():
            channel.stop()


def display_race_result(screen, score):
    screen.fill((0, 0, 0))

    # Create a larger font for the result and score
    large_font = pg.font.SysFont('Arial', 50)
    normal_font = pg.font.SysFont('Arial', 30)

    result_text = large_font.render('Race Over!', True, (255, 0, 0))
    score_text = large_font.render(f'Score: {score}', True, (255, 255, 255))

    # Load background image
    background_image = pg.image.load('main-game contents/Backgrounds/result.png')
    background_rect = background_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(background_image, background_rect)

    # Button dimensions and positions
    button_width = 200
    button_height = 60
    restart_button = pg.Rect(screen.get_width() // 2 - button_width // 2, screen.get_height() // 2 + 50, button_width,
                             button_height)
    quit_button = pg.Rect(screen.get_width() // 2 - button_width // 2, screen.get_height() // 2 + 120, button_width,
                          button_height)

    # Button colors
    restart_color = (0, 200, 0)  # Green
    quit_color = (200, 0, 0)  # Red

    # Draw buttons
    pg.draw.rect(screen, restart_color, restart_button)
    pg.draw.rect(screen, quit_color, quit_button)

    # Position texts at the top
    screen.blit(result_text, (screen.get_width() // 2 - result_text.get_width() // 2, 20))
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 80))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    main()  # Restart game
                elif quit_button.collidepoint(mouse_pos):
                    pg.quit()
                    return

        # Render button text
        restart_text = normal_font.render('Try Again', True, (255, 255, 255))
        quit_text = normal_font.render('Quit', True, (255, 255, 255))
        screen.blit(restart_text, (restart_button.x + (button_width - restart_text.get_width()) // 2,
                                   restart_button.y + (button_height - restart_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2,
                                quit_button.y + (button_height - quit_text.get_height()) // 2))

        pg.display.flip()


def main():
    # Initialize the game
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption('Top-Down Race')
    clock = pg.time.Clock()
    running = True
    dt = 0
    paused = False
    road_background = pg.image.load('main-game contents/Backgrounds/Road_Background.jpg')
    resized_background = pg.transform.scale(road_background, (1290, 723))
    score = Score()
    tree_props_1 = pg.image.load('main-game contents/Backgrounds/Bunch_of_Trees1.png')
    background_road_pos_y1 = 0
    background_road_pos_y2 = -723
    tree_props_pos_y1 = 0
    tree_props_pos_y2 = -723
    obstacle_x_pos_1 = 390
    obstacle_x_pos_2 = 900
    player = Player(random.choice(VEHICLES), (screen.get_width() / 2, screen.get_height() / 2))
    pg.mixer.Sound(random.choice(BGM)).play(-1).set_volume(0.6)
    obstacle_images = [pg.transform.scale(pg.image.load(obstacle), (50, 50)) for obstacle in OBSTACLES]
    obstacles = []
    spawn_times = {
        "obstacle": pg.time.get_ticks(),
        "mud_puddle": pg.time.get_ticks(),
        "speed_platform": pg.time.get_ticks()
    }
    mud_puddle_image = pg.image.load('main-game contents/Obstacles/Mud.png').convert_alpha()
    mud_puddle_image = pg.transform.scale(mud_puddle_image, (100, 100))
    mud_puddle_rect = mud_puddle_image.get_rect(midtop=(screen.get_width() // 2, -50))
    speed_platform_image = pg.image.load('main-game contents/Obstacles/arrow.png').convert_alpha()
    speed_platform_image = pg.transform.scale(speed_platform_image, (50, 100))
    speed_platform_rect = speed_platform_image.get_rect(
        midtop=(random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50))
    speed_reduction_factor = 0.2
    bgm_manager = BackgroundMusic(BGM)
    movement_sounds = MovementSounds(MOVEMENT_SOUNDS)
    bgm_manager.play_random()
    scroll_speed = 10  # Initial scroll speed
    speed_increase_interval = 15000  # Interval to increase speed (in milliseconds)
    last_speed_increase_time = pg.time.get_ticks()

    # Define border rectangles
    left_border = pg.Rect(0, 0, 353, 720)
    right_border = pg.Rect(935, 0, 353, 720)

    def draw_background():
        screen.blit(resized_background, (0, background_road_pos_y1))
        screen.blit(resized_background, (0, background_road_pos_y2))

    def draw_trees():
        screen.blit(tree_props_1, (-500, tree_props_pos_y1))
        screen.blit(tree_props_1, (700, tree_props_pos_y1))
        screen.blit(tree_props_1, (-500, tree_props_pos_y2))
        screen.blit(tree_props_1, (700, tree_props_pos_y2))

    def spawn_entity(entity_type):
        if entity_type == "obstacle":
            if random.random() < 0.5:
                obstacle_image = random.choice(obstacle_images)
                obstacle_rect = obstacle_image.get_rect(
                    midtop=(random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50))
                obstacles.append((obstacle_image, obstacle_rect))
        elif entity_type == "mud_puddle":
            mud_puddle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
        elif entity_type == "speed_platform":
            speed_platform_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)

    def draw_border():
        border = pg.Surface((353, 720), pg.SRCALPHA).convert()
        screen.blit(border, (0, 0))
        screen.blit(border, (935, 0))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = not paused
                if not paused:
                    if event.key == pg.K_w:
                        movement_sounds.play("w")
                    elif event.key == pg.K_a:
                        movement_sounds.play("a")
                    elif event.key == pg.K_s:
                        movement_sounds.play("s")
                    elif event.key == pg.K_d:
                        movement_sounds.play("d")
            elif event.type == pg.KEYUP and not paused:
                if event.key == pg.K_w:
                    movement_sounds.stop("w")
                if event.key == pg.K_a:
                    movement_sounds.stop("a")
                if event.key == pg.K_s:
                    movement_sounds.stop("s")
                if event.key == pg.K_d:
                    movement_sounds.stop("d")

        if not paused:
            draw_border()
            draw_background()
            screen.blit(mud_puddle_image, mud_puddle_rect)
            screen.blit(speed_platform_image, speed_platform_rect)
            player.draw(screen)
            draw_trees()
            score.draw(screen)
            current_time = pg.time.get_ticks()
            score.update(current_time, increment=1, interval=500)

            for entity_type, last_spawn_time in spawn_times.items():
                if (current_time - last_spawn_time) >= 5000 and entity_type == "obstacle":
                    spawn_entity(entity_type)
                    spawn_times[entity_type] = current_time
                elif (current_time - last_spawn_time) >= 10000 and entity_type == "mud_puddle":
                    spawn_entity(entity_type)
                    spawn_times[entity_type] = current_time
                elif (current_time - last_spawn_time) >= 12000 and entity_type == "speed_platform":
                    spawn_entity(entity_type)
                    spawn_times[entity_type] = current_time

            for obstacle_image, obstacle_rect in obstacles:
                obstacle_rect.y += scroll_speed
                if obstacle_rect.top > screen.get_height():
                    obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
                screen.blit(obstacle_image, obstacle_rect)
                if obstacle_rect.colliderect(player.get_rect()):
                    player.reduce_health()
                    print(f"Collision detected! Health: {player.health}")
                    if player.health <= 0:
                        running = False
                    obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)

            mud_puddle_rect.y += scroll_speed
            speed_platform_rect.y += scroll_speed

            if mud_puddle_rect.top > screen.get_height():
                mud_puddle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
            if speed_platform_rect.top > screen.get_height():
                speed_platform_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)

            player_slowed = mud_puddle_rect.colliderect(player.get_rect())
            player_speeded = speed_platform_rect.colliderect(player.get_rect())

            background_road_pos_y1 += scroll_speed
            background_road_pos_y2 += scroll_speed
            tree_props_pos_y1 += scroll_speed
            tree_props_pos_y2 += scroll_speed

            if background_road_pos_y1 >= 723:
                background_road_pos_y1 = -723
            if background_road_pos_y2 >= 723:
                background_road_pos_y2 = -723
            if tree_props_pos_y1 >= 723:
                tree_props_pos_y1 = -723
            if tree_props_pos_y2 >= 723:
                tree_props_pos_y2 = -723

            keys = pg.key.get_pressed()

            if player_slowed:
                speed_modifier = speed_reduction_factor
            elif player_speeded:
                speed_modifier = 2
                player.pos.y -= 50  # Move the player up when colliding with the speed platform
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
                player.image = pg.transform.scale(player.image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))

            if not (keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]):
                movement_sounds.stop_all()

            player_rect = player.get_rect()
            border_push_down_speed = 500  # Speed at which the player is pushed down

            if player_rect.colliderect(left_border) or player_rect.colliderect(right_border):
                player.pos.y += border_push_down_speed * dt

            player.draw_health(screen)

            # Increase scroll speed over time
            if (current_time - last_speed_increase_time) >= speed_increase_interval:
                scroll_speed += 1
                last_speed_increase_time = current_time

            pg.display.flip()
            dt = clock.tick(60) / 1000

        else:
            # Display "Paused" message when the game is paused
            font = pg.font.Font(None, 74)
            text = font.render("Paused", True, (255, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(text, text_rect)
            pg.display.flip()
            dt = clock.tick(60) / 1000

    movement_sounds.stop_all()
    bgm_manager.stop()
    display_race_result(screen, score.score)
    pg.quit()


main()
