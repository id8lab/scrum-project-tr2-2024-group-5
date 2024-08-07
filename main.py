import pygame as pg
import random
import json

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
LEADERBOARD_FILE = "leaderboard.json"
ICON_SIZE = (100, 100)
RED_COLOR = (200, 0, 0)  # Red
WHITE_COLOR = (255, 255, 255)
PLAYER_SIZE_Y = 160
PLAYER_SIZE_X = 80
INGAME_BUTTON_WIDTH = 200
INGAME_BUTTON_HEIGHT = 60
TARGET_SEQUENCE = ['r', 'e', 's', 'e', 't']

# Define constants
OBSTACLES = ["main-game contents/Obstacles/Wood.png", "main-game contents/Obstacles/crate.png",
             "main-game contents/Obstacles/Stone.png"]

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
       "main-game contents/Audio/bgm3.mp3", "main-game contents/Audio/bgm4.mp3",
       "main-game contents/Audio/bgm5.mp3"]
BGM_LOBBY = ["main-game contents/Audio/lobby.mp3"]
BGM_RESULT = ["main-game contents/Audio/result.mp3"]
POWER_UPS = {
    "invincibility": "main-game contents/PowerUps/invincibility.png",
    "point_up": "main-game contents/PowerUps/point_up.png",
    "life_up": "main-game contents/PowerUps/life_up.png"
}


# Define classes
class Score:
    def __init__(self, font_name='Arial', font_size=50, color=(255, 255, 255), initial_score=0):
        self.score = initial_score
        self.font = pg.font.SysFont(font_name, font_size)
        self.color = color
        self.last_update_time = pg.time.get_ticks()
        self.points = 0
        self.double_points_until = 0

    def update(self, current_time, increment=1, interval=1000):
        if (current_time - self.last_update_time) >= interval:
            if current_time <= self.double_points_until:
                increment *= 2
            self.score += increment
            self.last_update_time = current_time

    def draw(self, screen, x=10, y=10):
        score_surface = self.font.render(f'Score: {self.score}', True, self.color)
        screen.blit(score_surface, (x, y))

    def reset(self):
        self.score = 0
        self.last_update_time = pg.time.get_ticks()


def save_score(score):
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = []
    leaderboard.append(score)
    leaderboard = sorted(leaderboard, reverse=True)[:5]
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file)


class Player:
    def __init__(self, image_path, start_pos):
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (PLAYER_SIZE_X, PLAYER_SIZE_Y))
        self.pos = pg.Vector2(start_pos)
        self.invincible_until = 0
        self.health = 3
        self.max_health = 3
        self.heart_image = pg.transform.scale(pg.image.load('main-game contents/Icons/heart.png'), (50, 50))

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

    def is_invincible(self):
        return pg.time.get_ticks() < self.invincible_until

    def reduce_health(self):
        if not self.is_invincible():
            self.health -= 1


class BackgroundMusic:
    def __init__(self, bgm_paths):
        self.bgm_paths = bgm_paths
        self.current_bgm = None
        self.volume = 0.4

    def play_random(self):
        bgm_play_track = random.choice(self.bgm_paths)
        print(f"Playing BGM: {bgm_play_track}")
        self.current_bgm = pg.mixer.music.load(bgm_play_track)
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(self.volume)

    def stop(self):
        pg.mixer.music.stop()

    def set_volume(self, volume_change):
        self.volume = max(0, min(1, self.volume + volume_change))
        pg.mixer.music.set_volume(self.volume)


class MovementSounds:
    def __init__(self, move_sounds_paths):
        self.move_channels = {key: pg.mixer.Channel(i) for i, key in enumerate(move_sounds_paths.keys())}
        self.move_sounds = {key: pg.mixer.Sound(path) for key, path in move_sounds_paths.items()}
        self.volume = 1
        for sound in self.move_sounds.values():
            sound.set_volume(self.volume)

    def play(self, key):
        if key in self.move_channels:
            self.move_channels[key].play(self.move_sounds[key])

    def stop(self, key):
        if key in self.move_channels:
            self.move_channels[key].stop()

    def stop_all(self):
        for channel in self.move_channels.values():
            channel.stop()

    def set_volume(self, volume_change):
        self.volume = max(0, min(1, self.volume + volume_change))
        pg.mixer.music.set_volume(self.volume)


class PowerUp:
    def __init__(self, power_up_type, image_path, position):
        self.type = power_up_type
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(midtop=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def apply_effect(self, player, score):
        if self.type == "invincibility":
            player.invincible_until = pg.time.get_ticks() + 5000  # 5 seconds
        elif self.type == "point_up":
            score.double_points_until = pg.time.get_ticks() + 5000  # 5 seconds
        elif self.type == "life_up":
            if player.health < player.max_health:
                player.health += 1

    def get_rect(self):
        return self.rect


def display_race_result(screen, score):
    screen.fill((0, 0, 0))
    save_score(score)
    bgm = BackgroundMusic(BGM_RESULT)
    bgm.play_random()

    # Create a larger font for the result and score
    large_font = pg.font.SysFont('Arial', 50)
    normal_font = pg.font.SysFont('Arial', 30)

    result_text = large_font.render('Race Over!', True, (255, 0, 0))
    score_text = large_font.render(f'Score: {score}', True, WHITE_COLOR)

    # Load background image
    background_image = pg.image.load('main-game contents/Icons/result.png')
    background_rect = background_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(background_image, background_rect)

    # Button dimensions and positions
    restart_button = pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, screen.get_height() // 2 + 50,
                             INGAME_BUTTON_WIDTH, INGAME_BUTTON_HEIGHT)
    quit_button = pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, screen.get_height() // 2 + 120,
                          INGAME_BUTTON_WIDTH, INGAME_BUTTON_HEIGHT)

    # Button colors
    restart_color = (0, 200, 0)  # Green

    # Draw buttons
    pg.draw.rect(screen, restart_color, restart_button)
    pg.draw.rect(screen, RED_COLOR, quit_button)

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
                    main_menu_display()
                    return

        # Render button text
        restart_text = normal_font.render('Try Again', True, WHITE_COLOR)
        quit_text = normal_font.render('Main Menu', True, WHITE_COLOR)
        screen.blit(restart_text, (restart_button.x + (INGAME_BUTTON_WIDTH - restart_text.get_width()) // 2,
                                   restart_button.y + (INGAME_BUTTON_HEIGHT - restart_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (INGAME_BUTTON_WIDTH - quit_text.get_width()) // 2,
                                quit_button.y + (INGAME_BUTTON_HEIGHT - quit_text.get_height()) // 2))

        pg.display.flip()


def main_menu(screen):
    menu_font = pg.font.SysFont('Arial', 30)
    menu_background = pg.image.load('main-game contents/Backgrounds/mainmenubackground.jpg')
    menu_background = pg.transform.scale(menu_background, (1280, 720))

    buttons = {
        'Play': pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, 300, INGAME_BUTTON_WIDTH,
                        INGAME_BUTTON_HEIGHT),
        'How to Play': pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, 380, INGAME_BUTTON_WIDTH,
                            INGAME_BUTTON_HEIGHT),
        'Leaderboard': pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, 460, INGAME_BUTTON_WIDTH,
                               INGAME_BUTTON_HEIGHT),
        'Quit': pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, 540, INGAME_BUTTON_WIDTH,
                        INGAME_BUTTON_HEIGHT)
    }

    button_colors = {
        'Play': (0, 200, 0),
        'How to Play': (0, 0, 200),
        'Leaderboard': (200, 200, 0),
        'Quit': (200, 0, 0)
    }

    while True:
        screen.blit(menu_background, (0, 0))

        for button_text, button_rect in buttons.items():
            pg.draw.rect(screen, button_colors[button_text], button_rect)
            text_surface = menu_font.render(button_text, True, WHITE_COLOR)
            screen.blit(text_surface, (button_rect.x + (INGAME_BUTTON_WIDTH - text_surface.get_width()) // 2,
                                       button_rect.y + (INGAME_BUTTON_HEIGHT - text_surface.get_height()) // 2))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button_text, button_rect in buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        if button_text == 'Play':
                            main()
                            return  # Start the game
                        elif button_text == 'How to Play':
                            controls(screen)
                        elif button_text == 'Leaderboard':
                            leaderboard_menu(screen)
                        elif button_text == 'Quit':
                            pg.quit()
                            return


def controls(screen):
    settings_font = pg.font.SysFont('Arial', 30)
    settings_background = pg.Surface(screen.get_size())
    settings_background.fill((0, 0, 0))
    settings_background.set_alpha(180)

    while True:
        screen.blit(settings_background, (0, 0))
        font = pg.font.SysFont('Arial', 50)
        text = font.render("Controls", True, WHITE_COLOR)
        text_rect = text.get_rect(midtop=(screen.get_width() / 2, 50))
        screen.blit(text, text_rect)

        # Controls, Volume and Gameplay Info
        controls_text = settings_font.render("Controls: A: Move left | S: Move down | D: Move right | "
                                             "ESC to pause.", True, WHITE_COLOR)
        volume_text = settings_font.render("Volume Settings: Use the Down (decrease) and Up (increase)"
                                           "arrow keys to adjust the volume.", True, WHITE_COLOR)
        gameplay_text = settings_font.render("Gameplay:",
                                             True, WHITE_COLOR)
        obstacle_text = settings_font.render("Avoid Obstacles (Rocks, Tree Logs, Wood Crate)", True,
                                             WHITE_COLOR)
        misc_text = settings_font.render("Mud puddle slows down your movement | Speed platform forces you to"
                                         " move up ", True, WHITE_COLOR)
        road_text = settings_font.render("Don't go off road, you will  be pushed down to the bottom of the screen",
                                         True, WHITE_COLOR)
        game_over_text = settings_font.render("Game over if you lose all of your lives or you went off screen",
                                              True, WHITE_COLOR)
        screen.blit(controls_text, (50, 150))
        screen.blit(volume_text, (50, 200))
        screen.blit(gameplay_text, (50, 250))
        screen.blit(obstacle_text, (50, 300))
        screen.blit(misc_text, (50, 350))
        screen.blit(road_text, (50, 400))
        screen.blit(game_over_text, (50, 450))

        # Button to return to Main Menu
        return_button = draw_return_button(font, screen, text)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if return_button.collidepoint(mouse_pos):
                    return


def check_sequence(buffer, sequence):  # For the leaderboard menu
    """Check if the buffer ends with the target sequence."""
    return buffer[-len(sequence):] == sequence


def leaderboard_menu(screen):
    leaderboard_font = pg.font.SysFont('Arial', 30)
    leaderboard_background = pg.Surface(screen.get_size())
    leaderboard_background.fill((0, 0, 0))
    leaderboard_background.set_alpha(180)
    key_buffer = []

    # 尝试加载排行榜
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            top_scores = json.load(file)
    except FileNotFoundError:
        top_scores = []

    while True:
        screen.blit(leaderboard_background, (0, 0))
        font = pg.font.SysFont('Arial', 50)
        text = font.render("Leaderboard", True, WHITE_COLOR)
        reset_text = font.render("Type 'reset' if you want to reset your leaderboard", True, WHITE_COLOR)
        text_rect = text.get_rect(midtop=(screen.get_width() / 2, 50))
        reset_rect = reset_text.get_rect(midtop=(screen.get_width() / 2, 380))
        screen.blit(text, text_rect)
        screen.blit(reset_text, reset_rect)

        # Display top 5 scores
        for i, score in enumerate(top_scores):
            score_text = leaderboard_font.render(f"{i + 1}. Score: {score}", True, WHITE_COLOR)
            screen.blit(score_text, (50, 150 + i * 40))

        # Button to return to Main Menu
        return_button = draw_return_button(font, screen, text)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if return_button.collidepoint(mouse_pos):
                    return
            if event.type == pg.KEYDOWN:
                key_buffer.append(event.unicode)
                # Check if the key buffer matches the target sequence
                if check_sequence(key_buffer, TARGET_SEQUENCE):
                    top_scores = [0, 0, 0, 0, 0]
                    with open(LEADERBOARD_FILE, "w") as file:
                        json.dump(top_scores, file)


def vehicle_type_selection_screen(screen, vehicle_type):
    # Paths to images for different types of the selected vehicle
    VEHICLE_TYPES = {
        "roadster": ["main-game contents/Vehicles/roadster1.png", "main-game contents/Vehicles/roadster2.png",
                     "main-game contents/Vehicles/roadster3.png", "main-game contents/Vehicles/roadster4.png"],
        "supercar": ["main-game contents/Vehicles/supercar1.png", "main-game contents/Vehicles/supercar2.png",
                     "main-game contents/Vehicles/supercar3.png", "main-game contents/Vehicles/supercar4.png"],
        "motorbike": ["main-game contents/Vehicles/motorbike1.png", "main-game contents/Vehicles/motorbike2.png",
                      "main-game contents/Vehicles/motorbike3.png", "main-game contents/Vehicles/motorbike4.png"],
        "SUV": ["main-game contents/Vehicles/SUV1.png", "main-game contents/Vehicles/SUV2.png",
                "main-game contents/Vehicles/SUV3.png", "main-game contents/Vehicles/SUV4.png"]
    }

    vehicle_images = [pg.image.load(path).convert_alpha() for path in VEHICLE_TYPES[vehicle_type]]
    scaled_vehicle_images = [pg.transform.scale(image, (50, 100)) for image in vehicle_images]  # Scale vehicle images

    # Adjust the spacing between vehicles
    vehicle_width = 50
    vehicle_spacing = 250  # Increase the spacing here
    num_vehicles = len(scaled_vehicle_images)
    total_width = num_vehicles * vehicle_width + (num_vehicles - 1) * vehicle_spacing
    start_x = (screen.get_width() - total_width) // 2  # Center the vehicles horizontally

    vehicle_rects = [
        image.get_rect(topleft=(start_x + i * (vehicle_width + vehicle_spacing), screen.get_height() // 2 - 50)) for
        i, image in
        enumerate(scaled_vehicle_images)]

    selected_vehicle_index = None  # Index of the currently selected vehicle
    hovered_vehicle_index = None  # Index of the currently hovered vehicle

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Draw the vehicle images
        for i, (image, rect) in enumerate(zip(scaled_vehicle_images, vehicle_rects)):
            screen.blit(image, rect)
            if i == selected_vehicle_index:
                # Highlight the selected vehicle
                pg.draw.rect(screen, (255, 255, 0), rect, 3)  # Yellow border
            elif i == hovered_vehicle_index:
                # Highlight the hovered vehicle
                pg.draw.rect(screen, (0, 255, 0), rect, 3)  # Green border

        # Draw the selection prompt text
        font = pg.font.SysFont('Arial', 30)
        text = font.render(f"Select {vehicle_type.capitalize()} Type: Click on the vehicle to choose", True,
                           (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 50))
        return_button = draw_return_button(font, screen, text)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if return_button.collidepoint(mouse_pos):
                    return

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(vehicle_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_vehicle_index = i
                        return VEHICLE_TYPES[vehicle_type][i]  # Return the path of the selected vehicle

            if event.type == pg.MOUSEMOTION:
                mouse_pos = event.pos
                hovered_vehicle_index = None
                for i, rect in enumerate(vehicle_rects):
                    if rect.collidepoint(mouse_pos):
                        hovered_vehicle_index = i

        pg.display.flip()


def draw_return_button(font, screen, text):
    return_button = pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, screen.get_height() // 2 + 140,
                            INGAME_BUTTON_WIDTH, INGAME_BUTTON_HEIGHT)
    pg.draw.rect(screen, RED_COLOR, return_button)
    return_text = font.render('Back', True, WHITE_COLOR)
    screen.blit(return_text, (return_button.x + (INGAME_BUTTON_WIDTH - return_text.get_width()) // 2,
                              return_button.y + (INGAME_BUTTON_HEIGHT - return_text.get_height()) // 2))
    return return_button


def vehicle_selection_screen(screen):
    # Vehicle type image paths
    VEHICLE_TYPES = ["roadster", "supercar", "motorbike", "SUV"]
    VEHICLE_IMAGES = {
        "roadster": "main-game contents/Vehicles/roadster1.png",
        "supercar": "main-game contents/Vehicles/supercar1.png",
        "motorbike": "main-game contents/Vehicles/motorbike2.png",
        "SUV": "main-game contents/Vehicles/SUV1.png"
    }

    # Load and scale vehicle images
    vehicle_images = [pg.image.load(VEHICLE_IMAGES[vehicle_type]).convert_alpha() for vehicle_type in VEHICLE_TYPES]
    scaled_vehicle_images = [pg.transform.scale(image, (50, 100)) for image in vehicle_images]  # Scale vehicle images
    vehicle_rects = [image.get_rect(center=(200 + i * 250, screen.get_height() // 2)) for i, image in
                     enumerate(scaled_vehicle_images)]

    selected_vehicle_type = None  # Currently selected vehicle type
    hovered_vehicle_type = None  # Currently hovered vehicle type

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Draw the vehicle type images
        for i, (image, rect) in enumerate(zip(scaled_vehicle_images, vehicle_rects)):
            screen.blit(image, rect)
            if VEHICLE_TYPES[i] == selected_vehicle_type:
                # Highlight the selected vehicle type
                pg.draw.rect(screen, (255, 255, 0), rect, 3)  # Yellow border
            elif VEHICLE_TYPES[i] == hovered_vehicle_type:
                # Highlight the hovered vehicle type
                pg.draw.rect(screen, (0, 255, 0), rect, 3)  # Green border

        # Draw the selection prompt text
        font = pg.font.SysFont('Arial', 50)
        text = font.render("Select Vehicle Type: Click on the vehicle to choose", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 50))
        return_button = draw_return_button(font, screen, text)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if return_button.collidepoint(mouse_pos):
                    main_menu_display()
                    return

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(vehicle_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_vehicle_type = VEHICLE_TYPES[i]
                        # Proceed to the specific type selection screen
                        selected_vehicle_path = vehicle_type_selection_screen(screen, selected_vehicle_type)
                        if selected_vehicle_path:
                            return selected_vehicle_path  # Return the path of the final selected vehicle

            if event.type == pg.MOUSEMOTION:
                mouse_pos = event.pos
                hovered_vehicle_type = None
                for i, rect in enumerate(vehicle_rects):
                    if rect.collidepoint(mouse_pos):
                        hovered_vehicle_type = VEHICLE_TYPES[i]

        pg.display.flip()


def main_menu_display():
    pg.init()
    pg.display.set_caption('Top-Down Race')
    screen = pg.display.set_mode((1280, 720))
    bgm_manager = BackgroundMusic(BGM_LOBBY)
    bgm_manager.play_random()
    main_menu(screen)


def main():
    # Initialize the game
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Top-Down Race')
    font = pg.font.Font(None, 36)
    clock = pg.time.Clock()
    # Display the vehicle selection screen and get the selected vehicle
    selected_vehicle_path = vehicle_selection_screen(screen)
    if selected_vehicle_path is None:
        pg.quit()
        return
    running = True
    dt = 0
    paused = False
    power_ups = []
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
    player = Player(selected_vehicle_path, (screen.get_width() / 2, screen.get_height() / 2))
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
    left_border = pg.Rect(0, 0, 353, SCREEN_HEIGHT)
    right_border = pg.Rect(935, 0, 353, SCREEN_HEIGHT)

    def display_timers(screen, player, score, font):
        current_time = pg.time.get_ticks()
        invincibility_time_left = max(0, player.invincible_until - current_time)
        double_points_time_left = max(0, score.double_points_until - current_time)

        invincibility_text = font.render(f'Invincibility: {invincibility_time_left // 1000}', True, (255, 255, 255))
        double_points_text = font.render(f'Double Points: {double_points_time_left // 1000}', True, (255, 255, 255))

        screen.blit(invincibility_text, (10, 120))
        screen.blit(double_points_text, (10, 150))

    def spawn_power_up():
        power_up_type = random.choice(list(POWER_UPS.keys()))
        power_up_image = POWER_UPS[power_up_type]
        power_up = PowerUp(power_up_type, power_up_image, (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50))
        power_ups.append(power_up)

    def draw_pause_icon():
        pause_icon = pg.image.load('main-game contents/Icons/Paused.png').convert_alpha()
        pause_icon_resized = pg.transform.scale(pause_icon, ICON_SIZE)
        icon_x = screen.get_width() - 120
        icon_y = 20
        pause_icon_rect = pause_icon_resized.get_rect(topleft=(icon_x, icon_y))
        font = pg.font.Font(None, 24)
        esc_text = font.render('ESC', True, WHITE_COLOR)
        text_margin = 10
        esc_text_rect = esc_text.get_rect(midtop=(pause_icon_rect.centerx, pause_icon_rect.bottom + text_margin))
        screen.blit(pause_icon_resized, pause_icon_rect)
        screen.blit(esc_text, esc_text_rect)

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
        border = pg.Surface((353, SCREEN_HEIGHT), pg.SRCALPHA).convert()
        screen.blit(border, (0, 0))
        screen.blit(border, (935, 0))

    def pause_screen():
        # Create a semi-transparent surface for darkening effect
        dark_overlay = pg.Surface(screen.get_size())
        dark_overlay.set_alpha(180)  # Adjust alpha value for better visibility of overlay

        # Display "Paused" message when the game is paused
        draw_pause_icon()
        screen.blit(dark_overlay, (0, 0))
        font = pg.font.Font(None, 74)
        text = font.render("Paused", True, WHITE_COLOR)
        text_rect = text.get_rect(midtop=(screen.get_width() / 2, 50))
        screen.blit(text, text_rect)

        # Button dimensions and positions
        end_race_button = pg.Rect(screen.get_width() // 2 - INGAME_BUTTON_WIDTH // 2, screen.get_height() // 2 + 120,
                                  INGAME_BUTTON_WIDTH, INGAME_BUTTON_HEIGHT)
        end_race_color = RED_COLOR
        pg.draw.rect(screen, end_race_color, end_race_button)

        # Render button text
        normal_font = pg.font.Font(None, 30)
        end_race_text = normal_font.render('End Race', True, WHITE_COLOR)
        screen.blit(end_race_text, (end_race_button.x + (INGAME_BUTTON_WIDTH - end_race_text.get_width()) // 2,
                                    end_race_button.y + (INGAME_BUTTON_HEIGHT - end_race_text.get_height()) // 2))

        font = pg.font.SysFont('Arial', 50)
        score_text = font.render(f'Current Score: {score.score}', True, WHITE_COLOR)
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 200))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if end_race_button.collidepoint(mouse_pos):
                    movement_sounds.stop_all()
                    bgm_manager.stop()
                    display_race_result(screen, score.score)
                    return

        pg.display.flip()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = not paused
                if not paused:
                    if event.key == pg.K_a:
                        movement_sounds.play("a")
                    elif event.key == pg.K_s:
                        movement_sounds.play("s")
                    elif event.key == pg.K_d:
                        movement_sounds.play("d")
                if event.key == pg.K_UP:
                    bgm_manager.set_volume(0.1)
                    movement_sounds.set_volume(0.1)
                elif event.key == pg.K_DOWN:
                    bgm_manager.set_volume(-0.1)
                    movement_sounds.set_volume(-0.1)
            elif event.type == pg.KEYUP and not paused:
                if event.key == pg.K_a:
                    movement_sounds.stop("a")
                if event.key == pg.K_s:
                    movement_sounds.stop("s")
                if event.key == pg.K_d:
                    movement_sounds.stop("d")

        if paused:
            pause_screen()
        else:
            draw_border()
            draw_background()
            screen.blit(mud_puddle_image, mud_puddle_rect)
            screen.blit(speed_platform_image, speed_platform_rect)
            for obstacle_image, obstacle_rect in obstacles:
                obstacle_rect.y += scroll_speed
                if obstacle_rect.top > screen.get_height():
                    obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
                screen.blit(obstacle_image, obstacle_rect)
                if not player.is_invincible():
                    if obstacle_rect.colliderect(player.get_rect()):
                        player.reduce_health()
                        if player.health <= 0:
                            running = False
                        obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
            player.draw(screen)
            draw_trees()
            score.draw(screen)
            current_time = pg.time.get_ticks()
            score.update(current_time, increment=1, interval=500)
            draw_pause_icon()
            display_timers(screen, player, score, font)

            # Manage power-ups
            for power_up in power_ups:
                power_up.rect.y += scroll_speed
                if power_up.rect.top > screen.get_height():
                    power_ups.remove(power_up)
                else:
                    power_up.draw(screen)
                    if power_up.get_rect().colliderect(player.get_rect()):
                        power_up.apply_effect(player, score)
                        power_ups.remove(power_up)

            # Spawn power-ups periodically
            if random.random() < 0.01:  # Adjust probability as needed
                spawn_power_up()

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

            if keys[pg.K_s]:
                player.pos.y += 200 * dt * speed_modifier
            if keys[pg.K_a]:
                player.pos.x -= 300 * dt * speed_modifier
            if keys[pg.K_d]:
                player.pos.x += 300 * dt * speed_modifier

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

            if (player.pos.x < -100 or player.pos.x > SCREEN_WIDTH or player.pos.y < 0 or player.pos.y >
                    (SCREEN_HEIGHT + 150) - PLAYER_SIZE_Y):
                bgm_manager.stop()
                movement_sounds.stop_all()
                display_race_result(screen, score.score)
                return

            pg.display.flip()
            dt = clock.tick(60) / 1000

    pg.display.flip()
    movement_sounds.stop_all()
    bgm_manager.stop()
    display_race_result(screen, score.score)
    pg.quit()


main_menu_display()
