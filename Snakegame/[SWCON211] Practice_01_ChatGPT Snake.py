import pygame
import time
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180) 

# Food colors based on operator
LIME = (198, 255, 0)       # +
ORANGE_RED = (255, 61, 0)  # -
AQUA = (0, 229, 255)      # *
PINK = (255, 64, 129)      # /

# Snake properties
snake_pos = [WIDTH // 2, HEIGHT // 2]
initial_length = 3
snake_body = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2 - 10, HEIGHT // 2], [WIDTH // 2 - 20, HEIGHT // 2]]

# Food properties
food_pos = []
food_operators = ['+', '-', '*', '/']
food_spawn_count = 2

# Font for food text
font = pygame.font.SysFont('comicsans', 20)

# Direction
direction = 'RIGHT'
change_to = direction

# Initial frame rate
framerate = 15

# Score
score = 0

# Load sounds
try:
    sound_background = pygame.mixer.Sound('background.mp3')
    sound_death = pygame.mixer.Sound('death.mp3')
    sound_downgrade = pygame.mixer.Sound('downgrade.mp3')
    sound_upgrade = pygame.mixer.Sound('upgrade.mp3')
    sound_eat = pygame.mixer.Sound('eat.mp3')
    sound_scoreboard = pygame.mixer.Sound('scoreboard.mp3')
except pygame.error as e:
    print(f"Failed to load audio files. Please make sure they are in the same directory: {e}")
    sound_background = sound_death = sound_downgrade = sound_upgrade = sound_eat = sound_scoreboard = None

# Functions
def Your_score(score):
    value = pygame.font.SysFont('comicsans', 30).render("Your Score: " + str(score), True, WHITE)
    window.blit(value, [0, 0])

def Your_length(length):
    value = pygame.font.SysFont('comicsans', 30).render("Length: " + str(length), True, WHITE)
    window.blit(value, [0, 30])

def message(msg, color, y_displace=0, size=25):
    mesg = pygame.font.SysFont('comicsans', size).render(msg, True, color)
    text_rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_displace))
    window.blit(mesg, text_rect)

def spawn_food():
    global food_pos
    food_pos = []
    while len(food_pos) < food_spawn_count:
        new_food = {
            'pos': [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10],
            'operator': random.choice(food_operators),
            'value': random.randrange(1, 6)
        }
        food_pos.append(new_food)

def draw_food():
    operator_colors = {
        '+': LIME,
        '-': ORANGE_RED,
        '*': AQUA,
        '/': PINK
    }
    for food in food_pos:
        color = operator_colors.get(food['operator'], BLACK)
        pygame.draw.rect(window, color, pygame.Rect(food['pos'][0], food['pos'][1], 10, 10))
        food_text = font.render(f"{food['operator']}{food['value']}", True, WHITE)
        text_rect = food_text.get_rect(center=(food['pos'][0] + 5, food['pos'][1] + 5))
        window.blit(food_text, text_rect)

def get_snake_color(length):
    if 1 <= length <= 9: return GREEN
    elif 10 <= length <= 49: return (0, 0, 255)
    elif 50 <= length <= 99: return (255, 0, 0)
    elif 100 <= length <= 149: return (128, 0, 128)
    elif 150 <= length <= 199: return (255, 255, 0)
    elif 200 <= length <= 499: return (139, 69, 19)
    elif 500 <= length <= 999: return (255, 165, 0)
    else: return WHITE

# Initial food spawn
spawn_food()

# Main Function
def gameLoop():
    global direction, change_to
    global snake_pos, snake_body
    global food_pos
    global score, framerate

    game_over = False
    game_close = False

    if sound_background:
        sound_background.play(-1)

    has_played_scoreboard_sound = False

    while not game_over:
        while game_close == True:
            if not has_played_scoreboard_sound and sound_scoreboard:
                if pygame.mixer.get_busy():
                    sound_background.stop()
                sound_scoreboard.play() # 사운드를 한 번만 재생
                has_played_scoreboard_sound = True

            window.fill(BLACK)
            Your_score(score)
            message("You Lost!", (255, 0, 0), -50, 40)
            message("Press 'R' to Restart or 'Q' to Quit", GRAY, 50, 25)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                        if pygame.mixer.get_busy():
                            sound_scoreboard.stop()
                    if event.key == pygame.K_r:
                        if pygame.mixer.get_busy():
                            sound_scoreboard.stop()
                        snake_pos = [WIDTH // 2, HEIGHT // 2]
                        snake_body = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2 - 10, HEIGHT // 2], [WIDTH // 2 - 20, HEIGHT // 2]]
                        spawn_food()
                        direction = 'RIGHT'
                        change_to = direction
                        framerate = 15
                        score = 0
                        game_close = False
                        has_played_scoreboard_sound = False
                        if sound_background:
                            sound_background.play(-1)
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                    if pygame.mixer.get_busy():
                        sound_scoreboard.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        elif change_to == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'
        elif change_to == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        elif change_to == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP': snake_pos[1] -= 10
        elif direction == 'DOWN': snake_pos[1] += 10
        elif direction == 'LEFT': snake_pos[0] -= 10
        elif direction == 'RIGHT': snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))

        food_eaten = False
        for food in food_pos:
            if snake_pos[0] == food['pos'][0] and snake_pos[1] == food['pos'][1]:
                food_eaten = True
                
                current_length = len(snake_body)
                
                if sound_eat: sound_eat.play()
                
                new_length = current_length
                if food['operator'] == '+': new_length = current_length + food['value']
                elif food['operator'] == '-': new_length = current_length - food['value']
                elif food['operator'] == '*': new_length = current_length * food['value']
                elif food['operator'] == '/':
                    if food['value'] == 0: new_length = current_length
                    else: new_length = current_length / food['value']
                
                new_length = int(new_length + 0.5)
                
                if new_length > current_length and sound_upgrade:
                    sound_upgrade.play()
                elif new_length < current_length and sound_downgrade:
                    sound_downgrade.play()
                
                if new_length <= 0:
                    if sound_death: sound_death.play()
                    game_close = True
                    break

                if new_length > current_length:
                    for _ in range(new_length - current_length):
                        snake_body.append(snake_body[-1])
                elif new_length < current_length:
                    del snake_body[new_length:]
                
                spawn_food()
                break
        
        if not food_eaten:
            snake_body.pop()

        window.fill(BLACK)
        
        current_snake_color = get_snake_color(len(snake_body))

        if len(snake_body) > 0:
            for pos in snake_body:
                pygame.draw.rect(window, current_snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
        else:
            game_close = True
            if sound_death: sound_death.play()

        draw_food()
        Your_score(score)
        Your_length(len(snake_body))

        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10:
            game_close = True
            if sound_death: sound_death.play()
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            game_close = True
            if sound_death: sound_death.play()

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_close = True
                if sound_death: sound_death.play()

        pygame.display.update()
        pygame.time.Clock().tick(framerate)

    pygame.quit()
    quit()

# Run the game
gameLoop()