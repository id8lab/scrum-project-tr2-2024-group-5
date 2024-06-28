import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

class Car:
    def __init__(self, name, music_file, channel):
        self.name = name
        self.music_file = music_file
        self.channel = channel
        self.sound = pygame.mixer.Sound(music_file)

    def play_music(self):
        self.sound.play(-1)  # infinite loop play

    def stop_music(self):
        self.sound.stop()

    def set_volume(self, volume):
        self.sound.set_volume(volume)

 # Create 4 different audio channels
channels = [pygame.mixer.Channel(i) for i in range(4)]

# Create an instance of each car and assign it to a different audio channel
car1 = Car("Car A", "main-game contents/Vehicle_Audio/motorbike.wav", channels[0])
car2 = Car("Car B", "main-game contents/Vehicle_Audio/roadster.wav", channels[1])
car3 = Car("Car C", "main-game contents/Vehicle_Audio/supercar.wav", channels[2])
car4 = Car("Car D", "main-game contents/Vehicle_Audio/suv.wav", channels[3])

cars = [car1, car2, car3, car4]

# play all sound
for car in cars:
    car.play_music()

# voice
for car in cars:
    car.set_volume(0.5)

# major
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                car1.play_music()
            elif event.key == pygame.K_2:
                car2.play_music()
            elif event.key == pygame.K_3:
                car3.play_music()
            elif event.key == pygame.K_4:
                car4.play_music()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                car1.stop_music()
            elif event.key == pygame.K_2:
                car2.stop_music()
            elif event.key == pygame.K_3:
                car3.stop_music()
            elif event.key == pygame.K_4:
                car4.stop_music()

for car in cars:
    car.stop_music()

pygame.quit()
