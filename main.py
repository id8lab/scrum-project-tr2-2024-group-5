import pygame as pg
import random

# Paths to game contents
OBSTACLES = ["main-game contents/Obstacles/crate.png", "main-game contents/Vehicles/roadster2.png",
             "main-game contents/Vehicles/supercar4.png", "main-game contents/Vehicles/SUV1.png"]
VEHICLES = ["main-game contents/Vehicles/roadster1.png", "main-game contents/Vehicles/roadster2.png",
            "main-game contents/Vehicles/roadster3.png", "main-game contents/Vehicles/roadster4.png",
            "main-game contents/Vehicles/supercar1.png", "main-game contents/Vehicles/supercar2.png",
            "main-game contents/Vehicles/supercar3.png", "main-game contents/Vehicles/supercar4.png",
            "main-game contents/Vehicles/SUV1.png", "main-game contents/Vehicles/SUV2.png",
            "main-game contents/Vehicles/SUV3.png", "main-game contents/Vehicles/SUV4.png"]

# Sound paths for vehicles and movements
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

# Background music paths
bgm = ["main-game contents/Audio/bgm1.mp3",
       "main-game contents/Audio/bgm2.mp3",
       "main-game contents/Audio/bgm3.mp3",
       "main-game contents/Audio/bgm4.mp3"
]


class Score:
    def __init__(self, font_name='Arial', font_size=50, color=(255, 255, 255), initial_score=0):
        self.score = initial_score
        self.font = pg.font.SysFont(font_name, font_size)
        self.color = color
        self.last_update_time = pg.time.get_ticks()

    def update(self, current_time, increment=1, interval=1000):
        if current_time - self.last_update_time >= interval:
            self.score += increment
            self.last_update_time = current_time

    def draw(self, screen, x=10, y=10):
        score_surface = self.font.render(f'Score: {self.score}', True, self.color)
        screen.blit(score_surface, (x, y))

    def reset(self):
        self.score = 0
        self.last_update_time = pg.time.get_ticks()


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
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption('Top-Down Race')
    clock = pg.time.Clock()
    running = True
    dt = 0

    pg.mixer.init()

    # Load game background
    road_background = pg.image.load('main-game contents/Backgrounds/Road_Background.jpg')
    resized_background = pg.transform.scale(road_background, (1290, 723))
    score = Score()

    # Load tree props
    tree_props_1 = pg.image.load('main-game contents/Backgrounds/Bunch_of_Trees1.png')
    # Initial positions
    background_road_pos_y1 = 0
    background_road_pos_y2 = -723
    tree_props_pos_y1 = 0
    tree_props_pos_y2 = -723
    # Load player image
    vehicle_choice = random.choice(VEHICLES)
    player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player_image = pg.image.load(vehicle_choice)
    player_image = pg.transform.scale(player_image, (200, 200))  # Scale image

    bgm_manager = BackgroundMusic(bgm)
    movement_sounds = MovementSounds(MOVEMENT_SOUNDS)

    # Play background music
    bgm_manager.play_random()

    while running:
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

        # Render elements
        screen.blit(resized_background, (0, background_road_pos_y1))
        screen.blit(resized_background, (0, background_road_pos_y2))
        screen.blit(player_image, player_pos)
        screen.blit(tree_props_1, (-500, tree_props_pos_y1))
        screen.blit(tree_props_1, (700, tree_props_pos_y1))
        screen.blit(tree_props_1, (-500, tree_props_pos_y2))
        screen.blit(tree_props_1, (700, tree_props_pos_y2))
        score.draw(screen)
        current_time = pg.time.get_ticks()
        score.update(current_time, increment=1, interval=500)

        # Scroll effect
        scroll_speed = 18
        background_road_pos_y1 += scroll_speed
        background_road_pos_y2 += scroll_speed
        tree_props_pos_y1 += scroll_speed
        tree_props_pos_y2 += scroll_speed

        # Reset positions
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

        # Stop sounds when no movement
        if not (keys[pg.K_w] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_d]):
            movement_sounds.stop_all()

        # Change vehicle image (testing)
        if keys[pg.K_l]:
            vehicle_choice = random.choice(VEHICLES)
            player_image = pg.image.load(vehicle_choice)
            player_image = pg.transform.scale(player_image, (200, 200))

        # Update screen
        pg.display.flip()

        # Cap FPS
        dt = clock.tick(60) / 1000

    # Cleanup
    movement_sounds.stop_all()
    bgm_manager.stop()
    pg.quit()

if __name__ == "__main__":
    main()
