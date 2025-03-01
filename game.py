import pygame
import random
from pygame.transform import scale


count = count_kill = 0


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.images = []
        self.index = 0

        for i in range(8):
            image = scale(pygame.image.load(f"explosion/tile00{i}.png"), (40, 40))
            self.images.append(image)

    def draw(self, screen):
        if self.index < 8:
            screen.blit(self.images[self.index], (self.rect.x, self.rect.y))
            self.index += 1
        else:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = scale(pygame.image.load("img/asteroid.png"), (50, 50))
        self.rect = pygame.Rect(x, y, 50, 50)
        self.yvel = 5

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, puli):
        global count_kill
        self.rect.y += self.yvel

        if self.rect.y > 900:
            self.kill()

        # для каждого астероида
        for pul in puli:
            # если область, занимаемая астероидом пересекает область корабля
            if self.rect.colliderect(pul.rect):
                # уменьшаем жизнь
                self.kill()
                count_kill += 1


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = scale(pygame.image.load("img/puli.png"), (60, 50))
        self.rect = pygame.Rect(x, y, 10, 10)
        self.yvel = 10

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y -= self.yvel


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, 50, 75)
        self.image = scale(pygame.image.load("img/ship.png"), (50, 100))
        self.xvel = 0
        # добавим кораблю здоровье
        self.life = 100
        self.explosions = pygame.sprite.Group()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        for explosion in self.explosions:
            explosion.draw(screen)

    # добавим группу с астероидами в обновление координат корабля
    def update(self, left, right, asteroids):
        if left:
            self.xvel -= 3
        if right:
            self.xvel += 3
        if not (left or right):
            self.xvel = 0
        
        if self.rect.x >= 750:
            self.rect.x -= 3
        elif self.rect.x <= 0:
            self.rect.x += 3
        else:
            self.rect.x += self.xvel

        # для каждого астероида
        for asteroid in asteroids:
            # если область, занимаемая астероидом пересекает область корабля
            if self.rect.colliderect(asteroid.rect):
                # уменьшаем жизнь
                self.life -= 1
                rx = random.randint(-5, 40)
                ry = random.randint(-5, 40)
                explosion = Explosion(self.rect.x + rx, self.rect.y + ry)
                self.explosions.add(explosion)


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Asteroids")

sky = scale(pygame.image.load("img/sky.jpg"), (800, 600))

ship = Spaceship(400, 400)

left = False
right = False

asteroids = pygame.sprite.Group()
puli = pygame.sprite.Group()

# загрузим системный шрифт
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()

state = "menu"

while True:
    if state == "menu":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit("QUIT")

            if e.type == pygame.MOUSEBUTTONUP:
                if pygame.Rect(200, 350, 400, 100).collidepoint(e.pos):
                    raise SystemExit
                if pygame.Rect(200, 150, 400, 100).collidepoint(e.pos):
                    ship = Spaceship(400, 400)
                    state = "game"
        
        bg = pygame.image.load('img/menu.jpg').convert()
        screen.blit(bg, (50, 0))
        pygame.draw.rect(screen, "red", pygame.Rect(200, 150, 400, 100))
        pygame.draw.rect(screen, "blue", pygame.Rect(200, 350, 400, 100))

        screen.blit(font.render(f'Начать', False, (255, 255, 255)), (360, 180))
        screen.blit(font.render(f'Закрыть', False, (255, 255, 255)), (360, 380))

    if state == 'menu2':
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit("QUIT")

            if e.type == pygame.MOUSEBUTTONUP:
                if pygame.Rect(200, 300, 400, 100).collidepoint(e.pos):
                    raise SystemExit
                if pygame.Rect(200, 100, 400, 100).collidepoint(e.pos):
                    ship = Spaceship(400, 400)
                    state = "game"
                    count_kill = 0
        
        bg = pygame.image.load('img/menu.jpg').convert()
        screen.blit(bg, (50, 0))
        pygame.draw.rect(screen, "red", pygame.Rect(200, 100, 400, 100))
        pygame.draw.rect(screen, "blue", pygame.Rect(200, 270, 400, 100))
        pygame.draw.rect(screen, "green", pygame.Rect(200, 420, 400, 100))

        screen.blit(font.render(f'Начать', False, (255, 255, 255)), (360, 135))
        screen.blit(font.render(f'Закрыть', False, (255, 255, 255)), (360, 300))
        screen.blit(font.render(f'Вы уничтожили: {count_kill} угроз', False, (255, 255, 255)), (270, 450))

    if state == "game":
        if random.randint(1, 1000) > 900:
            asteroid_x = random.randint(-100, 700)
            asteroid_y = -100
            asteroid = Asteroid(asteroid_x, asteroid_y)
            asteroids.add(asteroid)
        if count % 10 == 0:
            pul = Bullets(ship.rect.x, 425)
            puli.add(pul)
        count += 1

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right = True

            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right = False
            if e.type == pygame.QUIT:
                raise SystemExit("QUIT")

        screen.blit(sky, (0, 0))

        # добавим группу астероидов в параметры
        ship.update(left, right, asteroids)
        ship.draw(screen)

        for pul in puli:
            pul.update()
            pul.draw(screen)

        for asteroid in asteroids:
            asteroid.update(puli)
            asteroid.draw(screen)
        

        # выведем жизнь на экран белым цветом
        life = font.render(f'HP: {ship.life}', False, (255, 255, 255))
        screen.blit(life, (20, 20))

        if ship.life <= 0:
            screen.fill((0, 0, 0))
            state = "menu2"

    pygame.display.update()
    clock.tick(60)