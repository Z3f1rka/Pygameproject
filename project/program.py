import pygame
import os
import sys
import random


level = "#.txt"


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


FPS = 50
#
def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = [""]

    fon = pygame.transform.scale(load_image('fon.jpg'), (1155, 830))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50

# основной персонаж
player = None
max_points = 0
level_now = 1

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
points_group = pygame.sprite.Group()
proectors_group = pygame.sprite.Group()
portals_group = pygame.sprite.Group()
death = False

def end_screen():
    global death
    endscreen = pygame.transform.scale(load_image('end.jpg'), (1155, 830))
    screen.blit(endscreen, (0, 0))
    death = True

def death_screen():
    global death
    endscreen = pygame.transform.scale(load_image('death.jpg'), (1155, 830))
    screen.blit(endscreen, (0, 0))
    death = True


class Rating:
    def __init__(self):
        self.points = 0

    def update_r(self):
        self.points += 1
        intro_text = [f"Рейтинг:{self.points}"]
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        if self.points == max_points:
            global player
            global level_x
            global level_y
            global level_now
            if level_now == 1:
                for i in all_sprites:
                    i.kill()
                player, level_x, level_y = generate_level(load_level('map.txt'))
                print(max_points)
                level_now += 1
            else:
                end_screen()



    def update(self):
        intro_text = [f"Рейтинг: {self.points}"]
        font = pygame.font.Font(None, 50)
        text_coord = 50
        rect = pygame.draw.rect(screen, (254, 206, 0), (1, 1, 250, 100))
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)



class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = load_image('box.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Point(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(points_group, all_sprites)
        self.image = load_image('point.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            points.update_r()

class Proector_left(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(proectors_group, all_sprites)
        self.image = pygame.transform.scale(load_image('proector.png'), (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.left = True

    def update(self):
        if self.left:
            self.rect.x -= 10
            if pygame.sprite.spritecollideany(self, walls_group):
                self.left = False
            if pygame.sprite.spritecollideany(self, player_group):
                death_screen()
        else:
            self.rect.x += 10
            if pygame.sprite.spritecollideany(self, walls_group):
                self.left = True
            if pygame.sprite.spritecollideany(self, player_group):
                death_screen()


class Proector_up(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(proectors_group, all_sprites)
        self.image = pygame.transform.scale(load_image('proector.png'), (50, 50))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.up = True

    def update(self):
        if self.up:
            self.rect.y -= 10
            if pygame.sprite.spritecollideany(self, walls_group):
                self.up = False
            if pygame.sprite.spritecollideany(self, player_group):
                death_screen()
        else:
            self.rect.y += 10
            if pygame.sprite.spritecollideany(self, walls_group):
                self.up = True
            if pygame.sprite.spritecollideany(self, player_group):
                death_screen()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

def generate_level(level):
    global max_points
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '-':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
            elif level[y][x] == '<':
                Tile('empty', x, y)
            elif level[y][x] == '^':
                Tile('empty', x, y)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '-':
                Point(x, y)
                max_points += 1
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '<':
                Proector_left(x, y)
            elif level[y][x] == '^':
                Proector_up(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

def draw(screen):
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.left = True
        self.right = True
        self.up = True
        self.down = True

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.left:
                    target.rect.x -= 10
                    if pygame.sprite.spritecollideany(player, walls_group):
                        target.rect.x += 10

            if keys[pygame.K_RIGHT]:
                if self.right:
                    target.rect.x += 10
                    if pygame.sprite.spritecollideany(player, walls_group):
                        target.rect.x -= 10

            if keys[pygame.K_UP]:
                if self.up:
                    target.rect.y -= 10
                    if pygame.sprite.spritecollideany(player, walls_group):
                        target.rect.y += 10

            if keys[pygame.K_DOWN]:
                if self.down:
                    target.rect.y += 10
                    if pygame.sprite.spritecollideany(player, walls_group):
                        target.rect.y -= 10
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(0, -50)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('Ы')
    size = width, height = 1155, 830
    screen = pygame.display.set_mode(size)


    fps = 10
    clock = pygame.time.Clock()
    b = 0
    start = True
    running = False
    camera = Camera()
    points = Rating()


    while start:
        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                running = True
                start = False
        pygame.display.flip()
    player, level_x, level_y = generate_level(load_level(level))

    dragon = AnimatedSprite(load_image("dragon_sheet8x2.png"), 5, 1, -100, -100)
    while running:
        dragon.update()
        screen2 = pygame.Surface(screen.get_size())
        screen2.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
        if not death:
            draw(screen)
            all_sprites.update()
            points.update()
            clock.tick(10)
        pygame.display.flip()


