import pygame
import os
import sys

pygame.init()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
screen.fill((50, 80, 255))
clock = pygame.time.Clock()
FPS = 60
run_x = False
run_y = False
x_pos = width//2
y_pos = height//2
v_x = 0
v_y = 0
speed = 200
total = 0
choos = 0
colding = 5
coords_x = 0
coords_y = 0
xx = 0
yy = 0
left =True
right = True
up =True
down =True
pew = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Star Ship", "",
                  "Правила игры:",
                  "У игрока под контролем есть космический корабль, который управляется стрелками мыши",
                  "Цель игры:"
                  "Набраться как можно больше очков."
                  "Нажмите 'F', чтобы продолжить."]

    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and key[pygame.K_f]:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

class Background(pygame.sprite.Sprite):
    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))

    def __init__(self, group):
        super().__init__(group)
        self.image = Background.fon
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Ship(pygame.sprite.Sprite):
    image = load_image("ship_3.png", -1)


    def __init__(self, player_group):
        super().__init__(player_group)
        self.image = Ship.image
        self.rect = self.image.get_rect()
        self.rect.x = width//2
        self.rect.y = height//2

    def update(self, x_1, y_1):
        self.rect = self.image.get_rect().move(x_1, y_1)


class Weapon(pygame.sprite.Sprite):
    image = load_image("ship.png", -1)


    def __init__(self, glavniy_weapon_group):
        super().__init__(glavniy_weapon_group)
        self.image = Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = x_pos - 45
        self.rect.y = y_pos
        xx = self.rect.x
        yy = self.rect.y

    def update(self):
        self.rect = self.rect.move(0, -10)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            pygame.sprite.spritecollide(self, glavniy_weapon_group, True)

        if pygame.sprite.spritecollideany(self, vertical_borders):
            pygame.sprite.spritecollide(self, glavniy_weapon_group, True)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Enemy(pygame.sprite.Sprite):
    image = load_image("ship.png", -1)

    def __init__(self, enemy_group):
        super().__init__(enemy_group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = coords_x
        self.rect.y = coords_y

vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
glavniy_weapon_group = pygame.sprite.Group()
back_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ship = Ship(player_group)
back = Background(back_group)


Border(-300, -300, width + 300, -300)
Border(-300, height + 300, width + 300, height + 300)
Border(-300, -300, -300, height + 300)
Border(width + 300, -300, width + 300, height + 300)
start_screen()

running = True
while running:

    if enemy_group.sprites() == []:
        for i in range(15):
            enemy = Enemy(enemy_group)

    if total % 25 != 0:
        total += 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and colding == 15:
            green = Weapon(glavniy_weapon_group)
            colding = 0
            pew = True
        if event.type == pygame.QUIT:
            running = False



    key = pygame.key.get_pressed()
    back_group.draw(screen)
    if x_pos < 0:
        v_x = 0
        left = False

    else:
        left = True

    if x_pos == width - 90:
        v_x = 0
        right = False

    else:
        right = True

    if y_pos < 0:
        v_y = 0
        up = False

    else:
        up = True

    if y_pos == height - 90:
        v_y = 0
        down = False

    else:
        down = True

    if key[pygame.K_SPACE] and total % 25 == 0 and not pew:
        green = Weapon(glavniy_weapon_group)
        total += 1
    if not key[pygame.K_LEFT]:
        if v_x == -speed:
            v_x = 0
    if not key[pygame.K_RIGHT]:
        if v_x == speed:
            v_x = 0
    if not key[pygame.K_UP]:
        if v_y == -speed:
            v_y = 0
    if not key[pygame.K_DOWN]:
        if v_y == speed:
            v_y = 0

    if key[pygame.K_LEFT] and left:
        if speed/FPS - x_pos > 0:
            v_x = -(speed/FPS - x_pos) * FPS
        else:
            v_x = -speed

    if key[pygame.K_RIGHT] and right:
        if x_pos + speed/FPS > width - 90:
            v_x = (width - 90 - x_pos) * FPS
        else:
            v_x = speed

    if key[pygame.K_DOWN] and down:
        if y_pos + speed/FPS > height - 90:
            v_y = (height - 90 - y_pos) * FPS
        else:
            v_y = speed

    if key[pygame.K_UP] and up:
        if speed/FPS - y_pos > 0:
            v_y = -(speed/FPS - y_pos) * FPS
        else:
            v_y = -speed

    pew = False
    if colding != 15:
        colding += 1
    x_pos += v_x / FPS
    y_pos += v_y / FPS
    player_group.update(x_pos, y_pos)
    glavniy_weapon_group.update()
    vertical_borders.draw(screen)
    horizontal_borders.draw(screen)
    player_group.draw(screen)
    glavniy_weapon_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
    #clock.tick(1000)

terminate()