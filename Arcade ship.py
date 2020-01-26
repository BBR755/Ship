import pygame
import os
import sys
import random

pygame.init()
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
screen.fill((50, 80, 255))
clock = pygame.time.Clock()
list_coords = []
FPS = 60
run_x = False
run_y = False
x_pos = width//2
y_pos = height//2
v_x = 0
v_y = 0
a = -0.001307932583525568
b = 1.3393229655301817
c = 41.133320824273454
speed = 200
reload_1_green = 0
reload_2_red = 0
choos = 0
repeat = -1
colding = 5
coords_x = 0
coords_y = 0
change_x = 0
change_y = 0
x_enemy = 0
y_enemy = 0
#xx = 0
#yy = 0
temp = 0
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

    fon = pygame.transform.scale(load_image('Prerol.jpg'), (width, height))
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
    image = load_image("ship.png", -1)


    def __init__(self, player_group):
        super().__init__(player_group)
        self.image = Ship.image
        self.rect = self.image.get_rect()
        self.rect.x = width//2
        self.rect.y = height//2

    def update(self, x_1, y_1):
        self.rect = self.image.get_rect().move(x_1, y_1)


class Weapon(pygame.sprite.Sprite):
    image = load_image("lazer.png", -1)
    image = pygame.transform.rotate(image, 90)


    def __init__(self, glavniy_weapon_group):
        super().__init__(glavniy_weapon_group)
        self.image = Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = x_pos + 30
        self.rect.y = y_pos
        #xx = self.rect.x
        #yy = self.rect.y

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


class Enemy_left(pygame.sprite.Sprite):
    image = load_image("standart_unit_2.png", -1)
    image = pygame.transform.rotate(image, 180)

    def __init__(self, enemy_left_group):
        super().__init__(enemy_left_group)
        self.image = Enemy_left.image
        self.rect = self.image.get_rect()
        self.rect.x = coords_x
        self.rect.y = coords_y
        self.hp = 1

    def update(self):
        y = self.rect[1]
        global choos, x_enemy, y_enemy

        d = b**2 - 4 * a * (c - y - 1)
        x1 = (-b - d**0.5)/2/a
        x2 = (-b + d ** 0.5) / 2 / a
        if choos != -1:
            x = min(x2, x1)
            self.rect = self.rect.move(x - self.rect[0], 1)
        if self.rect[0] > 400:
            choos = -1


class Enemy_Weapon(pygame.sprite.Sprite):
    image = load_image("Enemy_lazer_type3.png", -1)
    image = pygame.transform.rotate(image, 90)


    def __init__(self, enemy_left_group):
        print(0)
        super().__init__(enemy_left_group)
        self.image = Enemy_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = x_enemy + 30
        self.rect.y = y_enemy + 30

    def update(self):
        #u = 1024 // 100
        #x_s = x_pos - x_enemy - 30
        #y_s = y_pos - y_enemy - 30
        #s = (x_s ** 2 + y_s ** 2) ** 0.5
        #time = s / u
        #u_x = x_s / time
        #y_u = y_s / time
        self.rect.move_ip(u_x, y_u)
        #if pygame.sprite.spritecollideany(self, horizontal_borders):
         #   pygame.sprite.spritecollide(self, enemy_left_group, True)



vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
glavniy_weapon_group = pygame.sprite.Group()
enemy_weapon_group = pygame.sprite.Group()
back_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_left_group = pygame.sprite.Group()
ship = Ship(player_group)
back = Background(back_group)


Border(-300, -300, width + 300, -300)
Border(-300, height + 300, width + 300, height + 300)
Border(-300, -300, -300, height + 300)
Border(width + 300, -300, width + 300, height + 300)
start_screen()


running = True
while running:

    if enemy_left_group.sprites() == []:
        choos = random.randint(0, 2)
        if choos != repeat:
            repeat = choos
            if choos == 1:
                for i in range(5):
                    coords_x = -90
                    coords_y = -90 + -90 * temp//2
                    enemy = Enemy_left(enemy_left_group)
                    temp += 1

    if reload_1_green % 25 != 0:
        reload_1_green += 1
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

    if key[pygame.K_SPACE] and reload_1_green % 25 == 0 and not pew:
        green = Weapon(glavniy_weapon_group)
        reload_1_green = 1
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
    if enemy_left_group.sprites() != [] and choos == 1:
        enemy_left_group.update()
    if enemy_left_group.sprites() != [] and reload_2_red % 25 == 0:
        for sprit in range(len(enemy_left_group.sprites())):
            x_enemy = enemy_left_group.sprites()[sprit].rect[0]
            y_enemy = enemy_left_group.sprites()[sprit].rect[1]
            red = Enemy_Weapon(enemy_weapon_group)
            u = 1024 // 100
            x_s = x_pos - x_enemy - 30
            y_s = y_pos - y_enemy - 30
            s = (x_s ** 2 + y_s ** 2) ** 0.5
            time = s / u
            u_x = x_s / time
            y_u = y_s / time
            enemy_weapon_group.update()
        reload_2_red = 1
    reload_2_red += 1
    player_group.update(x_pos, y_pos)
    glavniy_weapon_group.update()
    enemy_weapon_group.draw(screen)
    enemy_left_group.draw(screen)
    vertical_borders.draw(screen)
    horizontal_borders.draw(screen)
    player_group.draw(screen)
    glavniy_weapon_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
    #clock.tick(1000)

terminate()

