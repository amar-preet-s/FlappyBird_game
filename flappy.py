#FLAPPY BIRD
import pygame
import random
from pygame.locals import*
import time
import sys

#Creating pipes
def create_bottompipe():
    bottom_pipe = pipe_surface[col].get_rect(midtop = (300,pipe_pos))
    return  bottom_pipe

def create_upperpipe():
    upper_pipe = pipe_surface[col].get_rect(midbottom=(300,pipe_pos-110))
    return upper_pipe

#moving pipes
def move_pipe (pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return pipes

#checking for collision
def collision (pipd,pipu):
    global over
    global play
    for pipe1 in pipu:
        if (imagerect.colliderect(pipe1)):
            crsound()
            over = True
            play = False
    for pipe2 in pipd:
        if (imagerect.colliderect(pipe2)):
            crsound()
            over = True
            play = False
    if imagerect.top <= 0 or imagerect.bottom >= 390:
        crsound()
        over = True
        play = False

#dying sound
def crsound():
    sounds['hit'].play()
    sounds['die'].play()
    time.sleep(0.3)
    pygame.mixer.Channel(3).play(sounds['game_over'])

#motion of bird
def animation():
    new_image= image[color][index]
    new_image_rect= new_image.get_rect(center = (100,imagerect.centery))
    return new_image,new_image_rect
        
#rotating a bird
def rotate(bird):
    new_bird = pygame.transform.rotozoom(bird,-movement * 3,1)
    return new_bird

#score for games
def game_score(pipes):
    global score,high_score
    for i in range(len(pipes)):
        if pipes[i].centerx + 26 == imagerect.centerx:
            score +=1
            sounds['point'].play()
        if score > high_score:
            high_score = score

#drawing visuals on the screen
def redraw(pipes2,pipes1):
    if over:
        disp.blit(gameover,(48,156))
        font= pygame.font.Font('freesansbold.ttf',17)
        text=font.render('Press > ENTER < to restart',True,(0,0,0),(255,255,255))
        rect= text.get_rect()
        rect.center = (144,230)
        disp.blit(text,rect)


    if play:
        disp.blit(bg[scene],(xpos,0))
        disp.blit(bg[scene],(xpos+288,0))

        for pipe in pipes2:
            disp.blit(pipe_surface[col],pipe)

        for pipe in pipes1:
            pipup=pygame.transform.rotate(pipe_surface[col],-180)
            disp.blit(pipup,pipe)

        disp.blit(base,(xpos,400))
        disp.blit(base,(xpos+288,400))

        font1= pygame.font.Font('freesansbold.ttf',20)

        text_score= font1.render('Score : '+str(score),True,(0,0,0))
        rect_score=text_score.get_rect()
        rect_score.center = (50,10)
        disp.blit(text_score,rect_score)

        text_highscore = font1.render('Highscore:'+str(high_score),True,(0,0,0))
        rect_highscore = text_highscore.get_rect()
        rect_highscore.center = (223,10)
        disp.blit(text_highscore,rect_highscore)

        disp.blit(rotated_bird,imagerect)

    elif over == False and play==False:
        disp.blit(bg[scene],(0,0))
        disp.blit(image[color][0],imagerect)
        disp.blit(base,(0,400))
        disp.blit(message,(52,40))

    pygame.display.update()
    clock.tick(100)
    
pygame.init()
disp = pygame.display.set_mode((288,512))
pygame.display.set_caption('flappy game')
clock =pygame.time.Clock()

#image loading for the game

bg = {}
bg['1'] = pygame.image.load(r'C:\Users\User\Pictures\b-day.png').convert()
bg['2'] = pygame.image.load(r'C:\Users\User\Pictures\b-night.png').convert()

gameover = pygame.image.load(r'C:\Users\User\Pictures\gameover.png').convert()
base = pygame.image.load(r'C:\Users\User\Pictures\base.png').convert()

image = {}
image['1'] = [pygame.image.load(r'C:\Users\User\Pictures\1.png').convert_alpha(),pygame.image.load(r'C:\Users\User\Pictures\2.png').convert_alpha(),pygame.image.load(r'C:\Users\User\Pictures\3.png').convert_alpha()]
image['2'] = [pygame.image.load(r'C:\Users\User\Pictures\4.png').convert_alpha(),pygame.image.load(r'C:\Users\User\Pictures\5.png').convert_alpha(),pygame.image.load(r'C:\Users\User\Pictures\6.png').convert_alpha()]
image['3'] = [pygame.image.load(r'C:\Users\User\Pictures\7.png').convert_alpha(),pygame.image.load(r'C:\Users\User\Pictures\8.png').convert_alpha(),pygame.image.load(r'C:\Users\User\Pictures\9.png').convert_alpha()]

message = pygame.image.load(r'C:\Users\User\Pictures\message.png')

sounds = {}
if 'win' in sys.platform:
    soundExt = '.wav'
else:
    soundExt = '.ogg'

sounds['die']    = pygame.mixer.Sound(r'C:\Users\User\Pictures\audio\die' + soundExt)
sounds['hit']    = pygame.mixer.Sound(r'C:\Users\User\Pictures\audio\hit' + soundExt)
sounds['point']  = pygame.mixer.Sound(r'C:\Users\User\Pictures\audio\point' + soundExt)
sounds['swoosh'] = pygame.mixer.Sound(r'C:\Users\User\Pictures\audio\swoosh' + soundExt)
sounds['wing']   = pygame.mixer.Sound(r'C:\Users\User\Pictures\audio\wing' + soundExt)
sounds['bgm'] = pygame.mixer.Sound(r'C:\Users\User\Pictures\audio\bgm' + soundExt)
sounds['game_over']   = pygame.mixer.Sound(r'C:\Users\User\Pictures\audio\game_over' + soundExt)



index=0
col = 0
color = '1'
scene = '1'

imagerect = image[color][index].get_rect(center=(100,220))
pipe_surface =[ pygame.image.load(r'C:\Users\User\Pictures\red-pipe.png').convert(),pygame.image.load(r'C:\Users\User\Pictures\green-pipe.png').convert()]

#game variable
pipe_height = 320
pipe_listu = []
pipe_listd = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,2000)
BIRD_TIME = pygame.USEREVENT+1
pygame.time.set_timer(BIRD_TIME,200)

crashed  = False
over = False
play = False

movement  = 0
gravity   = 0.22
xpos      = 0
direction = 0
index= 0
score = 0
high_score = 0
fps = 90
pygame.mixer.Channel(0).play(sounds['bgm'],loops = 100)
while not crashed:

    #selecting pipes position
    pipe_pos = random.randrange(140,pipe_height,1)    
    for event in pygame.event.get():  

        if event.type ==  SPAWNPIPE and over == False:
            pipe_listu.append(create_upperpipe())
            pipe_listd.append(create_bottompipe())

        if event.type == BIRD_TIME and over ==False:
            if index <3:
                index+=1
            if index ==3:
                index=0
            image[color][index],imagerect =animation()
            
        if event.type == pygame.QUIT:
            crashed=True   
        if event.type == pygame.KEYDOWN and play == True :
            if event.key == pygame.K_SPACE :
                pygame.mixer.Channel(1).play(sounds['swoosh'])
                movement =0
                movement = -4
    if play:
        movement+=gravity
        imagerect.centery +=movement

#rotation of bird
        rotated_bird = rotate(image[color][index])

#moves pipe across the screen
        pipe_listd = move_pipe(pipe_listd)     
        pipe_listu = move_pipe(pipe_listu)
        xpos-=1
        game_score(pipe_listd)
        if xpos < -288:
            xpos=0
    redraw(pipe_listd,pipe_listu)
    collision(pipe_listd,pipe_listu)    

#restarting the game
    if over == True:
        pygame.time.set_timer(SPAWNPIPE,2000)
        imagerect.centery = 220
        movement =0
        xpos= 0
        score = 0
        pipe_listu.clear()
        pipe_listd.clear()
        key = pygame.key.get_pressed()
        if key[pygame.K_KP_ENTER] :
            color = str(random.randrange(1,4,1))
            scene = str(random.randrange(1,3,1))
            col = random.randrange(0,2,1)
            over= False	
            time.sleep(0.2)

    elif over == False and play ==  False :
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            play = True
            pipe_listu.clear()
            pipe_listd.clear()
            pygame.time.set_timer(SPAWNPIPE,2000)

pygame.quit()
quit()
