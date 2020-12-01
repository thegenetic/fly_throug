import pygame
import sys
import random

# pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=6120)
pygame.init()

# Game screen
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()  # controls the frame rate
# adding background image
bground = pygame.image.load('background.png').convert()  # convert() makes things more perfect
# bground = pygame.transform.scale2x(bground)

# TITLE AND LOGO
pygame.display.set_caption("Fly Through")
logo = pygame.image.load('origami.png')
pygame.display.set_icon(logo)

# TEXTS
game_font = pygame.font.Font('04B_19.ttf', 40)

# BASE
base = pygame.image.load('base1.png').convert()
# base = pygame.transform.scale2x(base)  # it fits the image to the game window
floor_x_position = 0


def draw_floor():  # looping the floor
    screen.blit(base, (floor_x_position, 500))
    screen.blit(base, (floor_x_position + 400, 500))
    screen.blit(base, (floor_x_position + 800, 500))


# BIRD
# *********for multiple bird animations*********
bird1 = pygame.image.load('bluebird-upflap.png').convert_alpha()
bird2 = pygame.image.load('bluebird-midflap.png').convert_alpha()
bird3 = pygame.image.load('bluebird-downflap.png').convert_alpha()
bird_frame = [bird1, bird2, bird3]
bird_index = 0
bird = bird_frame[bird_index]
bird_body = bird.get_rect(center=(80, 300))
# wings movement of the bird
ANIMATEBIRD = pygame.USEREVENT
pygame.time.set_timer(ANIMATEBIRD, 5)


def bird_animation():
    new_bird = bird_frame[bird_index]
    new_bird_body = new_bird.get_rect(center=(80, bird_body.centery))
    return new_bird, new_bird_body


# *****this was for a single bird animation******
# bird = pygame.image.load('bluebird-upflap.png').convert_alpha()
# # bird = pygame.transform.scale2x(bird)
# bird_body = bird.get_rect(center=(80, 300))

# bird movement
gravity = 0.1
bird_y_movement = 0


# rotates the bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_y_movement * 8, 1)
    return new_bird


# PIPES
pipe = pygame.image.load('pillar.png').convert()  # adding pipe image
# pipe = pygame.transform.scale2x(pipe)
pipes_list = []  # making mulitple pipes
SPAWNPIPE = pygame.USEREVENT  # for respawning pipes
pygame.time.set_timer(SPAWNPIPE, 1300)  # respwans pipes after 1200 milliseconds\
pipe_height = [200, 250, 300, 350]


def create_pipe():
    height_y = random.choice(pipe_height)
    new_pipebody_bottom = pipe.get_rect(midtop=(550, height_y))
    new_pipebody_up = pipe.get_rect(midbottom=(550, (height_y - 125)))
    return new_pipebody_bottom, new_pipebody_up


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for p in pipes:
        if p.bottom >= 500:
            screen.blit(pipe, p)
        else:
            flip_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(flip_pipe, p)


#  COLLISIONS
def check_collision(pipes):
    for pipe in pipes:
        if bird_body.colliderect(pipe):
            death_sound.play()
            return False
        if bird_body.top <= 0 or bird_body.bottom >= 500:
            death_sound.play()
            return False
    return True


# texts --> scores
score = 0
high_score = 0


def print_score(game_event):
    if game_event == "main game":
        score_surface = game_font.render(f'{int(score)}', True, (255, 255, 255))
        score_body = score_surface.get_rect(center=(250, 50))
        screen.blit(score_surface, score_body)
    if game_event == 'end game':
        score_surface = game_font.render(f'Score : {int(score)}', True, (255, 255, 255))
        score_body = score_surface.get_rect(center=(250, 200))
        screen.blit(score_surface, score_body)

        high_score_surface = game_font.render(f'High Score : {int(high_score)}', True, (255, 255, 255))
        h_s_body = high_score_surface.get_rect(center=(250, 100))
        screen.blit(high_score_surface, h_s_body)


# incrementing high score
def high_score_value(score, highscore):
    if score > highscore:
        highscore = score
    return highscore


# MESSAGE AfTER GAME
message = pygame.image.load('message.png')
message_body = message.get_rect(center=(250, 350))

# GAME VARIABLE
game_status = True

# SOUND
fly_sound = pygame.mixer.Sound('sfx_wing.wav')
point_sound = pygame.mixer.Sound('sfx_point.wav')
death_sound = pygame.mixer.Sound('sfx_hit.wav')
score_sound = 1000
# def sound_point(score_sound):
#     score_sound -= 1
#     if score_sound == 0:
#         point_sound.play()
#         score_sound = 1000
#     else:
#         return None

# game loop
while True:

    # Management of the game screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_status:
                fly_sound.play()
                bird_y_movement = 0
                bird_y_movement -= 3

            if event.key == pygame.K_SPACE and game_status == False:
                game_status = True
                pipes_list.clear()
                bird_body.center = (80, 300)
                bird_y_movement = 0
                score = 0  # for reseting score to zero

        # for the appearance of pipe
        if event.type == SPAWNPIPE:
            # pipes_list.append(create_pipe())  -> this was for one pipe
            pipes_list.extend(create_pipe())  # this is for pipes on the top and bottom (here 'extend' adds tupples)

        #     for bird animation
        if event.type == ANIMATEBIRD:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_body = bird_animation()

    # background image
    screen.blit(bground, (0, 0))

    if game_status:
        # pipes
        pipes_list = move_pipes(pipes_list)
        draw_pipes(pipes_list)

        # bird image
        bird_y_movement += gravity  # adds gravity to the movement
        bird_body.centery += bird_y_movement  # it pulls the bird downward
        screen.blit(rotate_bird(bird), bird_body)  # bird body contains the position of the bird
        # rotate_bird helps in the rotation of the bird
        game_status = check_collision(pipes_list)

        #     score increament
        score += 0.01
        #     SCORE PRINTINGS
        print_score("main game")

        # PLAYING A SOUND AT 10 POINTS
        score_sound -= 1
        if score_sound == 0:
            point_sound.play()
            score_sound = 1000


    else:
        score_sound = 1000
        screen.blit(message, message_body)  # printing message
        high_score = high_score_value(score, high_score)  # printing high score
        print_score("end game")

    # base image
    floor_x_position -= 3
    screen.blit(base, (floor_x_position, 500))
    draw_floor()
    if floor_x_position <= (-400):
        floor_x_position = 0

    pygame.display.update()
    clock.tick(130)  # controls the frame rate
