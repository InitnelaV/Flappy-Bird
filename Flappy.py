import pygame
import random
import sys

# Initialisation
pygame.init()

# Constants
Width = 800
High = 600
FPS = 60

# Color
Backgd = (0, 0, 0)
Bird = (255, 255, 0)
High_pipe = (0, 255, 0)
Low_pipe = (0, 255, 0)
Score_life = (255, 255, 255)

# Player
Bird_size = 30
Gravity = 0.5
Jump = -10

# Pipes
Width_pipe = 60
Space_pipe = 200
Scrolling_speed = 3

# Lives
Lives_max = 3

# Pygame setup
screen = pygame.display.set_mode((Width, High))
pygame.display.set_caption("Flappy Square")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Player
player_x = 80
Player_y = High // 2
speed_y = 0
Lives = Lives_max
score = 0

# Pipes : list of tuples (x, height_high)
pipes = []

def append_pipe():
    Height_High = random.randint(50, High - Space_pipe - 50)
    x = Width + 100
    pipes.append([x, Height_High])


# Pipes init
for i in range(3):
    append_pipe()
    pipes[-1][0] += i * 200

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(Backgd)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        speed_y = Jump

    # Jump mechanics
    speed_y += Gravity
    Player_y += speed_y

    player_rect = pygame.Rect(player_x, Player_y, Bird_size, Bird_size)
    pygame.draw.rect(screen, Bird, player_rect)

    # Pipes : list of tuples (x, height_high)
    pipes_to_delte = []
    for i, pipe in enumerate(pipes):
        x = pipe[0]
        height_high = pipe[1]
        x -= Scrolling_speed
        pipes[i][0] = x  # Updated pipe position

        # High pipe
        pipe_high = pygame.Rect(x, 0, Width_pipe, height_high)
        pygame.draw.rect(screen, High_pipe, pipe_high)

        # Low pipe
        pipe_low = pygame.Rect(x, height_high + Space_pipe, Width_pipe, High - (height_high + Space_pipe))
        pygame.draw.rect(screen, High_pipe, pipe_low)

        # Collision
        if player_rect.colliderect(pipe_high) or player_rect.colliderect(pipe_low):
            Lives -= 1
            speed_y = 0
            Player_y = High // 2
            if Lives <= 0:
                running = False

        # Score
        if x + Width_pipe < player_x and 'score' not in pipe:
            score += 10
            pipes[i].append('score')  # Marque le pipe comme "déjà compté"

    # Filtering  pipes out of the screen
    pipes = [pipe for pipe in pipes if pipe[0] > -Width_pipe]

    # Appen pipe (if necessary)
    if len(pipes) < 3:
        append_pipe()

    # delete pipe (exit from the screen)
    for pipe in pipes_to_delte:
        pipes.remove(pipe)


        # Collision
        if player_rect.colliderect(pipe_high) or player_rect.colliderect(pipe_low):
            Lives -= 1
            speed_y = 0
            Player_y = High // 2
            if Lives <= 0:
                running = False

        # Score
        if x + Width_pipe < player_x and not pipes[i].__contains__('score'):
            score += 10
            pipes[i].append('score')  # Marque le pipe comme "déjà compté"

        # delete pipe exit from the screen (action to do)
        if x < -Width_pipe:
            pipes_to_delte.append(pipes[i])

    for t in pipes_to_delte:
        pipes.remove(t)
        append_pipe()

    # Floor to ceiling
    if Player_y > High or Player_y < 0:
        Lives -= 1
        speed_y = 0
        Player_y = High // 2
        if Lives <= 0:
            running = False

    # Dsiplay score et Lives
    texte_score = font.render(f"Score : {score}", True, Score_life)
    texte_vies = font.render(f"Lives : {Lives}", True, Score_life)
    screen.blit(texte_score, (10, 10))
    screen.blit(texte_vies, (10, 50))

    pygame.display.flip()

# Game Over
screen.fill(Backgd)
message = font.render("Game Over", True, Score_life)
score_final = font.render(f"Final Score : {score}", True, Score_life)
screen.blit(message, (Width // 2 - 80, High // 2 - 30))
screen.blit(score_final, (Width // 2 - 100, High // 2 + 10))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
sys.exit()
