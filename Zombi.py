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
    personaggio_dx = pygame.image.load("immagini/personaggio_dx.png")  
    personaggio_sx = pygame.image.load("immagini/personaggio_sx.png")  
    personaggio_up = pygame.image.load("immagini/personaggio_up.png")  
    personaggio_down = pygame.image.load("immagini/personaggio_down.png")  
    return schermataTitolo, SfondoMappe, personaggio_dx, personaggio_sx, personaggio_up, personaggio_down

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
    direzione = None
    if tastiPremuti[pygame.K_a] and x > 0:  
        x -= velocita
        direzione = "sx"
    if tastiPremuti[pygame.K_d] and x < LARGHEZZASCHERMO - personaggio_dx.get_width(): 
        x += velocita
        direzione = "dx"
    if tastiPremuti[pygame.K_w] and y > 0:  
        y -= velocita
        direzione = "up"
    if tastiPremuti[pygame.K_s] and y < ALTEZZASCHERMO - personaggio_dx.get_height(): 
        y += velocita
        direzione = "down"
    return x, y, direzione

def SparaProiettile(x, y, direzione):
    
    proiettili.append({"rect": pygame.Rect(x + personaggio_dx.get_width() // 2, y + personaggio_dx.get_height() // 2, 10, 5), "direzione": direzione})

def GestisciProiettili(proiettili, velocita_proiettile):
    
    for proiettile in proiettili[:]:
        if proiettile["direzione"] == "dx":
            proiettile["rect"].x += velocita_proiettile
        elif proiettile["direzione"] == "sx":
            proiettile["rect"].x -= velocita_proiettile
        elif proiettile["direzione"] == "up":
            proiettile["rect"].y -= velocita_proiettile
        elif proiettile["direzione"] == "down":
            proiettile["rect"].y += velocita_proiettile

        
        if (proiettile["rect"].x > LARGHEZZASCHERMO or proiettile["rect"].x < 0 or
                proiettile["rect"].y > ALTEZZASCHERMO or proiettile["rect"].y < 0):
            proiettili.remove(proiettile)

schermataTitolo, sfondoMappe, personaggio_dx, personaggio_sx, personaggio_up, personaggio_down = CaricaImmagini()

mappaCorrente = None
SpazioPremuto = False

posX = 300
posY = 300
velocita = 5

proiettili = []  
velocita_proiettile = 10  

clock = pygame.time.Clock()
gameOver = False

direzione_corrente = "dx"

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

        SpazioPremuto = GestisciSpazio(event, SpazioPremuto)

        if SpazioPremuto and mappaCorrente is None:
            scelta = ScegliMappa(event)
            if scelta:
                mappaCorrente = scelta

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mappaCorrente is not None:
            SparaProiettile(posX, posY, direzione_corrente)

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
            posX, posY, nuova_direzione = GestisciMovimento(tasti, posX, posY, velocita)
            if nuova_direzione:
                direzione_corrente = nuova_direzione

            if direzione_corrente == "dx":
                schermo.blit(personaggio_dx, (posX, posY))
            elif direzione_corrente == "sx":
                schermo.blit(personaggio_sx, (posX, posY))
            elif direzione_corrente == "up":
                schermo.blit(personaggio_up, (posX, posY))
            elif direzione_corrente == "down":
                schermo.blit(personaggio_down, (posX, posY))

           
            GestisciProiettili(proiettili, velocita_proiettile)
            for proiettile in proiettili:
                pygame.draw.rect(schermo, (255, 0, 0), proiettile["rect"])  

    pygame.display.update()
    clock.tick(120)

pygame.quit()