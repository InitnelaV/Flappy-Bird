import pygame
import random
import sys

# --- Initialisation ---
pygame.init()

# --- Constants ---
Width = 800
High = 600
FPS = 60

# Player
Gravity = 0.5
Jump = -10

# Pipes
Width_pipe = 60
Space_pipe = 200
Scrolling_speed = 3

# Music
pygame.mixer.music.load("sound/sound.wav")
pygame.mixer.music.play(-1)  # -1 = loop infini
flap_sound = pygame.mixer.Sound("sound/flap.wav")

# Lives
Lives_max = 3

# --- Pygame setup ---
screen = pygame.display.set_mode((Width, High))
pygame.display.set_caption("Flappy Bird Final")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- Images ---
bg_img = pygame.image.load("tileset/bckgd_day.png").convert()
bg_img = pygame.transform.scale(bg_img, (Width, High))

pipe_down_img = pygame.image.load("tileset/pipe_down.png").convert_alpha()
pipe_down_img = pygame.transform.scale(pipe_down_img, (Width_pipe, High))
pipe_down_img.set_colorkey(pipe_down_img.get_at((0, 0))[:3])

pipe_up_img = pygame.image.load("tileset/pipe_up.png").convert_alpha()
pipe_up_img = pygame.transform.scale(pipe_up_img, (Width_pipe, High))
pipe_up_img.set_colorkey(pipe_up_img.get_at((0, 0))[:3])

floor_img = pygame.image.load("tileset/floor.png").convert_alpha()
floor_img = pygame.transform.scale(floor_img, (Width, floor_img.get_height()))

# Bird animation + echantillonage en pixel (0,0) et transparence
bird_tileset = pygame.image.load("tileset/bird_animation.png").convert_alpha()
sample_key = bird_tileset.get_at((0, 0))[:3]
bird_tileset.set_colorkey(sample_key)

frame_width = bird_tileset.get_width() // 3
frame_height = bird_tileset.get_height()
desired_bird_size = (40, 40)

bird_frames = []
for i in range(3):
    frame = bird_tileset.subsurface((i * frame_width, 0, frame_width, frame_height)).copy()
    frame = pygame.transform.scale(frame, desired_bird_size)
    frame.set_colorkey(sample_key)
    bird_frames.append(frame)


def append_pipe(pipes):
    top_h = random.randint(80, High - Space_pipe - 100)
    x = Width + 100
    pipes.append({"x": x, "top_h": top_h, "scored": False})


def game_loop():
    # Variables du jeu
    player_x = 80
    Player_y = High // 2
    speed_y = 0
    Lives = Lives_max
    score = 0
    bird_frame_index = 0
    bird_anim_counter = 0
    bird_anim_speed = 5
    floor_x = 0

    # Pipes
    pipes = []
    for i in range(3):
        append_pipe(pipes)
        pipes[-1]["x"] += i * 400

    running = True
    while running:
        clock.tick(FPS)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Controls ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            speed_y = Jump
            flap_sound.play()

        # --- Physics ---
        speed_y += Gravity
        Player_y += speed_y

        # --- Animation Bird ---
        bird_anim_counter += 1
        if bird_anim_counter >= bird_anim_speed:
            bird_anim_counter = 0
            bird_frame_index = (bird_frame_index + 1) % len(bird_frames)

        current_bird_frame = bird_frames[bird_frame_index]
        angle = max(min(-speed_y * 3, 45), -45)
        rotated_bird = pygame.transform.rotate(current_bird_frame, angle)
        rotated_bird.set_colorkey(sample_key)
        player_rect = rotated_bird.get_rect(topleft=(player_x, Player_y))

        # --- Draw background ---
        screen.blit(bg_img, (0, 0))

        # --- Pipes ---
        for pipe in pipes:
            pipe["x"] -= Scrolling_speed
            x = pipe["x"]
            top_h = pipe["top_h"]

            screen.blit(pipe_up_img, (x, top_h - pipe_up_img.get_height()))
            screen.blit(pipe_down_img, (x, top_h + Space_pipe))

            pipe_up_rect = pygame.Rect(x, 0, Width_pipe, top_h)
            pipe_down_rect = pygame.Rect(x, top_h + Space_pipe, Width_pipe, High - (top_h + Space_pipe))

            if player_rect.colliderect(pipe_up_rect) or player_rect.colliderect(pipe_down_rect):
                Lives -= 1
                speed_y = 0
                Player_y = High // 2
                bird_frame_index = 0
                if Lives <= 0:
                    running = False
                player_x = 80

            if not pipe["scored"] and (x + Width_pipe) < player_x:
                score += 10
                pipe["scored"] = True

        pipes = [p for p in pipes if p["x"] > -Width_pipe]
        while len(pipes) < 3:
            append_pipe(pipes)

        # --- Bird ---
        screen.blit(rotated_bird, (player_x, Player_y))

        # --- Floor ---
        floor_x -= Scrolling_speed
        if floor_x <= -floor_img.get_width():
            floor_x = 0
        screen.blit(floor_img, (floor_x, High - floor_img.get_height()))
        screen.blit(floor_img, (floor_x + floor_img.get_width(), High - floor_img.get_height()))

        # --- Borders ---
        if Player_y + rotated_bird.get_height() >= High - floor_img.get_height():
            running = False

        # --- Score & Lives ---
        texte_score = font.render(f"Score : {score}", True, (255, 255, 255))
        texte_vies = font.render(f"Lives : {Lives}", True, (255, 255, 255))
        screen.blit(texte_score, (10, 10))
        screen.blit(texte_vies, (10, 50))

        pygame.display.flip()

    return score


def game_over_menu(score):
    while True:
        screen.blit(bg_img, (0, 0))
        message = font.render("Game Over", True, (255, 255, 255))
        score_final = font.render(f"Final Score : {score}", True, (255, 255, 255))
        retry_text = font.render("Press R to Try Again", True, (0, 255, 0))
        quit_text = font.render("Press Q to Quit", True, (255, 0, 0))

        screen.blit(message, (Width // 2 - 80, High // 2 - 60))
        screen.blit(score_final, (Width // 2 - 100, High // 2 - 20))
        screen.blit(retry_text, (Width // 2 - 120, High // 2 + 40))
        screen.blit(quit_text, (Width // 2 - 100, High // 2 + 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # relancer le jeux
                    return True
                elif event.key == pygame.K_q:  # quitter et fermer
                    return False


# --- Boucle principale ---
while True:
    final_score = game_loop()
    retry = game_over_menu(final_score)
    if not retry:
        break

pygame.quit()
sys.exit()
