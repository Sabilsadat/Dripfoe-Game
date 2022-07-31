import pygame
import os
from pygame import mixer
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DRIP OR DROWN!")
WHITE =(255,255,255)
BLACK= (0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
BORDER=pygame.Rect(WIDTH//2-5,0, 10, HEIGHT)
FPS=60
VEL=5
BULLETS_VEL=7
MAX_BULLETS=3
BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))
THEME=pygame.mixer.Sound(os.path.join("Assets", "theme.wav"))
YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2

HEALTH_FONT=pygame.font.SysFont("agencyfb",40)
WINNER_FONT=pygame.font.SysFont("perpetua",100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT=200, 200
YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets", "goblin.png"))
YELLOW_SPACESHIP=pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets", "drip.png"))
RED_SPACESHIP=pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
BOMB1=pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bomb1.png")),(40,40))
BOMB2=pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bomb2.png")),(40,40))
BACKGROUND=pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Oscorp_Tower_Building.png")), (WIDTH,HEIGHT))
def draw_window(red,yellow,redbullets,yellowbullets,redhealth,yellowhealth):
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    redhealth_text=HEALTH_FONT.render("Health: "+ str(redhealth), 1, BLACK)
    yellowhealth_text=HEALTH_FONT.render("Health: "+ str(yellowhealth), 1, BLACK)
    WIN.blit(redhealth_text, (WIDTH-redhealth_text.get_width()-10,10))
    WIN.blit(yellowhealth_text, (10,10))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    for bullet in redbullets:
        WIN.blit(BOMB2,bullet)
    for bullet in yellowbullets:
        WIN.blit(BOMB1,bullet)
    pygame.display.update()

def yellow_handlemovement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0:
        yellow.x-=VEL
    if keys_pressed[pygame.K_d] and yellow.x-VEL+yellow.width <BORDER.x:
        yellow.x+=VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL>0:
        yellow.y-=VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height <HEIGHT-15:
        yellow.y+=VEL

def red_handlemovement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x+BORDER.width:
        red.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x-VEL+red.width <WIDTH:
        red.x+=VEL
    if keys_pressed[pygame.K_UP] and red.y-VEL>0:
        red.y-=VEL
    if keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height <HEIGHT-15:
        red.y+=VEL

def handlebullets(yellowbullets,redbullets,yellow,red):
    for bullet in yellowbullets:
        bullet.x+=BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowbullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellowbullets.remove(bullet)
    for bullet in redbullets:
        bullet.x-=BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redbullets.remove(bullet)
        elif bullet.x<0:
            redbullets.remove(bullet)
def draw_winner(text):
    draw_text =WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2, HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
def main():
    THEME.play()
    red =pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow =pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    redbullets=[]
    yellowbullets=[]
    redhealth=10
    yellowhealth=10
    clock=pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(yellowbullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x+yellow.width, yellow.y+yellow.height//2-2, 10, 5)
                    yellowbullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key==pygame.K_RCTRL and len(redbullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x, red.y+red.height//2-2, 10, 5)
                    redbullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type== RED_HIT:
                redhealth-=1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellowhealth-=1
                BULLET_HIT_SOUND.play()
        winner_text=""
        if redhealth<=0:
            winner_text="Goblin Wins!"
        if yellowhealth<=0:
            winner_text="Dripfoe Wins!"
        if winner_text!="":
            draw_winner(winner_text)
            break
        keys_pressed=pygame.key.get_pressed()
        yellow_handlemovement(keys_pressed, yellow)
        red_handlemovement(keys_pressed, red)
        handlebullets(yellowbullets,redbullets,yellow,red)
        draw_window(red, yellow,redbullets,yellowbullets,redhealth,yellowhealth)

    main()
if __name__=="__main__":
    main()