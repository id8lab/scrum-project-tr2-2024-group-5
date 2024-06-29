import pygame
import time


pygame.init()


start_sound = pygame.mixer.Sound('main-game contents/Voices/motor start.wav')
brake_sound = pygame.mixer.Sound('main-game contents/Voices/motor stop.wav')


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Car Sound Effects')

running = True
sound_played = {'start': False, 'brake': False}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not sound_played['start']:
                pygame.mixer.stop()
                start_sound.play()
                sound_played['start'] = True
            elif event.key == pygame.K_s and not sound_played['brake']:
                pygame.mixer.stop()
                brake_sound.play()
                sound_played['brake'] = True

    screen.fill((0, 0, 0))

    pygame.display.flip()

    time.sleep(0.1)


pygame.quit()
