import random

import pygame

WIDTH = 1280
HEIGHT = 720

FPS = 60
frame_per_sec = pygame.time.Clock()

BLACK = pygame.Color(0, 0, 0)         # Black
WHITE = pygame.Color(255, 255, 255)   # White
GREY = pygame.Color(128, 128, 128)   # Grey
RED = pygame.Color(255, 0, 0)       # Red

N_CARS = 50
SPEED_LIMIT = 5

class Deer:
    def __init__(self) -> None:
        image = pygame.image.load("deer.jpeg")
        self.size = 50
        self.x = WIDTH // 1.5
        self.y = HEIGHT // 1.5 + 20
        self.color = RED
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))




class Car:
    def __init__(self, x=-50, y=HEIGHT-2, length=50, height=20, speed=SPEED_LIMIT, reaction_time=.3, color=GREY, autonomous=True) -> None:
        self.x = x
        self.real_x = x
        self.y = y
        self.length = length
        self.height = height
        self.speed = speed
        self.reaction_time = reaction_time
        self.color = color
        self.direction = 1
        self.autonomous = autonomous

        self.y -= self.height

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, BLACK, (self.x-1, self.y-1, self.length+2, self.height+2), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, self.height), 0)

    def drive(self) -> None:
        self.x += max(0, self.speed) * self.direction
        self.real_x += max(0, self.speed)

        # if self.x > WIDTH + self.length:
        #     self.direction *= -1
        #     self.y -= self.height * 2
        
        if self.x > WIDTH + self.length:
            self.x = - self.length
            self.y -= self.height * 2

        # if self.x < -self.length:
        #     self.direction *= -1
        #     self.y -= self.height * 2

        if self.y < 0:
            self.y = HEIGHT - self.height - 2

    def check_distance(self, cars) -> None:
        # print(cars)
        if self != cars[0]:
            for car in cars:
                    # same_lane = abs(car.y - self.y) < self.height * 2
                    same_lane = True 
                    delta_dist = car.real_x - car.length - self.real_x
                    if self.autonomous == True:
                        if same_lane and car.real_x > self.real_x and delta_dist < car.length + self.reaction_time:
                                if self.speed > 0:
                                    if delta_dist <= car.length // 10:
                                        self.speed = 0
                                    self.speed -= .5 + (self.reaction_time / (delta_dist * .1))
                        elif same_lane and delta_dist > car.length:
                                if self.speed < SPEED_LIMIT:
                                    self.speed += SPEED_LIMIT / 600
                        else:
                            pass

    def check_obstacle(self, obstacle) -> None:
        if obstacle.visible:
            if obstacle.x - self.x < self.length * 3 and abs(self.y - (obstacle.y + obstacle.size)) < self.height:
                self.speed -= self.speed / 3
                obstacle.visible = False

def start_screen(screen, font) -> None:
    text = font.render("PRESS ANY KEY TO START SIMULATION", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, textRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                return True
        pygame.display.update()




def draw_speed(screen, font, car, color) -> None:
    text = font.render(f"Speed: {round(car.speed, 2)}", True, color)
    textRect = text.get_rect()
    textRect.center = (WIDTH - textRect.width, textRect.height)
    screen.blit(text, textRect)


def start_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font("freesansbold.ttf", 32)
    pygame.display.set_caption("Traffic Simulation 0.1")
    running = True

    return screen, running, font


def main():
    pygame.init()

    screen, running, font = start_game()
    
    # car = Car()
    cars = [Car(color=RED, autonomous=False)]
    deer = Deer()
    # for _ in range(N_CARS):
    #     cars.append(Car())

    running = start_screen(screen, font)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    # cars[0].speed -= SPEED_LIMIT / 10
                    cars[0].speed -= cars[0].speed / 3
                # if event.key == pygame.K_UP:
                #     cars[0].speed += SPEED_LIMIT / 10
        
        if cars[0].speed < SPEED_LIMIT:
            cars[0].speed += SPEED_LIMIT / 600

        # Clear the screen
        screen.fill(WHITE)

        # Draw speed
        draw_speed(screen, font, cars[0], cars[0].color)

        # Draw cars
        for car in cars:
            car.draw(screen)
            car.drive()
            car.check_distance(cars)

        deer.draw(screen)

        cars[0].check_obstacle(deer)

        if cars[-1].x >= cars[-1].length * 2 and len(cars) < N_CARS:
            # cars.append(Car(color=(random.randint(40,100), random.randint(40,100), random.randint(40,100))))
            cars.append(Car(color=GREY))
        
        # Update display and tick clock
        pygame.display.update()    
        frame_per_sec.tick(FPS)

if __name__ == '__main__':
    main()
