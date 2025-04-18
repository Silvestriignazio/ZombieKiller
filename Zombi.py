import pygame
import os

os.system("cls")

pygame.init()

MINIMAPPA_LARGHEZZA = 300
MINIMAPPA_ALTEZZA = 250

DizionarioMappe = {
    1: pygame.image.load("mappe/mappa1.png"),
    2: pygame.image.load("mappe/mappa2.png"),
    3: pygame.image.load("mappe/mappa3.png")
}

MiniMappe = {
    1: pygame.transform.scale(DizionarioMappe[1], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
    2: pygame.transform.scale(DizionarioMappe[2], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
    3: pygame.transform.scale(DizionarioMappe[3], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
}

LARGHEZZASCHERMO = 1440
ALTEZZASCHERMO = 796
pygame.display.set_caption('ZOMBI KILLER')
schermo = pygame.display.set_mode((LARGHEZZASCHERMO, ALTEZZASCHERMO))

def CaricaImmagini():
    schermataTitolo = pygame.image.load("immagini/titolo.png")
    SfondoMappe = pygame.image.load("immagini/sfondoMappe.png")
    personaggio = pygame.image.load("immagini/personaggio1.png")
    return schermataTitolo, SfondoMappe, personaggio

def ScegliMappa(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            return DizionarioMappe[1]
        elif event.key == pygame.K_2:
            return DizionarioMappe[2]
        elif event.key == pygame.K_3:
            return DizionarioMappe[3]
    return None

def GestisciSpazio(event, SpazioPremuto):
    if not SpazioPremuto and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        return True
    return SpazioPremuto

def GestisciMovimento(tastiPremuti, x, y, velocita):
    if tastiPremuti[pygame.K_a]:
        x -= velocita
    if tastiPremuti[pygame.K_d]:
        x += velocita
    if tastiPremuti[pygame.K_w]:
        y -= velocita
    if tastiPremuti[pygame.K_s]:
        y += velocita
    return x, y

schermataTitolo, sfondoMappe, personaggio = CaricaImmagini()

mappaCorrente = None
SpazioPremuto = False

posX = 300
posY = 300
velocita = 5

clock = pygame.time.Clock()
gameOver = False

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

        SpazioPremuto = GestisciSpazio(event, SpazioPremuto)

        if SpazioPremuto and mappaCorrente is None:
            scelta = ScegliMappa(event)
            if scelta:
                mappaCorrente = scelta

    if not SpazioPremuto:
        schermo.blit(schermataTitolo, (0, 0))
    elif mappaCorrente is None:
        schermo.blit(sfondoMappe, (0, 0))
        schermo.blit(MiniMappe[1], (100, 400))
        schermo.blit(MiniMappe[2], (580, 400))
        schermo.blit(MiniMappe[3], (1100, 400))
    else:
        schermo.blit(mappaCorrente, (0, 0))
        if mappaCorrente == DizionarioMappe[1]:
            tasti = pygame.key.get_pressed()
            posX, posY = GestisciMovimento(tasti, posX, posY, velocita)
            schermo.blit(personaggio, (posX, posY))
            

    pygame.display.update()
    clock.tick(120)

pygame.quit()
