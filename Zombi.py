import pygame


pygame.init()
LARGHEZZASCHERMO = 1440
ALTEZZASCHERMO = 800
pygame.display.set_caption('ZOMBI KILLER')
schermo = pygame.display.set_mode((LARGHEZZASCHERMO, ALTEZZASCHERMO))

def CaricaImmagini():
    sfondo = pygame.image.load("mappe\mappa1.png")
    return sfondo

def StampaImmagini(sfondo):
    schermo.blit(sfondo, (0,0))



sfondo = CaricaImmagini()
# sfondo = StampaImmagini(sfondo)


clock = pygame.time.Clock()
gameOver = False
while not gameOver:



    StampaImmagini(sfondo)
    pygame.display.update()
    clock.tick(120)

pygame.quit() 