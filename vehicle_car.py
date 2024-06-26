import pygame
import time


class Car:
    def __init__(self, name, music_file):
        self.name = name
        self.music_file = music_file

    def play_music(self):
        print(f"{self.name} is playing: {self.music_file}")
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)


# Define four cars and their in-car music file paths
car1 = Car("motorbke", "main-game contents/Vehicle_Audio/motorbike.mp3")
car2 = Car("supercar", "main-game contents/Vehicle_Audio/supercar.mp3")
car3 = Car("roadster", "main-game contents/Vehicle_Audio/roadster.mp3")
car4 = Car("SUV", "main-game contents/Vehicle_Audio/SUV.mp3")

# Play each car's music
cars = [car1, car2, car3, car4]
for car in cars:
    car.play_music()
