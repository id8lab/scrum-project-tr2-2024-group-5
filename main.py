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
        self.image = pg.transform.scale(self.image, (150, 150))
        self.pos = pg.Vector2(start_pos)
        self.health = 3
        self.max_health = 3  # Maximum health
        self.heart_image = pg.transform.scale(pg.image.load('main-game contents/Obstacles/heart.png'), (50, 50))
        # Load and scale the heart image

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def draw_health(self, screen, x=10, y=70):
        for i in range(self.max_health):
            if i < self.health:
                screen.blit(self.heart_image, (x + i * 55, y))
            else:
                empty_heart_image = pg.Surface((50, 50), pg.SRCALPHA)  # Create an empty surface for the empty heart
                pg.draw.rect(empty_heart_image, (255, 255, 255, 50), empty_heart_image.get_rect(), border_radius=5)
                # Draw a transparent rectangle
                screen.blit(empty_heart_image, (x + i * 55, y))

    def get_rect(self):
        return self.image.get_rect(topleft=self.pos)

    def reduce_health(self):
        self.health -= 1
        return self.health


def main():
    pg.init()
    bgm = ["main-game contents/Audio/bgm1.mp3", "main-game contents/Audio/bgm2.mp3",
           "main-game contents/Audio/bgm3.mp3",
           "main-game contents/Audio/bgm4.mp3"]
    bgm_play_track = random.choice(bgm)
    vehicle_choice = random.choice(VEHICLES)
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption('Top-Down Race')
    clock = pg.time.Clock()
    running = True
    dt = 0
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
    player = Player(vehicle_choice, (screen.get_width() / 2, screen.get_height() / 2))
    bgm_play = pg.mixer.Sound(bgm_play_track).play(-1)
    bgm_play.set_volume(0.6)
    obstacle_images = [pg.transform.scale(pg.image.load(obstacle), (50, 50)) for obstacle in OBSTACLES]
    obstacles = []
    obstacle_spawn_time = pg.time.get_ticks()
    mud_puddle_image = pg.image.load('main-game contents/Obstacles/Mud.png').convert_alpha()
    mud_puddle_image = pg.transform.scale(mud_puddle_image, (100, 100))
    mud_puddle_rect = mud_puddle_image.get_rect(midtop=(screen.get_width() // 2, -50))
    mud_puddle_spawn_time = pg.time.get_ticks()
    speed_reduction_factor = 0.2

    def draw_background():
        screen.blit(resized_background, (0, background_road_pos_y1))
        screen.blit(resized_background, (0, background_road_pos_y2))

    def draw_trees():
        screen.blit(tree_props_1, (-500, tree_props_pos_y1))
        screen.blit(tree_props_1, (700, tree_props_pos_y1))
        screen.blit(tree_props_1, (-500, tree_props_pos_y2))
        screen.blit(tree_props_1, (700, tree_props_pos_y2))

    def spawn_obstacle():
        obstacle_image = random.choice(obstacle_images)
        obstacle_rect = obstacle_image.get_rect(midtop=(random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50))
        obstacles.append((obstacle_image, obstacle_rect))

    def spawn_mud_puddle():
        mud_puddle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        draw_background()
        screen.blit(mud_puddle_image, mud_puddle_rect)
        player.draw(screen)
        draw_trees()
        score.draw(screen)
        player.draw_health(screen)
        current_time = pg.time.get_ticks()
        score.update(current_time, increment=1, interval=500)

        if (current_time - obstacle_spawn_time) >= 3000:
            spawn_obstacle()
            obstacle_spawn_time = current_time

        for obstacle_image, obstacle_rect in obstacles:
            obstacle_rect.y += 5
            if obstacle_rect.top > screen.get_height():
                obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
            screen.blit(obstacle_image, obstacle_rect)
            if obstacle_rect.colliderect(player.get_rect()):
                player.reduce_health()
                print(f"Collision detected! Health: {player.health}")
                if player.health <= 0:
                    running = False
                obstacle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)

        if (current_time - mud_puddle_spawn_time) >= 5000:
            spawn_mud_puddle()
            mud_puddle_spawn_time = current_time

        mud_puddle_rect.y += 5
        if mud_puddle_rect.top > screen.get_height():
            mud_puddle_rect.midtop = (random.randint(obstacle_x_pos_1, obstacle_x_pos_2), -50)
        player_slowed = mud_puddle_rect.colliderect(player.get_rect())

        scroll_speed = 18
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
            player.image = pg.transform.scale(player.image, (150, 150))

        pg.display.flip()
        dt = clock.tick(60) / 1000
    pg.quit()


main()
