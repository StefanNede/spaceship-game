import pygame
import os
# init the pygame font library so that we can use it when adding text to the window
pygame.font.init()

WIDTH, HEIGHT = 900, 500
# creating the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

# FPS setting
FPS = 60
# the relative velocity (the amount of pixels they move when they press a key)
VEL = 5
# setting the velocity of the bullets
BULLET_VEL = 7
# max bullets that can be fired at one time
MAX_BULLETS = 10

# colours (set in rgb values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

red_health = 20
yellow_health = 20
# line in the middle, arguments are x,y,width,height
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)

# define the font, and then its size
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# importing the image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
# resizing the image with the old variable name, and then the width and height
# doing the same but then rotating it to face the right way
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (55, 40))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (55, 40))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, -90)

SPACE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    # draws the rectangle, arguments to pass are: window name, colour, variable holding the rectangle
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # use blit when you want to add something to the screen
    # first the variable name, and then the position to add it
    # the coordinate system for python is 0,0 at the top left
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def handle_yellow_movement(keys_pressed, yellow):
    # use pygame.K_key to detect what key is pressed
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # down
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # down
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    global red_health, yellow_health
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            red_health -= 1
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            yellow_health -= 1
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    winner_text = ""

    if red_health <= 0:
        winner_text = "Yellow wins!"

    if yellow_health <= 0:
        winner_text = "Red wins!"

    if winner_text != "":
        draw_winner(winner_text)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2-draw_text.get_width() //
                         2, HEIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    # show the winning text for 5 seconds and then restart the game
    pygame.time.delay(5000)


def main():
    # creating rectangles that the user can then move
    # the arguments for these are x,y,width,height
    red = pygame.Rect(700, 200, 55, 40)
    yellow = pygame.Rect(100, 200, 55, 40)
    # to create a bullet we add one to the list, and then draw them at the x and y coordinate
    # that the player was at
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # quitting the main game loop
            if event.type == pygame.QUIT:
                run = False
            # this is a method to see if the person is pressing down a key
            # but it only works for one key at a time, and holding down doesn't work either
            if event.type == pygame.KEYDOWN:
                # checks for right shift for person on the right to shoot, and
                # left shift for person on the left to shoot
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    # when setting the x and y positions, you want the bullet to come from the direct middle of the character
                    red_bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(red_bullet)

                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    # when setting the x and y positions, you want the bullet to come from the direct middle of the character
                    # here we add yellow.width to the x value so that it comes of the right of the ship
                    yellow_bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(yellow_bullet)

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        # this is the other method for getting key presses, and here multiple keys can be pressed
        # and it will work for a person to hold the key down
        # tells us what keys are currently being pressed down
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow,
                       red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    pygame.quit()


if __name__ == '__main__':
    main()
