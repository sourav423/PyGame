import pygame
import random
import math
from pygame import mixer


# initialization

pygame.init()

# set screen

screen = pygame.display.set_mode((800, 600))

# background,caption,icon,music
pygame.display.set_caption("GAME")
background = pygame.image.load('img/background.png')
icon = pygame.image.load('img/air.png')
pygame.display.set_icon(icon)
mixer.music.load('Music/background_music.wav')
mixer.music.play(-1)

# Player
PlayerImg = pygame.image.load('img/jet.png')
playerX = 370
playerY = 455
playerX_change = 0

# Enemy
EnemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_numbers = 10

for i in range(enemy_numbers):
    EnemyImg.append(pygame.image.load('img/alien.png'))
    enemyX.append(random.randint(6, 730))
    enemyY.append(random.randint(10, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(30)

# Bullet
# Ready means you can't see the bullet
# Fire means Bullet currently moving

BulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 455
bulletX_change = 0
bulletY_change = 0.9
bullet_state = "Ready"

# score
Score = 0
font = pygame.font.Font('Fonts/Racing Catalogue.ttf', 32)
textX = 10
textY = 10

# Game Over
game_over_font = pygame.font.Font('Fonts/DF-GameOver.otf', 84)
game_over_textX = 200
game_over_textY = 250


def game_over_text(x, y):
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(game_over_text, (x, y))


def show_Score(x, y):
    Score_Value = font.render("Score : " + str(Score), True, (0, 255, 0))
    screen.blit(Score_Value, (x, y))


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow((x2 - x1), 2)) + (math.pow((y2 - y1), 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop Starts Here
running = True
while running:

    # color of the screen
    screen.fill((37, 150, 190))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check any keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    # fire sound
                    fire_sound = mixer.Sound('Music/laser.wav')
                    fire_sound.play()
                    # Get the current x coordinates of space-ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change

    if playerX <= 6:
        playerX = 6
    elif playerX >= 730:
        playerX = 730

    # enemy movement
    for i in range(enemy_numbers):
        # Game Over
        if enemyY[i] > 370:
            for j in range(enemy_numbers):
                enemyY[j] = 2000
            game_over_text(game_over_textX, game_over_textY)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 6:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('Music/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            Score += 1
            enemyX[i] = random.randint(6, 730)
            enemyY[i] = random.randint(10, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 455
        bullet_state = "Ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_Score(textX, textY)
    pygame.display.update()
