import os
import queue
import random
import sys
import math
import time
import threading

import pygame

pygame.init()
pygame.font.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# загружаем уровень
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    # for i in level_map:
    #     print(i)
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    # return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return level_map


# загружаем картинку
def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


FPS = 50


# выход из приложения
def terminate():
    pygame.quit()
    sys.exit()


# стартовый экран
def start_screen():
    # Текст
    intro_text = ["            BUM", "",
                  "",
                  ]
    # Генерируем фон
    fon = pygame.transform.scale(load_image('startscreen.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    # Идем по тексту, для каждой строки применяем свойство
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.draw.rect(screen, (255, 255, 0),
                     (230, 320, 265, 155))
    pygame.draw.rect(screen, (255, 255, 255),
                     (240, 400, 70, 70))
    screen.blit(font.render('1', True, (0, 200, 255)), (446 - 180, 420))
    pygame.draw.rect(screen, (255, 255, 255),
                     (330, 400, 70, 70))
    screen.blit(font.render('2', True, (0, 200, 255)), (446 - 90, 420))
    pygame.draw.rect(screen, (255, 255, 255),
                     (420, 400, 70, 70))
    screen.blit(font.render('3', True, (0, 200, 255)), (446, 420))
    screen.blit(font.render('Уровни', True, (0, 200, 255)), (240, 330))

    # Ждем, пока нажмут любую кнопку
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                if 240 <= mousex <= 310 and 400 <= mousey <= 470:
                    print(1, "lavel")
                    return 1
                elif 330 <= mousex <= 400 <= mousey <= 470:
                    print(2, "lavel")
                    return 2
                elif 420 <= mousex <= 490 and 400 <= mousey <= 470:
                    print(3, "lavel")
                    return 3
        pygame.display.flip()
        clock.tick(FPS)


# создание плиток
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.rotate = False
        self.points = 0
        self.image = player_image
        self.anim = 0
        self.count = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    # анимация
    def update(self):
        global side
        print(self.anim)
        if self.anim:
            self.image = player_image
            print("First image set")
        else:
            self.image = player_image2
            print("Second Image set")
        if not side:
            self.image = pygame.transform.flip(self.image, True, False)
        self.anim = abs(self.anim - 1)


# создание гопника
class Gopnic(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.rotate = False

        self.image = load_image("gop1.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# генерация уровня
def generate_level(level):
    am_bottles = 0
    new_player, new_gopnic, x, y = None, None, None, None
    # Ищем максимальное кол - во бутылок на карте
    amount_of_bottles = int(math.sqrt(len(level) * len(level[0])))
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                # Если на карте должна быть трава, то смотрим, стоит ли ставить туда бутылку
                Tile('empty', x, y)
                if amount_of_bottles and random.randint(0, amount_of_bottles) == 1:
                    am_bottles += 1
                    Tile('bottle', x, y)
                    level[y][x] = 'b'
                    amount_of_bottles -= 1
            elif level[y][x] == '#':
                # Ставим стенку
                Tile('wall', x, y)
            elif level[y][x] == '@':
                # Ставим персонажа
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '*':
                # Ставим персонажа
                Tile('empty', x, y)
                new_gopnic = Gopnic(x, y)
    # вернем игрока, а также размер поля в клетках
    print(x, y)
    return new_player, new_gopnic, x, y, am_bottles


# ждём нажатия кнопки
def wait_for_button():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# создаём список смежностей графа
def make_sm_list(a):
    sm = []
    for i in range(len(a)):
        for j in range(len(a[i])):
            d = []
            if a[i][j] == "." or a[i][j] == "@" or a[i][j] == "*":
                if i + 1 < len(a) and a[i + 1][j] in ".@*":
                    d.append(len(a[i]) * (i + 1) + j + 1)
                if i - 1 >= 0 and a[i - 1][j] in ".@*":
                    d.append(len(a[i]) * (i - 1) + j + 1)
                if j + 1 < len(a[i]) and a[i][j + 1] in "@.*":
                    d.append(len(a[i]) * i + j + 2)
                if j - 1 >= 0 and a[i][j - 1] in "@.*":
                    d.append(len(a[i]) * i + j)
                sm.append(d)
            else:
                sm.append([])
    return sm


# запускаем обход в глубину dfs
def bfs(start, sm):
    q = queue.Queue()
    di[start] = 0
    q.put(start)
    while not q.empty():
        v = q.get()
        try:
            for u in sm[v - 1]:
                if di[u] == 1000000:
                    di[u] = di[v] + 1
                    q.put(u)
                    p[u] = v
        except Exception:
            print("dfhsfd", v)


# возвращаем востановленный маршрут
def return_way(start, t):
    f = [t]
    try:
        while t != start:
            print("t:", t)
            f.append(p[t])
            t = p[t]
        f.reverse()
    except Exception:
        print(t, f)
    return f


# начало игры
while True:
    pygame.mouse.set_visible(True)
    num_lavel = start_screen()
    count = 0
    # print(load_level("1.txt"))
    # Тут словарь для более удобной генерации карты
    tile_images = {
        'bottle': load_image('bottle.png'),
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mar.png')
    player_image2 = load_image('mar2.png')
    tile_width = tile_height = 50
    # основной персонаж
    player = None

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    if num_lavel == 1:
        lavel = load_level("1.txt")
        di = [1000000] * (len(lavel) * len(lavel[0]) + 1)
        p = [1000000] * (len(lavel) * len(lavel[0]) + 1)
        sm_lst = make_sm_list(lavel)
        # Замеряем размеры карты для того, чтобы изменить размер экрана
        size = width, height = len(lavel[0]) * 50, len(lavel) * 50
        player, gopnic, level_x, level_y, am_bottles = generate_level(lavel)
        bfs((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1, sm_lst)
        hodyi = return_way((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1,
                           (player.rect.x // 50) + (player.rect.y // 50) * len(lavel[0]) + 1)
        running = True
        side = 1
        pygame.mouse.set_visible(False)
        # Изменяем размер экрана под размер карты
        pygame.display.set_mode(size)
        my_font = pygame.font.Font(None, 30)
        text_surface = my_font.render("Бутылок: " + str(player.points), 1, pygame.Color("white"))
        screen.blit(text_surface, (10, 10))
        font = pygame.font.Font(None, 50)
        time_elapsed_since_last_action = 0
        clock = pygame.time.Clock()
        hod = 1
        win = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and player.rect.x // 50 and \
                            lavel[player.rect.y // 50][player.rect.x // 50 - 1] != "#":
                        player.image = pygame.transform.flip(player.image, not player.rotate, False)
                        side = 0
                        player.rotate = True
                        player.rect.x -= 50
                    elif event.key == pygame.K_RIGHT and player.rect.x // 50 + 1 < len(lavel[0]) and "#" != \
                            lavel[player.rect.y // 50][player.rect.x // 50 + 1]:
                        side = 1
                        player.image = pygame.transform.flip(player.image, player.rotate, False)
                        player.rotate = False
                        player.rect.x += 50
                    elif event.key == pygame.K_UP and player.rect.y // 50 and \
                            lavel[player.rect.y // 50 - 1][player.rect.x // 50] != "#":
                        player.rect.y -= 50
                    elif event.key == pygame.K_DOWN and player.rect.y // 50 + 1 < len(lavel) and \
                            lavel[player.rect.y // 50 + 1][player.rect.x // 50] != "#":
                        player.rect.y += 50
                    di = [1000000] * (len(lavel) * len(lavel[0]) + 1)
                    p = [1000000] * (len(lavel) * len(lavel[0]) + 1)
                    bfs((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1, sm_lst)

                    hodyi = return_way((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1,
                                       (player.rect.x // 50) + (player.rect.y // 50) * len(lavel[0]) + 1)
                    hod = 1

            if lavel[player.rect.y // 50][player.rect.x // 50] == "b":
                lavel[player.rect.y // 50][player.rect.x // 50] = '.'
                Tile('empty', player.rect.x // 50, player.rect.y // 50)
                player.points += 1
                # for i in lavel:
                #     print(i)
            if gopnic.rect.x // 50 == player.rect.x // 50 and gopnic.rect.y // 50 == player.rect.y // 50:
                running = False
                win = False
            elif player.points == am_bottles:
                running = False
                win = True
            dt = clock.tick()
            time_elapsed_since_last_action += dt
            if time_elapsed_since_last_action > 225 and hod < len(hodyi):
                cur = (gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1
                # print(cur, (gopnic.rect.x // 50), (gopnic.rect.y // 50))
                if hodyi[hod] + len(lavel[0]) == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.y -= 50
                elif hodyi[hod] - len(lavel[0]) == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.y += 50
                elif hodyi[hod] - 1 == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.x += 50
                elif hodyi[hod] + 1 == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.x -= 50
                hod += 1
                time_elapsed_since_last_action = 0
            text = font.render("Бутылок: " + str(player.points), True,
                               (10, 50, 183))
            text.get_rect().x = 0
            screen.blit(text, (0, 0))
            pygame.display.flip()
            all_sprites.draw(screen)
            tiles_group.draw(screen)
            player_group.draw(screen)
            count = count + 1 if count <= 100 else 1
            if count % 15 == 0:
                all_sprites.update()

        size = width, height = 500, 500
        screen = pygame.display.set_mode(size)
        if not win:
            fon = pygame.transform.scale(load_image('death_screen.png'), (width, height))
            intro_text = ["Вы проиграли!", "",
                          "Нажмите, чтобы выйти",
                          ]
            screen.blit(fon, (0, 0))
        else:
            fon = pygame.transform.scale(load_image('win_screen.png'), (width, height))
            intro_text = ["Вы выиграли!", "",
                          "Нажмите, чтобы выйти",
                          ]
            screen.blit(fon, (0, 0))
        pygame.display.flip()
        time.sleep(1)
        font = pygame.font.Font(None, 30)
        text_coord = 50
        # Идем по тексту, для каждой строки применяем свойство
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        wait_for_button()
    elif num_lavel == 2:
        lavel = load_level("12.txt")
        di = [1000000] * (len(lavel) * len(lavel[0]) + 1)
        p = [1000000] * (len(lavel) * len(lavel[0]) + 1)
        sm_lst = make_sm_list(lavel)
        # Замеряем размеры карты для того, чтобы изменить размер экрана
        size = width, height = len(lavel[0]) * 50, len(lavel) * 50
        player, gopnic, level_x, level_y, am_bottles = generate_level(lavel)
        bfs((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1, sm_lst)
        hodyi = return_way((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1,
                           (player.rect.x // 50) + (player.rect.y // 50) * len(lavel[0]) + 1)
        running = True
        side = 1
        pygame.mouse.set_visible(False)
        # Изменяем размер экрана под размер карты
        pygame.display.set_mode(size)
        my_font = pygame.font.Font(None, 30)
        text_surface = my_font.render("Бутылок: " + str(player.points), 1, pygame.Color("white"))
        screen.blit(text_surface, (10, 10))
        font = pygame.font.Font(None, 50)
        time_elapsed_since_last_action = 0
        clock = pygame.time.Clock()
        hod = 1
        win = False
        print(sm_lst)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and player.rect.x // 50 and \
                            lavel[player.rect.y // 50][player.rect.x // 50 - 1] != "#":
                        player.image = pygame.transform.flip(player.image, not player.rotate, False)
                        side = 0
                        player.rotate = True
                        player.rect.x -= 50
                    elif event.key == pygame.K_RIGHT and player.rect.x // 50 + 1 < len(lavel[0]) and "#" != \
                            lavel[player.rect.y // 50][player.rect.x // 50 + 1]:
                        player.image = pygame.transform.flip(player.image, player.rotate, False)
                        side = 1
                        player.rotate = False
                        player.rect.x += 50
                    elif event.key == pygame.K_UP and player.rect.y // 50 and \
                            lavel[player.rect.y // 50 - 1][player.rect.x // 50] != "#":
                        player.rect.y -= 50
                    elif event.key == pygame.K_DOWN and player.rect.y // 50 + 1 < len(lavel) and \
                            lavel[player.rect.y // 50 + 1][player.rect.x // 50] != "#":
                        player.rect.y += 50
                    di = [1000000] * (len(lavel) * len(lavel[0]) + 1)
                    p = [1000000] * (len(lavel) * len(lavel[0]) + 1)
                    bfs((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1, sm_lst)

                    hodyi = return_way((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1,
                                       (player.rect.x // 50) + (player.rect.y // 50) * len(lavel[0]) + 1)
                    hod = 1

            if lavel[player.rect.y // 50][player.rect.x // 50] == "b":
                lavel[player.rect.y // 50][player.rect.x // 50] = '.'
                Tile('empty', player.rect.x // 50, player.rect.y // 50)
                player.points += 1
                # for i in lavel:
                #     print(i)
            if gopnic.rect.x // 50 == player.rect.x // 50 and gopnic.rect.y // 50 == player.rect.y // 50:
                running = False
                win = False
            elif player.points == am_bottles:
                running = False
                win = True
            dt = clock.tick()
            time_elapsed_since_last_action += dt
            if time_elapsed_since_last_action > 200 and hod < len(hodyi):
                cur = (gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1
                # print(cur, (gopnic.rect.x // 50), (gopnic.rect.y // 50))
                if hodyi[hod] + len(lavel[0]) == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.y -= 50
                elif hodyi[hod] - len(lavel[0]) == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.y += 50
                elif hodyi[hod] - 1 == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.x += 50
                elif hodyi[hod] + 1 == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.x -= 50
                hod += 1
                time_elapsed_since_last_action = 0
            text = font.render("Бутылок: " + str(player.points), True,
                               (10, 50, 183))
            text.get_rect().x = 0
            screen.blit(text, (0, 0))
            pygame.display.flip()
            all_sprites.draw(screen)
            tiles_group.draw(screen)
            player_group.draw(screen)
            count = count + 1 if count <= 100 else 1
            if count % 15 == 0:
                all_sprites.update()

        size = width, height = 500, 500
        screen = pygame.display.set_mode(size)
        if not win:
            fon = pygame.transform.scale(load_image('death_screen.png'), (width, height))
            intro_text = ["Вы проиграли!", "",
                          "Нажмите, чтобы выйти",
                          ]
            screen.blit(fon, (0, 0))
        else:
            fon = pygame.transform.scale(load_image('win_screen.png'), (width, height))
            intro_text = ["Вы выиграли!", "",
                          "Нажмите, чтобы выйти",
                          ]
            screen.blit(fon, (0, 0))
        pygame.display.flip()
        time.sleep(1)
        font = pygame.font.Font(None, 30)
        text_coord = 50
        # Идем по тексту, для каждой строки применяем свойство
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        wait_for_button()
    else:
        lavel = load_level("13.txt")
        di = [1000000] * (len(lavel) * len(lavel[0]) + 1)
        p = [1000000] * (len(lavel) * len(lavel[0]) + 1)
        sm_lst = make_sm_list(lavel)
        # Замеряем размеры карты для того, чтобы изменить размер экрана
        size = width, height = len(lavel[0]) * 50, len(lavel) * 50
        player, gopnic, level_x, level_y, am_bottles = generate_level(lavel)
        bfs((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1, sm_lst)
        hodyi = return_way((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1,
                           (player.rect.x // 50) + (player.rect.y // 50) * len(lavel[0]) + 1)
        running = True
        side = 1
        pygame.mouse.set_visible(False)
        # Изменяем размер экрана под размер карты
        pygame.display.set_mode(size)
        my_font = pygame.font.Font(None, 30)
        text_surface = my_font.render("Бутылок: " + str(player.points), 1, pygame.Color("white"))
        screen.blit(text_surface, (10, 10))
        font = pygame.font.Font(None, 50)
        time_elapsed_since_last_action = 0
        clock = pygame.time.Clock()
        hod = 1
        win = False
        print(sm_lst)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and player.rect.x // 50 and \
                            lavel[player.rect.y // 50][player.rect.x // 50 - 1] != "#":
                        player.image = pygame.transform.flip(player.image, not player.rotate, False)
                        side = 0
                        player.rotate = True
                        player.rect.x -= 50
                    elif event.key == pygame.K_RIGHT and player.rect.x // 50 + 1 < len(lavel[0]) and "#" != \
                            lavel[player.rect.y // 50][player.rect.x // 50 + 1]:
                        player.image = pygame.transform.flip(player.image, player.rotate, False)
                        side = 1
                        player.rotate = False
                        player.rect.x += 50
                    elif event.key == pygame.K_UP and player.rect.y // 50 and \
                            lavel[player.rect.y // 50 - 1][player.rect.x // 50] != "#":
                        player.rect.y -= 50
                    elif event.key == pygame.K_DOWN and player.rect.y // 50 + 1 < len(lavel) and \
                            lavel[player.rect.y // 50 + 1][player.rect.x // 50] != "#":
                        player.rect.y += 50
                    di = [1000000] * (len(lavel) * len(lavel[0]) + 1)
                    p = [1000000] * (len(lavel) * len(lavel[0]) + 1)
                    bfs((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1, sm_lst)

                    hodyi = return_way((gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1,
                                       (player.rect.x // 50) + (player.rect.y // 50) * len(lavel[0]) + 1)
                    hod = 1

            if lavel[player.rect.y // 50][player.rect.x // 50] == "b":
                lavel[player.rect.y // 50][player.rect.x // 50] = '.'
                Tile('empty', player.rect.x // 50, player.rect.y // 50)
                player.points += 1
                # for i in lavel:
                #     print(i)
            if gopnic.rect.x // 50 == player.rect.x // 50 and gopnic.rect.y // 50 == player.rect.y // 50:
                running = False
                win = False
            elif player.points == am_bottles:
                running = False
                win = True
            dt = clock.tick()
            time_elapsed_since_last_action += dt
            if time_elapsed_since_last_action > 150 and hod < len(hodyi):
                cur = (gopnic.rect.x // 50) + (gopnic.rect.y // 50) * len(lavel[0]) + 1
                # print(cur, (gopnic.rect.x // 50), (gopnic.rect.y // 50))
                if hodyi[hod] + len(lavel[0]) == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.y -= 50
                elif hodyi[hod] - len(lavel[0]) == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.y += 50
                elif hodyi[hod] - 1 == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.x += 50
                elif hodyi[hod] + 1 == cur:
                    gopnic.image = pygame.transform.flip(gopnic.image, not gopnic.rotate, False)
                    gopnic.rect.x -= 50
                hod += 1
                time_elapsed_since_last_action = 0
            text = font.render("Бутылок: " + str(player.points), True,
                               (10, 50, 183))
            text.get_rect().x = 0
            screen.blit(text, (0, 0))
            pygame.display.flip()
            all_sprites.draw(screen)
            tiles_group.draw(screen)
            player_group.draw(screen)
            count = count + 1 if count <= 100 else 1
            if count % 15 == 0:
                all_sprites.update()

        size = width, height = 500, 500
        screen = pygame.display.set_mode(size)
        if not win:
            fon = pygame.transform.scale(load_image('death_screen.png'), (width, height))
            intro_text = ["Вы проиграли!", "",
                          "Нажмите, чтобы выйти",
                          ]
            screen.blit(fon, (0, 0))
        else:
            fon = pygame.transform.scale(load_image('win_screen.png'), (width, height))
            intro_text = ["Вы выиграли!", "",
                          "Нажмите, чтобы выйти",
                          ]
            screen.blit(fon, (0, 0))
        pygame.display.flip()
        time.sleep(1)
        font = pygame.font.Font(None, 30)
        text_coord = 50
        # Идем по тексту, для каждой строки применяем свойство
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        wait_for_button()
