import math
import pygame
import random

#Initialize pygame to access all it's methods
pygame.init()
over= False
#Creating a screen/ window
screen = pygame.display.set_mode((800,600))

"""Anything happening within our game window is called an event"""

#Title and Icon
pygame.display.set_caption("Shoot the Board")
ic= pygame.image.load('man.png')
pygame.display.set_icon(ic)

#Background  Image
bg = pygame.image.load("bgShoot.png")

#Player
playerIcon= pygame.image.load('police.png')
playerX=40
playerY=250
playerY_change=0

#Score
scoreVal=0
font= pygame.font.Font('freesansbold.ttf',32)
textX,textY=10,10

def showScore(x,y):
    score= font.render("Score:"+ str(scoreVal),True,(0,0,0))
    screen.blit(score,(x,y))

#Game over text
overFont= pygame.font.Font('freesansbold.ttf',64)
def gameOverTxt():
    overText= overFont.render("GAME OVER",True,(0,0,0))
    screen.blit(overText,(200,250))

def player(x,y):
    screen.blit(playerIcon, (x,y))# Drawing the player image on the screen

#Enemy
EnIcon=[]
EnX=[]
EnY=[]
EnY_change=[]
EnX_change=[]
noOfEn=10
for i in range(noOfEn):
    EnIcon.append(pygame.image.load('boardEnemy.png'))
    EnX.append(random.randint(600,750)) #getting random position of the enemy
    EnY.append(random.randint(0,540))
    EnY_change.append(3)
    EnX_change.append(-20)

def enemy(x,y,i):
    screen.blit(EnIcon[i], (x,y))# Drawing the player image on the screen

#Bullet
BuIcon= pygame.image.load('bullet.png')
BuX= 40 #getting random position of the enemy
BuY= 0
BuY_change= 0
BuX_change= 2
Bu_state ="noFire"

def fire_bullet(x,y):
    global Bu_state
    Bu_state = "Fire"
    screen.blit(BuIcon, (x+45,y-4))

#Collision detection
def isCollision(EnX,EnY,BuX,BuY):
    #euclidian distance between bullet and enemy board
    dist= math.sqrt(math.pow(EnX-BuX,2)+math.pow(EnY-BuY,2))
    if dist<27:
        return True
    return False

#Game loop
running= True
while running:
    screen.fill((255,255,255)) #background color
    screen.blit(bg, (0,0))

    #Looping through all the events to check if any event was performed
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running= False

        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_UP:
                playerY_change= -4
            if event.key== pygame.K_DOWN:
                playerY_change= 4
            if event.key== pygame.K_SPACE:
                if Bu_state is "noFire":
                    BuY= playerY
                    fire_bullet(BuX,BuY)
        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_UP or event.key== pygame.K_DOWN:
                playerY_change=0
    
    playerY += playerY_change
    # Creating boundaries for the player
    if playerY<=0:
        playerY=0
    elif playerY>=536:
        playerY=536

    #Enemy Movement
    for i in range(noOfEn):
        #Game Over
        if EnX[i]<100:
            over=True
            for j in range(noOfEn):
                EnX[j]= 2000            
            break

        EnY[i] += EnY_change[i]
        # Creating boundaries for the enemy board
        if EnY[i]<=0:
            EnY_change[i]=3
            EnX[i]+= EnX_change[i]
        elif EnY[i]>=536:
            EnY_change[i]= -3
            EnX[i]+= EnX_change[i]
        #Collision
        collision = isCollision(EnX[i], EnY[i], BuX,BuY)
        if collision:
            BuX= 40
            Bu_state= "noFire"
            scoreVal+=3
            
            EnX[i]= random.randint(600,750) #getting random position of the enemy
            EnY[i]=random.randint(0,540)
        enemy(EnX[i], EnY[i],i)

    #BulletMoverment
    if BuX>=800:
        BuX= 40
        Bu_state="noFire"

    if Bu_state is "Fire":
        fire_bullet(BuX,BuY)
        BuX+= BuX_change

    if over==True:
        gameOverTxt()

    player(playerX,playerY)
    showScore(textX,textY)
    pygame.display.update() #update the display of your screen after 
            