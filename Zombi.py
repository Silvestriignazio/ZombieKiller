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
    3: pygame.transform.scale(DizionarioMappe[3], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA))
}


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
    rett = immagineRuotata.get_rect(center=(x + immagine.get_width()//2, y + immagine.get_height()//2))
    return immagineRuotata, rett

def RotazioneZombie(immagine, zx, zy, giocatoreX, giocatoreY):
    dx = giocatoreX - zx
    dy = giocatoreY - zy
    angolo = -math.degrees(math.atan2(dy, dx))
    immagineRuotata = pygame.transform.rotate(immagine, angolo)
    rett = immagineRuotata.get_rect(center=(zx, zy))
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


def SparaProiettile(x, y, mouseX, mouseY, listaProiettili):
    angoloRad = math.atan2(mouseY - (y+32), mouseX - (x+32))
    dx = math.cos(angoloRad)
    dy = math.sin(angoloRad)
    distanza = 32
    startX = x + 32 + dx * distanza
    startY = y + 32 + dy * distanza
    listaProiettili.append([startX, startY, dx, dy, -math.degrees(angoloRad)])

def GestisciProiettili(listaProiettili, velocitaProiettile):
    restanti = []
    for p in listaProiettili:
        p[0] += p[2] * velocitaProiettile
        p[1] += p[3] * velocitaProiettile
        if 0 <= p[0] <= LARGHEZZASCHERMO and 0 <= p[1] <= ALTEZZASCHERMO:
            restanti.append(p)
    listaProiettili[:] = restanti

def InfoProiettili(schermo, proiettili_rimanenti, ricarica, ultimaRicarica):
    font = pygame.font.Font("font/ZOMBIE.TTF", 36)
    testoColpi = font.render(f"Colpi {proiettili_rimanenti}", True, (255,255,255))
    schermo.blit(testoColpi, (10,10))
    if ricarica:
        tempo = max(0, 2 - int(time.time() - ultimaRicarica))
        testoRicarica = font.render(f"Ricarica {tempo}s", True, (255,0,0))
        schermo.blit(testoRicarica, (10,50))

def SpawnZombie():
    lato = random.choice(["su","giu","sinistra","destra"])
    if lato == "su":
        return [random.randint(0, LARGHEZZASCHERMO), -50]
    if lato == "giu":
        return [random.randint(0, LARGHEZZASCHERMO), ALTEZZASCHERMO + 50]
    if lato == "sinistra":
        return [-50, random.randint(0, ALTEZZASCHERMO)]
    return [LARGHEZZASCHERMO + 50, random.randint(0, ALTEZZASCHERMO)]

def GestisciZombie(ListaZombie, giocatoreX, giocatoreY, velocitaZombie, zombie):
    centroX = giocatoreX + 32
    centroY = giocatoreY + 32
    for z in ListaZombie:
        if z[0] < centroX:
            z[0] += velocitaZombie
        elif z[0] > centroX:
            z[0] -= velocitaZombie
        if z[1] < centroY:
            z[1] += velocitaZombie
        elif z[1] > centroY:
            z[1] -= velocitaZombie
        zImg, zRect = RotazioneZombie(zombie, z[0], z[1], giocatoreX, giocatoreY)
        schermo.blit(zImg, zRect.topleft)


def CollisioniZombie(ListaZombie, listaProiettili):
    daRimuovereZ = []
    daRimuovereP = []
    for z in ListaZombie:
        rectZ = pygame.Rect(z[0], z[1], 40, 43)
        for p in listaProiettili:
            rectP = pygame.Rect(p[0], p[1], 10, 10)
            if rectZ.colliderect(rectP):
                daRimuovereZ.append(z)
                daRimuovereP.append(p)
    for z in daRimuovereZ:
        if z in ListaZombie:
            ListaZombie.remove(z)
    for p in daRimuovereP:
        if p in listaProiettili:
            listaProiettili.remove(p)


def AumentoSpawnZombie(tempoUltimoSpawn, frequenzaSpawn, tempoUltimoAumento, ListaZombie):
    if pygame.time.get_ticks() - tempoUltimoAumento >= 15000:
        if frequenzaSpawn > 500:
            frequenzaSpawn -= 500
        tempoUltimoAumento = pygame.time.get_ticks()
    if pygame.time.get_ticks() - tempoUltimoSpawn >= frequenzaSpawn:
        ListaZombie.append(SpawnZombie())
        tempoUltimoSpawn = pygame.time.get_ticks()
    return tempoUltimoSpawn, frequenzaSpawn, tempoUltimoAumento, ListaZombie


schermataTitolo, SfondoMappe, personaggioBase, proiettile, zombie = CaricaImmagini()

mappaCorrente = None
spazioPremuto = False

giocatoreX = 300
giocatoreY = 300
velocita = 5

listaProiettili = []
maxProiettili = 12
proiettili_rimanenti = maxProiettili
velocitaProiettile = 10
ultimoColpo = time.time()
ultimaRicarica = 0
ricarica = False

ListaZombie = []
velocitaZombie = 2
tempoUltimoSpawn = 0
frequenzaSpawn = 2000
tempoUltimoAumento = 0

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mappaCorrente:
            mouseX, mouseY = pygame.mouse.get_pos()
            if proiettili_rimanenti > 0 and not ricarica and time.time() - ultimoColpo >= 0.5:
                SparaProiettile(giocatoreX, giocatoreY, mouseX, mouseY, listaProiettili)
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
            giocatoreX, giocatoreY = GestisciMovimento(tasti, giocatoreX, giocatoreY, velocita)
            giocatoreRuotato, giocatoreRett = RuotaVersoMouse(personaggioBase, giocatoreX, giocatoreY, *pygame.mouse.get_pos())
            schermo.blit(giocatoreRuotato, giocatoreRett.topleft)
            GestisciProiettili(listaProiettili, velocitaProiettile)
            for p in listaProiettili:
                img = pygame.transform.rotate(proiettile, p[4])
                rect = img.get_rect(center=(p[0], p[1]))
                schermo.blit(img, rect.topleft)
            CollisioniZombie(ListaZombie, listaProiettili)
            InfoProiettili(schermo, proiettili_rimanenti, ricarica, ultimaRicarica)
            tempoUltimoSpawn, frequenzaSpawn, tempoUltimoAumento, ListaZombie = AumentoSpawnZombie(
                tempoUltimoSpawn, frequenzaSpawn, tempoUltimoAumento, ListaZombie
            )
            GestisciZombie(ListaZombie, giocatoreX, giocatoreY, velocitaZombie, zombie)

    pygame.display.update()
    clock.tick(120)

pygame.quit()
