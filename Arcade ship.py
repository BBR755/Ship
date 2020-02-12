import pygame
import os
import sys
import random

pygame.init()
# координаты направления - т.е. на сколько измениться координата по оси x и y
size = width, height = 1024, 768
screen = pygame.display.set_mode(size)
screen.fill((50, 80, 255))
clock = pygame.time.Clock()

# Константы (a ,b , c - константы квадратноо уравнения), u - скорость за которую должен пройти лазер расстояние в
# 1024 пикселя за 100 тиков
a = -0.001307932583525568
b = 1.3393229655301817
c = 41.133320824273454
u = 1024 // 100
FPS = 60
speed = 200

# Список координат движения выстрелов противника
list_coords_x = []
list_coords_y = []
# Таймер жизни спрайты - взрыв
list_time_of_delete = []
#  Переменные отвечающие координаты корабля игрока
x_pos = width//2
y_pos = height//2
# Переменные отвечающие за перемещение корабля игрока
v_x = 0
v_y = 0
# Триггер смерти игрока
trigger_death = 0
# Кол-во подбитых кораблей врага
death = 0
# Номер спрайта - вражеского выстрела в группе спрайтов
number_of_enemy_sprite_coords = -1
# Перезарядка вражеских выстрелов
reload_2_red = 0
# Координаты союзного лазера
x_laser_delete = 0
y_laser_delete = 0
# Переменные отвечающии за генерацию врагов
choos = 0
repeat = -1
# Перезарядка для выстрелов игрока при разовом нажатии на Space
colding = 5
# Перезарядка для выстрелов игрока при зажатом Space
reload_1_blue = 0
#
coords_x = 0
coords_y = 0
# Координаты спрайтов - вражеских выстрелов
x_enemy = 0
y_enemy = 0
# Дополнительное ускорение, увеличивающаяся со временем
addition_speed = 0
adition_move_speed = 0
# Триггеры ограничиваюшии движение корабля игрока
left = True
right = True
up = True
down = True
# Контролирует, чтобы не было двойного выстрела
pew = False

# Убирает фон у спрайта


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
# Осуществляет безопасное выключение программы(чтобы не крашилась)


def terminate():
    pygame.quit()
    sys.exit()
# Выводит картинку с текстои о смерти и счетом


def restart():
    global ship, back, death
    intro_text = ['Ваш корабль уничтожен',
                  'Уничтожено противников:   ' + str(death),
                  'Для новой игры нажмите "Space"']
    fon = pygame.transform.scale(load_image('restart.jpg'), (width, height))
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

        for event_restart in pygame.event.get():
            key_restart = pygame.key.get_pressed()
            if event_restart.type == pygame.QUIT:
                terminate()
            elif event_restart.type == pygame.KEYDOWN and key_restart[pygame.K_SPACE]:
                death = 0
                # Начинаем игру заного
                return
        pygame.display.flip()
        clock.tick(FPS)
# Стартовый экран, объясняющий правила игры


def start_screen():
    intro_text = ["Star Ship", "",
                  "Правила игры:",
                  "У игрока под контролем есть космический корабль, который управляется стрелками на клавиатуре",
                  "Для стрельбы нажмите 'Space'",
                  "Если Вы долго будете убивать противников, то они начнут использовать запутанную траекторию",
                  "полета снарядов. Бойтесь, их тактики коварны",
                  "Цель игры:",
                  " Набраться как можно больше очков",
                  " Нажмите 'F', чтобы начать"]

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
        for event_start in pygame.event.get():
            key_start = pygame.key.get_pressed()
            if event_start.type == pygame.QUIT:
                terminate()
            elif event_start.type == pygame.KEYDOWN and key_start[pygame.K_f]:
                # Начинаем игру
                return
        pygame.display.flip()
        clock.tick(FPS)
# Создает фон


class Background(pygame.sprite.Sprite):
    fon = pygame.transform.scale(load_image('space.jpg'), (width, height))

    def __init__(self, group):
        super().__init__(group)
        self.image = Background.fon
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
# Создает корабль игрока


class Ship(pygame.sprite.Sprite):
    image = load_image("ship.png", -1)

    def __init__(self, player_group):
        super().__init__(player_group)
        self.image = Ship.image
        self.rect = self.image.get_rect()
        self.rect.x = width//2
        self.rect.y = height//2

    def update(self, x_1, y_1):
        # Перемещает корабль по экрану на значения x_1 и y_1
        self.rect = self.image.get_rect().move(x_1, y_1)
# Создает спрайты выстрелов главного корабля


class Weapon(pygame.sprite.Sprite):
    image = load_image("laser.png", -1)
    image = pygame.transform.rotate(image, 90)

    def __init__(self, glavniy_weapon_group):
        super().__init__(glavniy_weapon_group)
        self.image = Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = x_pos + 40
        self.rect.y = y_pos

    def update(self):
        # Перемещает спрайты
        global trigger_death, boom, x_laser_delete, y_laser_delete, death
        self.rect = self.rect.move(0, -10)
        # Если пересекся с горизонтальной границей, то удаляется
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            pygame.sprite.spritecollide(self, glavniy_weapon_group, True)
        # Если пересекся с вертикальной границей, то удаляется
        if pygame.sprite.spritecollideany(self, vertical_borders):
            pygame.sprite.spritecollide(self, glavniy_weapon_group, True)
        # Если пересекся с врагом, то удаляется выстрел, враг, вызывается спрайт взрыва и звуковая дорожка
        if pygame.sprite.spritecollideany(self, enemy_group):
            pygame.sprite.spritecollide(self, glavniy_weapon_group, True)
            pygame.sprite.spritecollide(self, enemy_group, True)
            death += 1
            x_laser_delete = self.rect[0]
            y_laser_delete = self.rect[1]
            trigger_death = 2
            pygame.mixer.music.load(boom2)
            pygame.mixer.music.play()
            boom = Destroy(boom_group)
# Создает горизонтальные и вертикальные границы


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
# Создает корабль противника


class Enemy(pygame.sprite.Sprite):
    image = load_image("standart_unit_2.png", -1)
    image = pygame.transform.rotate(image, 180)

    def __init__(self, enemy_group):
        super().__init__(enemy_group)
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = coords_x
        self.rect.y = coords_y
        self.hp = 1

    def update(self):
        global choos, x_enemy, y_enemy, trigger_death, boom
        # Если вражеский корабль столкнулся с кораблем игрока, то они удаляются, вызывается спрайт взрыва и
        # звуковая дорожка взрыва
        if pygame.sprite.spritecollideany(self, player_group):
            pygame.sprite.spritecollide(self, enemy_group, True)
            pygame.sprite.spritecollide(self, player_group, True)
            trigger_death = 1
            pygame.mixer.find_channel().play(sound3)
            boom = Destroy(boom_group)
        # Расчет движения для 1 варианта полета
        if choos == 1 and self.rect[1] < 300:
            y = self.rect[1]
            d = b**2 - 4 * a * (c - y - 1)
            x1 = (-b - d**0.5)/2/a
            x2 = (-b + d ** 0.5) / 2 / a
            x_min = min(x2, x1)
            x_max = max(x2, x1)
            if self.rect[0] > 512:
                self.rect = self.rect.move(x_max - self.rect[0] - 90, 1)
            else:
                self.rect = self.rect.move(x_min - self.rect[0], 1)
        # Расчет движения для 2 варианта полета
        elif choos == 2 and self.rect[1] < 200:
            self.rect = self.rect.move(0, 1)
        # Не дает двигаться дальше
        else:
            choos = -1
# Создает спрайты вражеских лазеров


class Enemy_Weapon(pygame.sprite.Sprite):
    image = load_image("Enemy_lazer_type3.png", -1)
    image = pygame.transform.rotate(image, 90)

    def __init__(self, enemy_left_group):
        super().__init__(enemy_left_group)
        self.image = Enemy_Weapon.image
        self.rect = self.image.get_rect()
        self.rect.x = x_enemy + 30
        self.rect.y = y_enemy

    def update(self):
        global number_of_enemy_sprite_coords, trigger_death, boom, addition_speed
        number_of_enemy_sprite_coords += 1
        # Осуществляет передвижения вражеских спрайтов на определенное значение
        self.rect = \
            self.rect.move(list_coords_x[number_of_enemy_sprite_coords], list_coords_y[number_of_enemy_sprite_coords])
        # Если пересекся с горизонтальной границей, то удаляется лазер и направление его полета
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            pygame.sprite.spritecollide(self, enemy_weapon_group, True)
            del list_coords_x[number_of_enemy_sprite_coords], list_coords_y[number_of_enemy_sprite_coords]
            number_of_enemy_sprite_coords -= 1
        # Если пересекся с вертикальной границей, то удаляется лазер и направление его полета
        if pygame.sprite.spritecollideany(self, vertical_borders):
            pygame.sprite.spritecollide(self, enemy_weapon_group, True)
            del list_coords_x[number_of_enemy_sprite_coords], list_coords_y[number_of_enemy_sprite_coords]
            number_of_enemy_sprite_coords -= 1
        # Если пересекся с кораблем игрока границей, то удаляется лазер, направление его полета, корабль
        # игрока ивызываеся звуковая дорожка взрыва
        if pygame.sprite.spritecollideany(self, player_group):
            pygame.sprite.spritecollide(self, enemy_weapon_group, True)
            pygame.sprite.spritecollide(self, player_group, True)
            trigger_death = 1
            pygame.mixer.find_channel().play(sound3)
            boom = Destroy(boom_group)
# Создает спрайт взрыва


class Destroy(pygame.sprite.Sprite):
    image = load_image("Boom_2.png", -1)

    def __init__(self, boom_group):
        global trigger_death
        super().__init__(boom_group)
        self.image = Destroy.image
        self.rect = self.image.get_rect()
        if trigger_death == 1:
            self.rect.x = x_pos
            self.rect.y = y_pos
            list_time_of_delete.append(5)
        elif trigger_death == 2:
            self.rect.x = x_laser_delete
            self.rect.y = y_laser_delete - 90
            list_time_of_delete.append(3)
        trigger_death = 0

    def update(self):
        # По истечении времени удаляет спрайт взрыва
        pygame.sprite.spritecollide(self, boom_group, True)
        del list_time_of_delete[j]


# Создаются группы спрайтов
boom_group = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
glavniy_weapon_group = pygame.sprite.Group()
enemy_weapon_group = pygame.sprite.Group()
back_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Создается корабль игрока
ship = Ship(player_group)
# Создается фон
back = Background(back_group)
# Создается 5 каналов
pygame.mixer.set_num_channels(5)
# Обозначаем переменными путь к звуковой дорожке
PEW_PEW = 'data/PEW-PEW.wav'
PEW = 'data/PEW.wav'
boom2 = 'data/boom.wav'
# Вызываем микшер и прописываем его характеристики
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
# Создаем звуковые объекты
sound1 = pygame.mixer.Sound(PEW_PEW)
sound2 = pygame.mixer.Sound(PEW)
sound3 = pygame.mixer.Sound(boom2)

# Создаем границы
Border(-300, -100, width + 300, -100)
Border(-300, height + 100, width + 300, height + 100)
Border(-300, -100, -300, height + 100)
Border(width + 300, -100, width + 300, height + 100)
# Вызываем экран с правилами
start_screen()
# Запускаем цикл
running = True
while running:
    # Если нет вражеских кораблей, то создаем их
    if enemy_group.sprites() == []:
        choos = random.randint(0, 2)
        # Создаем корабли по 1 шаблону
        if choos == 1:
            for i in range(5):
                for l in range(2):
                    if (-1) ** l < 0:
                        coords_x = -90
                    else:
                        coords_x = width + 90
                    coords_y = -90 + -90 * (i+1) // 2
                    enemy = Enemy(enemy_group)
        # Создаем корабли по 2 шаблону
        if choos == 2:
            for hi in range(2):
                for wi in range(1, 10):
                    coords_x = wi * 90
                    coords_y = -90 * hi - 90
                    enemy = Enemy(enemy_group)

    # Таймер перезарядки орижия игрока
    if reload_1_blue % 25 != 0:
        reload_1_blue += 1

    # Если игрок нажимает на кнопку space то совершается выстрел(если оружие перезарядилось)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and colding == 15:
            # Вызывем звуковую дорожку  лазерного выстрела
            pygame.mixer.find_channel().play(sound2)
            green = Weapon(glavniy_weapon_group)
            colding = 0
            pew = True
        if event.type == pygame.QUIT:
            running = False

    # Проверяем допустимые направления движения корабля игрока
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

    # Проверяем, что кнопка зажата
    key = pygame.key.get_pressed()
    # Если зажата кнопка Space и оружие перезарядилось, то производит выстерлы, каждые 25 тиков, пока игрок не
    # отпустит Space
    if key[pygame.K_SPACE] and reload_1_blue % 25 == 0 and not pew:
        # Вызываем звуковую дорожку лазерного выстрела
        pygame.mixer.find_channel().play(sound2)
        green = Weapon(glavniy_weapon_group)
        reload_1_blue = 1
    # Проверка на зажатие стрелок, отвечающие за движение и осуществление передвижения
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

    # Высчитываем координаты направления движения корабля игрока
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

    # Координаты передвижения
    x_pos += v_x / FPS
    y_pos += v_y / FPS

    # Разрешает сделать новый выстрел(чтобы не было 2 выстрелов подряд)
    pew = False
    # Перезарядка оридия корабля игрока при однократном нажатии Space
    if colding != 15:
        colding += 1
    # Если есть вражеские корабли на карте, то заставляет их двигаться
    if enemy_group.sprites() != [] and choos != - 1:
        enemy_group.update()
    # Если есть врежеские корабли на карте и осуществлена перезарядка их орудий, то создаются новые лазеры врага
    if enemy_group.sprites() != [] and reload_2_red % 250 == 0:
        # Вызываем звуковую дорожку выстрелов противник
        pygame.mixer.find_channel().play(sound1)
        for sprit in range(len(enemy_group.sprites())):
            # Берем координаты вражеского корабля
            x_enemy = enemy_group.sprites()[sprit].rect[0]
            y_enemy = enemy_group.sprites()[sprit].rect[1]
            # Создаем лазер
            red = Enemy_Weapon(enemy_weapon_group)
            # Расчитываем расстояние от лазера до корабля игрока через проекцию на оси x и y
            x_s = x_pos - x_enemy - 30
            y_s = y_pos - y_enemy - 30
            # Через теорему пифагора находим расстояние от лазера до корабля игрока
            s = (x_s ** 2 + y_s ** 2) ** 0.5
            # Находим время, за которое лазер должен добратсья на корабля игрока
            time = s / u
            # Находим скорость движения лазера по осям x и y; и складываем их в списки
            u_x = (x_s / time) + addition_speed
            u_y = (y_s / time) + addition_speed
            list_coords_x.append(u_x)
            list_coords_y.append(u_y)
        # Немного увеличиваем скорость лазеров
        addition_speed += 0.2
        # Начинаем перезарядку орудий противника
        reload_2_red = 1

    # Каждые 5 тиков, если есть вражеские лазеры, двигаем их на координаты, лежащиие в списках, указаные на 5 строчек
    # выше
    if reload_2_red % 5 == 0 and enemy_weapon_group.sprites() != []:
        number_of_enemy_sprite_coords = -1
        enemy_weapon_group.update()

    # Перезаряжаем орудия вражеских кораблей
    reload_2_red += 1

    # Передвигаем корабль игрока и его лазеров
    player_group.update(x_pos, y_pos)
    glavniy_weapon_group.update()

    # Если есть взрывы на экране
    if list_time_of_delete:
        for j in range(len(list_time_of_delete)):
            if not list_time_of_delete:
                break
            # Уменьшаем время жизни спрайта по j
            list_time_of_delete[j] = list_time_of_delete[j] - 0.4
            # Если времяя жизни спрайта меньше 0, то удаляем его
            if list_time_of_delete[j] <= 0:
                boom_group.update()

    # Если корабль игрока уничтожен, то обнуляем значения
    if not player_group.sprites():
        reload_1_green = 0
        colding = 0
        x_pos = width // 2
        y_pos = height // 2
        v_x = 0
        v_y = 0
        reload_2_red = 0
        enemy_group.empty()
        enemy_weapon_group.empty()
        glavniy_weapon_group.empty()
        ship = Ship(player_group)
        back = Background(back_group)
        list_time_of_delete = []
        boom_group.empty()
        left = True
        right = True
        up = True
        down = True
        pew = False
        repeat = -1
        addition_speed_for_relaod = 0
        addition_speed = 0
        list_coords_x = []
        list_coords_y = []
        # Останавливаем звуковые дорожки
        pygame.mixer.Channel(0).stop()
        pygame.mixer.Channel(1).stop()
        pygame.mixer.Channel(2).stop()
        pygame.mixer.Channel(3).stop()
        pygame.mixer.Channel(4).stop()
        restart()

    # Прорисовываем гурппы спрайтов
    back_group.draw(screen)
    boom_group.draw(screen)
    enemy_weapon_group.draw(screen)
    glavniy_weapon_group.draw(screen)
    enemy_group.draw(screen)
    vertical_borders.draw(screen)
    horizontal_borders.draw(screen)
    player_group.draw(screen)
    # Обновляем/прорисовываем экран
    pygame.display.flip()
    clock.tick(FPS)

terminate()
