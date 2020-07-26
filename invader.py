import math
import random

import pygame
from pygame import mixer

# initializing pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('/root/PycharmProjects/SpaceInvader/background.png')

# Background Sound
mixer.music.load('/root/PycharmProjects/SpaceInvader/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Welcome Gaming")
icon = pygame.image.load('/root/PycharmProjects/SpaceInvader/spaceship.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 255))
    screen.blit(over_text, (200, 250))
    score_text = over_font.render("Score is: " + str(score_value), True, (0, 255, 255))
    screen.blit(score_text, (200, 350))


# Player
playerImg = pygame.image.load('/root/PycharmProjects/SpaceInvader/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = list()
enemyX = list()
enemyY = list()
enemyX_change = list()
enemyY_change = list()
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('/root/PycharmProjects/SpaceInvader/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet
# Ready - You can't see the bullet on the screen
# Fire - Bullet is currently moving
bulletImg = pygame.image.load('/root/PycharmProjects/SpaceInvader/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision
def is_collision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + ((math.pow(bulletY - enemyY, 2))))
    if distance < 27:
        return True
    return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # check events
        if event.type == pygame.QUIT:
            # if quit then change running to False
            running = False
        # if keystroke is pressed then check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('/root/PycharmProjects/SpaceInvader/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            # if event.key == pygame.K_UP:
            #     playerY_change = -2
            # if event.key == pygame.K_DOWN:
            #     playerY_change = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # player movement
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # if playerY <= 0:
    #     playerY = 0
    # elif playerY >= 526:
    #     playerY = 526

    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            collision_sound = mixer.Sound('/root/PycharmProjects/SpaceInvader/explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling operations
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
