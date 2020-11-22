
import pygame, random
pygame.init()
FPS = 4
WIN_WIDTH = 350
WIN_HEIGHT = 700
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 100, 255)

ORANGE_BLOCK_IMAGE = pygame.image.load('ORANGE_BLOCK.png')
BLUE_BLOCK_IMAGE = pygame.image.load('BLUE_BLOCK.png')
PINK_BLOCK_IMAGE = pygame.image.load('PINK_BLOCK.png')
GREEN_BLOCK_IMAGE = pygame.image.load('GREEN_BLOCK.png')
EMPTY_BLOCK_IMAGE = pygame.image.load('EMPTY_BLOCK.png')
LIMIT_BLOCK_IMAGE = pygame.image.load('LIMIT_BLOCK.png')

IMAGES_SIDE_LENGTH = 20
ORANGE_BLOCK_IMAGE = pygame.transform.scale(ORANGE_BLOCK_IMAGE, (IMAGES_SIDE_LENGTH, IMAGES_SIDE_LENGTH))
BLUE_BLOCK_IMAGE = pygame.transform.scale(BLUE_BLOCK_IMAGE, (IMAGES_SIDE_LENGTH, IMAGES_SIDE_LENGTH))
PINK_BLOCK_IMAGE = pygame.transform.scale(PINK_BLOCK_IMAGE, (IMAGES_SIDE_LENGTH, IMAGES_SIDE_LENGTH))
GREEN_BLOCK_IMAGE = pygame.transform.scale(GREEN_BLOCK_IMAGE, (IMAGES_SIDE_LENGTH, IMAGES_SIDE_LENGTH))
EMPTY_BLOCK_IMAGE = pygame.transform.scale(EMPTY_BLOCK_IMAGE, (IMAGES_SIDE_LENGTH, IMAGES_SIDE_LENGTH))
LIMIT_BLOCK_IMAGE = pygame.transform.scale(LIMIT_BLOCK_IMAGE, (IMAGES_SIDE_LENGTH, IMAGES_SIDE_LENGTH))

COLORS_LIST = ['ORANGE', 'BLUE', 'PINK', 'GREEN']

NUMBER_OF_ROWS = 30
NUMBER_OF_COLUMNS = 10
ROW_LIMIT = NUMBER_OF_ROWS - 6
IMAGES = {'EMPTY': EMPTY_BLOCK_IMAGE, 'ORANGE': ORANGE_BLOCK_IMAGE,
          'BLUE': BLUE_BLOCK_IMAGE, 'PINK': PINK_BLOCK_IMAGE, 'GREEN': GREEN_BLOCK_IMAGE}

SHAPES_LIST = ['L', 'INV_L', 'KEYS', 'UP_STEPS', 'DOWN_STEPS', 'I', 'SQUARE']

#[column, row]      so its [x, y]
POSITIONS = {'L': [[0, 0], [0, -1], [0, 1], [1, 1]], 'INV_L': [[0, 0], [0, -1], [0, 1], [-1, 1]],
             'KEYS': [[0, 0], [0, 1], [-1, 1], [1, 1]],
             'UP_STEPS': [[0, 0], [1, 0], [0, -1], [-1, -1]], 'DOWN_STEPS': [[0, 0], [-1, 0], [0, 1], [1, 1]],
             'I': [[0, 0], [0, -1], [0, 1], [0, 2]], 'SQUARE': [[0, 0], [0, 1], [1, 0], [1, 1]]}

#[row, column]
# will use this for less confustion
POSITIONS2 = {'L': [[0, 0], [-1, 0], [1, 0], [1, 1]], 'INV_L': [[0, 0], [-1, 0], [1, 0], [1, -1]],
              'KEYS': [[0, 0], [1, 0], [1, -1], [1, 1]], 'UP_STEPS': [[0, 0], [0, 1], [-1, 0], [-1, -1]],
              'DOWN_STEPS': [[0, 0], [0, -1], [1, 0], [1, 1]], 'I': [[0, 0], [-1, 0], [1, 0], [2, 0]],
              'SQUARE': [[0, 0], [1, 0], [0, 1], [1, 1]]}

class Block:
    SIDE = IMAGES_SIDE_LENGTH
    def __init__(self, color):
        self.x = 0
        self.y = 0
        self.shape = random.choice(SHAPES_LIST)
        self.color = color
        self.img = IMAGES[color]
        self.location_grid = [0, 0] #[row, column]
        self.position_list = POSITIONS2[self.shape] #[row, column]
        self.rotated_position_list = None


    def draw_block(self):
        WIN.blit(self.img, (self.x, self.y))

    def draw_shape(self, x, y):
        self.x = x
        self.y = y
        for i in range(4):
            x = self.x + self.position_list[i][0] * Block.SIDE
            y = self.y + self.position_list[i][1] * Block.SIDE
            WIN.blit(self.img, (x, y))

    def rotate_shape(self): #inverse x and y and then multiply the new y by -1
         x = []
         for i in range(len(self.position_list)):
            xx = []
            for ii in range(1, -1, -1):
                xx += [self.position_list[i][ii]]
            x += [xx]

         for i in range(len(x)):
            x[i][1] = -1 * x[i][1]
         return x[:]

def new_grid():
    g = []
    for row in range(NUMBER_OF_ROWS):
        r = []
        for column in range(NUMBER_OF_COLUMNS):
                r += ['EMPTY']
        g += [r]

    return g


def draw_grid(grid):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            color = grid[row][column]
            x = Block.SIDE * (column + 1)
            y = WIN_HEIGHT - Block.SIDE * (row + 1) - Block.SIDE
            block = Block(color)
            block.x = x
            block.y = y
            block.draw_block()


def draw_limit(x, y):
    for i in range(NUMBER_OF_COLUMNS):
        WIN.blit(LIMIT_BLOCK_IMAGE, (x * (i + 1), y))

def draw_message(text, x, y, color, font_size = 40):
    font_style = pygame.font.SysFont('FUTURAM.ttf', font_size)
    b = font_style.render(text, True, color)
    WIN.blit(b, [x, y])


def main():
    done = False
    new_turn = True
    grid = new_grid()
    rotate = False
    move_right = False
    move_left = False
    hit_ground = False
    next_block = Block(random.choice(COLORS_LIST))
    points = 0
    while not done:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rotate = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_LEFT:
                    move_left = True

        if new_turn:
            new_turn = False

            block = next_block
            next_block = Block(random.choice(COLORS_LIST))

            block.location_grid = [len(grid) - 3, 5]

            grid[block.location_grid[0]][block.location_grid[1]] = block.color
            for i in block.position_list:
                grid[i[0] + block.location_grid[0]][i[1] + block.location_grid[1]] = block.color

        grid[block.location_grid[0]][block.location_grid[1]] = 'EMPTY'
        for i in block.position_list:
            grid[i[0] + block.location_grid[0]][i[1] + block.location_grid[1]] = 'EMPTY'


        move_down = True
        for i in block.position_list:
            if i[0] + block.location_grid[0] == 0:
                hit_ground = True

            if i[0] + block.location_grid[0] - 1 < NUMBER_OF_ROWS and i[0] + block.location_grid[0] - 1 >= 0:
                if grid[i[0] + block.location_grid[0] - 1][i[1] + block.location_grid[1]] != 'EMPTY':
                    move_down = False
                    hit_ground = True
            else:
                move_down = False
            if i[1] + block.location_grid[1] + 1 < NUMBER_OF_COLUMNS and i[1] + block.location_grid[1] + 1 >= 0:
                if grid[i[0] + block.location_grid[0]][i[1] + block.location_grid[1] + 1] != 'EMPTY':
                    move_right = False
                if grid[i[0] + block.location_grid[0] - 1][i[1] + block.location_grid[1] + 1] != 'EMPTY':
                    move_right = False
            else:
                move_right = False
            if i[1] + block.location_grid[1] - 1 < NUMBER_OF_COLUMNS and i[1] + block.location_grid[1] - 1 >= 0:
                if grid[i[0] + block.location_grid[0]][i[1] + block.location_grid[1] - 1] != 'EMPTY':
                    move_left = False
                elif grid[i[0] + block.location_grid[0] - 1][i[1] + block.location_grid[1] - 1] != 'EMPTY':
                    move_left = False
            else:
                move_left = False


        if rotate and not hit_ground:
            rotate = False

            block.rotated_position_list = block.rotate_shape()[:]
            move_row_to_fit_screen = 0
            move_column_to_fit_screen = 0
            beyond_list_row = []
            beyond_list_column = []

            for i in block.rotated_position_list:
                if i[0] + block.location_grid[0] >= NUMBER_OF_ROWS or i[0] + block.location_grid[0] < 0:
                    beyond_list_row += [i[0] + block.location_grid[0]]
                elif i[1] + block.location_grid[1] >= NUMBER_OF_COLUMNS or i[1] + block.location_grid[1] < 0:
                    beyond_list_column += [i[1] + block.location_grid[1]]

            if len(beyond_list_row) > 0:
                x = max(beyond_list_row)
                xx = min(beyond_list_row)
                if abs(x) > abs(xx):
                    move_row_to_fit_screen = x - block.location_grid[0]
                else:
                    move_row_to_fit_screen = xx - block.location_grid[0]

            if len(beyond_list_column) > 0:
                x = max(beyond_list_column)
                xx = min(beyond_list_column)
                if abs(x) > abs(xx):
                    move_column_to_fit_screen = x - block.location_grid[1]
                else:
                    move_column_to_fit_screen = xx - block.location_grid[1]

            block.location_grid[0] -= move_row_to_fit_screen
            block.location_grid[1] -= move_column_to_fit_screen

            count = 0
            for i in block.rotated_position_list:
                if grid[i[0] + block.location_grid[0]][i[1] + block.location_grid[1]] != 'EMPTY':
                    break
                count += 1

            if count == 4:
                block.position_list = block.rotated_position_list[:]




        if hit_ground:
            hit_ground = False
            new_turn = True
            move_down = False
            move_right = False
            move_left = False
            points += 40


            for i in grid[ROW_LIMIT]:
                if i != 'EMPTY':
                    points -= 10
                    done = True
            completed_row = None
            for row in range(len(grid)):
                for column in range(NUMBER_OF_ROWS):
                    if grid[row][column] == 'EMPTY':
                        break
                    completed_row = row
                    break
            if completed_row != None:

                moving_grid = []
                for i in grid[completed_row: ROW_LIMIT]:
                    row = []
                    for item in i:
                        row += [item]
                    moving_grid += [row]

                for i in range(len(moving_grid)):
                    for ii in range(NUMBER_OF_COLUMNS):
                        grid[completed_row][ii] = moving_grid[i][ii]



        if move_down:
            block.location_grid[0] -= 1

        if move_right:
            move_right = False
            block.location_grid[1] += 1

        if move_left:
            move_left = False
            block.location_grid[1] -= 1



        for i in block.position_list:
            grid[i[0] + block.location_grid[0]][i[1] + block.location_grid[1]] = block.color

        WIN.fill(WHITE)
        draw_message('Points: ' + str(points), 10, 20, YELLOW)
        next_block.draw_shape(WIN_WIDTH - 80, 40)
        draw_grid(grid)
        draw_limit(Block.SIDE, WIN_HEIGHT - (Block.SIDE * (ROW_LIMIT + 1)))
        pygame.display.flip()

main()