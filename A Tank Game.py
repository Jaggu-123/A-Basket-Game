import pygame
import random

pygame.init()

Display_width = 800
Display_height =600

black = (0,0,0)
white = (255,255,255)
green = (0,155,0)
blue = (0,0,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((Display_width,Display_height))
pygame.display.set_caption("A Basket Game By Manish")

pygame.display.update()
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms",25)
middlefont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

basket = pygame.image.load("basket.png")
basket = pygame.transform.scale(basket ,(75, 75))

apple = pygame.image.load("apple.png")
apple = pygame.transform.scale(apple, (20, 20))

garden = pygame.image.load("garden.jpg")
garden = pygame.transform.scale(garden, (800, 600))
direction = "right"

def text_objects(msg,color,size):

    if size == "small":
        textSurface = smallfont.render(msg, True, color)
    elif size == "middle":
        textSurface = middlefont.render(msg, True , color)
    elif size == "large":
        textSurface = largefont.render(msg, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace = 0,size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (Display_width/2),(Display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def Score(score):
    text = smallfont.render("Score: "+str(score),True , white)
    gameDisplay.blit(text, [0,0])

def Pause_Screen(score):

    Pause = True

    while Pause:
        gameDisplay.fill(white)
        message_to_screen("Paused", red, -60, size="large")
        message_to_screen("Press p to continue and q to quit", black, 10)
        Score(score)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Pause = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def Start_Screen():

    Start = True

    while Start:

        gameDisplay.fill(white)
        message_to_screen("Welcome to Basket Game", green, -60, size="middle")
        message_to_screen("Press c to play and q to quit", black, 10, size="small")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    Start  = False

def make_apple(Apple_list):

    for i in range(0,len(Apple_list),1):
        Apple_list[i][1] += 3
        gameDisplay.blit(apple,(Apple_list[i][0], Apple_list[i][1]))

def gameLoop():

    gameExit = False
    gameOver = False

    basketX = 350
    basketY = 525
    basket_change = 0
    appleX = 0
    appleY = 0
    FPS = 15
    interval = 0
    Apple_list = []
    New_Apple = []
    New_Apple.append(appleX)
    New_Apple.append(appleY)
    Apple_list.append(New_Apple)
    score = 0
    
    while not gameExit:
        
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("GameOver", green, -50, "large")
            message_to_screen("Press P to Play Again and Q to quit", black, 10, "small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_p:
                        gameLoop()

        New_Apple = []
        if interval == 2*FPS:
            appleX = random.randrange(0,Display_width-20)
            interval = 0
            New_Apple.append(appleX)
            New_Apple.append(appleY)
            Apple_list.append(New_Apple)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    basket_change += -10
                    direction = "left"
                if event.key == pygame.K_RIGHT:
                    basket_change += 10
                    direction = "right"
                if event.key == pygame.K_p:
                    Pause_Screen(score)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    basket_change = 0
                if event.key == pygame.K_RIGHT:
                    basket_change = 0

        if score < 0:
            gameOver = True

        if (basketX >= Display_width-65) and direction == "right":
            basket_change = 0
        elif (basketX < -10) and direction == "left":
            basket_change = 0

        
        
        basketX += basket_change
        interval +=1

        gameDisplay.blit(garden ,(0,0))
        gameDisplay.blit(basket ,(basketX, basketY))
        
        make_apple(Apple_list)

        if Apple_list[0][1] == Display_height-75 and Apple_list[0][0]>=basketX+10 and Apple_list[0][0]<=basketX+65:
            score += 1
            del(Apple_list[0])
        elif Apple_list[0][1] >= Display_height-50:
            del(Apple_list[0])
            score -= 1

        Score(score)
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

Start_Screen()
gameLoop()
