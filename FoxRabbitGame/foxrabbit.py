import pygame
import math

pygame.init()

dimension = [300, 300]
screen = pygame.display.set_mode(dimension)
pygame.display.set_caption("Catch Me If You Can")

foxSheet = pygame.image.load("FoxRabbitGame\\FoxSpriteSheet.png").convert_alpha()
field = pygame.image.load("FoxRabbitGame\\bg.png").convert_alpha()

rabbitSheet = pygame.image.load("FoxRabbitGame\\rabbit.png").convert_alpha()
rabbitSheet = pygame.transform.scale(rabbitSheet, (32, 32))


close = False

#Colores:
BG = '#3C3C3C'
BLACK = '#000000'
def get_image(sheet, x, y, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), (x, y, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)

    return image

frame_right1 = get_image(foxSheet, 6, 16, 20, 16, 2, BLACK)
frame_right2 = get_image(foxSheet, 38, 16, 20, 16, 2, BLACK)
frame_left1 = pygame.transform.flip(frame_right1, True, False).convert_alpha()
frame_left2 = pygame.transform.flip(frame_right2, True, False).convert_alpha()
frame_run_right1 = get_image(foxSheet, 100, 80, 22, 16, 2, BLACK)
frame_run_right2 = get_image(foxSheet, 164, 80, 22, 16, 2, BLACK)
frame_run_left1 = pygame.transform.flip(frame_run_right1, True, False).convert_alpha()
frame_run_left2 = pygame.transform.flip(frame_run_right2, True, False).convert_alpha()

frame_Standing1 = frame_right1
frame_Standing2 = frame_right2
frame_Running1 = frame_run_right1
frame_Running2 = frame_run_right2

clock = pygame.time.Clock()

#Variables para el zorro:
fox = {
    "running": False,
    "breathing": True,
    "stepAltern": True,
    "frameDivider": 0,
    "x": 0,
    "y": 0
}

#Variables para el conejo:
rabbit = {
    "x": 150,
    "y": 150
}
    



while not close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close = True

        if event.type == pygame.KEYDOWN:
            fox["running"] = True
            fox["frameDivider"] = 7
            fox["stepAltern"] = not fox["stepAltern"]
            if event.key == pygame.K_UP and fox["y"]>0:
                fox["y"]-=15 
            if event.key == pygame.K_DOWN and fox["y"]<260:
                fox["y"]+=15
            if event.key == pygame.K_RIGHT and fox["x"]<250:
                frame_Standing1 = frame_right1
                frame_Standing2 = frame_right2
                frame_Running1 = frame_run_right1
                frame_Running2 = frame_run_right2
                fox["x"]+=15
            if event.key == pygame.K_LEFT and fox["x"]>0:
                frame_Standing1 = frame_left1
                frame_Standing2 = frame_left2
                frame_Running1 = frame_run_left1
                frame_Running2 = frame_run_left2
                fox["x"]-=15

            distanceBetween = abs(rabbit["x"]-fox["x"]) + abs(rabbit["y"]-fox["y"])

            if distanceBetween <= 100:
                if rabbit["x"] >= fox["x"] and rabbit["x"] < 250:
                    rabbit["x"]+=20
                elif rabbit["x"] <= fox["x"] and rabbit["x"] > 25:
                    rabbit["x"]-=20
                if rabbit["y"] >= fox["y"] and rabbit["y"] <270:
                    rabbit["y"]+=20
                elif rabbit["y"] <= fox["y"] and rabbit["y"] > 25:
                    rabbit["y"]-=20
                
                if rabbit["x"] >= 250 and rabbit["y"] >= 270:
                    if rabbit["x"] - fox["x"] <= rabbit["y"] - fox["y"]:
                        rabbit["x"] -= 40
                    else :
                        rabbit["y"] -= 40
                if rabbit["x"] <= 25 and rabbit["y"] <= 25:
                    if abs(rabbit["x"] - fox["x"]) <= abs(rabbit["y"] - fox["y"]):
                        rabbit["x"] += 40
                    else :
                        rabbit["y"] += 40
                if rabbit["x"] <= 25 and rabbit["y"] >= 270:
                    if abs(rabbit["x"] - fox["x"]) <= abs(rabbit["y"] - fox["y"]):
                        rabbit["x"] += 40
                    else :
                        rabbit["y"] -= 40
                if rabbit["x"] >=250 and rabbit["y"] <= 25:
                    if abs(rabbit["x"] - fox["x"]) <= abs(rabbit["y"] - fox["y"]):
                        rabbit["x"] -= 40
                    else :
                        rabbit["y"] += 40
                
                    

    

    
    screen.fill('#FFFFFF')
    screen.blit(field, (0,0))
    if not fox["running"]:
        if fox["breathing"]:
            screen.blit(frame_Standing1, (fox["x"], fox["y"]))
        else:
            screen.blit(frame_Standing2, (fox["x"], fox["y"]))
        fox["frameDivider"]+=1
        if fox["frameDivider"] == 15:
            fox["breathing"] = not fox["breathing"]
            fox["frameDivider"] = 0
    else:
        if fox["stepAltern"]:
            screen.blit(frame_Running1, (fox["x"], fox["y"]))
        else :
            screen.blit(frame_Running2, (fox["x"], fox["y"]))
        fox["frameDivider"]+=1
        if fox["frameDivider"] == 15:
            fox["stepAltern"] = not fox["stepAltern"]
            fox["running"] = False
            fox["frameDivider"] = 0

    

    screen.blit(rabbitSheet, (rabbit["x"], rabbit["y"]))
    pygame.display.flip()
    clock.tick(30)


pygame.quit