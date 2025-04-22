import pygame
import os
import math
import time
import random

os.system("cls")
pygame.init()

MINIMAPPA_LARGHEZZA = 300
MINIMAPPA_ALTEZZA = 250
LARGHEZZASCHERMO = 1440
ALTEZZASCHERMO = 796

pygame.display.set_caption('ZOMBI KILLER')
schermo = pygame.display.set_mode((LARGHEZZASCHERMO, ALTEZZASCHERMO))

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

pygame.display.set_caption('ZOMBI KILLER')
schermo = pygame.display.set_mode((LARGHEZZASCHERMO, ALTEZZASCHERMO))

def CaricaImmagini():
    schermataTitolo = pygame.image.load("immagini/titolo.png")
    sfondoMappe = pygame.image.load("immagini/sfondoMappe.png")
    personaggio = pygame.image.load("immagini/personaggio.png")
    proiettile = pygame.transform.scale(pygame.image.load("immagini/weapon_gun.png"), (10, 10))
    zombie = pygame.image.load("immagini/zombie.png")
    return schermataTitolo, sfondoMappe, personaggio, proiettile, zombie

def RuotaVersoMouse(immagine, x, y, mouseX, mouseY):
    dx = mouseX - x
    dy = mouseY - y
    angolo = -math.degrees(math.atan2(dy, dx))
    immagineRuotata = pygame.transform.rotate(immagine, angolo)
    rett = immagineRuotata.get_rect(center=(x + immagine.get_width() // 2, y + immagine.get_height() // 2))
    return immagineRuotata, rett

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

def GestisciMovimento(tasti, x, y, velocita):
    if tasti[pygame.K_a] and x > 0:
        x -= velocita
    if tasti[pygame.K_d] and x < LARGHEZZASCHERMO - 64:
        x += velocita
    if tasti[pygame.K_w] and y > 0:
        y -= velocita
    if tasti[pygame.K_s] and y < ALTEZZASCHERMO - 64:
        y += velocita
    return x, y

def SparaProiettile(x, y, mouseX, mouseY, Proiettili):
    angolo_rad = math.atan2(mouseY - y, mouseX - x)
    dx = math.cos(angolo_rad)
    dy = math.sin(angolo_rad)
    Proiettili.append({
        "x": x + 32,
        "y": y + 32,
        "dx": dx,
        "dy": dy,
        "angolo": -math.degrees(angolo_rad)
    })

def GestisciProiettili(proiettile, velocitaProiettile, ListaProiettili):
    for proiettile in ListaProiettili:
        if proiettile["direzione"] == "dx":
            proiettile += velocitaProiettile
        elif proiettile["direzione"] == "sx":
            proiettile -= velocitaProiettile
        elif proiettile["direzione"] == "up":
            proiettile -= velocitaProiettile
        elif proiettile["direzione"] == "down":
            proiettile += velocitaProiettile

        
        if (proiettile> LARGHEZZASCHERMO or proiettile < 0 or proiettile> ALTEZZASCHERMO or proiettile < 0):
            listaProiettili.remove(proiettile)

def InfoProiettili():
    pass 

def SpawnZombie(): 
    pass

def RotazioneZombie(): 
    lato = random.choice(["su", "giu", "sinistra", "destra"])
    if lato == "su":
        return random.randint(0, LARGHEZZASCHERMO), -50
    elif lato == "giu":
        return random.randint(0, LARGHEZZASCHERMO), ALTEZZASCHERMO + 50
    elif lato == "sinistra":
        return -50, random.randint(0, ALTEZZASCHERMO)
    elif lato == "destra":
        return LARGHEZZASCHERMO + 50, random.randint(0, ALTEZZASCHERMO)

def GestisciZombie(immagine, x, y, giocatoreX, giocatoreY):
    # Calcoliamo la direzione verso il giocatore
    dx = giocatoreX - x
    dy = giocatoreY - y
    angolo = -math.degrees(math.atan2(dy, dx))  # Calcoliamo l'angolo tra zombie e giocatore
    immagineRuotata = pygame.transform.rotate(immagine, angolo)  # Ruotiamo l'immagine dello zombie
    ImmagineCorretta = immagineRuotata.get_rect(center=(x, y))  # Posizioniamo l'immagine ruotata correttamente
    return immagineRuotata, ImmagineCorretta

schermataTitolo, SfondoMappe, personaggioBase, proiettile, zombie = CaricaImmagini()

mappaCorrente = None
spazioPremuto = False

giocatoreX = 300
giocatoreY = 300
velocita = 5

listaProiettili = []
maxProiettili = 12
proiettili_rimanenti = maxProiettili
velocita_proiettile = 10
ultimoColpo = time.time()
ultimaRicarica = 0
ricarica = False

ListaZombie = []
velocitàZombie = 2

clock = pygame.time.Clock()
gameOver = False

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

        spazioPremuto = GestisciSpazio(event, spazioPremuto)

        if spazioPremuto and mappaCorrente is None:
            scelta = ScegliMappa(event)
            if scelta:
                mappaCorrente = scelta

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mappaCorrente is not None:
            mouseX, mouseY = pygame.mouse.get_pos()
            if proiettili_rimanenti > 0 and not ricarica and time.time() - ultimoColpo >= 0.5:
                SparaProiettile(giocatore_x, giocatore_y, mouseX, mouseY, listaProiettili)
                proiettili_rimanenti -= 1
                ultimoColpo = time.time()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if not ricarica and proiettili_rimanenti < maxProiettili:
                ricarica = True
                ultimaRicarica = time.time()

    if ricarica and time.time() - ultimaRicarica >= 3:
        proiettili_rimanenti = maxProiettili
        ricarica = False

    if not spazioPremuto:
        schermo.blit(schermataTitolo, (0, 0))
    elif mappaCorrente is None:
        schermo.blit(SfondoMappe, (0, 0))
        schermo.blit(MiniMappe[1], (100, 400))
        schermo.blit(MiniMappe[2], (580, 400))
        schermo.blit(MiniMappe[3], (1100, 400))
    else:
        schermo.blit(mappaCorrente, (0, 0))
        if mappaCorrente == DizionarioMappe[1]:
            tasti = pygame.key.get_pressed()
            giocatore_x, giocatore_y = GestisciMovimento(tasti, giocatoreX, giocatoreY, velocita)

            mouseX, mouseY = pygame.mouse.get_pos()
            giocatoreRuotato, giocatoreRett = RuotaVersoMouse(personaggioBase, giocatore_x, giocatore_y, mouseX, mouseY)
            schermo.blit(giocatoreRuotato, giocatoreRett.topleft)

            GestisciProiettili(listaProiettili, velocita_proiettile)
            for p in listaProiettili:
                img = pygame.transform.rotate(proiettile, p["angolo"])
                rect = img.get_rect(center=(p["x"], p["y"]))
                schermo.blit(img, rect.topleft)

            InfoProiettili(schermo, proiettili_rimanenti, maxProiettili, ricarica, ultimaRicarica)

            if pygame.time.get_ticks() % 2000 < 20:
                zx, zy = SpawnZombie()
                ListaZombie.append({"x": zx, "y": zy})

            GestisciZombie(ListaZombie, giocatoreX, giocatore_y, velocitàZombie, zombie) 

    pygame.display.update()
    clock.tick(120)

pygame.quit()