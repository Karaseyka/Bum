import os

import random
import sys
import math

import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

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

def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    # Текст
    intro_text = ["ЗАСТАВКА", "",
                  "Нажмите, чтобы начать",
                  ]
    # Генерируем фон
    fon = pygame.transform.scale(load_image('startscreen.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    # Идем по тексту, для каждой буквы применяем свойство
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # Ждем, пока нажмут любую кнопку
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()



print(load_level("1.txt"))
# Тут словарь для более удобной генерации карты
tile_images = {
    'bottle': load_image('bottle.png'),
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.rotate = False
        self.points = 0
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    # Хз что это
    new_player, x, y = None, None, None
    # Ищем максимальное кол - во бутылок на карте
    amount_of_bottles = int(math.sqrt(len(level) * len(level[0])))
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                # Если на карте должна быть трава, то смотрим, стоит ли ставить туда бутылку
                Tile('empty', x, y)
                if amount_of_bottles and random.randint(0, amount_of_bottles) == 1:
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
    # вернем игрока, а также размер поля в клетках
    print(x, y)
    return new_player, x, y

lavel = load_level("1.txt")
# Замеряем размеры карты для того, чтобы изменить размер экрана
size = width, height = len(lavel[0]) * 50, len(lavel) * 50
player, level_x, level_y = generate_level(lavel)
for i in lavel:
    print(i)
running = True
pygame.mouse.set_visible(False)
# Изменяем размер экрана под размер карты
pygame.display.set_mode(size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.rect.x // 50 and\
                    lavel[player.rect.y // 50][player.rect.x // 50 - 1] != "#":
                player.image = pygame.transform.flip(player.image, not player.rotate, False)
                player.rotate = True
                player.rect.x -= 50
            elif event.key == pygame.K_RIGHT and player.rect.x // 50 + 1 < len(lavel[0]) and "#" != \
                    lavel[player.rect.y // 50][player.rect.x // 50 + 1]:
                player.image = pygame.transform.flip(player.image, player.rotate, False)
                player.rotate = False
                player.rect.x += 50
            elif event.key == pygame.K_UP and player.rect.y // 50 and\
                    lavel[player.rect.y // 50 - 1][player.rect.x // 50] != "#":
                player.rect.y -= 50
            elif event.key == pygame.K_DOWN and player.rect.y // 50 + 1 < len(lavel) and\
                    lavel[player.rect.y // 50 + 1][player.rect.x // 50] != "#":
                player.rect.y += 50
    screen.fill(pygame.Color("white "))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(10)
    if lavel[player.rect.y // 50][player.rect.x // 50] == "b":
        lavel[player.rect.y // 50][player.rect.x // 50] = '.'
        Tile('empty', player.rect.x // 50, player.rect.y // 50)
        player.points += 1
        print(player.points)
        # for i in lavel:
        #     print(i)
