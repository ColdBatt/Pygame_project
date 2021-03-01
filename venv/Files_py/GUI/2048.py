import pygame
import sys
import os
from random import choice, randint


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 385, 580
FPS = 60
X, Y = 4, 4


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.space = [[0] * 4 for i in range(4)]
        self.left_space = 10
        self.top = 10
        self.cell_size = 30
        self.color_values = {2048: '#eec63d',
                             1024: '#eec63d',
                             512: '#eec94f',
                             256: '#eecd61',
                             128: '#eed073',
                             64: '#f65e38',
                             32: '#f67d5f',
                             16: '#f59663',
                             8: '#f2b37a',
                             4: '#eee1c9',
                             2: '#eee5db',
                             0: '#cdc1b4'}


    def set_view(self, left_space, top, cell_size):
        self.left_space = left_space
        self.top = top
        self.cell_size = cell_size


    def render(self, screen):
        font = pygame.font.Font(pygame.font.match_font('arial'), 25)
        font_size = 1
        x_pos = 0
        y_pos = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.space[y][x] in [2, 4, 8]:
                    font_size = 50
                    x_pos = x * self.cell_size + self.left_space + 0.345 * self.cell_size
                    y_pos = y * self.cell_size + self.top + 0.2 * self.cell_size
                elif self.space[y][x] in [64, 32, 16]:
                    font_size = 40
                    x_pos = x * self.cell_size + self.left_space + 0.26 * self.cell_size
                    y_pos = y * self.cell_size + self.top + 0.25 * self.cell_size
                elif self.space[y][x] in [128, 256, 512]:
                    font_size = 30
                    x_pos = x * self.cell_size + self.left_space + 0.25 * self.cell_size
                    y_pos = y * self.cell_size + self.top + 0.3 * self.cell_size
                elif self.space[y][x] in [1024, 2048]:
                    font_size = 25
                    x_pos = x * self.cell_size + self.left_space + 0.19 * self.cell_size
                    y_pos = y * self.cell_size + self.top + 0.34 * self.cell_size

                font = pygame.font.Font(pygame.font.match_font('arial'), font_size)
                figure = pygame.draw.rect(screen, self.color_values[self.space[y][x]],
                                          (x * self.cell_size + self.left_space, y * self.cell_size + self.top,
                                           self.cell_size, self.cell_size))

                count = font.render(str(self.space[y][x]) if self.space[y][x] != 0 else '',
                                    True, (249, 246, 242) if not self.space[y][x] in [2, 4] else (120, 110, 101))
                screen.blit(count, (x_pos, y_pos))


    def new_game(self):
        self.save(new=True)
        self.load()
        self.add_random_number()
        self.add_random_number()


    def load(self):
        save = list(open(os.path.join('data', 'save.txt'), encoding='utf8'))
        cells = save[0].split(':')[:-1]

        values = []

        for elem in range(len(cells)):
            values.append(cells[elem].split(','))
        for i in range(len(values)):
            for j in range(len(values[i])):
                values[i][j] = int(values[i][j])

        self.space = values


    def save(self, new=False):
        if new:
            save = open(os.path.join('data', 'save.txt'), 'w', encoding='utf8')
            save.write('0,0,0,0:0,0,0,0:0,0,0,0:0,0,0,0:')
        else:
            save_str = ''
            for elem in self.space:
                save_str += ','.join(list(map(lambda x: str(x), elem)))
                save_str += ':'
            save = open(os.path.join('data', 'save.txt'), 'w', encoding='utf8')
            save.write(save_str)


    def summ(self):
        return sum([sum(i) for i in self.space])


    def are_ya_winning_son(self): # Небольшая отсылка к мему
        for row in self.space:
            for cell in row:
                if cell == 2048:
                    return True
        return False


    def up(self):
        for i in range(len(self.space)):
            for j in range(len(self.space[i])):
                if self.space[i][j] == self.space[i - 1][j] and self.space[i] != 0:
                    self.space[i][j] = 0
                    self.space[i - 1][j] *= 2
                if self.space[i][j] == 0 and i != len(self.space) - 1:
                    self.space[i][j] = self.space[i + 1][j]
                    self.space[i + 1][j] = 0


    def down(self):
        for i in range(len(self.space)):
            for j in range(len(self.space[i])):
                if i != len(self.space) - 1:
                    if self.space[i][j] == self.space[i + 1][j] and self.space[i] != 0:
                        self.space[i][j] = 0
                        self.space[i + 1][j] *= 2
                    if self.space[i + 1][j] == 0 and i != len(self.space):
                        self.space[i + 1][j] = self.space[i][j]
                        self.space[i][j] = 0


    def left(self):
        for i in range(len(self.space)):
            for j in range(len(self.space[i])):

                if self.space[i][j] == self.space[i][j - 1] and j != 0:
                    self.space[i][j] = 0
                    self.space[i][j - 1] *= 2
                if self.space[i][j] == 0 and j != len(self.space[i]) - 1:
                    self.space[i][j] = self.space[i][j + 1]
                    self.space[i][j + 1] = 0


    def right(self):
        for i in range(len(self.space)):
            for j in range(len(self.space[i])):
                if j != len(self.space[i]) - 1:
                    if self.space[i][j] == self.space[i][j + 1]:
                        self.space[i][j] = 0
                        self.space[i][j + 1] *= 2
                if self.space[i][j] == 0 and j != 0:
                    self.space[i][j] = self.space[i][j - 1]
                    self.space[i][j - 1] = 0


    def add_random_number(self):

        empty_cells = []
        for i in range(len(self.space)):
            for j in range(len(self.space[i])):
                if self.space[i][j] == 0:
                    empty_cells.append((i, j))

        if bool(empty_cells):
            random_cell = choice(empty_cells)

            if randint(1, 100) > 10:
                self.space[random_cell[0]][random_cell[1]] = 2
            else:
                self.space[random_cell[0]][random_cell[1]] = 4


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def show_score(screen, score):
    font = pygame.font.Font(pygame.font.match_font('arial'), 50)
    text = font.render('2048', True, (120, 110, 100))

    text_x = 20
    text_y = 20
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(pygame.font.match_font('arial'), 30)
    label = font.render(f'Счет:', True, (120, 110, 100))

    screen.blit(label, (text_x + 250, text_y + 90))
    count = font.render(str(score), True, (120, 110, 100))
    screen.blit(count, (text_x + 260, text_y + 130))
    font = pygame.font.Font(pygame.font.match_font('arial'), 15)
    save = font.render('Новая игра', True, (120, 110, 100))
    screen.blit(save, (265, 35))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    board = Board(X, Y)
    board.set_view(10, 200, 90)
    board.add_random_number()
    board.add_random_number()

    cells_group = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("cells.png")
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 9
    sprite.rect.y = 199
    button = pygame.sprite.Sprite()
    button.image = load_image('button.png')
    button.rect = sprite.image.get_rect()
    button.rect.x = 255
    button.rect.y = 20
    cells_group.add(button)
    cells_group.add(sprite)
    board.load()

    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.save()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for i in range(4):
                        board.up()
                    board.add_random_number()

                if event.key == pygame.K_DOWN:
                    for i in range(4):
                        board.down()
                    board.add_random_number()
                if event.key == pygame.K_LEFT:
                    for i in range(4):
                        board.left()
                    board.add_random_number()
                if event.key == pygame.K_RIGHT:
                    for i in range(4):
                        board.right()
                    board.add_random_number()
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = event.pos
                if coords[0] >= 255 and coords[0] <= 355:
                    if coords[1] >= 20 and coords[1] <= 70:
                        board.new_game()

        screen.fill((250, 248, 239))

        board.render(screen)
        cells_group.draw(screen)
        show_score(screen, board.summ())
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()