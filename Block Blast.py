import pygame
import random
import math
from pygame import gfxdraw
pygame.init()

WIDTH, HEIGHT = 1366, 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT))  # Seperate so we can do screen shake
pygame.display.set_caption("Block Blast")
pygame.display.set_icon(pygame.image.load("assets/textures/Icon.png"))
timer = pygame.time.Clock()
FPS = 60

shapes = {
    "1x2": [
        [1, 1]
    ],

    "2x1": [
        [1],
        [1]
    ],

    "2x2": [
        [1, 1],
        [1, 1]
    ],

    "2x3": [
        [1, 1],
        [1, 1],
        [1, 1]
    ],

    "3x2": [
        [1, 1, 1],
        [1, 1, 1]
    ],

    "3x3": [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ],

    "3x1": [
        [1, 1, 1]
    ],

    "1x3": [
        [1],
        [1],
        [1]
    ],

    "4x1": [
        [1, 1, 1, 1]
    ],

    "1x4": [
        [1],
        [1],
        [1],
        [1]
    ],

    "5x1": [
        [1, 1, 1, 1, 1]
    ],

    "1x5": [
        [1],
        [1],
        [1],
        [1],
        [1]
    ],

    "Small Left Corner": [
        [1, 1],
        [1, 0]
    ],

    "Large Left Corner": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0]
    ],

    "Large Right Corner": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],

    "Large Bottom-Left Corner": [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ],

    "Upside-down L": [
        [1, 1],
        [0, 1],
        [0, 1]
    ],

    "Sideways L": [
        [1, 0, 0],
        [1, 1, 1]
    ],

    "Mirrored L": [
        [0, 1],
        [0, 1],
        [1, 1]
    ],

    "Sideways Mirrored L": [
        [0, 0, 1],
        [1, 1, 1]
    ],

    "Upside-down Mirrored L": [
        [1, 1],
        [1, 0],
        [1, 0]
    ],

    "Another L": [
        [1, 1, 1],
        [1, 0, 0]
    ],

    "Yet Another L": [
        [1, 1, 1],
        [0, 0, 1]
    ],

    "T": [
        [1, 1, 1],
        [0, 1, 0]
    ],

    "Upside-down T": [
        [0, 1, 0],
        [1, 1, 1]
    ],

    "Sideways T": [
        [1, 0],
        [1, 1],
        [1, 0]
    ],

    "Mirrored Sideways T": [
        [0, 1],
        [1, 1],
        [0, 1]
    ],

    "S": [
        [0, 1, 1],
        [1, 1, 0]
    ],

    "Sideways S": [
        [1, 0],
        [1, 1],
        [0, 1]
    ],

    "Z": [
        [1, 1, 0],
        [0, 1, 1]
    ],

    "Sideways Z": [
        [0, 1],
        [1, 1],
        [1, 0]
    ],

    "Small Diagonal": [
        [1, 0],
        [0, 1]
    ],

    "1x1": [
        [1]
    ]
}

shape_probabilities = {
    '1x2': 7,
    '2x1': 10,
    '2x2': 49,
    '2x3': 8,
    '3x2': 18,
    '3x3': 40,
    '3x1': 19,
    '1x3': 11,
    '4x1': 12,
    '1x4': 49,
    '5x1': 50,
    '1x5': 14,
    'Small Left Corner': 14,
    'Large Left Corner': 1,
    'Large Right Corner': 31,
    'Large Bottom-Left Corner': 3,
    'Upside-down L': 2,
    'Sideways L': 40,
    'Mirrored L': 2,
    'Sideways Mirrored L': 2,
    'Upside-down Mirrored L': 2,
    'Another L': 2,
    'Yet Another L': 1,
    'T': 2,
    'Upside-down T': 41,
    'Sideways T': 4,
    'Mirrored Sideways T': 1,
    'S': 18,
    'Sideways S': 6,
    'Z': 1,
    'Sideways Z': 1,
    'Small Diagonal': 1,
    '1x1': 1  # Not experimental
}

assert shapes.keys() == shape_probabilities.keys()

shape_names = list(shapes.keys())

# Import fonts
font = pygame.font.Font("assets/fonts/gg sans Semibold.ttf", 90)
font_small = pygame.font.Font("assets/fonts/gg sans Semibold.ttf", 50)
font_bold = pygame.font.Font("assets/fonts/gg sans Bold.ttf", 90)

# Import textures
background = pygame.image.load("assets/textures/Board.png").convert_alpha()
heart = pygame.image.load("assets/textures/Heart.png").convert_alpha()
combo_text = pygame.image.load("assets/textures/Combo.png").convert_alpha()
play_button = pygame.image.load("assets/textures/Play Button.png").convert_alpha()
crown = pygame.image.load("assets/textures/Crown.png")

dark_blue_block = pygame.image.load("assets/textures/blocks/Dark Blue Block.png").convert_alpha()
green_block = pygame.image.load("assets/textures/blocks/Green Block.png").convert_alpha()
light_blue_block = pygame.image.load("assets/textures/blocks/Light Blue Block.png").convert_alpha()
orange_block = pygame.image.load("assets/textures/blocks/Orange Block.png").convert_alpha()
purple_block = pygame.image.load("assets/textures/blocks/Purple Block.png").convert_alpha()
red_block = pygame.image.load("assets/textures/blocks/Red Block.png").convert_alpha()
yellow_block = pygame.image.load("assets/textures/blocks/Yellow Block.png").convert_alpha()

dark_blue_glow = pygame.image.load("assets/textures/glows/Dark Blue Glow.png").convert_alpha()
green_glow = pygame.image.load("assets/textures/glows/Green Glow.png").convert_alpha()
light_blue_glow = pygame.image.load("assets/textures/glows/Light Blue Glow.png").convert_alpha()
orange_glow = pygame.image.load("assets/textures/glows/Orange Glow.png").convert_alpha()
purple_glow = pygame.image.load("assets/textures/glows/Purple Glow.png").convert_alpha()
red_glow = pygame.image.load("assets/textures/glows/Red Glow.png").convert_alpha()
yellow_glow = pygame.image.load("assets/textures/glows/Yellow Glow.png").convert_alpha()

dark_blue_particle = pygame.image.load("assets/textures/particles/Dark Blue Particle.png").convert_alpha()
green_particle = pygame.image.load("assets/textures/particles/Green Particle.png").convert_alpha()
light_blue_particle = pygame.image.load("assets/textures/particles/Light Blue Particle.png").convert_alpha()
orange_particle = pygame.image.load("assets/textures/particles/Orange Particle.png").convert_alpha()
purple_particle = pygame.image.load("assets/textures/particles/Purple Particle.png").convert_alpha()
red_particle = pygame.image.load("assets/textures/particles/Red Particle.png").convert_alpha()
yellow_particle = pygame.image.load("assets/textures/particles/Yellow Particle.png").convert_alpha()

digits = [pygame.image.load(f"assets/textures/numbers/{x}.png") for x in range(10)]

# Game variables
board = [[' ' for _ in range(8)] for _ in range(8)]
ghost_board = [[' ' for _ in range(8)] for _ in range(8)]
colours = ['DB', 'G', 'LB', 'O', 'P', 'R', 'Y']
held_shape = []
held_came_from = 0
pickup_pile = [[' ', ' '] for _ in range(3)]
pickup_offset = pygame.Vector2(0, 0)
score = 0
display_score = 0
total_frames = 0
shapes_clear_frame = 0
moves_since_line_clear = 4
combo = 0
screen_offset = pygame.Vector2(0, 0)
shaking_started_frame = -60
prev_colour = 'R'
game_over = False
game_over_frame = 0
play_button_selected = False


class Particle:
    instances = []

    def __init__(self, centre, colour):
        self.centre = centre
        self.sprite = pygame.transform.smoothscale_by(get_particle(colour), random.uniform(0.5, 1))
        self.rotation = random.randint(0, 360)
        self.rot_direction = random.choice([1, -1]) * random.randint(5, 20)
        self.lifespan = random.randint(10, 20)

        self.vel = pygame.Vector2(0, random.randint(5, 10))
        self.vel = self.vel.rotate(random.randint(0, 360))

        Particle.instances.append(self)

    def update(self):
        self.rotation += self.rot_direction
        self.vel += pygame.Vector2(0, 1)  # Accelerate downwards slightly (like some gravity)
        self.centre += self.vel

        self.lifespan -= 1
        if self.lifespan == 0:
            Particle.instances.remove(self)

    def draw(self):
        # Fade out with time
        opacity = int(min(self.lifespan, 10) / 10 * 255)
        self.sprite.set_alpha(opacity)
        draw_sprite = pygame.transform.rotate(self.sprite, self.rotation)
        screen.blit(draw_sprite, draw_sprite.get_rect(center=self.centre))


class ComboMessage:
    instances = []

    def __init__(self, centre, combo_number):
        self.centre = centre
        self.number = combo_number
        self.frame_created = total_frames

        ComboMessage.instances.append(self)

    def draw(self):
        frames_since_creation = total_frames - self.frame_created
        opacity = 255

        if frames_since_creation > 30:
            scale = 1

            # After 1 second, start fading away
            if frames_since_creation > 60:
                opacity = 255 - (frames_since_creation - 60) * 5

            # Destroy self once completely transparent
            if opacity <= 0:
                ComboMessage.instances.remove(self)
        else:
            # Grow into existance quadratically so that it grows a bit past its final scale
            scale = -11/3750 * frames_since_creation ** 2 + 91/750 * frames_since_creation

        draw_sprite = pygame.transform.smoothscale_by(combo_text, scale)
        draw_sprite.set_alpha(opacity)
        screen.blit(draw_sprite, draw_sprite.get_rect(center=self.centre))

        # Draw the combo number next to it if its >= 2
        if self.number > 1:
            i = 0
            for digit in str(self.number):
                number = digits[int(digit)]
                number = pygame.transform.smoothscale_by(number, scale)
                number.set_alpha(opacity)
                screen.blit(number, number.get_rect(center=(self.centre + pygame.Vector2(90 + i * 40, 5))))
                i += 1


def get_block(colour_id: str):
    if colour_id not in colours and colour_id != "shadow":
        raise ValueError("Invalid colour id")

    if colour_id == 'DB':
        return dark_blue_block
    elif colour_id == 'G':
        return green_block
    elif colour_id == 'LB':
        return light_blue_block
    elif colour_id == 'O':
        return orange_block
    elif colour_id == 'P':
        return purple_block
    elif colour_id == 'R':
        return red_block
    elif colour_id == 'Y':
        return yellow_block
    elif colour_id == "shadow":
        shadow_block = pygame.Surface((70, 70))
        pygame.draw.rect(shadow_block, (10, 10, 10), (1, 1, 68, 68))
        return shadow_block


def get_shape(name: str, colour: str):
    if name not in shape_names:
        raise ValueError("Invalid shape name")

    shape = shapes[name]
    shape_x = len(shape[0])
    shape_y = len(shape)

    shape_surface = pygame.Surface((shape_x * 70, shape_y * 70))
    block = get_block(colour)

    # Go through the shape and draw to the new surface if there is a block there
    for y in range(shape_y):
        for x in range(shape_x):
            if shape[y][x] == 1:
                shape_surface.blit(block, (x * 70, y * 70))

    shape_surface.set_colorkey((0, 0, 0))

    return shape_surface


def get_glow(colour_id: str):
    if colour_id not in colours:
        raise ValueError("Invalid colour id")

    if colour_id == 'DB':
        return dark_blue_glow
    elif colour_id == 'G':
        return green_glow
    elif colour_id == 'LB':
        return light_blue_glow
    elif colour_id == 'O':
        return orange_glow
    elif colour_id == 'P':
        return purple_glow
    elif colour_id == 'R':
        return red_glow
    elif colour_id == 'Y':
        return yellow_glow


def get_particle(colour_id: str):
    if colour_id not in colours:
        raise ValueError("Invalid colour id")

    if colour_id == 'DB':
        return dark_blue_particle
    elif colour_id == 'G':
        return green_particle
    elif colour_id == 'LB':
        return light_blue_particle
    elif colour_id == 'O':
        return orange_particle
    elif colour_id == 'P':
        return purple_particle
    elif colour_id == 'R':
        return red_particle
    elif colour_id == 'Y':
        return yellow_particle


def draw_board():
    # Combine the board and ghost board into one
    combined_board = [[' ' for _ in range(8)] for _ in range(8)]
    for board_y in range(8):
        for board_x in range(8):
            if board[board_y][board_x] != ' ' or ghost_board[board_y][board_x] != ' ':
                combined_board[board_y][board_x] = '_'

    # Check for filled lines in the combined version, i.e. what it will be if this piece gets placed
    remove_rows, remove_cols = find_lines(combined_board)

    for y, row in enumerate(board):
        for x, colour in enumerate(row):
            if colour == ' ':
                continue

            # Turn the whole line into the colour of the held piece if it's about to fill a row
            if held_shape and (x in remove_cols or y in remove_rows):
                colour = held_shape[1]

            block = get_block(colour)
            screen.blit(block, (303 + x * 70, 134 + y * 70))

    # Make (soon to be) filled rows/columns glow
    if held_shape:
        glow = get_glow(held_shape[1])

        for row in remove_rows:
            screen.blit(glow, (281, 112 + 70 * row))

        glow = pygame.transform.rotate(glow, 90)

        for column in remove_cols:
            screen.blit(glow, (281 + 70 * column, 112))


def draw_pickup_area():
    frames_since_clear = total_frames - shapes_clear_frame

    for i, shape in enumerate(pickup_pile):
        name, colour = shape
        if name != ' ' and colour != ' ':
            if frames_since_clear > 10:
                scale_factor = 0.7
                opacity = 255
            else:
                # Make the block grow and become opaque instead of just appearing
                scale_factor = 0.7 * frames_since_clear / 10
                opacity = 255 * frames_since_clear / 10

            # Draw a shadow behind the shape
            shadow = get_shape(name, "shadow")
            shadow = pygame.transform.scale_by(shadow, scale_factor)
            shadow.set_alpha(min(opacity, 100))
            screen.blit(shadow, shadow.get_rect(center=(1105, 205 + i * 200)))

            # Draw the shape
            shape = get_shape(name, colour)
            shape = pygame.transform.smoothscale_by(shape, scale_factor)
            shape.set_alpha(opacity)
            screen.blit(shape, shape.get_rect(center=(1100, 200 + i * 200)))


def fill_pickup_area():
    global pickup_pile, shapes_clear_frame

    if pickup_pile == [[' ', ' '] for _ in range(3)] and not held_shape:  # if pickup_pile and held_shape are empty
        pickup_pile = []

        # Don't have multiple of the same colour in the pickup pile at once
        unused_colours = colours.copy()
        random.shuffle(unused_colours)

        for _ in range(3):
            # Choose a shape accoridng to the predefined distribution
            shape_name = random.choices(shape_names, list(shape_probabilities.values()))[0]
            shape_colour = unused_colours.pop()
            pickup_pile.append([shape_name, shape_colour])

        # Make them grow instead of appearing in draw_pickup_area()
        shapes_clear_frame = total_frames


def draw_held_shape():
    if held_shape:
        shape = get_shape(*held_shape)
        screen.blit(shape, shape.get_rect(center=(pygame.mouse.get_pos() + pickup_offset)))


def pick_up_shape():
    global held_shape, held_came_from, pickup_offset, prev_colour

    for i, shape in enumerate(pickup_pile):
        # Find hitbox of each shape in pickup pile
        if shape == [' ', ' ']:
            continue
        hitbox = get_shape(*shape).get_rect(center=(1100, 200 + i * 200))

        # If clicked on shape, put it in hand
        if hitbox.collidepoint(pygame.mouse.get_pos()):
            held_shape = pickup_pile[i].copy()
            held_came_from = i
            pickup_pile[i] = [' ', ' ']
            pickup_offset = (pygame.Vector2(1100, 200 + i * 200) - pygame.mouse.get_pos()) * 1/0.7
            prev_colour = held_shape[1]
            break


def draw_ghost():
    global ghost_board

    ghost_board = [[' ' for _ in range(8)] for _ in range(8)]

    if not held_shape:
        return

    board_rect = pygame.Rect(303, 134, 560, 560)
    shape_rect = get_shape(*held_shape).get_rect(center=pygame.mouse.get_pos() + pickup_offset)

    for y, row in enumerate(shapes[held_shape[0]]):
        for x, block in enumerate(row):
            if block:
                # For each block in the held shape, find the board grid where the centre is colliding
                centre = shape_rect.topleft + pygame.Vector2(35 + x * 70, 35 + y * 70)
                centre -= board_rect.topleft
                centre //= 70

                # If board coordinates are actually on the board
                if not (0 <= centre.x < 8 and 0 <= centre.y < 8):
                    ghost_board = [[' ' for _ in range(8)] for _ in range(8)]
                    # (if not, don't put any of the shape on the board at all)
                    return
                # And those coordinates are empty
                if not board[int(centre.y)][int(centre.x)] == ' ':
                    ghost_board = [[' ' for _ in range(8)] for _ in range(8)]
                    # (if not, don't put any of the shape on the board at all)
                    return

                # Add the block to the board
                ghost_board[int(centre.y)][int(centre.x)] = held_shape[1]

    # Draw ghost board
    for y, column in enumerate(ghost_board):
        for x, colour in enumerate(column):
            if colour == ' ':
                continue
            block = get_block(colour)
            block.set_alpha(150)
            screen.blit(block, (303 + x * 70, 134 + y * 70))
            block.set_alpha(255)  # Needed because it actually affects the original image's transparency


def place():
    global held_shape, score, moves_since_line_clear, combo

    if ghost_board == [[' ' for _ in range(8)] for _ in range(8)]:
        # Put the piece back where it came from
        if held_shape:
            pickup_pile[held_came_from] = held_shape.copy()
    else:
        # Add to board
        moves_since_line_clear += 1

        for y, row in enumerate(ghost_board):
            for x, colour in enumerate(row):
                if board[y][x] == ' ' and colour != ' ':
                    board[y][x] = colour
                    score += 1

    held_shape = []


def update_cursor():
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if not game_over:
        if held_shape:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return

        # If hovering over a shape in the pickup pile, change cursor to hand
        for i, shape in enumerate(pickup_pile):
            if shape == [' ', ' ']:
                continue
            hitbox = get_shape(*shape).get_rect(center=(1100, 200 + i * 200))
            if hitbox.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        if play_button_selected:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


def find_lines(board):
    remove_rows = []
    remove_cols = []

    # Find rows to remove
    for i, row in enumerate(board):
        if ' ' not in row:
            remove_rows.append(i)

    # Find columns to remove
    rotated_board = list(zip(*board[::-1]))
    for i, column in enumerate(rotated_board):
        if ' ' not in column:
            remove_cols.append(i)

    return remove_rows, remove_cols


def clear_lines():
    global score, moves_since_line_clear, combo, shaking_started_frame

    if moves_since_line_clear >= 3:
        combo = 0

    # Find which lines to clear first
    remove_rows, remove_cols = find_lines(board)

    # If a line was cleared
    if len(remove_rows + remove_cols) != 0:
        # Update combo-realted stuff
        if moves_since_line_clear < 3:
            combo += len(remove_rows + remove_cols) if combo > 1 else 1
            ComboMessage(pygame.mouse.get_pos(), combo)

        # If the whole board is cleared, award 200 points
        if board == [[' ' for _ in range(8)] for _ in range(8)]:
            score += 200

        moves_since_line_clear = 0
        shaking_started_frame = total_frames  # Slight screen shake

    score += 10 * len(remove_rows + remove_cols) * (combo + 1)

    # Remove the rows and columns now; this way allows to clear a row and column simultaneously
    for y, row in enumerate(board):
        for x, block in enumerate(row):
            if x in remove_cols or y in remove_rows:
                board[y][x] = ' '
                Particle(pygame.Vector2(303 + x * 70 + random.randint(0, 70), 134 + y * 70 + random.randint(0, 70)), prev_colour)


def draw_score():
    global display_score

    # Draw the heart behind the score when you have a combo streak going
    if combo > 1:
        scale_factor = 0.1 * math.cos(math.pi / 15 * total_frames) + 1.5
        heart.set_alpha(int(scale_factor/1.6 * 200))
        draw_heart = pygame.transform.smoothscale_by(heart, scale_factor)
        screen.blit(draw_heart, draw_heart.get_rect(center=(WIDTH / 2, 60)))

    # Draw the high score
    screen.blit(crown, (10, 10))
    with open("highscore.txt") as file:
        highscore = file.read()

    highscore_dropshadow = font_small.render(highscore, True, (10, 10, 10))
    highscore_dropshadow.set_alpha(100)
    screen.blit(highscore_dropshadow, (82, 7))

    highscore_text = font_small.render(highscore, True, (250, 181, 16))
    screen.blit(highscore_text, (80, 5))

    # Draw the current score
    score_dropshadow = font.render(str(display_score), True, (10, 10, 10))
    score_dropshadow.set_alpha(180)
    screen.blit(score_dropshadow, score_dropshadow.get_rect(center=(WIDTH / 2 + 2, 60 + 2)))

    score_text = font.render(str(display_score), True, (255, 255, 255))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH / 2, 60)))

    # Increment the displayed score every other frame so that it counts up to your current score
    if score > display_score and total_frames % 2:
        display_score += 1
    elif score == 0:
        display_score = 0


def shake_screen():
    # Shake the screen slightly for 15 frames
    global screen_offset

    shaking_since = total_frames - shaking_started_frame
    if shaking_since > 15:
        return

    screen_offset = pygame.Vector2(0, 1.5).rotate(random.randint(0, 360))


def test_game_over():
    global game_over, game_over_frame

    if held_shape or game_over:
        return

    game_over = True
    game_over_frame = total_frames

    # Loop over every shape left to pick up
    for shape in pickup_pile:
        if shape == [' ', ' ']:
            continue

        shape = shapes[shape[0]]

        shape_width = len(shape[0])
        shape_height = len(shape)

        # Then loop through all possible positions of that shape
        for y in range(9 - shape_height):
            for x in range(9 - shape_width):
                shape_fits = True

                # Then loop through all the blocks in that shape
                for shape_y in range(shape_height):
                    for shape_x in range(shape_width):
                        if shape[shape_y][shape_x]:
                            # And if that block is colliding with one on the board, the shape doesn't fit in this pos
                            if board[y + shape_y][x + shape_x] != ' ':
                                shape_fits = False
                                break

                # If any shape can fit in any position, there is still a valid move
                if shape_fits:
                    game_over = False
                    return


def draw_game_over_screen():
    global play_button_selected

    frames_since_game_over = total_frames - game_over_frame

    if frames_since_game_over > 40 and game_over:
        # Update high score
        with open("highscore.txt", 'r') as file:
            highscore = int(file.read())
        if score > highscore:
            with open("highscore.txt", 'w') as file:
                file.write(str(score))

        gfxdraw.filled_polygon(screen, ((0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)), (0, 0, 0, 150))

        game_over_text = font_bold.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH/2, 200)))

        # Draw replay button
        scale = 1.1 if play_button_selected else 1
        draw_play_button = pygame.transform.smoothscale_by(play_button, scale)
        screen.blit(draw_play_button, draw_play_button.get_rect(center=(WIDTH//2, HEIGHT//2)))

        play_button_selected = False
        if play_button.get_rect(center=(WIDTH//2, HEIGHT//2)).collidepoint(pygame.mouse.get_pos()):
            play_button_selected = True


def reset():
    global game_over, board, score, pickup_pile, moves_since_line_clear, combo

    board = board = [[' ' for _ in range(8)] for _ in range(8)]
    pickup_pile = [[' ', ' '] for _ in range(3)]
    game_over = False
    score = 0
    moves_since_line_clear = -4
    combo = 0


running = True
while running:
    timer.tick(FPS)
    total_frames += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not game_over:
                    pick_up_shape()
                elif play_button_selected:
                    reset()
        elif event.type == pygame.MOUSEBUTTONUP:
            place()

    # Game updates
    fill_pickup_area()
    update_cursor()
    clear_lines()
    [particle.update() for particle in Particle.instances]
    shake_screen()
    test_game_over()

    # Draw everything
    screen.fill((54, 77, 133))
    window.fill((54, 77, 133))
    screen.blit(background, (293, 124))
    draw_pickup_area()
    draw_ghost()
    draw_board()
    draw_score()
    [particle.draw() for particle in Particle.instances]
    [message.draw() for message in ComboMessage.instances]
    draw_held_shape()
    draw_game_over_screen()

    window.blit(screen, screen_offset)
    pygame.display.update()

pygame.quit()
