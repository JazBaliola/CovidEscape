"""
COVID ESCAPE

CREATED BY JAZ BALIOLA

APRIL 05 2021
"""

import pygame
import os
import sys

# INITIALIZE PYGAME
pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
FPS = 60

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(0)
clock = pygame.time.Clock()
game_running = True

""" SETUP GAME TITLE AND GAME ICON """
GAME_TITLE = "Covid Escape" # STORE GAME TITLE AT VARIABLE
pygame.display.set_caption(GAME_TITLE) # SET GAME TITLE
GAME_ICON = pygame.image.load(os.path.join(r'.\assets\player.png')).convert_alpha() # LOAD IMAGE
pygame.display.set_icon(GAME_ICON) # SET IMAGE


""" SETUP GAME BACKGROUND """
bg = pygame.image.load(os.path.join(r'.\assets\bg.png')).convert_alpha() # LOAD IMAGE
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT)) # RESIZE IMAGE

# BG MUSIC
bg_music = pygame.mixer.Sound('./assets/bg.mp3')
pygame.mixer.music.set_volume(0.01) # SET VOLUME OF THE BG MUSIC
pygame.mixer.Sound.play(bg_music) # PLAY BG MUSIC

def create_text(text, text_size, colour, surface, x, y):

    font = pygame.font.Font(r'.\assets\piaxeboy.ttf', text_size) # set font
    text = font.render(text, 1, colour) # create text
    text_to_rect = text.get_rect() # convert text to rect
    text_to_rect.topleft = (x, y) # set position of text
    surface.blit(text, text_to_rect) # draw text on screen



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        """ SETUP PLAYER """
        self.image = pygame.image.load(os.path.join(r'.\assets\player.png')).convert_alpha() # LOAD IMAGE
        self.image = pygame.transform.scale(self.image, (80, 80)) # RESIZE IMAGE
        self.rect = self.image.get_rect()

        self.rect.x = x # PLAYER X POSITION AT START
        self.rect.y = y # PLAYER Y POSITION AT START

        self.move_x = 0

        self.vel_y = 7
        self.jump = False

        self.highscore = 0
        self.score = 0
        self.auto = False

    def show_player(self): # SET POSITION AND SHOW PLAYER FUNCTION
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x ,y):
        super().__init__()
        """ SETUP OBSTACLES """

        self.image = pygame.image.load(os.path.join(r'.\assets\syringe.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        self.OBSTACLE_X_MOVE = 3

    def create_obstacle(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def reset_game(enemy, player):
    """resets the player and enemy position after restarting"""
    enemy.rect.x = 500 
    enemy.rect.y = 575

    player.rect.y = 575
    player.rect.x = 50


enemy = Enemy(500, 575)
enemys = pygame.sprite.Group()
enemys.add(enemy)

player = Player(50, 575)
players = pygame.sprite.Group()
players.add(player)


def gameover():
    while True:
        pygame.mixer.Sound.stop(bg_music)# stop bg music

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # CLICK ENTER KEY TO PLAY AGAIN
                if event.key == pygame.K_RETURN:
                    return # WILL STOP THE WHILE LOOP

        gameover_bg = pygame.image.load(os.path.join(r'./assets/game_over.jpg')).convert_alpha()
        gameover_bg = pygame.transform.scale(gameover_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.mixer.music.stop()

        screen.blit(gameover_bg, (0,0))
        create_text('COVID DIED!', 30, WHITE, screen, SCREEN_WIDTH/2-70, SCREEN_HEIGHT/2-115)
        create_text('Press Enter Key to Play Again', 20, YELLOW, screen, SCREEN_WIDTH/2-115, SCREEN_HEIGHT/2-90)
        create_text('SCORE: ', 20, WHITE, screen, SCREEN_WIDTH/2-40, SCREEN_HEIGHT/2-70)
        create_text(str(player.score), 20, WHITE, screen, SCREEN_WIDTH/2+15, SCREEN_HEIGHT/2-70)

        pygame.display.flip()
        clock.tick(FPS)
    
def Auto(enemy, player):
    if enemy.rect.x == 155:
        player.jump = True
        print('EVENT: AUTO JUMP',player.jump)

def scoring(score, highscore):
    if player.score > player.highscore:
        player.highscore = player.score # set new highscore
        print('UPDATE: SCORE IS GREATER THAN CURRENT HIGHSCORE, SET NEW HIGHSCORE')
    player.score -= player.score #reset score

def add_score(score):
    if player.rect.x > enemy.rect.x:
        player.score += 1

while game_running:
    """
        EVENTS - user interaction effects on the game
    """

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0: # False auto
                print('EVENT: AUTO DISABLED!')
                player.auto = False
            if event.key == pygame.K_1: # True auto
                print('EVENT: AUTO ENABLED!')
                player.auto = True
            if event.key == pygame.K_SPACE:
                if not player.auto:
                    player.jump = True
                    print('EVENT: PLAYER JUMP',player.jump)
                if player.auto:
                    print('EVENT: MANUAL JUMP DISABLED! PLEASE DISABLE AUTO JUMP TO USE MANUAL JUMP')
            


    """
        UPDATE - update objects
    """

    # CHECK IF AUTO IS TRUE 
    if player.auto:
        Auto(enemy, player)

    # NOT MAKE THE PLAYER GET YEETED 
    if player.rect.y >= SCREEN_HEIGHT-175: # not get yeeted from Y postion bottom
        player.rect.y = SCREEN_HEIGHT-175
    if player.rect.x >= SCREEN_WIDTH-80: # not get yeeted from X position right
        player.rect.x = SCREEN_WIDTH-80

    # THE JUMP
    if player.jump:
        player.rect.y -= player.vel_y*7 # CHANGE Y POSITION PLAYER / JUMP
        player.move_x = 10 # CHANGE X POSTION OF PLAYER / MOVE IN FRONT AFTER JUMP
        player.vel_y -= 1 # VELOCITY
        if player.vel_y <= -10: 
            player.move_x *= -.25 # MOVING BACKWARDS X POSTION
            player.jump = False
            player.vel_y = 7
            print('EVENT: PLAYER JUMP',player.jump)

    player.rect.x += player.move_x # UPDATE X PLAYER POSITION
    player.rect.y += player.vel_y # UPDATE Y PLAYER POSITION

    # STOPPING PLAYER MOVE X IF THE PLAYER IS AT IT'S DEFAULT X POSITION
    if player.rect.x  < 50:
        print('UPDATE: STOPPING PLAYER MOVE X')
        player.move_x = 0
        player.rect.x = 50


    enemy.rect.x -= enemy.OBSTACLE_X_MOVE # UPDATE OBSTACLE X POSITION

    if enemy.rect.x <= 0: # REMOVING OBSTACLE WHEN IT'S LESSER THAN OR EQUALS 0
        print('UPDATE: REMOVING OBSTACLE AND CREATING NEW')
        enemy.rect.x = 500


    # CHECK COLLISION
    hit = pygame.sprite.spritecollide(player, enemys, False)
    if len(hit):
        gameover()
        hit.clear()
        reset_game(enemy, player)
        scoring(player.score, player.highscore)

    # ADD SCORE
    add_score(player.score)

    """
        DRAW - what user see on screen
    """
        
    screen.blit(bg, (0, 0))

    create_text('High Score: ', 30, WHITE, screen, 10, 10)
    create_text(str(player.highscore), 30, WHITE, screen, 160, 10)
    create_text('Score:', 30, WHITE, screen, 10, 40)
    create_text(str(player.score), 30, WHITE, screen, 100, 40)
    create_text('Cheat:', 30, WHITE, screen, 10, 70)
    create_text(str(player.auto), 30, WHITE, screen, 90, 70)

    create_text('Created By: Jaz Baliola', 25, WHITE, screen, SCREEN_WIDTH/2-120, SCREEN_HEIGHT-50)

    enemy.create_obstacle()
    player.show_player()

    pygame.display.flip()
    clock.tick(FPS)
