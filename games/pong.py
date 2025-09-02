# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

paddle_height = 200
half_ph = paddle_height // 2
ball_radius = 15
bpm_height = 2
max_speed = 20
speed_factor = 1.0005


player_pos = pygame.Vector2(30, screen.get_height() / 2)

bot_pos = pygame.Vector2(screen.get_width() - 30, screen.get_height() / 2)

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

ball_pos_mov = [4,0]

score = [0,0]

# setup once, after pygame.init()
font = pygame.font.SysFont(None, 72)  # None = default font, 72 = size


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", ball_pos, ball_radius)
    pygame.draw.line(screen, "grey",(player_pos.x, player_pos.y - half_ph),(player_pos.x, player_pos.y + half_ph),width=1)
    pygame.draw.line(screen, "grey",(bot_pos.x, bot_pos.y - half_ph),(bot_pos.x, bot_pos.y + half_ph),width=1)
    # render score texts
    score_text_left = font.render(str(score[0]), True, "white")
    score_text_right = font.render(str(score[1]), True, "white")

    # blit to screen (centered near top)
    screen.blit(score_text_left, (screen.get_width()/4 - score_text_left.get_width()/2, 20))
    screen.blit(score_text_right, (3*screen.get_width()/4 - score_text_right.get_width()/2, 20))



    bot_pos.y = ball_pos.y

    keys = pygame.key.get_pressed()

    # player paddle
    if ball_pos.x - ball_radius <= player_pos.x and player_pos.y-half_ph < ball_pos.y < player_pos.y+half_ph:
        ball_pos_mov[0] = -ball_pos_mov[0]
        if ball_pos.y > player_pos.y+30: ball_pos_mov[1] = bpm_height
        if ball_pos.y < player_pos.y-30: ball_pos_mov[1] = -bpm_height

    # bot paddle
    if ball_pos.x + ball_radius >= bot_pos.x and bot_pos.y-half_ph < ball_pos.y < bot_pos.y+half_ph:
        ball_pos_mov[0] = -ball_pos_mov[0]
        if ball_pos.y > bot_pos.y+30: ball_pos_mov[1] = bpm_height
        if ball_pos.y < bot_pos.y-30: ball_pos_mov[1] = -bpm_height


    if abs(ball_pos_mov[0]) < max_speed:
        ball_pos_mov[0] *= speed_factor

    ball_pos.x += ball_pos_mov[0] 
    ball_pos.y += ball_pos_mov[1]

    if ball_pos.y + ball_radius >= screen.get_height():
        ball_pos_mov[1] = -bpm_height
    if ball_pos.y - ball_radius <= 0:
        ball_pos_mov[1] = bpm_height

    if ball_pos.x + ball_radius >= screen.get_width():
        score[0] += 1
        ball_pos.x = screen.get_width() / 2
        ball_pos.y = screen.get_height() / 2
        ball_pos_mov[0] = 4
        ball_pos_mov[1] = 0
    
    if ball_pos.x - ball_radius <= 0:
        score[1] += 1
        ball_pos.x = screen.get_width() / 2
        ball_pos.y = screen.get_height() / 2
        ball_pos_mov[0] = -4
        ball_pos_mov[1] = 0


    if keys[pygame.K_w]:
        if player_pos.y - 100>0:
            player_pos.y -= screen.get_width()//2 * dt
    if keys[pygame.K_s]:
        if player_pos.y + 100<(screen.get_height()):
            player_pos.y += screen.get_width()//2 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(120) / 1000

pygame.quit()