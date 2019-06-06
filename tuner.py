from threading import Thread
import pygame

#importuje queue i ,maina'
from recognizer import q, get_note




pygame.init()
pygame.display.set_caption('Guitar Tuner')
screenWidth, screenHeight = 300, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

running = True

titleFont = pygame.font.SysFont("comicsansms", 34)
titleText = titleFont.render("Note name:", True, (0, 128, 0))
noteFont = pygame.font.SysFont("comicsansms", 55)

#watek zeby rozpoznawiaine dzialalo w tle
t = Thread(target=get_note)
t.daemon = True
t.start()

def tuner():
    screen.fill((0, 0, 0))

    pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
    pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290),(screenWidth - 10, 310))
    pygame.draw.line(screen, (255, 255, 255), (screenWidth/2 - 10, 290),(screenWidth/2 - 10, 310))
    pygame.draw.line(screen, (255, 255, 255), (10, 300),(screenWidth - 10, 300))

    if not q.empty():
        b = q.get()
	if b['Cents'] < 15:
            pygame.draw.circle(screen, (0, 128, 0), 
                               (screenWidth // 2 + (int(b['Cents']) * 2),300),
                               10)
	else:
            pygame.draw.circle(screen, (128, 0, 0),
                               (screenWidth // 2 + (int(b['Cents']) * 2), 300),
                               10)

	noteText = noteFont.render(b['Note'], True, (0, 128, 0))
    else:
	noteText = noteFont.render('---', True, (0, 128, 0))
	
    screen.blit(noteText, (160, 80))
    screen.blit(titleText, (10,  80))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

    tuner()
    
    pygame.display.flip()
    clock.tick(30)

