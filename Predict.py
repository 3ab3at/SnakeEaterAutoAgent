"""
Snake Eater
Made with PyGame
Last modification in January 2024 by José Carlos Pulido
Machine Learning Classes - University Carlos III of Madrid
"""

import pygame, sys, time, random
from queue import Queue
from wekaI import Weka

# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = 2500

# Window size
FRAME_SIZE_X = 480
FRAME_SIZE_Y = 480

# Colors (R, G, B)
BLACK = pygame.Color(51, 51, 51)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(204, 51, 0)
GREEN = pygame.Color(204, 255, 153)
BLUE = pygame.Color(0, 51, 102)

# GAME STATE CLASS
class GameState:
    def __init__(self, FRAME_SIZE):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (FRAME_SIZE[0]//10)) * 10, random.randrange(1, (FRAME_SIZE[1]//10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.ticks = 0
        self.correct_pred = 0

# Game Over
def game_over(game, weka):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, WHITE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/4)
    game_window.fill(BLUE)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(game, 0, WHITE, 'times', 20)
    print("Regression model tested on "f"{game.ticks} instances out of which "f"{game.correct_pred} are correct!")
    pygame.display.flip()
    time.sleep(3)
    weka.stop_jvm()
    pygame.quit()
    sys.exit()

# Score
def show_score(game, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(game.score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X/8, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

# MOVE THE SNAKE BY KB
def move_keyboard(game, event):
    # Whenever a key is pressed down
    change_to = game.direction
    if event.type == pygame.KEYDOWN:
        # W -> Up; S -> Down; A -> Left; D -> Right
        if (event.key == pygame.K_UP or event.key == ord('w')) and game.direction != 'DOWN':
            change_to = 'UP'
        if (event.key == pygame.K_DOWN or event.key == ord('s')) and game.direction != 'UP':
            change_to = 'DOWN'
        if (event.key == pygame.K_LEFT or event.key == ord('a')) and game.direction != 'RIGHT':
            change_to = 'LEFT'
        if (event.key == pygame.K_RIGHT or event.key == ord('d')) and game.direction != 'LEFT':
            change_to = 'RIGHT'
    return change_to
    
# PRINTING DATA TO THE ARFF FILE
def print_line_data_arff(game, arff_file, new_score):
    snake_head_x = game.snake_pos[0]
    snake_head_y = game.snake_pos[1]
    food_x = game.food_pos[0]
    food_y = game.food_pos[1]
    current_score = game.score
    current_direction = game.direction
    x_distance = food_x - snake_head_x
    y_distance = food_y - snake_head_y
    arff_file.write(f"{snake_head_x},{snake_head_y},{food_x},{food_y},{x_distance},{y_distance},{current_score},{current_direction},{new_score}\n")

# AUTOMATIC MOVE SNAKE AGENT BASED ON BFS
def move_tutorial_1(game):
    def bfs(game, start, target):
        visited = set()
        queue = Queue()

        queue.put((start, []))

        while not queue.empty():
            current, path = queue.get()
            if current == target:
                return path

            if current in visited:
                continue

            visited.add(current)

            for move in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                next_pos = get_next_position(current, move)
                if is_valid_move(game, next_pos):
                    queue.put((next_pos, path + [move]))

        return []
    def get_next_position(current, move):
        x, y = current
        if move == 'UP':
            return x, y - 10
        elif move == 'DOWN':
            return x, y + 10
        elif move == 'LEFT':
            return x - 10, y
        elif move == 'RIGHT':
            return x + 10, y

    def is_valid_move(game, pos):
        x, y = pos
        return 0 <= x < FRAME_SIZE_X and 0 <= y < FRAME_SIZE_Y and [x, y] not in game.snake_body
    current_head = tuple(game.snake_pos)
    food_position = tuple(game.food_pos)

    path_to_food = bfs(game, current_head, food_position)

    if path_to_food:
        return path_to_food[0]
    else:
        return 'DOWN'
def update_error(game, new_score, a):
    ERROR_RANGE = 7
    game.ticks += 1
    # print("Predicted "f"{a} expected "f"{new_score}\n")
    if (abs(a - new_score) <= ERROR_RANGE):
        game.correct_pred += 1

# Checks for errors encounteRED
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater - Machine Learning (UC3M)')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Main logic
game = GameState((FRAME_SIZE_X,FRAME_SIZE_Y))
weka = Weka()
weka.start_jvm()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            weka.stop_jvm()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        # CALLING MOVE METHOD
        game.direction = move_keyboard(game, event)

    # PREDICT THE NEXT SCORE
    snake_head_x = game.snake_pos[0]
    snake_head_y = game.snake_pos[1]
    food_x = game.food_pos[0]
    food_y = game.food_pos[1]
    current_score = game.score
    x_distance = food_x - snake_head_x
    y_distance = food_y - snake_head_y
    next_dir =  move_tutorial_1(game)
    features = [
        snake_head_x,
        snake_head_y,
        food_x,
        food_y,
        x_distance,
        y_distance,
        current_score,
        next_dir
    ]

    # Snake body growing mechanism
    new_score = 0
    game.snake_body.insert(0, list(game.snake_pos))
    if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
        new_score = game.score + 100
        game.food_spawn = False
    else:
        game.snake_body.pop()
        new_score = game.score - 1

    pred_score = weka.predict('./Predict/LR.model', features, './Predict/score.arff')

    # Update ticks
    update_error(game, new_score, pred_score)

    # Printing ARFF line
    arff_filename = 'score.arff'
    # with open(arff_filename, mode='a', encoding='utf-8') as arff_file:
        # print_line_data_arff(game, arff_file, new_score)

    # Moving the snake
    game.direction = next_dir
    if game.direction == 'UP':
        game.snake_pos[1] -= 10
    if game.direction == 'DOWN':
        game.snake_pos[1] += 10
    if game.direction == 'LEFT':
        game.snake_pos[0] -= 10
    if game.direction == 'RIGHT':
        game.snake_pos[0] += 10

    # Updating the score
    game.score = new_score
    # Spawning food on the screen
    if not game.food_spawn:
        game.food_pos = [random.randrange(1, (FRAME_SIZE_X//10)) * 10, random.randrange(1, (FRAME_SIZE_Y//10)) * 10]
    game.food_spawn = True

    # GFX
    game_window.fill(BLUE)
    for pos in game.snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, RED, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if game.snake_pos[0] < 0 or game.snake_pos[0] > FRAME_SIZE_X-10:
        game_over(game, weka)
    if game.snake_pos[1] < 0 or game.snake_pos[1] > FRAME_SIZE_Y-10:
        game_over(game, weka)
    # Touching the snake body
    for block in game.snake_body[1:]:
        if game.snake_pos[0] == block[0] and game.snake_pos[1] == block[1]:
            game_over(game, weka)

    show_score(game, 1, WHITE, 'consolas', 15)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(DIFFICULTY)